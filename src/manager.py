import threading
import datetime
import requests

from time_util import time_in_week
from time import sleep

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
        while True:
            self.loop()

    def loop(self):
        now = time_in_week(datetime.datetime.now())
        tts = self.models.TimeTable.query.filter(
            self.models.TimeTable.start <= now,
            self.models.TimeTable.end > now,
            # self.models.TimeTable.end < self.models.TimeTable.start,
        ).all()
        for tt in tts:
            try:
                self.activity.start_bot(tt)
            except Exception as exc:
                print("Exception during loop():")
                print(exc)
                self.db.session.rollback()
                print("Session.rollback() Done")
        sleep(60)

    def clear_running(self):
        delete = self.db.session.query(self.models.Running).delete(synchronize_session='fetch')
        self.db.session.commit()
        print("### clear Entries: %r" % str(delete))
