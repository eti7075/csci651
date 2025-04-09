import socket
import threading
import os
from utils.config import CONFIG
from packet import create_packet, parse_packet, udp_checksum
from utils.logger import get_logger
import random
import time

logger = get_logger("Transfer")

class FileTransfer:
    def __init__(self, port, discovery, files):
        """
        constructor for the FileTransfer entity, defining the ip, ports, socks, discovery entity, and session files

        :param port: base transfer port that other ports are created from
        :type port: int
        :param discovery: the discovery entity for the peer, used to access known peers
        :type discovery: PeerDiscovery
        :param files: local session storage for the files available to the peer
        :type files: map<string, map<string, string>>
        """
        self.receiver_port = port
        self.sender_port = port + 1
        self.distributor_port = port + 2
        self.distributee_port = port + 3
        self.host = "0.0.0.0"
        self.receiver_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver_sock.bind((self.host, self.receiver_port))
        self.sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender_sock.bind((self.host, self.sender_port))        
        self.distributor_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.distributor_sock.bind((self.host, self.distributor_port))
        self.distributee_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.distributee_sock.bind((self.host, self.distributee_port))
        self.discovery = discovery
        self.files = files

    def distribute_files(self):
        """
        periodically (every 10 seconds) randomly send chunks of files that this peer knows to other peers.
        all chunks are sent, but the peer is randomly chosen. this is done to simulate peers not having perfect knowledge
        of the files from the start and to simulate rate limits of data sent.
        """
        logger.info(f"Starting distribution of files to peers...")
        while True:
            peers = [d for _, d in self.discovery.peers if d != self.distributee_port]
            if peers != []:
                for file, chunks in self.files.items():
                    for chunk_num, chunk in chunks.items():
                        port = peers[random.randint(0, len(peers) - 1)]
                        packet = create_packet(f"{file} {chunk}".encode(), chunk_num)
                        self.distributor_sock.sendto(packet, (self.host, int(port)))
            time.sleep(10) # simulate limiting the data available to each peer

    def receive_distributed_files(self):
        """
        recieve chunks of files sent to this port. extract the filename, chunk number, and chunk and save it to the 
        files dictionary representing local session storage.
        """
        logger.info(f"Starting receiver for distributed files...")
        while True:
            packet, _ = self.distributee_sock.recvfrom(1024)
            check_sum, chunk_num, data = parse_packet(packet)
            if udp_checksum(data) == check_sum:
                filename, chunk = data.decode().split(" ", 1)
                if filename in self.files.keys():
                    self.files[filename][chunk_num] = chunk
                else:
                    self.files[filename] = {chunk_num: chunk}
            else:
                logger.error(f"Filename packet was corrupted: {check_sum} != {udp_checksum(data)} || {data}")

    def start_server(self):
        """
        Start the file transfer server. start threads to handle requests from other peers, distribute chunks to other
        peers, and receive distributed chunks from other peers
        """
        logger.info(f"File transfer server listening on {self.sender_port}...")

        threading.Thread(target=self.handle_client, args=(), daemon=True).start()
        threading.Thread(target=self.distribute_files, args=(), daemon=True).start()
        threading.Thread(target=self.receive_distributed_files, args=(), daemon=True).start()

    def handle_client(self):
        """
        Handle an incoming file request. receive a file name to initialize this process, and then send all
        chunks that this peer has to the sender address in separate requests.
        """
        while True:
            packet, addr = self.sender_sock.recvfrom(1024)
            check_sum, _, data = parse_packet(packet)
            if udp_checksum(data) == check_sum:
                filename = data.decode()
                file = self.files[filename]
                for chunk_num, chunk in file.items():
                    logger.info(f"Sending file {filename} chunk {chunk_num}")
                    packet = create_packet(chunk.encode(), chunk_num)
                    self.sender_sock.sendto(packet, addr)
                logger.info(f"Sent {filename} to {addr}")
            else:
                logger.error(f"Filename packet was corrupted: {check_sum} != {udp_checksum(data)} || {data}")

    def request_file(self, filename, peer_port, chunks, peer):
        """
        Request a file from a peer. This is called as one of many threads, so we use a global chunks dictionary
        to store all downloaded chunks. When the chunks dictionary is 'full' (all chunks for file are present), this
        thread marks as so and attempts to write to a file. If a timeout occurs, the user is notified and an incomplete
        file is downloaded and written

        :param filename: the name of the file to be downloaded
        :type filename: string
        :param peer_port: the port of the peer that we want to request from
        :type peer_port: string
        :param chunks: global dictionary for this file's chunks being stored in
        :type chunks: map<string, string>
        :param peer: the peer that called this function, used to know status of other threads that the peer spawned.
        :type peer: Peer
        """
        if peer_port in [s for s, d in self.discovery.peers]:
            packet = create_packet(filename.encode(), 0)
            self.receiver_sock.sendto(packet, (self.host, int(peer_port)))
            start_time = time.time()
            timeout = True
            while time.time() - start_time < 20: # timeout to imply incomplete file
                packet, _ = self.receiver_sock.recvfrom(1024)
                check_sum, chunk_num, data = parse_packet(packet)
                if check_sum == udp_checksum(data):
                    logger.info(f"Received file {filename} chunk {chunk_num}")
                    chunks[chunk_num] = data.decode()
                else:
                    logger.error(f"Data integrity check failed: {check_sum} != {udp_checksum(data)} || ")   
                n = max(chunks.keys()) if chunks else -1 
                if all(k in chunks for k in range(n + 1)) and chunks.get(n) == '':
                    timeout = False
                    peer.receiving = False
                    break
                if peer.receiving == False:
                    timeout = False
                    break
            if timeout:
                logger.info(f"Timeout while requesting file...")
            if peer.writing is False:
                peer.writing = True
                with open(os.path.join(f"{os.getcwd()}/{CONFIG["DOWNLOAD_FOLDER"]}", filename), "wb") as file:
                    file.write(b''.join(chunks[k].encode() for k in sorted(chunks)))
                    logger.info("File finished downloading")
                peer.writing = False
        else:
            logger.error(f"Peer {peer_port} is not online.")
            logger.info(f"Available peers: {self.discovery.peers}")
