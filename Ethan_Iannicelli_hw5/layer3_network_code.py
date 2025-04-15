#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

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
        routerA = self.addNode('rA', cls=LinuxRouter, ip='20.10.172.129/26')
        routerB = self.addNode('rB', cls=LinuxRouter, ip='20.10.172.1/25')
        routerC = self.addNode('rC', cls=LinuxRouter, ip='20.10.172.193/27')

        # Switches for each LAN
        sA = self.addSwitch('sA')
        sB = self.addSwitch('sB')
        sC = self.addSwitch('sC')

        # Hosts for LAN A
        hA1 = self.addHost('hA1', ip='20.10.172.130/26', defaultRoute='via 20.10.172.129')
        hA2 = self.addHost('hA2', ip='20.10.172.131/26', defaultRoute='via 20.10.172.129')
        self.addLink(hA1, sA)
        self.addLink(hA2, sA)
        self.addLink(sA, routerA)

        # Hosts for LAN B
        hB1 = self.addHost('hB1', ip='20.10.172.2/25', defaultRoute='via 20.10.172.1')
        hB2 = self.addHost('hB2', ip='20.10.172.3/25', defaultRoute='via 20.10.172.1')
        self.addLink(hB1, sB)
        self.addLink(hB2, sB)
        self.addLink(sB, routerB)

        # Hosts for LAN C
        hC1 = self.addHost('hC1', ip='20.10.172.194/27', defaultRoute='via 20.10.172.193')
        hC2 = self.addHost('hC2', ip='20.10.172.195/27', defaultRoute='via 20.10.172.193')
        self.addLink(hC1, sC)
        self.addLink(hC2, sC)
        self.addLink(sC, routerC)

        # Inter-router links using 20.10.100.0/24
        self.addLink(routerA, routerB,
                     intfName1='rA-eth1', intfName2='rB-eth1',
                     params1={'ip': '20.10.100.1/24'},
                     params2={'ip': '20.10.100.2/24'})

        self.addLink(routerB, routerC,
                     intfName1='rB-eth2', intfName2='rC-eth1',
                     params1={'ip': '20.10.100.3/24'},
                     params2={'ip': '20.10.100.4/24'})

        self.addLink(routerC, routerA,
                     intfName1='rC-eth2', intfName2='rA-eth2',
                     params1={'ip': '20.10.100.5/24'},
                     params2={'ip': '20.10.100.6/24'})

def run():
    topo = CustomTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.start()

    print("\n=== TESTING LOCAL LAN REACHABILITY ===\n")
    net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
