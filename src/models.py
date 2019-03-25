from settings import db


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), nullable=False)
    settings = db.Column(db.Text(), nullable=False)
    timetables = db.relationship('TimeTable', backref='account', lazy=True)
    running = db.relationship('Running', backref='account', lazy=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    started = db.Column(db.Boolean, default=True)
    credit = db.Column(db.Integer, default=0)

    subscription = db.Column(db.String(10), unique=True)
    paid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Account %r>' % self.username


class TimeTable(db.Model):
    __tablename__ = 'timetable'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    start = db.Column(db.DateTime(), nullable=False)
    end = db.Column(db.DateTime(), nullable=False)

    def to_json(self):
        return {"start": str(self.start), "end": str(self.end)}

    def __repr__(self):
        return '<TimeTable %r %r:%r>' % (self.account_id, str(self.start), str(self.end))


class Running(db.Model):
    __tablename__ = 'running'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), unique=True, nullable=False)
    start = db.Column(db.DateTime(), nullable=False)
    end = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return '<Running %r %r:%r>' % (self.account_id, str(self.start), str(self.end))


def list():
    return [Account, TimeTable, Running]
