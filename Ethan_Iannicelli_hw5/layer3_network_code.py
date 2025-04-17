from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

class MultiLAN(Topo):
    def build(self):
        # LAN A
        sA = self.addSwitch('sA')
        hA1 = self.addHost('hA1', ip='20.10.172.129/26')
        hA2 = self.addHost('hA2', ip='20.10.172.130/26')
        self.addLink(hA1, sA)
        self.addLink(hA2, sA)

        # LAN B
        sB = self.addSwitch('sB')
        hB1 = self.addHost('hB1', ip='20.10.172.1/25')
        hB2 = self.addHost('hB2', ip='20.10.172.2/25')
        self.addLink(hB1, sB)
        self.addLink(hB2, sB)

        # LAN C
        sC = self.addSwitch('sC')
        hC1 = self.addHost('hC1', ip='20.10.172.193/27')
        hC2 = self.addHost('hC2', ip='20.10.172.194/27')
        self.addLink(hC1, sC)
        self.addLink(hC2, sC)

def run():
    topo = MultiLAN()
    net = Mininet(topo=topo, switch=OVSSwitch)
    net.start()

    print("\n✅ All LANs created. You can test connectivity within LANs.")
    print("Try: hA1 ping hA2 | hB1 ping hB2 | hC1 ping hC2")
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
