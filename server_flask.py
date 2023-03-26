import datetime
import os

from lib.display import ServerDisplay
from lib.online.data import players_api

display = ServerDisplay()


import flask

from flask_restful import Api

app = flask.Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)


def main():
    app.register_blueprint(players_api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    print(port)
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
