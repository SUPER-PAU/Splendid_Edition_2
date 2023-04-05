import socket
import pickle


BYTES = 4096 ** 2


class Network:
    def __init__(self, serv):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        self.server = serv
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getIP(self):
        if self.server:
            return f"{self.server}:{self.port}"
        return str(self.addr)

    def getP(self):
        return self.p

    def connect(self):
        try:
            print(f"Connecting to: {self.addr}")
            self.client.connect(self.addr)
            print(f"Connected to: {self.addr}")
            return pickle.loads(self.client.recv(BYTES))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(BYTES))
        except socket.error as e:
            print(e)

    def leave(self):
        pass
