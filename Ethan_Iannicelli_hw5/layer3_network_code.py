from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class CustomTopo(Topo):
    def build(self):
        # Routers
        rA = self.addNode('rA', cls=LinuxRouter, ip='20.10.172.129/26')
        rB = self.addNode('rB', cls=LinuxRouter, ip='20.10.172.1/25')
        rC = self.addNode('rC', cls=LinuxRouter, ip='20.10.172.193/27')

        # Hosts for LAN A
        hA1 = self.addHost('hA1', ip='20.10.172.130/26', defaultRoute='via 20.10.172.129')
        hA2 = self.addHost('hA2', ip='20.10.172.131/26', defaultRoute='via 20.10.172.129')

        # Hosts for LAN B
        hB1 = self.addHost('hB1', ip='20.10.172.2/25', defaultRoute='via 20.10.172.1')
        hB2 = self.addHost('hB2', ip='20.10.172.3/25', defaultRoute='via 20.10.172.1')

        # Hosts for LAN C
        hC1 = self.addHost('hC1', ip='20.10.172.194/27', defaultRoute='via 20.10.172.193')
        hC2 = self.addHost('hC2', ip='20.10.172.195/27', defaultRoute='via 20.10.172.193')

        # LAN links
        self.addLink(hA1, rA)
        self.addLink(hA2, rA)

        self.addLink(hB1, rB)
        self.addLink(hB2, rB)

        self.addLink(hC1, rC)
        self.addLink(hC2, rC)

        # Inter-router network (20.10.100.0/24)
        self.addLink(rA, rB, intfName1='rA-eth3', intfName2='rB-eth3', params1={'ip': '20.10.100.1/24'}, params2={'ip': '20.10.100.2/24'})
        self.addLink(rB, rC, intfName1='rB-eth4', intfName2='rC-eth3', params1={'ip': '20.10.100.3/24'}, params2={'ip': '20.10.100.4/24'})
        self.addLink(rC, rA, intfName1='rC-eth4', intfName2='rA-eth4', params1={'ip': '20.10.100.5/24'}, params2={'ip': '20.10.100.6/24'})

def run():
    topo = CustomTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.start()

    info('\n*** Ping test: hosts in the same LAN should be reachable\n')
    net.get('hA1').cmdPrint('ping -c 2 20.10.172.131')  # hA1 -> hA2
    net.get('hB1').cmdPrint('ping -c 2 20.10.172.3')    # hB1 -> hB2
    net.get('hC1').cmdPrint('ping -c 2 20.10.172.195')  # hC1 -> hC2

    info('\n*** Launching CLI\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
