import datetime
import json
import subprocess
import threading
import os
from time import sleep

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

        out, err, errcode = self.run_cmd("./is_running.sh %s %s" % ip)
        self.logger.warning("is_running(%s); err: %s; errcode: %s; out: %s" % (username, err, errcode, out))
        s = out.decode('utf_8')
        self.logger.info("is_running(%s); s: %s" % (username, s))
        l = s.split("\\n")
        self.logger.info("is_running(%s) l: %s" % (username, l))

        for e in l:
            if "bot" in str(e):
                return True
        return False

    def start(self, username):
        account = self.models.Account.query.filter_by(username=username).first()
        if not account:
            return "Account not found: %s" % username, 404
        user = self.models.User.query.filter_by(id=account.user_id).first()
        if not user:
            return "User not found for Account: %s" % username, 404

        email = user.email
        account.started = True
        self.db.session.commit()

        self.logger.info("start with Settings: " + str(username.settings))
        self.start_account(account=username, email=email)
        return "success", 200

    def start_bot(self, timetable):
        account = self.models.Account.query.filter_by(id=timetable.account_id).first()
        if not account:
            return "Account not found for timetable: %s" % timetable, 404

        user = self.models.User.query.filter_by(id=account.user_id).first()
        if not user:
            return "User not found for Account: %s" % account, 404
        email = user.email

        self.db.session.commit()
        if not (account.paid and account.started):
            return "not started Account: %s; paid: %s ; started: %s ; email: %s" % (
                account, account.paid, account.started, email)

        if not self.is_running(username=account.username):
            print("Start new Thread for Bot: %s" % account.username)
            thread = threading.Thread(target=self.start_account, args=(account, email))
            return thread.start()

    def start_account(self, account, email):
            ip = self.aws.start(user=account.username)
            self.logger.warning("start_bot for %s at ip: %s" % (account.username, ip))

            sleep(120)

            settings_split_json = json.dumps(str(account.settings).split(" "))
            email_server = "http://%s:%s" % (os.environ["MANAGER_IP"], os.environ["MAIL_PORT"])
            p = subprocess.Popen(["./start_bot.sh"] +
                                    [ip, settings_split_json, account.username, account.password, email, email_server])
            sleep(120)

            self.logger.warning("Kill start_bot.sh of %s at ip: %s" % (account.username, ip))
            p.kill()

    def start_try_login(self, username, password, email, sec_code):
            ip = self.aws.start(user=username)
            self.logger.warning("start_try_login for %s at ip: %s" % (username, ip))

            sleep(120)

            email_server = "http://%s:%s" % (os.environ["MANAGER_IP"], os.environ["MAIL_PORT"])
            p = subprocess.Popen(["./login_bot.sh"] +
                                    [ip, username, password, email, email_server, sec_code])
            sleep(120)

            self.logger.warning("Kill login_bot.sh of %s at ip: %s" % (username, ip))
            p.kill()

            return "success start_try_login for %s at ip: %s"

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
