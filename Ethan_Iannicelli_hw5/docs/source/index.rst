.. Mininet documentation master file, created by
   sphinx-quickstart on Fri Apr 18 20:23:52 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Mininet documentation
=====================

Mininet network
---------------
The ``LinuxRouter`` class represents a router that is a part of the network.
Notably, the net.ipv4.ip_forward value is set to 1 on initialization.

.. autoclass:: layer3_network_code.LinuxRouter
   :members:
   :undoc-members:
   :show-inheritance:

Our network topography is built in the ``NetworkTopo`` class. This class extends
the mininet ``Topo`` class, and overrides the ``build`` function
for this program.

.. autoclass:: layer3_network_code.NetworkTopo
   :members:
   :undoc-members:
   :show-inheritance:

To build, run and create routes between nodes, use the ``run`` function. This
function also starts the mininet CLI and cleans up the network on exiting.

.. autofunction:: layer3_network_code.run

.. toctree::
   :maxdepth: 2
   :caption: Contents:

