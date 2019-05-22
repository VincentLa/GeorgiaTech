#!/usr/bin/python

# CS6250 Computer Networks Project 1
# Loads the specified Topology and starts the Command Line Interface

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI

from complextopo import ComplexTopo

def runTopo():
    topo = ComplexTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('output')
    runTopo()
