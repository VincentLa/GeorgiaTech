#!/usr/bin/python

"Test client - This opens a connection to the IP and port specified by \
    the user in the command line. Sends over what is typed into the client."

# Based on http://pymotw.com/2/socket/tcp.html

import socket
import sys

if not (len(sys.argv) == 3):
    print "Syntax:"
    print "    python test-client.py <server-ip> <port>"
    print "  server-ip is the IP address running the server."
    print "  port is the TCP port that the server is running."
    exit()


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (sys.argv[1], int(sys.argv[2]))
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    # Send data
    message = 'This is the message.  It will be repeated.'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
