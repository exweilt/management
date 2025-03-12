import socket
import json
import pickle

players = []

def register_player(name):
    players.append(name)
    return 7

"""
    Protocol message : big endian
    4 bytes = (unsigned int) size of the following(rest) message in bytes (max. )
    1 byte = (unsigned int) number of headers
    n headers {
        4 bytes = (unsigned int) size of the following header in bytes (max. )
        n bytes = content of the header
    }

    The first header is typically type_of_message containing string

    Warning: security Risk due to pickle
"""
def encode_message(headers: list) -> bytes:
    message: bytes
    
    for idx, header in enumerate(headers):
        message_content: bytes = pickle.dumps(header)
        message += len(message_content) + message_content
    
    return len(message).to_bytes(4, "big") + message

def decode_message(message: bytes) -> list:
    message_size = int.from_bytes(message[:4], "big")
    number_of_headers = int.from_bytes(message[4], "big")

    headers: list = []

    pointer = 5 # points at the byte to read next
    for idx in range(number_of_headers):
        header_size = int.from_bytes(message[pointer:4])
        pointer += 4

        header_content = pickle.loads(message[pointer:header_size])
        pointer += header_size

        headers.append(header_content)
    
    return headers

class PeerRPC:
    def __init__(self):
        self.sock: socket

    def await_rpc_id(self, peer_id: int, procedure_name: str, *args):
        pass




if __name__ == "__main__":
    if input() == "s":
        server = PeerRPC()
        server.register_rpc("register_player", register_player)
        server.register_rpc("register_turn", register_player)

    else:
        client = PeerRPC()
        client.register_rpc()

        my_id = client.await_rpc_id(1, "register_player", "God")
