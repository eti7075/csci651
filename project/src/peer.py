import threading
import os
from discovery import PeerDiscovery
from transfer import FileTransfer
from utils.logger import get_logger
from utils.config import CONFIG

logger = get_logger("Peer")

class Peer:
    def __init__(self, discovery_port, transfer_port):
        """
        :param host: The local IP to bind to.
        :param discovery_listen_port: The port this peer listens on.
        :param discovery_broadcast_port: The port used to broadcast peer presence.
        :param transfer_port: The port used for file transfer.
        """
        self.discovery = PeerDiscovery(transfer_port, discovery_port)
        self.running = True
        self.sender_port = f"{transfer_port + 1}"

        chunks = {}
        for filename in os.listdir(f"{os.getcwd()}/{CONFIG["SHARED_FOLDER"]}"):
            file_path = os.path.join(f"{os.getcwd()}/{CONFIG["SHARED_FOLDER"]}", filename)

            if os.path.isfile(file_path):
                chunks[filename] = {}
                with open(file_path, 'rb') as f:
                    chunk_num = 0
                    while True:
                        chunk = f.read(CONFIG["CHUNK_SIZE"])
                        if not chunk:
                            chunks[filename][chunk_num] = b''
                            break
                        chunks[filename][chunk_num] = chunk
                        chunk_num += 1

        self.files = chunks
        print(self.files)
        self.transfer = FileTransfer(transfer_port, self.discovery, self.files)

    
    def start(self):
        """Start peer services."""
        threading.Thread(target=self.discovery.start, daemon=True).start()
        threading.Thread(target=self.transfer.start_server, daemon=True).start()
        logger.info("Peer started. Listening for connections...")

        while self.running:
            command = input("\nEnter command (list, download, exit): ").strip().lower()
            if command == "list":
                logger.info(self.files)
            elif command.startswith("download"):
                _, filename = command.split(" ")
                for s in [s for s, d in self.discovery.peers if s != self.sender_port]:
                    threading.Thread(target=self.transfer.request_file, args=(filename, s), daemon=True).start()
            elif command == "exit":
                self.running = False
                logger.info("Shutting down peer...")
            else:
                print("Unknown command. Try: list, download <file>, exit.")

