#!/usr/bin/env python
import pyshark
import argparse

def get_eth_summary(packet):
  """
  Print selected ethernet header properties in a formatted manner

  :param packet: required packet to be summarized
  :type packet: pyshark packet
  """
  if 'ETH' in packet:
    eth_layer = packet.eth
    print(f"Ethernet Header:")
    print(f"  Packet Size: {packet.length}")
    print(f"  Destination MAC Address: {eth_layer.dst}")
    print(f"  Source MAC Address: {eth_layer.src}")
    print(f"  Ethertype: {eth_layer.type}")

def get_ip_summary(packet):
  """
  Print selected ip header properties in a formatted manner

  :param packet: required packet to be summarized
  :type packet: pyshark packet
  """
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
  """
  Print any encapsulated packet(s) in a given packet (not specially
  formatted, does not extract specific properties)

  :param packet: required packet to be summarized
  :type packet: pyshark packet
  """
  if 'UDP' in packet:
    udp_layer = packet.udp
    print(udp_layer)

  if 'TCP' in packet:
    tcp_layer = packet.tcp
    print(tcp_layer)

  if 'ICMP' in packet:
    icmp_layer = packet.icmp
    print(icmp_layer)

def get_packet_summary(packet):
  """
  Print all available header summaries for a given packet

  :param packet: required packet to be summarized
  :type packet: pyshark packet
  """
  get_eth_summary(packet)
  get_ip_summary(packet)
  get_encapsulated_packets_summary(packet)

def filter_by_host(packets, host):
  """
  Filter all packets if they contain the host address in either the
  packet ip source property or the packet destination property

  :param packets: List of packets
  :type packets: list[pyshark packet]
  :param host: host to filter by
  :type host: MAC address
  :return: the filtered list
  :rtype: list[pyshark packet]
  """
  return [packet for packet in packets if packet.ip.src == host | packet.ip.dst == host]

def has_port(packet, port):
  """
  Check if a packet has a port number in a encapsulated TCP
  or UDP packet at the source or destination property

  :param packet: the packet to be checked
  :type packet: pyshark packet
  :param port: the port number
  :type port: Int
  :return: the boolean value indicating if the packet has the port
  :rtype: boolean
  """
  if 'TCP' in packet:
    return packet.tcp.src == port | packet.tcp.dst == port
  elif 'UDP' in packet:
    return packet.udp.src == port | packet.udp.dst == port
  else:
    return False

def filter_by_port(packets, port):
  """
  Filter all packets if they contain the port in either the
  encapsulated packet source property or encapsulated packet
  destination property

  :param packets: List of packets
  :type packets: list[pyshark packet]
  :param port: port to filter by
  :type host: Int
  :return: the filtered list
  :rtype: list[pyshark packet]
  """
  return [packet for packet in packets if has_port(packet, port)]

def filter_by_ip(packets, ip):
  """
  Filter all packets if they contain the ip version in the 
  packet ip header

  :param packets: List of packets
  :type packets: list[pyshark packet]
  :param ip: ip version to filter by
  :type ip: Int
  :return: the filtered list
  :rtype: list[pyshark packet]
  """
  return [packet for packet in packets if packet.version == ip]

def filter_by_tcp(packets):
  """
  Filter all packets if they contain the same address in 
  either the packet ip source or destination property

  :param packets: List of packets
  :type packets: list[pyshark packet]
  :param net: net to filter by
  :type net: MAC address
  :return: the filtered list
  :rtype: list[pyshark packet]
  """
  return [packet for packet in packets if 'TCP' in packet]

def filter_by_udp(packets):
  """
  Filter all packets if they contain an encapsulated tcp packet

  :param packets: List of packets
  :type packets: list[pyshark packet]
  :return: the filtered list
  :rtype: list[pyshark packet]
  """
  return [packet for packet in packets if 'UDP' in packet]

def filter_by_icmp(packets):
  """
  Filter all packets if they contain an encapsulated udp packet

  :param packets: List of packets
  :type packets: list[pyshark packet]
  :return: the filtered list
  :rtype: list[pyshark packet]
  """
  return [packet for packet in packets if 'TCP' not in packet and 'UDP' not in packet]

def filter_by_net(packets, net):
  """
  Filter all packets if they contain an encapsulated icmp packet

  :param packets: List of packets
  :type packets: list[pyshark packet]
  :return: the filtered list
  :rtype: list[pyshark packet]
  """
  net = '.'.join(net.split('.')[0:2])
  return [packet for packet in packets if packet.ip.src.startswith(net) | packet.ip.dst.startswith(net)]

def filter_packets(packets, filters):
  """
  This function uses all the filtering helper functions to filter 
  a list of packets given a set of (active) filters

  :param packets: list of packets
  :type packets: list[pyshark packet]
  :param filters: the filters to use in filtering the packets
  :type filters: map<string, value>
  :return: list of filtered packets
  :rtype: list[pyshark packet]
  """
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
  """
  This function creates and defines the parser for the packet
  sniffer program, including file arguments, filtering arguments,
  and count arguments

  :return: the initialized parser
  :rtype: ArgParser
  """
  parser = argparse.ArgumentParser("packet sniffer argument parser")
  parser.add_argument("-r", "--read", type=str, help="relative filename address for the pcap file to be analyzed", required=True)

  parser.add_argument("filter_type", nargs="?", choices=["host", "port", "ip", "net"], help="type of the filter")
  parser.add_argument("filter_value", nargs="?", help="Value for the selected filter")
  parser.add_argument("-tcp", "--tcp", action="store_true", help="does this packet contain a TCP header?", required=False)
  parser.add_argument("-udp", "--udp", action="store_true", help="does this packet contain a UDP header?", required=False)
  parser.add_argument("-icmp", "--icmp", action="store_true", help="does this packet contain a ICMP header?", required=False)

  parser.add_argument("-c", "--count", type=int, help="final number of packets to be summarized after filtering", required=False)
  return parser
  

def pktsniffer():
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

if __name__ == "__main__":
  pktsniffer()

# commands to make executable and run via command line:
#   chmod +x pktsniffer.py
#   scp pktsniffer.py /usr/local/bin/pktsniffer
#   pktsniffer -r file.pcap host 192.168.0.1

# Alternatively, you can run it via python as:
#   python pktsniffer.py -r file.pcap host 192.168.0.1
