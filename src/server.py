from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
import json
from manager import Manager
from time_util import parse_datetime

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

import models


@app.route('/', methods=['POST'])
def index():
    try:
        data = json.loads(request.data)
        user = update_user(data)
        update_timetable(user, data)

        return "updated %r" % user
    except Exception as exc:
        return str(exc)


def update_user(data):
    user = models.User(username=data.get("username"), password=data.get("password"),
                       settings=data.get("settings"))
    first = models.User.query.filter_by(username=user.username).first()
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


def update_timetable(user, data):
    timetable = data.get("timetable", [])
    for i in range(0, len(timetable), 2):
        timetable = models.TimeTable(user_id=user.id, start=parse_datetime(timetable[i]),
                                     end=parse_datetime(timetable[i + 1]))
        db.session.add(timetable)
    db.session.commit()


@app.before_first_request
def initDB():
    import sqlalchemy
    try:
        for m in models.list():
            print(str(m))
            print(str(m.query.filter_by(id=1).first()))
    except sqlalchemy.exc.ProgrammingError:
        print("sqlalchemy.exc.ProgrammingError")
        print("initDB now!")
        import create_db
        create_db
        print("initDB DONE")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765)
