import threading
import datetime
import requests

from time_util import sleep, time_in_week

from activity import Activity
import logging

class Manager:
    def __init__(self, db, models):
        """

        :type db: flask_sqlalchemy.SQLAlchemy
        :type models: models
        """
        self.db = db
        self.models = models
        self.activity = Activity(db=db, models=models, logger=logging)

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        print("### run")

        try:
            self.clear_running()
        except Exception as exc:
            print("Exception during clear_running():")
            print(exc)

        while sleep(60):
            now = time_in_week(datetime.datetime.now())
            print(str(now))
            tts = self.models.TimeTable.query.filter(
                self.models.TimeTable.start <= now,
                self.models.TimeTable.end > now,
                # self.models.TimeTable.end < self.models.TimeTable.start,
            ).all()
            print(str(tts))
            self.loop(tts)

    def loop(self, tts):
        for tt in tts:
            try:
                print("account_id: %s" % tt.account_id)
                print(self.activity.start_bot(tt))
            except Exception as exc:
                print("Exception during loop():")
                print(exc)
                self.db.session.rollback()
                print("Session.rollback() Done")

    def clear_running(self):
        delete = self.db.session.query(self.models.Running).delete()
        self.db.session.commit()
        print("### clear Entries: %r" % str(delete))