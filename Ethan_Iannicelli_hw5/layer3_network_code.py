from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    def config(self, **params):
        """
        Sets the configuration for the router. sets ipv4 forwarding to true.
        """
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        """
        Run on router ternimation. sets ipv4 forwarding to false
        """
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
    def build(self, **_opts):
        """
        Builds the network outlined for this homework. Three LANs represented by routers, each connected to 
        2 hosts via switches, and all routers connected through the provided IP gateway
        """
        # Create LAN A (Router A)
        rA = self.addNode('rA', cls=LinuxRouter, ip='20.10.172.129/26')

        # Create switch A that connects hosts to router
        s1 = self.addSwitch('s1')
        self.addLink(s1, rA, intfName2='rA-eth1', params2={'ip': '20.10.172.129/26'})

        # Hosts with IPs in the /26 subnet and rA as gateway
        hA1 = self.addHost(name='hA1', ip='20.10.172.130/26', defaultRoute='via 20.10.172.129')
        hA2 = self.addHost(name='hA2', ip='20.10.172.131/26', defaultRoute='via 20.10.172.129')
        self.addLink(hA1, s1)
        self.addLink(hA2, s1)

        # Create LAN B (Router B)
        rB = self.addNode('rB', cls=LinuxRouter, ip='20.10.172.1/25')

        # Create switch B that connects hosts to router
        s2 = self.addSwitch('s2')
        self.addLink(s2, rB, intfName2='rB-eth1', params2={'ip': '20.10.172.1/25'})

        # Hosts with IPs in the /25 subnet and rB as gateway
        hB1 = self.addHost(name='hB1', ip='20.10.172.2/25', defaultRoute='via 20.10.172.1')
        hB2 = self.addHost(name='hB2', ip='20.10.172.3/25', defaultRoute='via 20.10.172.1')
        self.addLink(hB1, s2)
        self.addLink(hB2, s2)

        # Create LAN C (Router C)
        rC = self.addNode('rC', cls=LinuxRouter, ip='20.10.172.193/27')

        # Create switch C that connects hosts to router
        s3 = self.addSwitch('s3')
        self.addLink(s3, rC, intfName2='rC-eth1', params2={'ip': '20.10.172.193/27'})

        # Hosts with IPs in the /27 subnet and rC as gateway
        hC1 = self.addHost(name='hC1', ip='20.10.172.194/27', defaultRoute='via 20.10.172.193')
        hC2 = self.addHost(name='hC2', ip='20.10.172.195/27', defaultRoute='via 20.10.172.193')
        self.addLink(hC1, s3)
        self.addLink(hC2, s3)

        # Task 3 - connect all three LANs (routers) to each other using the provided 20.10.100.0/24
        self.addLink(rA, rB, intfName1='rA-eth2', intfName2='rB-eth2', params1={'ip': '20.10.100.1/30'}, params2={'ip': '20.10.100.2/30'})
        self.addLink(rA, rC, intfName1='rA-eth3', intfName2='rC-eth2', params1={'ip': '20.10.100.5/30'}, params2={'ip': '20.10.100.6/30'})
        self.addLink(rB, rC, intfName1='rB-eth3', intfName2='rC-eth3', params1={'ip': '20.10.100.9/30'}, params2={'ip': '20.10.100.10/30'})

def run():
    """
    Create network for this assignment. Start the network running, then open the mininet CLI to support 
    running commands and examing network properties. Close the network when the CLI is exited.
    """
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    net.start()

    # Get hosts and routers
    hA1 = net.get('hA1')
    hA2 = net.get('hA2')
    hB1 = net.get('hB1')
    hB2 = net.get('hB2')
    hC1 = net.get('hC1')
    hC2 = net.get('hC2')

    rA = net.get('rA')
    rB = net.get('rB')
    rC = net.get('rC')

    # Add routes on hosts after the network has been started
    hA1.cmd('sudo route add -net 20.10.172.0 netmask 255.255.255.128 gw 20.10.172.129')
    hA1.cmd('sudo route add -net 20.10.172.192 netmask 255.255.255.224 gw 20.10.172.129')
    hA2.cmd('sudo route add -net 20.10.172.0 netmask 255.255.255.128 gw 20.10.172.129')
    hA2.cmd('sudo route add -net 20.10.172.192 netmask 255.255.255.224 gw 20.10.172.129')
    
    hB1.cmd('sudo route add -net 20.10.172.128 netmask 255.255.255.192 gw 20.10.172.1')
    hB1.cmd('sudo route add -net 20.10.172.192 netmask 255.255.255.224 gw 20.10.172.1')
    hB2.cmd('sudo route add -net 20.10.172.128 netmask 255.255.255.192 gw 20.10.172.1')
    hB2.cmd('sudo route add -net 20.10.172.192 netmask 255.255.255.224 gw 20.10.172.1')

    hC1.cmd('sudo route add -net 20.10.172.0 netmask 255.255.255.128 gw 20.10.172.193')
    hC1.cmd('sudo route add -net 20.10.172.128 netmask 255.255.255.192 gw 20.10.172.193')
    hC2.cmd('sudo route add -net 20.10.172.0 netmask 255.255.255.128 gw 20.10.172.193')
    hC2.cmd('sudo route add -net 20.10.172.128 netmask 255.255.255.192 gw 20.10.172.193')

    # Add routes between routers after the network has been started
    rA.cmd('sudo route add -net 20.10.172.0 netmask 255.255.255.128 gw 20.10.100.2')        
    rA.cmd('sudo route add -net 20.10.172.192 netmask 255.255.255.224 gw 20.10.100.6')        
    rB.cmd('sudo route add -net 20.10.172.128 netmask 255.255.255.192 gw 20.10.100.1')        
    rB.cmd('sudo route add -net 20.10.172.192 netmask 255.255.255.224 gw 20.10.100.10')        
    rC.cmd('sudo route add -net 20.10.172.0 netmask 255.255.255.128 gw 20.10.100.9')        
    rC.cmd('sudo route add -net 20.10.172.128 netmask 255.255.255.192 gw 20.10.100.5')        

    # Start the CLI
    CLI(net)

    # Terminate the network when the CLI is exited
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
