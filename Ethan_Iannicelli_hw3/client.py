import socket
import os
from rdt_protocol import ReliableDataTransferSender

# Constants
CLIENT_ADDRESS = ('localhost', 12347)  # Client Address
INTER_ADDRESS = ('localhost', 12346)
FILE_PATH = 'file_to_send.txt'  # Path of the file to send
BUFFER_SIZE = 1024  # Size of each packet

class FileTransferClient:
    def __init__(self):
        self.sender = ReliableDataTransferSender(INTER_ADDRESS, CLIENT_ADDRESS) 
    
    def send_file(self, file_path):
        """Send a file to the server using reliable data transfer."""
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist!")
            return

        with open(file_path, 'rb') as file:
            file_data = file.read(BUFFER_SIZE)
            seq_num = 0

            while file_data:
                # Send file data using the reliable data transfer protocol
                print(f"Sending packet {seq_num}")
                self.sender.send(file_data)
                seq_num += 1
                file_data = file.read(BUFFER_SIZE)

            print(f"File {file_path} sent successfully!")

if __name__ == "__main__":
    client = FileTransferClient()
    client.send_file(FILE_PATH)
