#!/usr/bin/python
# CS 6250 Summer 2019 - Project 4 - SDN Firewall

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core import packet


def define_rules(policy, rule):
    """
    Helper Function that takes in a policy, rule and returns the rule.
    """
    # If Rules say block everything:
    if (policy['srcmac']=='-' and policy['dstmac']=='-' and policy['srcip']=='-' and policy['dstip']=='-' and policy['srcport']=='-' and policy['dstport']=='-' and policy['protocol']=='-'):
        rule = match(ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
    else:  
        #Check srcmac and dstmac
        if ((policy['srcmac'] != '-') and (policy['dstmac'] != '-')):
            rule = match(srcmac = EthAddr(policy['srcmac']), dstmac = EthAddr(policy['dstmac']))
        elif (policy['srcmac'] != '-'):
            rule = match(srcmac = EthAddr(policy['srcmac']))
        elif (policy['dstmac'] != '-'):
            rule = match(dstmac = EthAddr(policy['dstmac']))

        #Check dstport & srcport
        if (policy['srcport'] != '-'):
            rule = rule & match(srcport = int(policy['srcport']))
        if (policy['dstport'] != '-'):
            rule = rule & match(dstport = int(policy['dstport']))
        
        #Check srcip and dstip
        if ((policy['srcip'] != '-') and (policy['dstip'] != '-')):
            rule = rule & match(srcip = IPAddr(policy['srcip']), dstip=IPAddr(policy['dstip']))
        elif (policy['srcip'] != '-'):
            rule = rule & match(dstip = IPAddr(policy['srcip']))
        elif (policy['dstip'] != '-'):
            rule = rule & match(dstip = IPAddr(policy['dstip']))
    return rule


def make_firewall_policy(config):

    # You may place any user-defined functions in this space.
    # You are not required to use this space - it is available if needed.

    # feel free to remove the following "print config" line once you no longer need it
    print config # for demonstration purposes only, so you can see the format of the config

    rules = []

    # Make Dictionary of Firewall Policy
    firewall_policy = {}

    for entry in config:
        # TODO - This is where you build your firewall rules...
        # Note that you will need to delete the rule line below when you create your own
        # firewall rules.  Refer to the Pyretic github documentation for instructions on how to
        # format these commands.
        # Example (but incomplete)
        # rule = match(srcport = int(entry['port_src']))
        # The line below is hardcoded to match TCP Port 1080.  You must remove this line
        # in your completed assignments.  Do not hardcode your solution - you must use items
        # in the entry[] dictionary object to build your final ruleset for each line in the
        # policy file.
        firewall_policy[entry['rulenum']] = {
            'srcmac': entry['macaddr_src'],
            'dstmac': entry['macaddr_dst'],
            'srcip': entry['ipaddr_src'],
            'dstip': entry['ipaddr_dst'],
            'srcport': entry['port_src'],
            'dstport': entry['port_dst'],
            'protocol': entry['protocol']
        }

    for policy in firewall_policy.values():
        if policy['protocol']=='T':
            rules.append(define_rules(policy, match(ethtype=packet.IPV4, protocol= packet.TCP_PROTO)))

        elif policy['protocol']=='U':
            rules.append(define_rules(policy, match(ethtype=packet.IPV4, protocol= packet.UDP_PROTO)))

        elif policy['protocol']=='I':
            rules.append(define_rules(policy, match(ethtype=packet.IPV4, protocol= packet.ICMP_PROTO)))

        elif policy['protocol']=='B':
            rules.append(define_rules(policy, match(ethtype=packet.IPV4, protocol= packet.TCP_PROTO)))
            rules.append(define_rules(policy, match(ethtype=packet.IPV4, protocol= packet.UDP_PROTO)))
    
    allowed = ~(union(rules))

    return allowed


