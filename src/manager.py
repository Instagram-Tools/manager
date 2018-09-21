import threading
import datetime
from time_util import sleep, time_in_week
from subprocess import Popen


class Manager:
    def __init__(self, db, models):
        """

        :type db: flask_sqlalchemy.SQLAlchemy
        :type models: models
        """
        self.db = db
        self.models = models

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        print("### run")

        try:
            self.clear_running()
        except Exception as exc:
            print(exc)

        while sleep(60):
            try:
                self.loop()
            except Exception as exc:
                print(exc)

    def loop(self):
        now = time_in_week(datetime.datetime.now())
        print(str(now))
        tts = self.models.TimeTable.query.filter(
            self.models.TimeTable.start <= now,
            self.models.TimeTable.end > now,
            # self.models.TimeTable.end < self.models.TimeTable.start,
        ).all()
        print(str(tts))
        for tt in tts:
            print("user_id: " + str(tt.user_id))

            first = self.models.Running.query.filter_by(user_id=tt.user_id).first()
            if first:
                if first.end < datetime.datetime.now():
                    self.db.session.delete(first)
                continue

            self.add_running(tt)

    def add_running(self, timetable):
        print("adding")
        timedelta = datetime.timedelta(days=timetable.end.day - timetable.start.day,
                                       hours=timetable.end.hour - timetable.start.hour,
                                       minutes=timetable.end.minute - timetable.start.minute,
                                       seconds=timetable.end.second - timetable.start.second)
        running = self.models.Running(user_id=timetable.user_id, start=datetime.datetime.now(),
                                      end=(datetime.datetime.now() + abs(timedelta)))
        self.db.session.add(running)
        print(str("add: " + str(running)))
        self.db.session.commit()

        self.start_bot(timetable)

    def start_bot(self, timetable):
        user = self.models.User.query.filter_by(id=timetable.user_id).first()
        self.db.session.commit()
        return Popen(["./start_bot.sh"] +
                     [user.username, user.password, user.settings])

    def clear_running(self):
        delete = self.db.session.query(self.models.Running).delete()
        self.db.session.commit()
        print("### clear Entries: %r" % str(delete))