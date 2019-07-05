#!/usr/bin/python

"Test server - This opens up the port specified by the user in the command \
    line. Repeats back what it hears and closes."

# Based on http://pymotw.com/2/socket/tcp.html


import sys
import socket

if not (len(sys.argv) == 3):
    print "Syntax:"
    print "    python test-server.py <server-ip> <port>"
    print "  server-ip is the IP address of the server - use ifconfig to find."
    print "  port is the TCP port to open a socket on."
    exit()


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (sys.argv[1], int(sys.argv[2]))
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                print >>sys.stderr, 'sending data back to the client'
                connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()
