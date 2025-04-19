# Mininet 

## Network Description

The network that this program creates has 3 LANs (routers in mininet), each of which is connected to two hosts via a switch. Additionally, each LAN is connected to each other, creating a network in which any host can reach another other host.

## Prerequisites

You have downloaded mininet from http://mininet.org/download/. If you are using a device with an Apple Silicone chip, I recommend using a VM such as UTM, since Virtual Box (mininet's official VM) does not support them. Additionally, the mininet VM provided does not come built in with the `traceroute` command, so you will have to install it via 
- `sudo apt update`
- `sudo apt install traceroute`
Running the mininet VM is very easy. After it is up an running, enter `mininet` for both username and password, then get the `layer3_network_code.py` file onto the VM in whatever way works for you.

## Running the Network

Running the network script is very easy. First, from the mininet VM, run 
- `sudo python layer3_network_code.py`
This should start the network, and you should see the nodes and links being generated. Once you see a `mininet> ` view in the CLI, you are ready to test the network. You can test the entire network availablity through `pingall`, or test individual connections through `ping` and `traceroute` commands. The naming convention for hosts is `hXY`, where X is the LAN (A, B, or C), and Y is the number of the host (1, 2). Routers are named like `rX`, where X is the LAN (A, B, C). For example, a `ping` command might look like:
- `hA1 ping hA2`
- `hB2 ping hC1`
A `traceroute` command might look like:
- `hA1 traceroute hA2`
- `hB2 traceroute hC1`
You are also able to view aspects of the network using other mininet commands, such as `arp`, `route`, `ifconfig`, or `net` (This list is not exhustive). 

Finally, to close the network, enter `exit` into the mininet CLI. This ends the network and cleans up the nodes and links cleanly.