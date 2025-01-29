import pyshark

# --- Output ---
def get_packet_summary(packet):
  # Ethernet Header: Packet size, Destination MAC Address, 
  #   Source MAC Address, Ethertype
  if 'ETH' in packet:
    eth_layer = packet.eth
    print(f"Ethernet Header:")
    print(f"  Packet Size: {packet.length}")
    print(f"  Destination MAC Address: {eth_layer.dst}")
    print(f"  Source MAC Address: {eth_layer.src}")
    print(f"  Ethertype: {eth_layer.type}")

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