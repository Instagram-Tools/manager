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
    try:
        data = json.loads(request.data)
        user = update_user(data)

        first = User.query.filter_by(username=user.username).first()
        if first:
            first.password = user.password
            first.settings = user.settings
            first.timetable = user.timetable
            db.session.add(first)
        else:
            db.session.add(user)

        db.session.commit()

        return str(User.query.all())
    except Exception as exc:
        return str(exc)


def update_user(data):
    user = User(username=data.get("username"), password=data.get("password"),
                settings=data.get("settings"))
    first = User.query.filter_by(username=user.username).first()
    if first:
        first.password = user.password
        first.settings = user.settings

        for t in first.timetables:
            db.session.delete(t)

        db.session.add(first)
        user = first
    db.session.add(user)
    db.session.commit()
    return user


if __name__ == '__main__':
    app.run(host='0.0.0.0')
