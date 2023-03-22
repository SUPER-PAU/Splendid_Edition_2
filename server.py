import socket
from _thread import *
import pickle

from lib.display import ServerDisplay
from lib.players import players_for_online

server_display = ServerDisplay()

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
server = str(IPAddr)
port = 5555

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
            print(0)
            data = pickle.loads(conn.recv(BYTES))
            print(data)
            players[player] = data
            print(1)
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)

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
