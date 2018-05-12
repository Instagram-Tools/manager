from manager import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    settings = db.Column(db.Text(), nullable=False)
    timetable = db.relationship('TimeTable', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username


class TimeTable(db.Model):
    __tablename__ = 'timetable'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start = db.Column(db.DateTime(), nullable=False)
    end = db.Column(db.DateTime(), nullable=False)
