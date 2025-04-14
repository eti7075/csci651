.. Peer 2 Peer File Transfer documentation master file, created by
   sphinx-quickstart on Thu Apr 10 10:34:10 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Peer 2 Peer File Transfer documentation
=======================================

Peer
----
The ``Peer`` class represents a Peer entity in a P2P file transfer
system that supports broadcast discovery and chunk file shring with
other peers in the network:

.. autoclass:: peer.Peer
   :members:
   :undoc-members:
   :show-inheritance:

Discovery
---------
The ``PeerDiscovery`` class represents the entity responsible for broadcasting
and discovering other peers in a network. This broadcast is 'parent' peer, and 
detects other discovery entities that are serving their respective 'parent' peers:

.. autoclass:: discovery.PeerDiscovery
   :members:
   :undoc-members:
   :show-inheritance:

Transfer
--------
The ``FileTransfer`` class represents the entity responsible for distributing, receiving,
requesting, and sending file chunks to other peers. It is always in a state of distributing
and receiving file chunks from other peers, and when it's peer starts a file request it is 
responsible for getting this data from other peers and saving it to a file:

.. autoclass:: transfer.FileTransfer
   :members:
   :undoc-members:
   :show-inheritance:

Packet
------
To calculate the psuedo udp checksum of the data, use the ``udp_checksum()`` function. This
function is neccessary for maintaining packet integrity:

.. autofunction:: packet.udp_checksum

To create a packet from a chunk number and a chunk of data, use the ``create_packet()`` function:

.. autofunction:: packet.create_packet

To parse the components of a packet into its different parts, used the ``parse_packet()`` function.
The parts of the packet returned are the checksum, chunk_number, and the chunk data:

.. autofunction:: packet.parse_packet

Main
----
To create and return a parser for the program, use the ``parse_arguments()`` function:

.. autofunction:: main.parse_arguments

The main function of this program is ``main()``. It parsers arguments using a parser, and starts
and instance of the peer:

.. autofunction:: main.main

Logger
------
To get the logger from the program, use the ``get_logger()`` function:

.. autofunction:: utils.logger.get_logger

To create a formatted string output for a in memory stored file dictionary containing chunks, use
the ``format_file_chunks()`` function:

.. autofunction:: utils.logger.format_file_chunks

.. toctree::
   :maxdepth: 2
   :caption: Contents:

