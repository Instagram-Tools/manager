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
        out, err, errcode = run_cmd("./is_running.sh")
        return out

    def start(self, account):
        return 404

    def stop(self, account):
        return 404

    def run_cmd(self, cmd):
        """
        :type cmd: str
        :return (str, str, int)
        """
        process = subprocess.Popen(cmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()
        errcode = process.returncode

        return out, err, errcode
