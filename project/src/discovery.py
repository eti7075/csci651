import socket
import threading
import time
from utils.logger import get_logger

logger = get_logger()

class PeerDiscovery:
    """Handles peer discovery over UDP broadcast."""

    def __init__(self, id, port):
        """
        :param listen_port: The unique port each peer listens on.
        :param broadcast_port: The shared broadcast port all peers send announcements to.
        """
        self.id = id
        self.port = port
        self.peers = set([f"{self.id}".encode("utf-8")])
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

                    if data not in self.peers:
                        self.peers.add(data)
                        logger.info(f"Discovered peer: {data} from broadcast")

                except socket.error as e:
                    logger.error(f"Error receiving broadcast: {e}")

    def broadcast_announcement(self):
        """Broadcast availability to the network."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = f"{self.id}".encode("utf-8")
            try:
                sock.sendto(message, ("255.255.255.255", self.port))
            except OSError as e:
                logger.error(f"Broadcast error: {e}")

    def stop(self):
        """Stop peer discovery."""
        self.running = False
