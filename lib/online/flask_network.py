import pickle

from requests import get, post


class FlaskNetwork:
    def __init__(self, serv):
        self.server_adress = f"https://{serv}/game"
        self.p = self.connect()
        print("player:", self.p)
        print(self.p)

    def getIP(self):
        return ""

    def getP(self):
        return self.p

    def connect(self):
        try:
            response = pickle.loads(get(f'{self.server_adress}/join_game').content)
            if response == "game is full":
                pass
            else:
                return response
        except:
            pass

    def send(self, data):
        res = pickle.loads(post(f'{self.server_adress}/{self.p}', pickle.dumps(data)).content)
        return res

    def leave(self):
        get(f"{self.server_adress}/leave")
