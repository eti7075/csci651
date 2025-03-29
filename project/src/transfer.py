import socket
import threading
import os
from utils.config import CONFIG
from integrity import verify_checksum, generate_checksum
from utils.logger import get_logger

logger = get_logger("Transfer")

class FileTransfer:
    """Handles chunked file transfers between peers."""

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_server(self):
        """Start the file transfer server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.host, self.port))
            server.listen(CONFIG["MAX_CONNECTIONS"])
            logger.info(f"File transfer server listening on {self.port}...")

            while True:
                conn, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(self, conn, addr):
        """Handle an incoming file request."""
        try:
            filename = conn.recv(1024).decode()
            file_path = os.path.join("shared", filename)

            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    while chunk := file.read(CONFIG["CHUNK_SIZE"]):
                        conn.sendall(chunk)
                logger.info(f"Sent {filename} to {addr}")
            else:
                conn.sendall(b"ERROR: File not found.")
        except Exception as e:
            logger.error(f"Error handling client {addr}: {e}")
        finally:
            conn.close()

    def request_file(self, filename, peer_ip, peer_port):
        """Request a file from a peer."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.connect((peer_ip, peer_port))
                client.sendall(filename.encode())

                file_path = os.path.join(CONFIG["DOWNLOAD_FOLDER"], filename)
                with open(file_path, "wb") as file:
                    while chunk := client.recv(CONFIG["CHUNK_SIZE"]):
                        file.write(chunk)

                if verify_checksum(file_path):
                    logger.info(f"File {filename} downloaded successfully!")
                else:
                    logger.error("File integrity check failed!")
            except Exception as e:
                logger.error(f"Error downloading {filename} from {peer_ip} {peer_port}: {e}")
