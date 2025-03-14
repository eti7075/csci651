.. Reliable Data Transfer Protocol documentation master file, created by
   sphinx-quickstart on Fri Mar 14 11:00:19 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Reliable Data Transfer Protocol documentation
=============================================

RDT Protocol
------------
To get the checksum of an ICMP packet based on the string representation of the packet, use the ``udp_checksum()`` function:

.. autofunction:: rdt_protocol.udp_checksum

To create a packet using a sequence number, acknowledgment number, and data, use the ``create_packet()`` function:

.. autofunction:: rdt_protocol.create_packet

To parse a packet into its sequence number, acknowledgment number, checksum, and data, use the ``parse_packet()`` function:

.. autofunction:: rdt_protocol.parse_packet

To split a bitstring of data into multiple parts of a given size, use the ``split_data()`` function:

.. autofunction:: rdt_protocol.split_data

The ``ReliableDataTransferEntity`` class represents an RDT entity that can act as a sender or receiver:

.. autoclass:: rdt_protocol.ReliableDataTransferEntity
    :members:
    :undoc-members:
    :show-inheritance:

To simulate packet loss, use the ``simulate_loss()`` function:

.. autofunction:: intermediary.simulate_loss

To simulate packet corruption, use the ``simulate_corruption()`` function:

.. autofunction:: intermediary.simulate_corruption

To simulate packet reordering in the packet queue, use the ``simulate_reordering()`` function:

.. autofunction:: intermediary.simulate_reordering

To simulate packet delay via sleep, use the ``simulate_delay()`` function:

.. autofunction:: intermediary.simulate_delay

To handle a packet by applying network conditions and forwarding it to an address, use the ``handle_packet()`` function:

.. autofunction:: intermediary.handle_packet

To run the intermediary that simulates network conditions and handles forwarding of packets, use the ``run_intermediary()`` function:

.. autofunction:: intermediary.run_intermediary

To send all data from a given file to the server, use the ``send_file()`` function:

The ``FileTransferClient`` class represents a client for the file transfer procedure:

.. autoclass:: client.FileTransferClient
    :members:
    :undoc-members:
    :show-inheritance:

To receive a file and save it to a designated folder, use the ``receive_file()`` function:

The ``FileTransferServer`` class represents a server for receiving and saving files:

.. autoclass:: server.FileTransferServer
    :members:
    :undoc-members:
    :show-inheritance:




.. toctree::
   :maxdepth: 2
   :caption: Contents:

