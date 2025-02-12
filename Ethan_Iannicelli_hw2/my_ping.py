#!/usr/bin/env python
import argparse
import time
import signal
import socket
import os
import select
import struct

ICMP_ECHO_REQUEST = 8

def checksum(source_string):
    sum = 0
    count_to = (len(source_string) // 2) * 2
    count = 0

    while count < count_to:
        this_val = source_string[count] + (source_string[count + 1] << 8)
        sum = sum + this_val
        sum = sum & 0xffffffff
        count = count + 2

    if count_to < len(source_string):
        sum = sum + source_string[count]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def create_packet(id, size):
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = bytes(size)  # 48-byte payload
    my_checksum = checksum(header + data)
    
    # Recreate header with correct checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, 1)
    return header + data

def send_ping(target, packetsize):
    success = False
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        packet_id = os.getpid() & 0xFFFF
        packet = create_packet(packet_id, packetsize)

        sock.sendto(packet, (target, 1)) # (ip_address, port_number)
        response = receive_ping(sock, packet_id)

        if response:
            ip, rtt, rsize = response
            print(f"{rsize} bytes from {ip}: time={rtt:.2f}ms")
            success = True
        else:
            print("Request timed out") 
    except Exception as e:
        print(f"error in ping: {e}")
    finally:
        sock.close()

    return success

def receive_ping(sock, packet_id, timeout=10):
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = timeout - elapsed_time
        
        if remaining_time <= 0:
            return None  # Timeout

        ready = select.select([sock], [], [], remaining_time)
        if not ready[0]:  
            return None  # Timeout

        recv_packet, addr = sock.recvfrom(1024)
        recv_time = time.time()

        # Extract ICMP Header from the received packet (skip the IP header)
        icmp_header = recv_packet[20:28]  # ICMP header is located after the 20-byte IP header
        icmp_type, code, checksum, response_id, sequence = struct.unpack("bbHHh", icmp_header)

        if icmp_type == 0 and response_id == packet_id:  # ICMP type 0 = Echo Reply
            round_trip_time = (recv_time - start_time) * 1000  # Convert to milliseconds
            return addr[0], round_trip_time, len(recv_packet) - 28 # Return sender IP, RTT and ICMP response echo size

def initialize_parser():
    parser = argparse.ArgumentParser("my_ping argument parser")
    parser.add_argument("target", type=str, help="the target to be pinged")
    parser.add_argument("-c", "--count", type=int, help="max number of packets to send", required=False)
    parser.add_argument("-i", "--wait", type=int, help="wait length between sending each packet. default is one second", required=False)
    parser.add_argument("-s", "--packetsize", type=int, help="number of data bytes to be send. default is 54 bytes", required=False)
    parser.add_argument("-t", "--timeout", type=int, help="timeout in seconds before ping exits regardless of status", required=False)
    return parser

def timeout_handler(signum, frame):
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
    while (echo != count):
        status = send_ping(args["target"], packetsize)
        echo += 1 if status else 0
        time.sleep(wait)

if __name__ == "__main__":
    my_ping()