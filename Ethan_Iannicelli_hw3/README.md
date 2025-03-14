# Reliable Data Transfer Protocol - HW3

## RDT Protocol

The rdt protocol is a separate class that is not run indepenently, but rather is utilized by other programs that are running themselves. In this project, those programs take the form of a mock client and mock server. This project makes use of hardcoded, static address and port numbers. Since this POC is meant to be run locally, the IP address is hardcoded to 127.0.0.1. THe port numbers are arbitrarily decided as 12345, 12346, and 12347. This allows us to run a client, server, and intermediary on the same time, each listening on different ports, representing different entities/programs.

## Intermediary

The intermediary in this project serves to simulate network conditions. It performs loss, corruption, reorddering, and packet delay, and essentially acts as a glorified forwarding service from the client/server to the server/client. This must be running for the RDT file transfer to take place. The command is as follows:

- python intermediary.py

To stop the program, use ctrl-C

## Server

The server in this file transfer example makes use of the RDT protocol and acts to receive the data extracted viua the RDT protocol. This accepts packets from the intermediary, and returns an ack to be forwarded to the sender. This must be running for the RDT file transfer to take place. The command is as follows:

- python server.py

To stop the program, use ctrl-C

## Client

The client in this file transfer example makes use of the RDT protocol to send data contained in a file to a server. This is done via the RDT protocol send() function, which using a sliding window methodology to increase link utilization. This is the most intensive part from a user interface perspective in this project.

First, to run the program, we use:
- python client.py

Then, we can enter the name of files we wish to transfer:
- file_to_send.txt
- file_to_send_long.txt
- file_to_send_even_longer.txt

The program will wait until a file is completely successful before prompting for the next file.

To end the program, we can enter 'quit' or ctrl-C. Since 'quit' is used to end the program, a filename as 'quit' will not be transfered. 

## Overall Summary

This project can easily be run through three terminal/command prompt windows that are open to the same directory. Files will be stored in a 'received_files/' folder of the project, and will be overwritten any time a duplicate file is 'transfered'. To measure the success of an operation, use this command:
- diff filename received_files/filename


