import socket
import os
from rdt_protocol import ReliableDataTransferSender
import rdt_protocol

# Constants
SENDER_ADDRESS = ('localhost', rdt_protocol.SENDER_PORT)
INTER_ADDRESS = ('localhost', rdt_protocol.INTER_PORT)
FILE_PATH = 'file_to_send_long.txt'  
BUFFER_SIZE = 1024 

class FileTransferClient:
    def __init__(self):
        self.sender = ReliableDataTransferSender(INTER_ADDRESS, SENDER_ADDRESS) 
    
    def send_file(self, file_path):
        """Send a file to the server using reliable data transfer."""
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist!")
            return

        with open(file_path, 'rb') as file:
            file_data = file.read(BUFFER_SIZE)
            seq_num = 0

            while file_data:
                print(f"Sending packet {seq_num}")
                self.sender.send(file_data)
                seq_num += 1
                file_data = file.read(BUFFER_SIZE)

            print(f"File {file_path} sent successfully!")

if __name__ == "__main__":
    client = FileTransferClient()
    client.send_file(FILE_PATH)
