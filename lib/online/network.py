import socket
import pickle


BYTES = 4096 ** 2


class Network:
    def __init__(self, serv):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        serv = serv.split(':')
        self.server = serv[0]
        self.port = int(serv[1])
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getIP(self):
        return self.server

    def getP(self):
        return self.p

    def connect(self):
        try:
            print(f"Connecting to: {self.addr[0]}:{self.addr[1]}")
            self.client.connect(self.addr)
            print(f"Connected to: {self.addr[0]}:{self.addr[1]}")
            return pickle.loads(self.client.recv(BYTES))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(BYTES))
        except socket.error as e:
            print(e)
