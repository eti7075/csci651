import socket
import random
import time
import struct
from rdt_protocol import checksum, parse_packet, create_packet, HEADER_SIZE, HEADER_FORMAT
import rdt_protocol

SENDER_PORT = ('127.0.0.1', rdt_protocol.SENDER_PORT)
INTER_PORT = ('127.0.0.1', rdt_protocol.INTER_PORT)
RECEIVER_PORT = ('127.0.0.1', rdt_protocol.RECEIVER_PORT)
BUFFER_SIZE = 1024
LOSS_PROBABILITY = 0.1
CORRUPTION_PROBABILITY = 0.1
REORDER_PROBABILITY = 0.1
DELAY_PROBABILITY = 0.05 
DELAY_TIME = 1

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
        corrupted_data[random.randint(0, len(corrupted_data) - 1)] ^= 0xFF 
        return bytes(corrupted_data)
    return packet

def simulate_reordering(packet_queue):
    """Simulate packet reordering with a certain probability."""
    if random.random() < REORDER_PROBABILITY and len(packet_queue) > 1:
        print("Simulating packet reordering.")
        packet_queue[0], packet_queue[1] = packet_queue[1], packet_queue[0]
    return packet_queue

def simulate_delay():
    """Simulate an artificial delay in packet transmission."""
    if random.random() < DELAY_PROBABILITY:
        print("Simulating artificial delay.")
        time.sleep(DELAY_TIME)

def handle_packet(packet, packet_queue, inter_socket, forward_address):
    """Handle the packet: apply network conditions and forward to receiver."""
    packet = simulate_loss(packet)
    packet = simulate_corruption(packet)
    simulate_delay()
    packet_queue.append((packet, forward_address))
    packet_queue = simulate_reordering(packet_queue)

    pkt, addr = packet_queue.pop(0)
    if pkt is not None:
        inter_socket.sendto(pkt, addr)

    print("packet handled")

def run_intermediary():
    """Simulate an intermediary that handles network conditions."""
    
    inter_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inter_socket.bind(INTER_PORT)

    packet_queue = []

    print(f"Intermediary started, listening on port {INTER_PORT}...")
    while True:
        packet, return_address = inter_socket.recvfrom(BUFFER_SIZE)

        if return_address == SENDER_PORT:
            handle_packet(packet, packet_queue, inter_socket,  RECEIVER_PORT)

        if return_address == RECEIVER_PORT:
            handle_packet(packet, packet_queue, inter_socket, SENDER_PORT)

if __name__ == "__main__":
    run_intermediary()
