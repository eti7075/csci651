# Packet Sniffer - HW1

## Packet Headers Summaries

These headers are summarized based on the provided criteria. Each header extracts specific properties and displayes them in a formatted fashion.

### Ethernet Layer 
- Entire packet size: `packet.length`
- Ethernet MAC Destination: `packet.eth.dst`
- Ethernet MAC Source: `packet.eth.src`
- Ethernet Type: `packet.eth.type`

### IP Layer
- Version: `packet.ip.version`
- Header Length: `packet.ip.hdr_len`
- Type of Service: `packet.ip.dsfield`
    - Derived from this field, ToS is not directly available in newer version of PyShark
- Total Length: `packet.ip.len`
- Identification: `packet.ip.id`
- Flags: `packet.ip.flags`
- Fragment Offset: `packet.ip.frag_offset`
- Time to Live: `packet.ip.ttl`
- Protocol: `packet.ip.proto`
- Header Checksum: `packet.ip.checksum`
- Source IP Address: `packet.ip.src`
- Destination IP Address: `packet.ip.dst`

### Transport Layer (UDP, TCP, ICMP)
- UDP: `packet.udp`
- TCP: `packet.tcp`
- ICMP: `packet.icmp`

These layers are printed in their default state, and are not formatted and do not extract specific properties from each packet.

## Filtering Arguments

These filters can be used to look at a subset of the packets in a capture. They are provided to the program via the command line arguments.

### Port
The `port` argument filters by packets that have the same source or destination address in the transport layer

### Host
The `host` argument filters by packets that have the same source or destination address in the ip layer

### IP
The `ip` argument filters by packets that have the same IP version in the ip layer

### TCP, UDP, ICMP
The `tcp`, `udp`, and `icmp` arguments filter by packets that have the specified encapsulated packets

### Net
The `net` argument filters by packets that belong to the network or either the source or destination addresss in the ip layer. The network is defined as the first 3 sections of numbers - in `192.168.1.0`, we only care about `192.168.1.x`

### Count
The count argument limits the number of packets after all other filtering has been perfored

## Use

The program can be run from the command line as a basic python file with the command `python pktsniffer.py -r FILENAME.pcap ARGUMENTS VALUES(?)`. 

Alternatively, you can run this as an executable by issuing the following commands first:
- `chmod +x pktsniffer.py`
- `scp pktsniffer.py /usr/local/bin/pktsniffer`

Now, you can run the python executable via `pktsniffer -r FILENAME.pcap ARGUMENTS VALUES(?)`

Here are some examples to get you started.
- `pktsniffer -r input.pcap host ---- -c 5`
- `pktsniffer -r input.pcap net ---- -c 5`
- `pktsniffer -r input.pcap ip 4 -c 2`
- `pktsniffer -r input.pcap udp -c 3`
- `pktsniffer -r input.pcap tcp`
- `pktsniffer -r input.pcap port -- -c 10`
