import json
import socket
import select
from bidict import bidict

from management_game import Player, ManagementGame, PlayerTurnData
from constants import *
from utils import fmt_dollars as d, fmt_bold as b

HOST = 'localhost'
PORT = 12345

def broadcast_message(sender_socket, message, clients):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                # Handle client disconnection
                pass

peer_to_id: bidict = bidict({})

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server listening on {HOST}:{PORT}")

    sockets_list = [server_socket]
    clients = {}

    mangame = ManagementGame()

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                sockets_list.append(client_socket)
                clients[client_socket] = client_address
                print(f"New connection from {client_address}")
            else:
                try:
                    message = notified_socket.recv(1024)
                    if not message:
                        print(f"Client {clients[notified_socket]} disconnected")
                        sockets_list.remove(notified_socket)
                        del clients[notified_socket]
                        continue

                    msg = json.loads(message)
                    
                    if "type" not in msg:
                        continue
                    
                    if msg["type"] == "register_player":
                        print(f"{msg["name"]} ready.")
                        # new_id = len(mangame.players) + 1
                        mangame.players.append( Player(msg["name"], notified_socket.fileno()) )
                        # peer_to_id[notified_socket]

                        # if len(mangame.players) >= 2:

                    if msg["type"] == "register_turn":
                        mangame.register_player_turn(notified_socket.fileno(), msg["turn"])


                    # broadcast_message(notified_socket, message, clients)
                except:
                    continue

        # for notified_socket in exception_sockets:
        #     sockets_list.remove(notified_socket)
        #     del clients[notified_socket]