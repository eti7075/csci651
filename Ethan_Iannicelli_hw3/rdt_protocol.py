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
TIMEOUT = 10  
MAX_RETRIES = 5  

# simulates a sending rate of 256 bits / second, not including headers
BIT_RATE_SIZE = 256
BIT_RATE_TIME = 1

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

def split_data(data, chunk_size):
    """Splits data into an array of chunks of size N."""
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

class ReliableDataTransferSender:
    def __init__(self, inter_address, sender_address, window_size=4):
        self.inter_address = inter_address
        self.window_size = window_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(sender_address)
        self.sock.settimeout(TIMEOUT)

        self.base = 0  # Base sequence number (oldest unacknowledged packet)
        self.next_seq_num = 0  # Next packet to send
        self.unacked_packets = {}  # Track sent packets with timestamps

    def send(self, data):
        data_list = split_data(data, BIT_RATE_SIZE)
        """Send multiple packets reliably using a sliding window."""
        while self.base < len(data_list):
            # Send packets up to the window size
            while self.next_seq_num < self.base + self.window_size and self.next_seq_num < len(data_list):
                packet = create_packet(self.next_seq_num, 0, data_list[self.next_seq_num])
                self.sock.sendto(packet, self.inter_address)
                self.unacked_packets[self.next_seq_num] = time.time()  # Track send time
                print(f"Sent packet {self.next_seq_num}")
                time.sleep(BIT_RATE_TIME)
                self.next_seq_num += 1
            
            try:
                ack_packet, _ = self.sock.recvfrom(BUFFER_SIZE)
                ack_seq_num, _, _, _ = parse_packet(ack_packet)

                if ack_seq_num >= self.base:  # Move the window forward
                    print(f"ACK received for {ack_seq_num}")
                    self.base = ack_seq_num + 1  # Slide window

            except socket.timeout:
                # Retransmit all unacknowledged packets
                print("Timeout! Retransmitting unacknowledged packets.")
                for seq_num in range(self.base, self.next_seq_num):
                    packet = create_packet(seq_num, 0, data_list[seq_num])
                    self.sock.sendto(packet, self.inter_address)
                    self.unacked_packets[seq_num] = time.time()
                    print(f"Retransmitted packet {seq_num}")

        print("All packets sent successfully.")

class ReliableDataTransferReceiver:
    def __init__(self, receiver_address):
        self.expected_seq_num = 0  # Expected in-order sequence number
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(receiver_address)

    def receive(self):
        """Receive packets and send cumulative acknowledgments (Go-Back-N)."""
        while True:
            packet, addr = self.sock.recvfrom(BUFFER_SIZE)
            seq_num, _, chk_sum, data = parse_packet(packet)

            if checksum(data) != chk_sum:
                print("Packet corrupted! Ignoring.")
                continue

            if seq_num == self.expected_seq_num:  # In-order packet
                print(f"Received in-order packet {seq_num}, sending ACK.")
                ack_packet = create_packet(seq_num, 0, b'')
                self.sock.sendto(ack_packet, addr)
                self.expected_seq_num += 1  # Move expected sequence forward
            else:
                print(f"Out-of-order packet {seq_num} received. Expecting {self.expected_seq_num}. Ignoring.")



