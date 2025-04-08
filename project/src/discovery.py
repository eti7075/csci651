import socket
import threading
import time
from utils.logger import get_logger

logger = get_logger()

class PeerDiscovery:
    """Handles peer discovery over UDP broadcast."""

    def __init__(self, transfer_port, port):
        """
        :param listen_port: The unique port each peer listens on.
        :param broadcast_port: The shared broadcast port all peers send announcements to.
        """
        self.sender_port = transfer_port + 1
        self.distributee_port = transfer_port + 3
        self.port = port
        self.peers = {(f"{self.sender_port}", f"{self.distributee_port}")}
        self.running = True
        self.broadcast_interval = 5
        self.host = "0.0.0.0"

    def start(self):
        """Start peer discovery."""
        threading.Thread(target=self.listen_for_peers, daemon=True).start()
        logger.info(f"Broadcasting presence on port {self.port} every {self.broadcast_interval} seconds.")
        while self.running:
            self.broadcast_announcement()
            time.sleep(self.broadcast_interval)

    def listen_for_peers(self):
        """Listen for incoming peer announcements."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

            sock.bind((self.host, self.port))
            
            logger.info(f"Listening for broadcasts on UDP port {self.port}...")

            while self.running:
                try:
                    data, _ = sock.recvfrom(1024)
                    s, d, m = data.decode().split(" ", 2)
                    t = (s, d)
                    if t not in self.peers and m == "start":
                        self.peers.add(t)
                        logger.info(f"Discovered peer: {t} from broadcast - adding to known peers")
                    if t in self.peers and m == "stop":
                        del [p for p in self.peers if p == t][0]
                        logger.info(f"Removing peer: {t} from known peers")

                except socket.error as e:
                    logger.error(f"Error receiving broadcast: {e}")

    def broadcast_announcement(self):
        """Broadcast availability to the network."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = f"{self.sender_port} {self.distributee_port} start".encode("utf-8")
            try:
                sock.sendto(message, ("255.255.255.255", self.port))
            except OSError as e:
                logger.error(f"Broadcast error: {e}")

    def stop(self):
        """Stop peer discovery."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = f"{self.sender_port} {self.distributee_port} stop".encode("utf-8")
            try:
                sock.sendto(message, ("255.255.255.255", self.port))
            except OSError as e:
                logger.error(f"Broadcast error: {e}")
        self.running = False
