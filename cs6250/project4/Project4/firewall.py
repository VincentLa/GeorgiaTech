#!/usr/bin/python

# CS 6250 Summer 2019 - Project 4 - SDN Firewall
# 
# This script implements the firewall you create through the config file
# and the firewall-policy.py file.  You should not need to edit this 
# configuration file.  You do not submit this with your final submission.

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.modules.pyretic_switch import ActLikeSwitch
from pyretic.modules.firewall_policy import make_firewall_policy
import re
import os


policy_file = "%s/pyretic/pyretic/modules/firewall-policies.cfg" % os.environ[ 'HOME' ]

def main():
    """ Initialization of the Firewall. This pulls its rules from the file
            defined above. You can change this file pointer, but be sure to 
            change it back before submission! The run-firewall.sh file copies 
            over both this file and the configuration file to the correct 
            location."""
        
    # Parse the input file - make sure it's valid.
    config = parse_config(policy_file)
    
    # Get learning switch module
    learningSwitch = ActLikeSwitch()
    
    # Make Firewall policy
    fwPolicy = make_firewall_policy(config)

    # Return composed policy
    return fwPolicy >> learningSwitch


# The following function parses the configuration file.  You may not edit this section.

def parse_config(filename):
    with open(filename, 'r') as f:
        policies = []
        for line in f:
            # Skip if it's a comment (begins with #) or empty
            if re.match("#.*", line.strip()) != None:
                continue
            cleanline = ''.join(line.split())
            if cleanline == '':
                continue

            # Check that it's valid
            if len(cleanline.split(',')) != 8:
                raise TypeError("There are only %i parts to the line \"%s\"; there must be 8."
                                % (len(cleanline.split(',')), line))

            (rulenum, macaddr_src, macaddr_dst, ipaddr_src, ipaddr_dst, 
             port_src, port_dst, protocol) = cleanline.split(',')
            
            
            if (macaddr_src != '-' and
                None == re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", 
                                 macaddr_src.lower())):
                raise TypeError("Source MAC Address for rule %s is invalid" % rulenum)
            if (macaddr_dst != '-' and
                None == re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", 
                                 macaddr_dst.lower())):
                raise TypeError("Destination MAC Address for rule %s is invalid" % rulenum)
            
            if (ipaddr_src != '-' and not valid_ip(ipaddr_src)):
                raise TypeError("Source IP Address for rule %s is invalid" % rulenum)                
            if (ipaddr_dst != '-' and not valid_ip(ipaddr_dst)):
                raise TypeError("Destination IP Address for rule %s is invalid" % rulenum)                
                
            if (port_src != '-' and (int(port_src) > 65535 or int(port_src) < 1)):
                raise TypeError("Source Port for rule %s is invalid" % rulenum)                
            if (port_dst != '-' and (int(port_dst) > 65535 or int(port_dst) < 1)):
                raise TypeError("Destination Port for rule %s is invalid" % rulenum)                
            if (protocol != '-' and (protocol not in ('T','B','U','I'))):
                raise TypeError("protocol for rule %s is invalid (seeing protocol %s)" % (rulenum,protocol))    
            # Add it to the policies structure
            pol = {'rulenum':rulenum,
                   'macaddr_src':macaddr_src,
                   'macaddr_dst':macaddr_dst,
                   'ipaddr_src':ipaddr_src,
                   'ipaddr_dst':ipaddr_dst,
                   'port_src':port_src,
                   'port_dst':port_dst,
                   'protocol':protocol}
            policies.append(pol)

        return policies

# from https://stackoverflow.com/questions/11264005/using-a-regex-to-match-ip-addresses-in-python
def valid_ip(address):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False
