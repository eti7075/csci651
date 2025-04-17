from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

class LinuxRouter(Node):
    # Enable forwarding on router
    def config(self, **params):
        super().config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super().terminate()

class MultiLANWithRouters(Topo):
    def build(self):
        # ---------------- LAN A ----------------
        sA = self.addSwitch('sA')
        rA = self.addNode('rA', cls=LinuxRouter, ip='20.10.172.129/26')  # router in LAN A
        hA1 = self.addHost('hA1', ip='20.10.172.130/26', defaultRoute='via 20.10.172.129')
        hA2 = self.addHost('hA2', ip='20.10.172.131/26', defaultRoute='via 20.10.172.129')

        self.addLink(hA1, sA)
        self.addLink(hA2, sA)
        self.addLink(rA, sA)

        # ---------------- LAN B ----------------
        sB = self.addSwitch('sB')
        rB = self.addNode('rB', cls=LinuxRouter, ip='20.10.172.1/25')
        hB1 = self.addHost('hB1', ip='20.10.172.2/25', defaultRoute='via 20.10.172.1')
        hB2 = self.addHost('hB2', ip='20.10.172.3/25', defaultRoute='via 20.10.172.1')

        self.addLink(hB1, sB)
        self.addLink(hB2, sB)
        self.addLink(rB, sB)

        # ---------------- LAN C ----------------
        sC = self.addSwitch('sC')
        rC = self.addNode('rC', cls=LinuxRouter, ip='20.10.172.193/27')
        hC1 = self.addHost('hC1', ip='20.10.172.194/27', defaultRoute='via 20.10.172.193')
        hC2 = self.addHost('hC2', ip='20.10.172.195/27', defaultRoute='via 20.10.172.193')

        self.addLink(hC1, sC)
        self.addLink(hC2, sC)
        self.addLink(rC, sC)

def run():
    topo = MultiLANWithRouters()
    net = Mininet(topo=topo, switch=OVSSwitch, controller=None)
    net.start()
    
    rA = net.get('rA')
    rB = net.get('rB')
    rC = net.get('rC')

    # Configure router interfaces (assumes they only have one interface each for now)
    rA.setIP('20.10.172.129/26', intf=rA.defaultIntf())
    rB.setIP('20.10.172.1/25', intf=rB.defaultIntf())
    rC.setIP('20.10.172.193/27', intf=rC.defaultIntf())

    print("\nRouters connected to each LAN.")
    print("Try pinging between hosts in each LAN, like: hA1 ping hA2")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
