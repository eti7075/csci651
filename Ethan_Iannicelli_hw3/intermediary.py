import socket
import random
import time
import struct
from rdt_protocol import checksum, parse_packet, create_packet, HEADER_SIZE, HEADER_FORMAT

# Constants
SENDER_PORT = ('127.0.0.1', 12347)
INTER_PORT = ('127.0.0.1', 12346)
RECEIVER_PORT = ('127.0.0.1', 12345)
BUFFER_SIZE = 1024
LOSS_PROBABILITY = 0.1    # 10% chance of packet loss
CORRUPTION_PROBABILITY = 0.1  # 10% chance of packet corruption
REORDER_PROBABILITY = 0.1   # 10% chance to reorder packets
DELAY_PROBABILITY = 0.05    # 5% chance to introduce artificial delay
DELAY_TIME = 1  # Delay time in seconds

# Simulate network conditions: loss, corruption, reordering, and delay
def simulate_loss(packet):
    """Simulate packet loss with a certain probability."""
    if random.random() < LOSS_PROBABILITY:
        print("Simulating packet loss.")
        return None
    return packet

def simulate_corruption(packet):
    """Simulate packet corruption with a certain probability."""
    if random.random() < CORRUPTION_PROBABILITY:
        print("Simulating packet corruption.")
        corrupted_data = bytearray(packet)
        corrupted_data[random.randint(0, len(corrupted_data) - 1)] ^= 0xFF  # Random byte corruption
        return bytes(corrupted_data)
    return packet

def simulate_reordering(packet_queue):
    """Simulate packet reordering with a certain probability."""
    if random.random() < REORDER_PROBABILITY and len(packet_queue) > 1:
        print("Simulating packet reordering.")
        packet_queue[0], packet_queue[1] = packet_queue[1], packet_queue[0]  # Swap first two packets
    return packet_queue

def simulate_delay():
    """Simulate an artificial delay in packet transmission."""
    if random.random() < DELAY_PROBABILITY:
        print("Simulating artificial delay.")
        time.sleep(DELAY_TIME)

def handle_packet(packet, packet_queue, inter_socket, forward_address):
    """Handle the packet: apply network conditions and forward to receiver."""
    # Apply network conditions
    # packet = simulate_loss(packet)
    # if packet is None:
    #     return  # Packet lost, do nothing

    # packet = simulate_corruption(packet)
    
    # simulate_delay()

    # Add packet to queue to simulate reordering
    # packet_queue.append(packet)
    # packet_queue = simulate_reordering(packet_queue)

    packet_queue = [packet]
    # Forward packets to receiver after conditions applied
    for pkt in packet_queue:
        print(f"forwarding packet: {pkt}")
        inter_socket.sendto(pkt, forward_address)

def run_intermediary():
    """Simulate an intermediary that handles network conditions."""
    
    # UDP socket for intermediary
    inter_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inter_socket.bind(INTER_PORT)  # Bind to an arbitrary local address and port

    packet_queue = []  # Queue for reordering packets

    print(f"Intermediary started, listening on port {INTER_PORT}...")
    while True:
        # Receive a packet from the sender
        packet, return_address = inter_socket.recvfrom(BUFFER_SIZE)

        print(return_address)

        # Process and forward the packet to the receiver
        if return_address == SENDER_PORT:
            handle_packet(packet, packet_queue, inter_socket,  RECEIVER_PORT)

        if return_address == RECEIVER_PORT:
            handle_packet(packet, packet_queue, inter_socket, SENDER_PORT)

if __name__ == "__main__":
    run_intermediary()
