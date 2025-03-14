import socket
import random
import time
import rdt_protocol

SENDER_PORT = ('127.0.0.1', rdt_protocol.SENDER_PORT)
INTER_PORT = ('127.0.0.1', rdt_protocol.INTER_PORT)
RECEIVER_PORT = ('127.0.0.1', rdt_protocol.RECEIVER_PORT)
BUFFER_SIZE = 1024
LOSS_PROBABILITY = 0.1
CORRUPTION_PROBABILITY = 0.1
REORDER_PROBABILITY = 0.1
DELAY_PROBABILITY = 0.05 
DELAY_TIME = 3

def simulate_loss(packet):
    """
    simulate packet loss

    :return: the packet if no loss, None if else
    :rtype: bitstring?
    """
    if random.random() < LOSS_PROBABILITY:
        print("Simulating packet loss.")
        return None
    return packet

def simulate_corruption(packet):
    """
    simulate packet curruption

    :return: the packet
    :rtype: bitstring
    """
    if random.random() < CORRUPTION_PROBABILITY and packet is not None:
        print("Simulating packet corruption.")
        corrupted_data = bytearray(packet)
        corrupted_data[random.randint(0, len(corrupted_data) - 1)] ^= 0xFF 
        return bytes(corrupted_data)
    return packet

def simulate_reordering(packet_queue):
    """
    simulate packet queue reordering

    :return: packet queue
    :rtype: array
    """
    if random.random() < REORDER_PROBABILITY and len(packet_queue) > 1:
        print("Simulating packet reordering.")
        packet_queue[0], packet_queue[1] = packet_queue[1], packet_queue[0]
    return packet_queue

def simulate_delay():
    """
    simulate packet delay via sleep
    """
    if random.random() < DELAY_PROBABILITY:
        print("Simulating artificial delay.")
        time.sleep(DELAY_TIME)

def handle_packet(packet, packet_queue, inter_socket, forward_address):
    """
    handles a packet by undergoing network conditions and forwarding to address

    :param packet: the packet to be handled
    :type packet: bitstring
    :param packet_queue: queue of packets to be delivered
    :type packet_queue: array
    :param inter_socket: the socket of this script
    :type inter_socker: socket
    :param forward_address: the address to forward the packet to
    :type forward_address: 2 tuple of ip and port
    """
    packet = simulate_loss(packet)
    packet = simulate_corruption(packet)
    simulate_delay()
    packet_queue.append((packet, forward_address))
    packet_queue = simulate_reordering(packet_queue)

    pkt, addr = packet_queue.pop(0)
    if pkt is not None:
        inter_socket.sendto(pkt, addr)

    print("-", end="")  # small output to show a packet was handled

def run_intermediary():  
    """
    runs the intermediary that acts as a network for this project. simulates network conditions
    and handles forwarding of packets
    """  
    inter_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inter_socket.bind(INTER_PORT)

    packet_queue = []

    print(f"Intermediary started, listening on port {INTER_PORT} (ctrl-C to quit)...")
    while True:
        packet, return_address = inter_socket.recvfrom(BUFFER_SIZE)

        if return_address == SENDER_PORT:
            handle_packet(packet, packet_queue, inter_socket,  RECEIVER_PORT)

        if return_address == RECEIVER_PORT:
            handle_packet(packet, packet_queue, inter_socket, SENDER_PORT)

if __name__ == "__main__":
    run_intermediary()
