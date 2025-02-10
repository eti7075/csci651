#!/usr/bin/env python
import argparse
import time
import signal

def send_ping(echos, packetsize):
    # send ping
    # ping response
    # output time and ping information
    echos += 1

def initialize_parser():
    parser = argparse.ArgumentParser("my_ping argument parser")
    parser.add_argument("-c", "--count", type=int, help="max number of packets to send", required=False)
    parser.add_argument("-i", "--wait", type=int, help="wait length between sending each packet. default is one second", required=False)
    parser.add_argument("-s", "--packetsize", type=int, help="number of data bytes to be send. default is 54 bytes", required=False)
    parser.add_argument("-t", "--timeout", type=int, help="timeout in seconds before ping exits regardless of status", required=False)
    return parser

def my_ping():
    parser = initialize_parser()
    args = vars(parser.parse_args())
    print(args)

    count = -1 if args["count"] == None else args["count"]
    wait = 1 if args["wait"] == None else args["wait"]
    packetsize = 56 if args["packetsize"] == None else args["packetsize"]
    timeout = -1 if args["timeout"] == None else args["timeout"]

    if timeout != -1:
        signal.signal(signal.SIGALRM, exit)
        signal.alarm(timeout) 

    echos = 0
    while (echos != count):
        send_ping(echos, packetsize)
        time.sleep(wait)

if __name__ == "__main__":
    my_ping()