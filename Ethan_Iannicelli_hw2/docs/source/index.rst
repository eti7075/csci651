ping_and_traceroute documentation
=================================
Ping Summary
------------

To get the checksum of an ICMP packet based on the
string representation of the packet, use the ``checksum()`` function:

.. autofunction:: my_ping.checksum

To create a ping icmp packet based on a packet id and size,
use the ``create_packet()`` function:

.. autofunction:: my_ping.create_packet

To send a ping to a target ip address, use the ``send_ping()`` function:

.. autofunction:: my_ping.send_ping

To recieve a ping echo response, use the ``receive_ping()`` function:

.. autofunction:: my_ping.receive_ping

To initialize the parser for a ping program,
use the ``initialize_parser()`` function:

.. autofunction:: my_ping.initialize_parser

To handle a timeout event, use the ``timeout_handler()`` function:

.. autofunction:: my_ping.timeout_handler

.. toctree::
   :maxdepth: 2
   :caption: Contents:

