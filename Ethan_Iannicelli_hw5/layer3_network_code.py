from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
    def build(self, **_opts):
        rA = self.addNode('rA', cls=LinuxRouter, ip='20.10.172.129/26')

        s1 = self.addSwitch('s1')
        self.addLink(s1, rA, intfName2='rA-eth1', params2={'ip': '20.10.172.129/26'})

        # Hosts with IPs in the /26 subnet and rA as gateway
        hA1 = self.addHost(name='hA1', ip='20.10.172.130/26', defaultRoute='via 20.10.172.129')
        hA2 = self.addHost(name='hA2', ip='20.10.172.131/26', defaultRoute='via 20.10.172.129')
        self.addLink(hA1, s1)
        self.addLink(hA2, s1)

        rB = self.addNode('rB', cls=LinuxRouter, ip='20.10.172.1/25')

        s2 = self.addSwitch('s2')
        self.addLink(s2, rB, intfName2='rB-eth1', params2={'ip': '20.10.172.1/25'})

        # Hosts with IPs in the /25 subnet and rB as gateway
        hB1 = self.addHost(name='hB1', ip='20.10.172.2/25', defaultRoute='via 20.10.172.1')
        hB2 = self.addHost(name='hB2', ip='20.10.172.3/25', defaultRoute='via 20.10.172.1')
        self.addLink(hB1, s2)
        self.addLink(hB2, s2)

        rC = self.addNode('rC', cls=LinuxRouter, ip='20.10.172.193/27')

        s3 = self.addSwitch('s3')
        self.addLink(s3, rC, intfName2='rC-eth1', params2={'ip': '20.10.172.193/27'})

        # Hosts with IPs in the /27 subnet and rC as gateway
        hC1 = self.addHost(name='hC1', ip='20.10.172.194/27', defaultRoute='via 20.10.172.193')
        hC2 = self.addHost(name='hC2', ip='20.10.172.195/27', defaultRoute='via 20.10.172.193')
        self.addLink(hC1, s3)
        self.addLink(hC2, s3)

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
