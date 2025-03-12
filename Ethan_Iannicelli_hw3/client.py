import socket
import os
from rdt_protocol import ReliableDataTransferEntity
import rdt_protocol

# Constants
SENDER_ADDRESS = ('127.0.0.1', rdt_protocol.SENDER_PORT)
INTER_ADDRESS = ('127.0.0.1', rdt_protocol.INTER_PORT)
BUFFER_SIZE = 1024 

class FileTransferClient:
    def __init__(self):
        self.sender = ReliableDataTransferEntity(INTER_ADDRESS, SENDER_ADDRESS) 
    
    def send_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist!")
            return
        
        self.sender.send(file_path.encode())

        with open(file_path, 'rb') as file:
            while file_data := file.read(2048):
                self.sender.send(file_data)

        self.sender.send(b'')

        print(f"File {file_path} sent successfully!")

if __name__ == "__main__":
    client = FileTransferClient()
    while True:
        print("Enter the filename to send (enter 'quit' to stop the program): ")
        filename = input()
        if filename == 'quit':
            break
        client.send_file(filename)
