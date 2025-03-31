import threading
import socket
import os
from discovery import PeerDiscovery
from search import FileIndex
from transfer import FileTransfer
from utils.logger import get_logger

logger = get_logger("Peer")

class Peer:
    def __init__(self, discovery_port, sender_port, receiver_port):
        """
        :param host: The local IP to bind to.
        :param discovery_listen_port: The port this peer listens on.
        :param discovery_broadcast_port: The port used to broadcast peer presence.
        :param transfer_port: The port used for file transfer.
        """
        self.discovery_port = discovery_port
        self.sender_port = sender_port
        self.receiver_port = receiver_port

        self.discovery = PeerDiscovery(id=self.sender_port, port=self.discovery_port)
        self.index = FileIndex()
        self.transfer = FileTransfer(self.receiver_port, self.sender_port)
        self.running = True

    def start(self):
        """Start peer services."""
        threading.Thread(target=self.discovery.start, daemon=True).start()
        threading.Thread(target=self.transfer.start_server, daemon=True).start()
        logger.info("Peer started. Listening for connections...")

        while self.running:
            command = input("\nEnter command (list, search, download, exit): ").strip().lower()
            if command == "list":
                self.index.list_files()
            elif command.startswith("search"):
                _, query = command.split(" ", 1)
                self.index.search_files(query)
            elif command.startswith("download"):
                _, filename, peer_port = command.split(" ", 3)
                self.transfer.request_file(filename, int(peer_port))
            elif command == "exit":
                self.running = False
                logger.info("Shutting down peer...")
            else:
                print("Unknown command. Try: list, search <query>, download <file> <peer_ip>, exit.")

