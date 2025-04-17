from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

class LAN_A(Topo):
    def build(self):
        # Create a switch to represent the LAN
        switch = self.addSwitch('s1')
        
        # Host 1 with IP 20.10.172.129/26
        h1 = self.addHost('h1', ip='20.10.172.129/26')
        self.addLink(h1, switch)

        # Host 2 with IP 20.10.172.130/26
        h2 = self.addHost('h2', ip='20.10.172.130/26')
        self.addLink(h2, switch)

def run():
    topo = LAN_A()
    net = Mininet(topo=topo, switch=OVSSwitch)
    net.start()

    print("\nTesting connectivity between hosts in LAN A...")
    net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
