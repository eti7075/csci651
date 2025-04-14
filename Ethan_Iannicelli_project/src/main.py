from peer import Peer
from utils.logger import get_logger
import argparse
from utils.config import CONFIG

logger = get_logger("P2P-Main")

def parse_arguments():
    """
    create and return argument parser. the parser handles the broadcasting port and the default transfer port.
    the transfer port requires it, +1, +2, +3 ports to be unused before running the program.
    """
    parser = argparse.ArgumentParser(description="P2P File Sharing Peer")
    parser.add_argument('--discovery-port', '-d', type=int, default=CONFIG["PEER_DISCOVERY_PORT"], help="Port for listening/broadcasting for peer discovery (default: 5000)")
    parser.add_argument('--transfer-port', '-t', type=int, default=CONFIG["FILE_TRANSFER_PORT"], help="Transfer port for file transfer service (default: 5001, 5002, 5003, 5004)")
    return parser.parse_args()

def main():
    """
    main function for P2P program, starts Peer and accepts arguments.
    """
    args = parse_arguments()

    peer = Peer(
        discovery_port=args.discovery_port,
        transfer_port=args.transfer_port,
    )
    peer.start()

if __name__ == "__main__":
    logger.info("Starting P2P File Sharing Application...")
    main()
