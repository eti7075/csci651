import pyshark

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
    tcp_layer = packet.udp
    print(tcp_layer)

  if 'ICMP' in packet:
    icmp_layer = packet.udp
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
  pass

def filter_by_tcp(packets):
  return [packet for packet in packets if 'TCP' in packet]

def filter_by_udp(packets):
  return [packet for packet in packets if 'UDP' in packet]

def filter_by_icmp(packets):
  return [packet for packet in packets if 'TCP' not in packet and 'UDP' not in packet]

def filter_by_net(packets, net):
  pass

def filter_packets(packets, filters):
  if 'host' in filters:
    packets = filter_by_host(packets, filters['host'])
  if 'port' in filters:
    packets = filter_by_port(packets, filters['port'])
  if 'ip' in filters:
    packets = filter_by_ip(packets, filters['ip'])
  if 'tcp' in filters:
    packets = filter_by_tcp(packets)
  if 'udp' in filters:
    packets = filter_by_udp(packets)
  if 'icmp' in filters:
    packets = filter_by_icmp(packets)
  if 'net' in filters:
    packets = filter_by_net(packets, filters['net'])
  if 'c' in filters:
    packets = packets[0:filters['c']]
  return packets

def main():
  # input.pcap as capture
  capture = pyshark.FileCapture('input.pcap')

  # reduced to array for testing, easy to change the size of the packets array
  packets = [packet for packet in capture][0:1]

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