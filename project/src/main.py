from peer import Peer
from utils.logger import get_logger
import argparse

logger = get_logger("P2P-Main")

def parse_arguments():
    parser = argparse.ArgumentParser(description="P2P File Sharing Peer")
    parser.add_argument('--ip', '-i', type=str, default='127.0.0.1', help="IP address of the peer (default: 127.0.0.1)")
    parser.add_argument('--discovery-port', '-d', type=int, default=5000, help="Port for DHT discovery service (default: 8468)")
    parser.add_argument('--transfer-port', '-t', type=int, default=5001, help="Port for file transfer service (default: 8500)")
    return parser.parse_args()

def main():
    args = parse_arguments()


    peer = Peer(host=args.ip, discovery_port=args.discovery_port, transfer_port=args.transfer_port)
    peer.start()

if __name__ == "__main__":
    logger.info("Starting P2P File Sharing Application...")
    main()
