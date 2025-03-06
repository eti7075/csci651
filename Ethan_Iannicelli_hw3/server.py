import socket
import os
from rdt_protocol import ReliableDataTransferReceiver, parse_packet
import rdt_protocol

# Constants
RECEIVER_ADDRESS = ('localhost', rdt_protocol.RECEIVER_PORT)
BUFFER_SIZE = 1024  
SAVE_PATH = 'received_file.txt'  

class FileTransferServer:
    def __init__(self):
        self.receiver = ReliableDataTransferReceiver(RECEIVER_ADDRESS)
    
    def receive_file(self):
        """Receive a file from the client and save it."""
        with open(SAVE_PATH, 'ab') as file:
            print("Waiting for file...")
            seq_num = 0
            while True:
                packet = self.receiver.receive()

                _, _, _, data = parse_packet(packet)
                
                print(data)
                file.write(data)
                seq_num += 1

                print(f"File saved to {SAVE_PATH}")

if __name__ == "__main__":
    server = FileTransferServer()
    while True:
        server.receive_file()
