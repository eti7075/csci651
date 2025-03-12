import socket
import time
import struct

# Constants
SENDER_PORT = 12347     # sender's port - this could be set dynamically, but for this project a constant will do
INTER_PORT = 12346      # intermediary port, same as above
RECEIVER_PORT = 12345   # receiver's port, same as above
BUFFER_SIZE = 1024      # receive packets (both ack and data) using this size. 
                        # this is sufficiently more than any packet size will actually be
TIMEOUT = 10            # arbitrary timeout length for this rdt protocol
MAX_RETRIES = 5         # arbitrary max number of retries to send a packet

# simulates a sending rate of 256 bits / second, not including headers
BIT_RATE_SIZE = 256
BIT_RATE_TIME = 1

# big endian, 4 bytes each
HEADER_FORMAT = '!I I I'  # sequence number, acknowledgment, checksum
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def udp_checksum(data):
    """
    perform a psuedo udp checksum by reducing the data to 4 bytes and taking one's complement
    """
    packet = data
    
    if len(packet) % 2 != 0:
        packet += b'\x00'
    
    s = 0
    for i in range(0, len(packet), 2):
        w = (packet[i] << 8) + packet[i + 1]
        s = s + w
        s = (s & 0xffff) + (s >> 16)
    
    checksum = ~s & 0xffff
    
    return checksum

def create_packet(seq_num, ack_num, data):
    header = struct.pack(HEADER_FORMAT, seq_num, ack_num, udp_checksum(data))
    return header + data

def parse_packet(packet):
    header = packet[:HEADER_SIZE]
    data = packet[HEADER_SIZE:]
    seq_num, ack_num, chk_sum = struct.unpack(HEADER_FORMAT, header)
    return seq_num, ack_num, chk_sum, data

def split_data(data, chunk_size):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

class ReliableDataTransferEntity:
    def __init__(self, inter_address, entity_address, window_size=4, timeout=True):
        self.inter_address = inter_address
        self.window_size = window_size
        self.entity_address = entity_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(entity_address)
        if timeout:
            self.sock.settimeout(TIMEOUT)

        self.base = 0  # Base sequence number (oldest unacknowledged packet)
        self.next_seq_num = 0  # Next packet to send
        self.unacked_packets = {}  # Track sent packets with timestamps

        self.expected_seq_num = 0  # Expected in-order sequence number

    def send(self, data):
        # data_list is the list of data packets that are to be sent for a current request
        # this is a local variable for this entity, and is not preserved between send instances, so
        # need to be careful when indexing
        data_list = split_data(data, BIT_RATE_SIZE)

        # if data_list is empty, we are actually try to emit an EOF packet, which our split_packet does not handle
        # therefore, add the empty b'' as a packet to send to signify EOF
        if data_list == []:
            data_list.append(b'')
        
        # sliding window
        prior_base = self.base  # save the current base so we have a starting point
        while self.base < len(data_list) + prior_base:
            # send packets up to the window size or packet list size
            while self.next_seq_num < self.base + self.window_size and self.next_seq_num < len(data_list) + prior_base:
                packet = create_packet(self.next_seq_num, 0, data_list[self.next_seq_num-prior_base])
                self.sock.sendto(packet, self.inter_address)
                self.unacked_packets[self.next_seq_num] = time.time()   # all packets are unacked to start
                print(f"Sent packet {self.next_seq_num}")
                time.sleep(BIT_RATE_TIME)
                self.next_seq_num += 1
            
            try:
                ack_packet, addr = self.sock.recvfrom(BUFFER_SIZE)

                ack_seq_num, _, chk_sum, data = parse_packet(ack_packet)
                if udp_checksum(data) != chk_sum:
                    print("Ack Packet corrupted! Ignoring.")
                    continue

                if ack_seq_num >= self.base:  # Move the window forward
                    print(f"ACK received for {ack_seq_num}")
                    self.base = ack_seq_num + 1  # Slide window

            except socket.timeout:
                # Retransmit all unacknowledged packets
                print("Timeout! Retransmitting unacknowledged packets.")
                for seq_num in range(self.base, self.next_seq_num):
                    packet = create_packet(seq_num, 0, data_list[seq_num-prior_base])
                    self.sock.sendto(packet, self.inter_address)
                    self.unacked_packets[seq_num] = time.time()
                    print(f"Retransmitted packet {seq_num}")

    def receive(self):
        while True:
            packet, addr = self.sock.recvfrom(BUFFER_SIZE)
            seq_num, _, chk_sum, data = parse_packet(packet)

            if udp_checksum(data) != chk_sum:
                print("Packet corrupted! Ignoring.")
                continue
            
            if seq_num == self.expected_seq_num:    # in-order packet
                print(f"Received in-order packet {seq_num}, sending ACK.")
                ack_packet = create_packet(seq_num, 0, b'')
                self.sock.sendto(ack_packet, addr)
                self.expected_seq_num += 1          # move expected sequence forward
                return packet
            elif seq_num < self.expected_seq_num:   # previously acked packet
                print(f"Received previously acked packet {seq_num}, re-sending ACK.")
                ack_packet = create_packet(seq_num, 0, b'')
                self.sock.sendto(ack_packet, addr)
            else:
                print(f"Out-of-order packet {seq_num} received. Expecting {self.expected_seq_num}. Ignoring.")




