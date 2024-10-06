import os
import socket
from _thread import *
import pickle
import datetime

import sys

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

server = "82.146.60.52"

port = int(os.environ.get("PORT", 10000))
print(f"{datetime.datetime.now()}, server {server}:{port}")

BYTES = 4096


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    s.bind((server, port))
except socket.error as e:
    print(datetime.datetime.now(), str(e))
    print(datetime.datetime.now(), "Error")

s.listen(2)
print(datetime.datetime.now(), "Waiting for a connection, Server Started")
players = [pickle.dumps([None, False, False, None, None, None, ""]),
           pickle.dumps([None, False, False, None, None, None, ""])]


def threaded_client(conn, player):
    global currentPlayer, players
    conn.send(pickle.dumps(currentPlayer))
    reply = ""
    while True:
        try:
            data = conn.recv(BYTES)
            players[player] = data
            if not data:
                print(datetime.datetime.now(), "Disconnected: player", player)
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
            size = sys.getsizeof(reply)
            if int(size) > 2000:
                print(size)
            conn.sendall(reply)
        except ConnectionResetError:
            print(datetime.datetime.now(), "==> ConnectionResetError")
            pass
        except socket.timeout:
            print(datetime.datetime.now(), "==> Timeout")
            continue
        except Exception as e:
            print(datetime.datetime.now(), e)
            break
    currentPlayer -= 1
    players = [pickle.dumps([None, False, False, None, None, None, ""]),
               pickle.dumps([None, False, False, None, None, None, ""])]
    print(datetime.datetime.now(), "players:", currentPlayer)
    print(datetime.datetime.now(), "Lost connection")
    conn.close()


currentPlayer = 0
while True:

    conn, addr = s.accept()
    print(datetime.datetime.now(), "Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    print(datetime.datetime.now(), "new player!", currentPlayer)
