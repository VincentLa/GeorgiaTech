#!/bin/bash

# Script to connect to a router's bgpd shell.
router=${1:-R1}
echo "Connecting to $router shell"

sudo python run.py --node $router --cmd "telnet localhost bgpd"
