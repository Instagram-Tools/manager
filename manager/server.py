from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
import json
import datetime
from manager import Manager

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

from models import *


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


def update_timetable(user, data):
    timetable = data.get("timetable", [])
    for i in range(0, len(timetable), 2):
        timetable = TimeTable(user_id=user.id, start=parse_datetime(timetable[i]),
                              end=parse_datetime(timetable[i + 1]))
        db.session.add(timetable)
    db.session.commit()


def parse_datetime(line):
    p = parse_datetime_prefix(str(line), '%Y-%m-%d %H:%M:%S')
    return datetime.datetime(1, 1, day=p.isoweekday(), hour=p.hour, minute=p.minute, second=p.second)


def parse_datetime_prefix(line, fmt):
    try:
        t = datetime.datetime.strptime(line, fmt)
    except ValueError as v:
        if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
            line = line[:-(len(v.args[0]) - 26)]
            t = datetime.datetime.strptime(line, fmt)
        else:
            raise
    return t


if __name__ == '__main__':
    Manager().start()
    app.run(host='0.0.0.0')
