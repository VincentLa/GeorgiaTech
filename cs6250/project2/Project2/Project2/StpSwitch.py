# Project 2 for OMS6250
#
# This defines a Spanning Tree Switch that serves as a Parent class to the switch class to be 
# implemented by the student.  It abstracts details of sending messages and verifying topologies.
#
# Copyright 2016 Michael Brown
#           Based on prior work by Sean Donovan, 2015

from Message import *
        	          
class StpSwitch(object):

    def __init__(self, idNum, topolink, neighbors):
    # switchID = id of the switch (lowest value determines root switcha nd breaks ties.)
    # topology = backlink to the Topology class. Used for sending messages.
    #   as follows: self.topology.send_message(message)
    # links = a list of the switch IDs linked to this switch.
        self.switchID = idNum
        self.topology = topolink
        self.links = neighbors

    # Invoked at initialization of topology of switches, this does NOT need to be invoked by student code.
    def verify_neighbors(self):
        ''' Verify that all your neighbors has a backlink to you. '''
        for neighbor in self.links:
            if self.switchID not in self.topology.switches[neighbor].links:
                raise Exception(str(neighbor) + " does not have link to " + str(self.switchID))

    # Wrapper for message passing to prevent students from having to access self.topology directly.
    def send_message(self, message):
        self.topology.send_message(message)
