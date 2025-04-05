import socket
import threading
import os
from utils.config import CONFIG
from packet import create_packet, parse_packet, udp_checksum
from utils.logger import get_logger

logger = get_logger("Transfer")

class FileTransfer:
    """Handles chunked file transfers between peers."""

    def __init__(self, receiver_port, sender_port, discovery):
        self.receiver_port = receiver_port
        self.sender_port = sender_port
        self.host = "0.0.0.0"
        self.receiver_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver_sock.bind((self.host, self.receiver_port))
        self.sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender_sock.bind((self.host, self.sender_port))
        self.discovery = discovery

    def start_server(self):
        """Start the file transfer server."""
        logger.info(f"File transfer server listening on {self.sender_port}...")

        threading.Thread(target=self.handle_client, args=(), daemon=True).start()

    def handle_client(self):
        """Handle an incoming file request."""
        while True:
            packet, addr = self.sender_sock.recvfrom(1024)
            check_sum, data = parse_packet(packet)
            if udp_checksum(data) == check_sum:
                filename = data.decode()
                file_path = os.path.join(f"{os.getcwd()}/{CONFIG["SHARED_FOLDER"]}", filename)

                if os.path.exists(file_path):
                    with open(file_path, "rb") as file:
                        chunk_num = 1
                        while chunk := file.read(CONFIG["CHUNK_SIZE"]):
                            logger.info(f"Sending file {filename} chunk {chunk_num}")
                            chunk_num += 1
                            packet = create_packet(chunk)
                            self.sender_sock.sendto(packet, addr)
                        packet = create_packet(b'')
                        self.sender_sock.sendto(packet, addr)
                    logger.info(f"Sent {filename} to {addr}")
                else:
                    logger.error(f"File specified was not found: {file_path}")
            else:
                logger.error(f"Filename packet was corrupted: {check_sum} != {udp_checksum(data)} || {data}")

    def request_file(self, filename, peer_port):
        """Request a file from a peer."""
        if f"{peer_port}".encode("utf-8") in self.discovery.peers:
            packet = create_packet(filename.encode())
            self.receiver_sock.sendto(packet, (self.host, peer_port))

            file_path = os.path.join(f"{os.getcwd()}/{CONFIG["DOWNLOAD_FOLDER"]}", filename)
            with open(file_path, "wb") as file:
                chunk_num = 1
                while True:
                    packet, _ = self.receiver_sock.recvfrom(CONFIG["CHUNK_SIZE"]+4)
                    check_sum, data = parse_packet(packet)
                    if check_sum == udp_checksum(data):
                        logger.info(f"Received file {filename} chunk {chunk_num}")
                        chunk_num += 1
                        file.write(data)
                        if data == b'':
                            break
                    else:
                        logger.error(f"Data integrity check failed: {check_sum} != {udp_checksum(data)} || ")
                
                logger.info("File finished downloading")
        else:
            logger.error(f"Peer {peer_port} is not online.")
            logger.info(f"Available peers: {self.discovery.peers}")
