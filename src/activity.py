import datetime

from subprocess import Popen


class Activity:
    def __init__(self, db, models):
        """

        :type db: flask_sqlalchemy.SQLAlchemy
        :type models: models
        """
        self.db = db
        self.models = models

    def is_running(self, account):
        return 404

    def start(self, account):
        return 404

    def stop(self, account):
        return 404
