from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
import json

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

from models import *


@app.route('/', methods=['POST'])
def index():
    d = json.loads(request.data)
    user = User(username=d.get("username"), password=d.get("password"),
                settings=d.get("settings"), timetable=d.get("timetable"))
    db.session.add(user)
    db.session.commit()

    return str(User.query.all())

if __name__ == '__main__':
    app.run(host='0.0.0.0')
