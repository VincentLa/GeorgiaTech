#!/usr/bin/python

"Test server - This opens up the UDP port specified by the user in the command \
    line. Repeats back what it hears and closes."

# Based on http://pymotw.com/2/socket/tcp.html


import sys
import socket

if not (len(sys.argv) == 3):
    print "Syntax:"
    print "    python test-server.py <server-ip> <port>"
    print "  server-ip is the IP address of the server - use ifconfig to find."
    print "  port is the UDP port to open a socket on."
    exit()


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = (sys.argv[1], int(sys.argv[2]))
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

while True:
    # Wait for a connection

    try:

        # Receive the data in small chunks and retransmit it
        while True:
            data,client_address = sock.recvfrom(32)
            print >>sys.stderr, 'received "%s" from %s' % (data, client_address)
            if data:
                print >>sys.stderr, 'sending data back to the client'
                sock.sendto(data,client_address)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        print >>sys.stderr,'finished'	
