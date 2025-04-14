# Peer 2 Peer File Transfer - Project

## Peer Architecure

The Peer architecure is composed of 3 main components: peer discovery, file chunk transfer, and a controller which mananges these components. The controller of the Peer sub-entities has two main funcitons. First, it serves to initialize the peer. This includes reading available files to session storage and intializing sub-entities. Second, the peer starts the command line UI that takes the form of a input loop. The peer's options are to list the available files on this peer, download a file from other peers, and exit the program.

## Peer Discovery

The peer discovery is a sub-entity of the peer itself. This takes place on a designated discovery port that all peers use. Every so often, a peer will broadcast its prescense, along with a port it sends requests data and a port that can be used to receive non-requested, distributed packets. On receiving a broadcast, the peer discovery attempts to add the peer to a set of known peers (each peer must remain unique). When a peer shuts down, they send a broadcast with their info that also includes a signal to remove the peer from the network.

## Peer File Transfer

The file transfer sub-entity is responsible for all messages sent that contain data relating to the files. This involves designating 4 ports for separate operations, all based on the `transfer_port`:
- receiver_port = transfer_port: port used to receive packets sent to fufill a file download request
- sender_port = transfer_port + 1: port used to send packet to fufill a file download request
- distributor_port = transfer_port + 2: port used for distributing chunks to all peers in the network
- distributee_port = transfer_port + 2: port used for receiving distributed chunks from other peers

These ports also describe the different actions that the file tranfer entity performs.

## How To

Using this peer 2 peer file sharing is easy. In the directory of this project, you will fine the folders peer1, peer2, and peer3. In separate terminals, navigate to these folders and enter the following command:
- python ../src/main.py -t X001
where X is the respective peer that is being used. You will then see the peer start up, and the different services being running. DUring this, you will be prompted to either 
- list
- download <file>
- exit
Entering a command will result in the action taking place. Downloaded files will be found in the downloads folder of your peer, and the files that each peer 'offers' the others is found in the shared folder. Messages should appear that notify you what state the application is in and what actions it performs.

Note: when exiting the program, be sure to use `exit` command rather than `crtl-c` or closing the window. While both these actions will terminate the program, only entering `exit` will send the broadcast signal to remove a peer from the group of known peers.

## Extending to more than one device

This program currently only supports locally hosting file sharing, which obviously is not real world applicable. To fix this, we would add a feature to change the default IP of each peer. Currently, the IP is hardcoded to `0.0.0.0` for localhost. While this does limit the capabilites of the program, the logic in other components is still sounds.



