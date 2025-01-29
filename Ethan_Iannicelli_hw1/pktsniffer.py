import pyshark
import argparse

def get_eth_summary(packet):
  # Ethernet Header: Packet size, Destination MAC Address, 
  #   Source MAC Address, Ethertype
  if 'ETH' in packet:
    eth_layer = packet.eth
    print(f"Ethernet Header:")
    print(f"  Packet Size: {packet.length}")
    print(f"  Destination MAC Address: {eth_layer.dst}")
    print(f"  Source MAC Address: {eth_layer.src}")
    print(f"  Ethertype: {eth_layer.type}")

def get_ip_summary(packet):
  # IP Header: Version, Header length, Type of service, Total length, 
  #   Identification, Flags, Fragment offset, Time to live, Protocol, 
  #   Header checksum, Source and Destination IP addresses.
  if 'IP' in packet:
    ip_layer = packet.ip
    print("IP Header:")  
    print(f"  Version: {ip_layer.version}")
    print(f"  Header Length: {ip_layer.hdr_len}")
    print(f"  Type of Service: {ip_layer.dsfield}")   # Double check this. ToS -> DSCP? ECN?
    print(f"  Total Length: {ip_layer.len}")
    print(f"  Identification: {ip_layer.id}")
    print(f"  Flags: {ip_layer.flags}")
    print(f"  Fragment Offset: {ip_layer.frag_offset}")
    print(f"  Time to Live: {ip_layer.ttl}")
    print(f"  Protocol: {ip_layer.proto}")
    print(f"  Header Checksum: {ip_layer.checksum}")
    print(f"  Source IP Address: {ip_layer.src}")
    print(f"  Desticnation IP Address: {ip_layer.dst}")
  
def get_encapsulated_packets_summary(packet):
  # Encapsulated Packets: TCP, UDP, or ICMP headers.
  if 'UDP' in packet:
    udp_layer = packet.udp
    print(udp_layer)

  if 'TCP' in packet:
    tcp_layer = packet.tcp
    print(tcp_layer)

  if 'ICMP' in packet:
    icmp_layer = packet.icmp
    print(icmp_layer)

# --- Output ---
def get_packet_summary(packet):
  get_eth_summary(packet)
  get_ip_summary(packet)
  get_encapsulated_packets_summary(packet)

def filter_by_host(packets, host):
  return [packet for packet in packets if packet.ip.src == host | packet.ip.dst == host]

def has_port(packet, port):
  if 'TCP' in packet:
    return packet.tcp.src == port | packet.tcp.dst == port
  elif 'UDP' in packet:
    return packet.udp.src == port | packet.udp.dst == port
  else:
    return False

def filter_by_port(packets, port):
  return [packet for packet in packets if has_port(packet, port)]

def filter_by_ip(packets, ip):
  return [packet for packet in packets if packet.version == ip]

def filter_by_tcp(packets):
  return [packet for packet in packets if 'TCP' in packet]

def filter_by_udp(packets):
  return [packet for packet in packets if 'UDP' in packet]

def filter_by_icmp(packets):
  return [packet for packet in packets if 'TCP' not in packet and 'UDP' not in packet]

def filter_by_net(packets, net):
  net = '.'.join(net.split('.')[0:2])
  return [packet for packet in packets if packet.ip.src.startswith(net) | packet.ip.dst.startswith(net)]

def filter_packets(packets, filters):
  if filters["filter_type"] == "host":
    packets = filter_by_host(packets, filters['filter_value'])
  if filters["filter_type"] == "port":
    packets = filter_by_port(packets, filters['filter_value'])
  if filters["filter_type"] == "ip":
    packets = filter_by_ip(packets, filters['filter_value'])
  if filters["filter_type"] == "net":
    packets = filter_by_net(packets, filters['filter_value'])
  if filters["tcp"]:
    packets = filter_by_tcp(packets)
  if filters["udp"]:
    packets = filter_by_udp(packets)
  if filters["icmp"]:
    packets = filter_by_icmp(packets)
  if filters["count"] != None:
    packets = packets[0:filters["count"]]
  return packets

def initialize_parser():
  parser = argparse.ArgumentParser("packet sniffer argument parser")
  parser.add_argument("-r", "--read", type=str, help="relative filename address for the pcap file to be analyzed", required=True)

  parser.add_argument("filter_type", nargs="?", choices=["host", "port", "ip", "net"], help="type of the filter")
  parser.add_argument("filter_value", nargs="?", help="Value for the selected filter")
  parser.add_argument("-tcp", "--tcp", action="store_true", help="does this packet contain a TCP header?", required=False)
  parser.add_argument("-udp", "--udp", action="store_true", help="does this packet contain a UDP header?", required=False)
  parser.add_argument("-icmp", "--icmp", action="store_true", help="does this packet contain a ICMP header?", required=False)

  parser.add_argument("-c", "--count", type=int, help="final number of packets to be summarized after filtering", required=False)
  return parser
  

def main():

  parser = initialize_parser()
  args = vars(parser.parse_args())
  print(args)
  
  # input.pcap as capture
  capture = pyshark.FileCapture(args["read"])

  # reduced to array for testing, easy to change the size of the packets array
  packets = filter_packets([packet for packet in capture], args)

  # summarize each packet
  for packet in packets:
    get_packet_summary(packet)

main()



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