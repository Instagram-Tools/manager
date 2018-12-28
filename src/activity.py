import datetime
import json
from time import sleep

import subprocess
from AWSProxy import AWSProxy

class Activity:
    def __init__(self, db, models, logger):
        """

        :type db: flask_sqlalchemy.SQLAlchemy
        :type models: models
        """
        self.logger = logger
        self.db = db
        self.models = models
        self.aws = AWSProxy(logger)

    def is_running(self, username):
        ip = self.aws.get_ip(user=username)

        if not ip:
            return False

        out, err, errcode = self.run_cmd("./is_running.sh %s %s" % (ip, username))
        self.logger.warning("is_running(%s); err: %s; errcode: %s; out: %s" % (username, err, errcode, out))
        s = out.decode('utf_8')
        self.logger.info("is_running(%s); s: %s" % (username, s))
        l = s.split("\\n")
        self.logger.info("is_running(%s) l: %s" % (username, l))

        for e in l:
            if username in str(e):
                return True
        return False

    def start(self, account):
        ac = self.models.Account.query.filter_by(username=account).first()
        if ac:
            ac.started = True
            self.db.session.commit()

            self.logger.info("start with Settings: " + str(account.settings))
            self.start_account(account=account)
            return "success", 200

        return "Account not found: %s" % account, 404

    def start_bot(self, timetable):
        account = self.models.Account.query.filter_by(id=timetable.account_id).first()
        self.db.session.commit()
        if not self.is_running(username=account.username):
            print("Start Bot: %s" % account.username)
            return self.start_account(account=account)

    def start_account(self, account):
        if account.paid and account.started:

            ip = self.aws.start(user=account.username)
            self.logger.warning("start_bot for %s at ip: %s" % (account.username, ip))

            sleep(120)

            settings_split_json = json.dumps(str(account.settings).split(" "))
            print("Settings: %s" % settings_split_json)
            return subprocess.Popen(["./start_bot.sh"] +
                                    [ip, settings_split_json, account.username, account.password])
        else:
            return "not started Account: %s; paid: %s ; started: %s" % (account, account.paid, account.started)

    def stop(self, account):
        ac = self.models.Account.query.filter_by(username=account).first()
        if ac:
            ac.started = False
            self.db.session.commit()

            self.aws.stop(account)
            return "success", 200

        return "Account not found: %s" % account, 404

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
