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
        switch = self.addSwitch('s1')

        # Add router without IP; assign manually after start
        rA = self.addNode('rA', cls=LinuxRouter, ip='20.10.172.129/26')
    
        s1 = self.addSwitch('s1')
    
        self.addLink(s1, rA, intfName2='rA-eth1', params2={'ip': '20.10.172.129/26'})

        # Hosts with IPs in the /26 subnet and rA as gateway
        hA1 = self.addHost(name='hA1', ip='20.10.172.130/26', defaultRoute='via 20.10.172.129')
        hA2 = self.addHost(name='hA2', ip='20.10.172.131/26', defaultRoute='via 20.10.172.129')

        # Connect everything to the switch
        self.addLink(hA1, switch)
        self.addLink(hA2, switch)

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
