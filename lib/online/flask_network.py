import pickle

from requests import get, post


class FlaskNetwork:
    def __init__(self, serv):
        self.server_adress = f"http://{serv}/game"
        self.player_num = self.connect()
        print("player:", self.player_num)
        self.p = pickle.loads(get(f'{self.server_adress}/get/{self.player_num}').content)
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
        res = pickle.loads(post(f'{self.server_adress}/{self.player_num}', pickle.dumps(data)).content)
        return res

    def leave(self):
        get(f"{self.server_adress}/leave")
