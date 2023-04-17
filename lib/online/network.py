import datetime
import socket
import pickle
import sys

# BYTES = 6144 ** 2
BYTES = 4096


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # hostname = socket.gethostname()
        # IPAddr = socket.gethostbyname(hostname)
        self.server = "188.120.248.249"
        self.port = 10000
        self.addr = (self.server, self.port)

        self.temp_data = [None, False, False, None, None, None, ""]
        self.temp_timer = 300
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
            return None

    def send(self, data):
        try:
            d = pickle.dumps(data)
            if int(sys.getsizeof(d)) > 2000:
                print(sys.getsizeof(pickle.dumps(data)))
            self.client.send(d)
            res = self.client.recv(BYTES)
            res = pickle.loads(res)
            self.temp_data = res
            self.temp_timer = 300
            return res
        except socket.error as e:
            print(datetime.datetime.now(), e)
        except UnicodeDecodeError as e:
            self.temp_timer -= 1
            return self.temp_data
        except pickle.UnpicklingError as e:
            if self.temp_timer > 0:
                self.temp_timer -= 1
                return self.temp_data
        except ValueError as e:
            if self.temp_timer > 0:
                self.temp_timer -= 1
                return self.temp_data
        except Exception as e:
            if self.temp_timer > 0:
                self.temp_timer -= 1
                return self.temp_data
            else:
                print(datetime.datetime.now(), e)
                return [None, False, True, None, None, None, ""]

    def leave(self):
        pass
