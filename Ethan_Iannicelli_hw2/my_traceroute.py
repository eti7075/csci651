#!/usr/bin/env python
import argparse
import socket
import struct
import sys

def traceroute(nqueries, destination, max_hops=64, timeout=2):
    destination_ip = socket.gethostbyname(destination)
    port = 33434 
    ttl = 1

    print(f"Tracerouting to {destination} ({destination_ip}) with a maximum of {max_hops} hops:")

    while ttl <= max_hops:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        recv_socket.settimeout(timeout)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        send_socket.settimeout(timeout)

        recv_socket.bind(('', port))
        send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

        send_socket.sendto(b'', (destination, port))
        
        curr_addr = None
        try:
            data, addr = recv_socket.recvfrom(512)
            curr_addr = addr[0]
        except socket.error as e:
            print(f"{ttl}\t* * *")
        else:
            print(f"{ttl}\t{curr_addr}")
            if curr_addr == destination_ip:
                break
        finally:
            recv_socket.close()
            send_socket.close()
            
        ttl += 1

def output(traceroute, numerical_flag):
    pass

def summarize(traceroute):
    pass

def initialize_parser():
    parser = argparse.ArgumentParser("my_traceroute argument parser")
    parser.add_argument("target", type=str, help="the target of the traceroute")
    parser.add_argument("-n", "--numerical", action="store_true", help="print hop addresses numerically rather than symbolically and numerically", required=False)
    parser.add_argument("-i", "--nqueries", type=int, help="Set the number of probes per TTL to nqueries", required=False)
    parser.add_argument("-S", "--summary", action="store_true", help="print a summary of how many probes were not answered for each hop", required=False)
    return parser

def my_traceroute():
    parser = initialize_parser()
    args = vars(parser.parse_args())

    nqueries = args["nqueries"] if args["nqueries"] else 3
    tr = traceroute(nqueries, args["target"])

    output(tr, args["numerical"])

    if args["summary"]:
        summarize(tr)



if __name__ == "__main__":
    my_traceroute()