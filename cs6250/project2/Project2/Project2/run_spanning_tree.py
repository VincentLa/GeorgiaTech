#!/usr/bin/python

# Project 2 for OMS6250 Spring 2017
#
# Usage:
# Generically, it is run as follows:
#     python run_spanning_tree.py <topology_file> <log_file>
# For instance, to run jellyfish_topo.py and log to jellyfish.log that we created, use the following:
#     python run_spanning_tree.py jellyfish_topo jellyfish.log
# Note how the topology file doesn't have the .py extension.
#
# Students should not modify this file.
#
# Copyright 2016 Michael Brown
#           Based on prior work by Sean Donovan, 2015


import sys
from Topology import *

if len(sys.argv) != 3:
    print "Syntax:"
    print "    python run_spanning_tree.py <topology_file> <log_file>"    
    exit()

# Populate the topology
topo = Topology(sys.argv[1])

# Run the topology.
topo.run_spanning_tree()

# Close the logfile
topo.log_spanning_tree(sys.argv[2])
