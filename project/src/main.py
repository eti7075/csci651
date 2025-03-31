from peer import Peer
from utils.logger import get_logger
import argparse
from utils.config import CONFIG

logger = get_logger("P2P-Main")

def parse_arguments():
    parser = argparse.ArgumentParser(description="P2P File Sharing Peer")
    parser.add_argument('--discovery-port', '-d', type=int, default=CONFIG["PEER_DISCOVERY_PORT"], help="Port for listening/broadcasting for peer discovery (default: 5000)")
    parser.add_argument('--sender-port', '-s', type=int, default=CONFIG["FILE_SENDER_PORT"], help="Sender port for file transfer service (default: 5001)")
    parser.add_argument('--receiver-port', '-r', type=int, default=CONFIG["FILE_RECEIVER_PORT"], help="Receiver port for file transfer service (default: 5001)")
    return parser.parse_args()

def main():
    args = parse_arguments()

    peer = Peer(
        discovery_port=args.discovery_port,
        sender_port=args.sender_port,
        receiver_port=args.receiver_port

    )
    peer.start()

if __name__ == "__main__":
    logger.info("Starting P2P File Sharing Application...")
    main()
