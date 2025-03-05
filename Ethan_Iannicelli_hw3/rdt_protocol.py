import socket
import threading
import time
import random
import struct

# Constants
SENDER_PORT = 12347
INTER_PORT = 12346
RECEIVER_PORT = 12345
BUFFER_SIZE = 1024
TIMEOUT = 10  # Timeout for retransmission in seconds
MAX_RETRIES = 5  # Max retries for retransmission

# Packet structure
HEADER_FORMAT = '!I I I'  # Sequence Number (4 bytes), Acknowledgment (4 bytes), Checksum (4 bytes)
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def checksum(data):
    """Simple checksum function to ensure data integrity."""
    return sum(data) % 256

def create_packet(seq_num, ack_num, data):
    """Creates a packet with header and data."""
    header = struct.pack(HEADER_FORMAT, seq_num, ack_num, checksum(data))
    return header + data

def parse_packet(packet):
    """Parses a packet into its components (seq_num, ack_num, checksum, data)."""
    header = packet[:HEADER_SIZE]
    data = packet[HEADER_SIZE:]
    seq_num, ack_num, chk_sum = struct.unpack(HEADER_FORMAT, header)
    return seq_num, ack_num, chk_sum, data

class ReliableDataTransferSender:
    def __init__(self, inter_address, sender_address):
        self.inter_address = inter_address
        self.seq_num = 0  # Start with sequence number 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(sender_address)
        self.sock.settimeout(TIMEOUT)

    def send(self, data):
        """Send data reliably with acknowledgment, retransmission, and timeout."""
        retries = 0
        while retries < MAX_RETRIES:
            print(f"Sending packet with seq_num {self.seq_num}")
            packet = create_packet(self.seq_num, 0, data)
            self.sock.sendto(packet, self.inter_address)
            
            try:
                # Wait for acknowledgment from intermediary
                ack_packet, _ = self.sock.recvfrom(BUFFER_SIZE)
                ack_seq_num, _, _, _ = parse_packet(ack_packet)
                
                if ack_seq_num == self.seq_num:
                    print(f"Acknowledgment received for seq_num {self.seq_num}")
                    self.seq_num += 1
                    break
                else:
                    print(f"Received incorrect acknowledgment: {ack_seq_num}. Retransmitting.")
            except socket.timeout:
                print("Timeout waiting for acknowledgment. Retransmitting.")
            retries += 1

        if retries == MAX_RETRIES:
            print("Max retries reached. Packet lost.")

class ReliableDataTransferReceiver:
    def __init__(self):
        self.seq_num = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', RECEIVER_PORT))

    def receive(self):
        """Receive data and send acknowledgments."""
        while True:
            packet, addr = self.sock.recvfrom(BUFFER_SIZE)
            seq_num, ack_num, chk_sum, data = parse_packet(packet)
            
            # Simulate packet corruption detection
            if checksum(data) != chk_sum:
                print("Packet corrupted! Ignoring.")
                continue

            print(f"Received packet with seq_num {seq_num}, sending acknowledgment.")
            
            # Simulate packet reordering or loss
            if random.random() > -0.1:  # 90% chance of acknowledgment
                ack_packet = create_packet(seq_num, 0, b'')
                self.sock.sendto(ack_packet, addr)
                print(f"Sent acknowledgment for seq_num {seq_num}")
                print(addr, ack_num, ack_packet)
                return packet
            else:
                print(f"Simulating loss of acknowledgment for seq_num {seq_num}")

def run_sender(receiver_address):
    sender = ReliableDataTransferSender(receiver_address)
    data = b"Hello, this is a test message."  # Example data to send
    sender.send(data)

def run_receiver():
    receiver = ReliableDataTransferReceiver()
    receiver.receive()

def start_protocol():
    receiver_thread = threading.Thread(target=run_receiver)
    receiver_thread.start()
    
    time.sleep(1)  # Ensure receiver starts first
    sender_thread = threading.Thread(target=run_sender, args=(('localhost', SENDER_PORT),))
    sender_thread.start()

if __name__ == "__main__":
    start_protocol()
