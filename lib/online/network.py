import socket
import pickle


BYTES = 4096 ** 2


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        self.server = str(IPAddr)
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getIP(self):
        return self.server

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(BYTES))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(BYTES))
        except socket.error as e:
            print(e)
