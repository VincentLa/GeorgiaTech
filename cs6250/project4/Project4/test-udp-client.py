#!/usr/bin/python

"Test client - This opens a connection to the IP and port over UDP specified by \
    the user in the command line. Sends over what is typed into the client."

# Based on http://pymotw.com/2/socket/tcp.html

import socket
import sys

if not (len(sys.argv) == 3):
    print "Syntax:"
    print "    python test-client.py <server-ip> <port>"
    print "  server-ip is the IP address running the server."
    print "  port is the UDP port that the server is running."
    exit()


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect the socket to the port where the server is listening
server_address = (sys.argv[1], int(sys.argv[2]))

try:
    
    # Send data
    message = 'This is the message'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendto(message,server_address)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data, address = sock.recvfrom(32)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s" from %s' % (data,address)

finally:
    print >>sys.stderr, 'closing socket'
