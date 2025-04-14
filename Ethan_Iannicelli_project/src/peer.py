import threading
import os
from discovery import PeerDiscovery
from transfer import FileTransfer
from utils.logger import get_logger, format_file_chunks
from utils.config import CONFIG

logger = get_logger("Peer")

class Peer:
    def __init__(self, discovery_port, transfer_port):
        """
        constructor for the Peer entity, defines global varaibles and reads all available
        files/chunks to local memory

        :param discovery_port: The port this peer broadcast/discovers on.
        :type discovery_port: int
        :param transfer_port: The base port used for file transfer.
        :param transfer_port: int
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
                            chunks[filename][chunk_num] = ''
                            break
                        chunks[filename][chunk_num] = chunk.decode()
                        chunk_num += 1

        self.files = chunks
        self.transfer = FileTransfer(transfer_port, self.discovery, self.files)
        self.receiving = False
        self.writing = False
    
    def start(self):
        """
        Start peer broadcasting and transfer services. Also start command line input loop
        for handling commands.
        - list: output the files and chunks available on this peer
        - download <file>: requests all available peers for any chunks they have for <file>.
        use threading for each request, and accumulate in a shared local memory to build the
        file on the receiver end.
        - exit: stop the peer and shut down
        """
        threading.Thread(target=self.discovery.start, daemon=True).start()
        threading.Thread(target=self.transfer.start_server, daemon=True).start()
        logger.info("Peer started. Listening for connections...")

        while self.running:
            command = input("\nEnter command (list, download, exit): ").strip().lower()
            if command == "list":
                logger.info(format_file_chunks(self.files))
            elif command.startswith("download"):
                c, filename = command.split(" ")
                chunks = {}
                self.receiving = True
                if len(self.discovery.peers) == 1:
                    logger.error("No peers available to download from...")
                else:
                    for s in [s for s, d in self.discovery.peers if s != self.sender_port]:
                        threading.Thread(target=self.transfer.request_file, args=(filename, s, chunks, self), daemon=True).start()
            elif command == "exit":
                self.discovery.stop()
                self.running = False
                logger.info("Shutting down peer...")
            else:
                print("Unknown command. Try: list, download <file>, exit.")

