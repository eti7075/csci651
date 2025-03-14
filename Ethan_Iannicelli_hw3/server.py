from rdt_protocol import ReliableDataTransferEntity, parse_packet
import rdt_protocol

# Constants
RECEIVER_ADDRESS = ('127.0.0.1', rdt_protocol.RECEIVER_PORT)
INTER_ADDRESS = ('127.0.0.1', rdt_protocol.INTER_PORT)
BUFFER_SIZE = 1024  
SAVE_FOLDER = 'received_files/'  

class FileTransferServer:
    def __init__(self):
        self.receiver = ReliableDataTransferEntity(INTER_ADDRESS, RECEIVER_ADDRESS, timeout=False)
    
    def receive_file(self):
        """
        receiver function for a file transfer destination/server saves data to a file destination (constant)

        :param self: the server object
        :type self: FileTransferServer
        """
        filename_packet = self.receiver.receive()
        _, _, _, filename = parse_packet(filename_packet)

        with open(SAVE_FOLDER + filename.decode(), 'wb') as file:
            pass
        
        with open(SAVE_FOLDER + filename.decode(), 'ab') as file:
            seq_num = 0
            while True:
                packet = self.receiver.receive()

                _, _, _, data = parse_packet(packet)
                
                file.write(data)
                seq_num += 1
                if not data:
                    break

            print(f"File saved to {SAVE_FOLDER + filename.decode()}")


if __name__ == "__main__":
    server = FileTransferServer()
    while True:
        print("Waiting for file (ctrl-C to quit)...")
        server.receive_file()
