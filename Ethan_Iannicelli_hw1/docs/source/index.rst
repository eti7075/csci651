PktSniffer documentation
========================
Packet Summary
--------------
To get the summary of the ethernet header, you can
use the ``get_eth_summary()`` function:

.. autofunction:: pktsniffer.get_eth_summary

To get the summary of the ip header, you can
use the ``get_ip_summary()`` function:

.. autofunction:: pktsniffer.get_ip_summary

To get the summary of an encapsulated packet, you can
use the ``get_encapsulated_packets_summary()`` function:

.. autofunction:: pktsniffer.get_encapsulated_packets_summary

To get all available packet summaries, you can 
use the ``get_packet_summary()`` function:

.. autofunction:: pktsniffer.get_packet_summary

To filter a list of packets by a host address, you can
use the ``filter_by_host()`` function:

.. autofunction:: pktsniffer.filter_by_host

To filter a list of packets by a port, you can
use the ``filter_by_port()`` function:

.. autofunction:: pktsniffer.filter_by_port

To check if a packet has a certain port number, you can
use the ``has_port()`` function:

.. autofunction:: pktsniffer.has_port

To filter a list of packets by a ip version, you can
use the ``filter_by_ip()`` function:

.. autofunction:: pktsniffer.filter_by_ip

To filter a list of packets by a net, you can
use the ``filter_by_net()`` function:

.. autofunction:: pktsniffer.filter_by_net

To filter a list of packets by a tcp, you can
use the ``filter_by_tcp()`` function:

.. autofunction:: pktsniffer.filter_by_tcp

To filter a list of packets by a udp, you can
use the ``filter_by_udp()`` function:

.. autofunction:: pktsniffer.filter_by_udp

To filter a list of packets by a icmp, you can
use the ``filter_by_icmp()`` function:

.. autofunction:: pktsniffer.filter_by_icmp

To filter a list of packets by all filters, use
the ``filter_packets()`` function:

.. autofunction:: pktsniffer.filter_packets

To initiate the program parser, you can use
the ``initialize_parser()`` function:

.. autofunction:: pktsniffer.initialize_parser

.. toctree::
   :maxdepth: 2
   :caption: Contents:
