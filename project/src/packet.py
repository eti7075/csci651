import struct

# big endian, 4 bytes each
HEADER_FORMAT = '!I'  # checksum
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def udp_checksum(data):
    """
    perform a psuedo udp checksum by reducing the data to 4 bytes and taking one's complement

    :param data: the data that the checksum is created from
    :type data: bitstring
    :return: generated checksum
    :rtype: int
    """
    packet = data
    
    if len(packet) % 2 != 0:
        packet += b'\x00'
    
    s = 0
    for i in range(0, len(packet), 2):
        w = (packet[i] << 8) + packet[i + 1]
        s = s + w
        s = (s & 0xffff) + (s >> 16)
    
    checksum = ~s & 0xffff
    
    return checksum

def create_packet(data):
    """
    create a packet using packet data

    :param data: the data to be included in the packet
    :type data: bitstring
    :return: bitstring representing formed packet
    :rtype: bitstring
    """
    check_sum = udp_checksum(data)
    header = struct.pack(HEADER_FORMAT, check_sum)
    return header + data

def parse_packet(packet):
    """
    extracts checksum and data from a packet

    :param packet: formatted packet
    :type packet: bitstring
    :return: 2 tuple of check, data
    :rtype: tuple
    """
    header = packet[:HEADER_SIZE]
    data = packet[HEADER_SIZE:]
    chk_sum = struct.unpack(HEADER_FORMAT, header)
    return chk_sum[0], data