#!/usr/bin/env python
import argparse
import socket
import time

TRACEROUTE_PORT = 33434
DEFAULT_NQUERIES = 3
DEFAULT_MAX_HOPS = 30
DEFAULT_WAIT_TIMEOUT = 5

def traceroute(nqueries, destination, numerical_flag=False, max_hops=DEFAULT_MAX_HOPS, timeout=DEFAULT_WAIT_TIMEOUT):
    destination_ip = socket.gethostbyname(destination)
    port = TRACEROUTE_PORT 
    ttl = 1
    unanswered_counts = {}
    print(f"Tracerouting to {destination} ({destination_ip}) with a maximum of {max_hops} hops:")

    while ttl <= max_hops:
        unanswered = 0 
        name_output = ""
        probe_output = ""
        for _ in range(0, nqueries):
            recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            recv_socket.settimeout(timeout)
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            send_socket.settimeout(timeout)
            recv_socket.bind(('', port))
            start = time.time()
            send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            send_socket.sendto(b'', (destination, port))
            curr_addr = None
            try:
                _, addr = recv_socket.recvfrom(512)
                end = time.time()
                curr_addr = addr[0]
            except socket.error as e:
                unanswered += 1
                probe_output += " * "
            else:
                name_output = output(numerical_flag, curr_addr, ttl)
                elapsed = round((end-start) * 1000, 3) # convert to ms
                probe_output += f" {elapsed}ms "
            finally:
                recv_socket.close()
                send_socket.close()
        
        print(f"{ttl}\t{name_output}{probe_output}")
        unanswered_counts[ttl] = unanswered
        if curr_addr == destination_ip:
            break
        ttl += 1

    return unanswered_counts

def output(numerical_flag, addr, ttl):
    if numerical_flag:
        return f"{addr} "
    else:
        try:
            hostname, _, _ = socket.gethostbyaddr(addr)
        except socket.herror:
            hostname = addr
        return f"{hostname} ({addr}) "


def summarize(traceroute_summary):
    print("\nNumber of unanswered probes at each hop: ")
    for hop, _ in enumerate(traceroute_summary):
        print(f"Hop: {hop + 1} | Probes Lost: {traceroute_summary[hop + 1]}")

def initialize_parser():
    parser = argparse.ArgumentParser("my_traceroute argument parser")
    parser.add_argument("target", type=str, help="the target of the traceroute")
    parser.add_argument("-n", "--numerical", action="store_true", help="print hop addresses numerically rather than symbolically and numerically", required=False)
    parser.add_argument("-q", "--nqueries", type=int, help="Set the number of probes per TTL to nqueries", required=False)
    parser.add_argument("-S", "--summary", action="store_true", help="print a summary of how many probes were not answered for each hop", required=False)
    return parser

def my_traceroute():
    parser = initialize_parser()
    args = vars(parser.parse_args())

    nqueries = args["nqueries"] if args["nqueries"] else DEFAULT_NQUERIES
    tr = traceroute(nqueries, args["target"], numerical_flag=args["numerical"])

    if args["summary"]:
        summarize(tr)

if __name__ == "__main__":
    my_traceroute()