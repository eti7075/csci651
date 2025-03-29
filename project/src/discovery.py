import socket
import threading
from utils.logger import get_logger
import time

logger = get_logger("Discovery")

class PeerDiscovery:
    """Handles peer discovery over UDP broadcast."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = set()

    def start(self):
        """Start peer discovery."""
        threading.Thread(target=self.listen_for_peers, daemon=True).start()
        while True:
            self.broadcast_announcement()
            time.sleep(5)

    def listen_for_peers(self):
        """Listen for incoming peer announcements."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((self.host, self.port))
            while True:
                data, addr = sock.recvfrom(1024)
                peer_ip = addr[0]
                if peer_ip not in self.peers:
                    self.peers.add(peer_ip)
                    logger.info(f"Discovered new peer: {peer_ip}")

    def broadcast_announcement(self):
        """Broadcast availability to the network."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = b"PEER_DISCOVERY"
            try:
                sock.sendto(message, ("<broadcast>", self.port))
                logger.info("Broadcasted peer presence.")
            except OSError as e:
                logger.error(f"Broadcast error: {e}")
