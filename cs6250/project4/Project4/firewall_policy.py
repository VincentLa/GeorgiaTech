#!/usr/bin/python
# CS 6250 Summer 2019 - Project 4 - SDN Firewall

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core import packet

from collections import namedtuple


def make_firewall_policy(config):

    # You may place any user-defined functions in this space.
    # You are not required to use this space - it is available if needed.

    # feel free to remove the following "print config" line once you no longer need it
    print config # for demonstration purposes only, so you can see the format of the config

    rules = []

    # Make Dictionary of Firewall Policy
    Policy_Rule= namedtuple('Policy_Rule',
                            ('srcmac', 'dstmac','srcip','dstip','srcport','dstport', 'protocol')
                           )
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
        firewall_policy[entry['rulenum']] = Policy_Rule(
            entry['macaddr_src'],
            entry['macaddr_dst'],
            entry['ipaddr_src'],
            entry['ipaddr_dst'],
            entry['port_src'],
            entry['port_dst'],
            entry['protocol']
        )

    for policy_rule in firewall_policy.values():
        if policy_rule.protocol=='T':
            rule = match(ethtype=packet.IPV4, protocol= packet.TCP_PROTO)
            rules.append(process_firewall_helper(policy_rule, rule))

        elif policy_rule.protocol=='U':
            rule = match(ethtype=packet.IPV4,protocol= packet.UDP_PROTO)
            rules.append(process_firewall_helper(policy_rule, rule))

        elif policy_rule.protocol=='I':
            rule = match(ethtype=packet.IPV4,protocol= packet.ICMP_PROTO)
            rules.append(process_firewall_helper(policy_rule, rule))

        elif policy_rule.protocol=='B':
            rule1 = match(ethtype=packet.IPV4,protocol= packet.TCP_PROTO) 
            rule2 = match(ethtype=packet.IPV4, protocol= packet.UDP_PROTO)
            rules.append(process_firewall_helper(policy_rule, rule1))
            rules.append(process_firewall_helper(policy_rule, rule2))
    
    allowed = ~(union(rules))

    return allowed


def process_firewall_helper(policy_rule, rule):
    # If Rules say block everything:
    if (policy_rule.srcmac == '-' and policy_rule.dstmac== '-' and policy_rule.srcip== '-' and policy_rule.dstip == '-' and policy_rule.srcport== '-' and policy_rule.dstport == '-' and policy_rule.protocol== '-'):
        print "Rules say Block Everything"
        rule = match(ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
    else:  
        #Check srcmac and dstmac
        if ((policy_rule.srcmac != '-') and (policy_rule.dstmac != '-')):
            rule = match(srcmac = EthAddr(policy_rule.srcmac), dstmac = EthAddr(policy_rule.dstmac))
        elif (policy_rule.srcmac != '-'):
            rule = match(srcmac = EthAddr(policy_rule.srcmac))
        elif (policy_rule.dstmac != '-'):
            rule = match(dstmac = EthAddr(policy_rule.dstmac))

        #Check dstport & srcport
        if (policy_rule.srcport != '-'):
            rule = rule & match(srcport = int(policy_rule.srcport))
        if (policy_rule.dstport != '-'):
            rule = rule & match(dstport = int(policy_rule.dstport))
        
        #Check srcip and dstip
        if ((policy_rule.srcip != '-') and (policy_rule.dstip != '-')):
            rule = rule & match(srcip = IPAddr(policy_rule.srcip), dstip=IPAddr(policy_rule.dstip))
        elif (policy_rule.srcip != '-'):
            rule = rule & match(dstip = IPAddr(policy_rule.srcip))
        elif (policy_rule.dstip != '-'):
            rule = rule & match(dstip = IPAddr(policy_rule.dstip))
    return rule


