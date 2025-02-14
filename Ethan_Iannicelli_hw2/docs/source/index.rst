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

Traceroute Summary
------------------

To format the output for a traceroute address hop, use the ``output()`` function:

.. autofunction:: my_traceroute.output

To output a summary of the probes left unanswered at each hop, use
the ``summarize()`` function:

.. autofunction:: my_traceroute.summarize

To perform a traceroute operation to a target address, use
the ``traceroute()`` function:

.. autofunction:: my_traceroute.traceroute

To create and initialize the parser for the traceroute program,
use the ``initialize_parser()`` function:

.. autofunction:: my_traceroute.initialize_parser

.. toctree::
   :maxdepth: 2
   :caption: Contents:

