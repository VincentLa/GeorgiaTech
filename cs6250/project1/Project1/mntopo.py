from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import custom
																			
# Topology to be instantiated in Mininet
class MNTopo(Topo):
    "Mininet test topology"

    def __init__(self, cpu=.1, max_queue_size=None, **params):

        # Initialize topo
        Topo.__init__(self, **params)

        # Host and link configuration
        hostConfig = {'cpu': cpu}
        linkConfig = {'bw': 50, 'delay': '10ms', 'loss': 0,
                   'max_queue_size': max_queue_size }

        # Hosts and switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')  # Added
        s3 = self.addSwitch('s3')  # Added
        sender = self.addHost('sender', **hostConfig)
        receiver = self.addHost('receiver', **hostConfig)

        # Wire receiver
        self.addLink(receiver, s1, port1=0, port2=1, **linkConfig)

        # Wire s1
        self.addLink(s1, s2, port1=2, port2=1, **linkConfig)

        # Wire s2
        self.addLink(s2, s3, port1=2, port2=1, **linkConfig)

        # Wire sender
        self.addLink(sender, s3, port1=0, port2=2, **linkConfig)
