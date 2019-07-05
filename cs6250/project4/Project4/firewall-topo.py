#!/usr/bin/python

# CS 6250 Summer 2019 - Project 4 - SDN Firewall
#
# This file defines to running topology for the network.  Feel free to edit
# versions of this file as different topologies may be used in grading your
# firewall_policy.py file.  However, make sure that the topology below
# is used when developing your my_config.cfg file.

from mininet.topo import Topo
from mininet.net  import Mininet
from mininet.node import CPULimitedHost, RemoteController
from mininet.util import custom
from mininet.link import TCLink
from mininet.cli  import CLI

class FWTopo(Topo):
    ''' Creates the following topoplogy:
                 e1   e2   e3
    server1  \     |    |    |
              \     \   |   /
    server2 ----  firewall (s1) --- mobile1
              /    /   |   \
    server3  /    |    |    |
                 w1    w2   w3
    '''
    def __init__(self, cpu=.1, bw=10, delay=None, **params):
        super(FWTopo,self).__init__()
        
        # Host in link configuration
        hconfig = {'cpu': cpu}
        lconfig = {'bw': bw, 'delay': delay}
        
        # Create the firewall switch
        s1 = self.addSwitch('s1')

        
        # Create East hosts and links)
        e1 = self.addHost('e1', **hconfig)
        e2 = self.addHost('e2', **hconfig)
        e3 = self.addHost('e3', **hconfig)
        self.addLink(s1, e1, port1=1, port2=1, **lconfig)
        self.addLink(s1, e2, port1=2, port2=1, **lconfig)
        self.addLink(s1, e3, port1=3, port2=1, **lconfig)
        
        # Create West hosts and links)
        w1 = self.addHost('w1', **hconfig)
        w2 = self.addHost('w2', **hconfig)
        w3 = self.addHost('w3', **hconfig)
        self.addLink(s1, w1, port1=4, port2=1, **lconfig)
        self.addLink(s1, w2, port1=5, port2=1, **lconfig)
        self.addLink(s1, w3, port1=6, port2=1, **lconfig)

        # Add 'host1' for packet flood testing
        mobile1 = self.addHost('mobile1', **hconfig)
        self.addLink(s1, mobile1, port1=7, port2=1, **lconfig)

        # Create Server hosts and links)
        server1 = self.addHost('server1', **hconfig)
        server2 = self.addHost('server2', **hconfig)
        server3 = self.addHost('server3', **hconfig)
        self.addLink(s1, server1, port1=8, port2=1, **lconfig)
        self.addLink(s1, server2, port1=9, port2=1, **lconfig)
        self.addLink(s1, server3, port1=10, port2=1, **lconfig)

def main():
    print "Starting topology"
    topo = FWTopo()
    net = Mininet(topo=topo, link=TCLink, controller=RemoteController, autoSetMacs=True)

    net.start()
    CLI(net)

if __name__ == '__main__':
    main()
