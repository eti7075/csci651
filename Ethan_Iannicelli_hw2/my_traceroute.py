#!/usr/bin/env python
import argparse

def traceroute(nqueries):
    pass

def output(traceroute, numerical_flag):
    pass

def summarize(traceroute):
    pass

def initialize_parser():
    parser = argparse.ArgumentParser("my_traceroute argument parser")
    parser.add_argument("-n", "--numerical", action="store_true", help="print hop addresses numerically rather than symbolically and numerically", required=False)
    parser.add_argument("-i", "--nqueries", type=int, help="Set the number of probes per TTL to nqueries", required=False)
    parser.add_argument("-S", "--summary", action="store_true", help="print a summary of how many probes were not answered for each hop", required=False)
    return parser

def my_traceroute():
    parser = initialize_parser()
    args = vars(parser.parse_args())
    print(args)

    tr = traceroute(args["nqueries"])

    output(tr, args["numerical"])

    if args["summary"]:
        summarize(tr)



if __name__ == "__main__":
    my_traceroute()