from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

class LinuxRouter(Node):
    def config(self, **params):
        super().config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super().terminate()

class SingleLANWithRouter(Topo):
    def build(self):
        switch = self.addSwitch('s1')

        # Add router without IP; assign manually after start
        rA = self.addNode('rA', cls=LinuxRouter)

        # Hosts with IPs in the /26 subnet and rA as gateway
        hA1 = self.addHost('hA1', ip='20.10.172.130/26', defaultRoute='via 20.10.172.129')
        hA2 = self.addHost('hA2', ip='20.10.172.131/26', defaultRoute='via 20.10.172.129')

        # Connect everything to the switch
        self.addLink(hA1, switch)
        self.addLink(hA2, switch)
        self.addLink(rA, switch)

def run():
    topo = SingleLANWithRouter()
    net = Mininet(topo=topo, switch=OVSSwitch, controller=None)
    net.start()

    rA = net.get('rA')
    # Assign IP manually to router's interface
    rA.setIP('20.10.172.129/26', intf=rA.intfNames()[0])

    print("\n✅ LAN A is up. Try:")
    print("  hA1 ping hA2")
    print("  hA1 ping rA")
    print("  hA2 ping rA")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
