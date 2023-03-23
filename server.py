import os
import socket
from _thread import *
import pickle

from lib.display import ServerDisplay

from lib.players import players_for_online


display = ServerDisplay()


hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
server = "192.168.1.35"
port = int(os.environ.get("PORT", 5555))
print(f"{server}:{port}")

BYTES = 4096 ** 2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    print("Error")

s.listen(2)
print("Waiting for a connection, Server Started")
players = players_for_online


def threaded_client(conn, player):
    global currentPlayer
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(BYTES))
            # print(data)
            players[player] = data
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                # print("Received: ", data)
                # print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break
    currentPlayer -= 1
    print("players:", currentPlayer)
    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    print("new player!")
    print(currentPlayer)
