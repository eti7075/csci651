import pyshark

# input.pcap

# --- Output ---
# Ethernet Header: Packet size, Destination MAC Address, 
#   Source MAC Address, Ethertype
# IP Header: Version, Header length, Type of service, Total length, 
#   Identification, Flags, Fragment offset, Time to live, Protocol, 
#   Header checksum, Source and Destination IP addresses.
# Encapsulated Packets: TCP, UDP, or ICMP headers.

# --- Filtering ---
# support filtering based on the following
#   host
#   port
#   ip
#   tcp
#   udp
#   icmp
#   net

# use -c argument to limit number of packets analyzed

# example: pktsniffer -r input.pcap -c 5 port 80

# --- Tips ---
# use argparse to parse command line inputs
# keep stuff modular (might be reused in the future)
# use git to show progress