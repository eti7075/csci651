#!/usr/bin/env python
import argparse
import time
import signal
import socket
import os
import struct

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_RESPONSE = 0

def checksum(data):
    """
    Creates the checksum for a given data for icmp packet

    :param data: the input data for the checksum
    :type data: String
    :return: calculated checksum
    :rtype: bitstring
    """
    sum = 0
    count_to = (len(data) // 2) * 2
    count = 0

    while count < count_to:
        this_val = data[count] + (data[count + 1] << 8)
        sum = sum + this_val
        sum = sum & 0xffffffff
        count = count + 2

    if count_to < len(data):
        sum = sum + data[count]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def create_packet(id, size):
    """
    Create a packet with a given id and of a given size

    :param id: id of the new packet
    :type id: string
    :param size: size of the new packet
    :type size: int
    :return: the new icmp packet
    :rtype: network packet
    """
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = bytes(size)  # simulate packet of size: {size}
    my_checksum = checksum(header + data) # recalculate checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, 1)
    return header + data

def send_ping(target, packetsize):
    """
    Send a recieve a packet to a given target (of a given packetsize)

    :param target: the target destination
    :type target: string
    :param packetsize: size of packets to be used as the pings
    :type packetsize: int
    :return: status of this ping
    :rtype: boolean
    """
    success = False
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        packet_id = os.getpid() & 0xFFFF
        packet = create_packet(packet_id, packetsize)

        sock.sendto(packet, (target, 1)) # (ip_address, port_number)
        response = receive_ping(sock, packet_id, packetsize)

        if response:
            ip, rtt, rsize = response
            print(f"{rsize} bytes from {ip}: time={rtt:.2f}ms")
            success = True # indicate a successful ping response
        else:
            print("request timed out") 
    except Exception as e:
        print(f"error during ping attempt: {e}")
    finally:
        sock.close()

    return success

def receive_ping(sock, packet_id, packetsize, timeout=10):
    """
    recieve a icmp ping echo response. the socket and packet_id are provided, so we
    know what to look for. A default timeout of 10 seconds is also applied, which should be plenty
    for any address that is known to be online

    :param sock: the socket that is prepared to accept the echo response
    :type sock: socket
    :param packet_id: id of the incoming echo response packet
    :type packet_id: string
    :return: a tuple of the target address, rtt, and size of icmp packet
    :rtype: tuple(string, double, int)
    """
    # measure rtt from the point at which we are trying to recieve the echo response
    start_time = time.time()
    while True: # loop until response is received
        elapsed_time = time.time() - start_time
        remaining_time = timeout - elapsed_time
        if remaining_time <= 0:
            return None  # Check for timeout - response took too long to return

        # recieve a packet as big as 28 + icmp packet size
        # handle the IP header and icmp header
        recv_packet, addr = sock.recvfrom(packetsize + 28) 
        recv_time = time.time()

        # Extract ICMP Header from the received packet (skip the IP header)
        icmp_header = recv_packet[20:28]  # ICMP header is located after the 20-byte IP header
        icmp_type, code, checksum, response_id, sequence = struct.unpack("bbHHh", icmp_header)

        if icmp_type == ICMP_ECHO_RESPONSE and response_id == packet_id:
            round_trip_time = (recv_time - start_time) * 1000  # Convert to milliseconds
            return addr[0], round_trip_time, len(recv_packet) - 28 # Return sender IP, RTT and ICMP response echo size

def initialize_parser():
    """
    initialize the parser for this program. The only required argument is the 'target' which is the target ip address
    to be pinged. Optional arguments include count, wait, packetsize, and timeout

    :return: fully initialized parser
    :rtype: parser
    """
    parser = argparse.ArgumentParser("my_ping argument parser")
    parser.add_argument("target", type=str, help="the target to be pinged")
    parser.add_argument("-c", "--count", type=int, help="max number of packets to send", required=False)
    parser.add_argument("-i", "--wait", type=int, help="wait length between sending each packet. default is one second", required=False)
    parser.add_argument("-s", "--packetsize", type=int, help="number of data bytes to be send. default is 54 bytes", required=False)
    parser.add_argument("-t", "--timeout", type=int, help="timeout in seconds before ping exits regardless of status", required=False)
    return parser

def timeout_handler(signum, frame):
    """
    handler for a program timeout. calls os._exit() to avoid raising an error, as this
    can be called as part of an expected functionality
    """
    print("Exited due to timeout")
    os._exit(1)

def my_ping():
    parser = initialize_parser()
    args = vars(parser.parse_args())

    count = -1 if args["count"] == None else args["count"]
    wait = 1 if args["wait"] == None else args["wait"]
    packetsize = 56 if args["packetsize"] == None else args["packetsize"]
    timeout = -1 if args["timeout"] == None else args["timeout"]

    if timeout != -1:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout) 

    echo = 0
    while (True):
        status = send_ping(args["target"], packetsize)
        echo += 1 if status else 0
        if (echo == count): break
        time.sleep(wait)

if __name__ == "__main__":
    my_ping()