import socket
import os
from rdt_protocol import ReliableDataTransferReceiver, parse_packet

# Constants
PORT = 12345
BUFFER_SIZE = 1024  # Size of each packet
SAVE_PATH = 'received_file.txt'  # Path to save the received file

class FileTransferServer:
    def __init__(self):
        self.receiver = ReliableDataTransferReceiver()
    
    def receive_file(self):
        """Receive a file from the client and save it."""
        with open(SAVE_PATH, 'wb') as file:
            print("Waiting for file...")
            seq_num = 0
            while True:
                # Receive a packet
                packet = self.receiver.receive()
                print(packet)
                if packet is None:
                    break  # No more packets to receive

                # Write received packet data to file
                _, _, _, data = parse_packet(packet)
                print(data)
                file.write(data)
                seq_num += 1
                break

            print(f"File saved to {SAVE_PATH}")

if __name__ == "__main__":
    server = FileTransferServer()
    server.receive_file()
