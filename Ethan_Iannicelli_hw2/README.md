# Ping and Traceroute - HW2

## Ping

The ping python script sends a small ping to a specified destination repeatedly, recording the packet size and the round trip time. This program has multiple options:

- -c count: Stop after sending (and receiving) count ECHO_RESPONSE packets. If this option is not specified, ping will operate until interrupted.
- -i wait: Wait for wait seconds between sending each packet. Default is one second.
- -s packetsize: Specify the number of data bytes to be sent. Default is 56 (64 ICMP data bytes including the header).
- -t timeout: Specify a timeout in seconds before ping exits regardless of how many packets have been received.

Here are some example commands you can use when running the program:

- python my_ping.py 8.8.8.8 -c 5
- python my_ping.py 8.8.8.8 -i 5
- python my_ping.py 8.8.8.8 -s 70
- python my_ping.py 8.8.8.8 -t 10

  8.8.8.8 is the dns server for google, which is easily accessible and almostalways online.

** Note ** When running this program, you may need to enable admin privileges, for example on MacOS: sudo python my_ping ...

## Traceroute

The traceoute program performs a traceroute operation to track the intermediate servers between your local machine and a target destination. It also provides information regarding the probe success at each hop. Here are the provided options that go with this program:

- -n: Print hop addresses numerically rather than symbolically and numerically.
- -q nqueries: Set the number of probes per TTL to nqueries.
- -S: Print a summary of how many probes were not answered for each hop.

Here are some example commands you can use when running this program:

- python my_traceroute.py 8.8.8.8 -n
- python my_traceroute.py 8.8.8.8 -q 5
- python my_traceroute.py 8.8.8.8 -S

** Note ** Similar to the ping program, you may have to run this with admin privileges.
