import datetime

import subprocess


class Activity:
    def __init__(self, db, models, logger=print):
        """

        :type db: flask_sqlalchemy.SQLAlchemy
        :type models: models
        """
        self.logger = logger
        self.db = db
        self.models = models

    def is_running(self, account):
        out, err, errcode = self.run_cmd("./is_running.sh %s" % account)
        self.logger("is_running(%s); err: %s; errcode: %s; out: %s" % (account, err, errcode, out))
        s = out.decode('utf_8')
        self.logger("is_running(%s); s: %s" % (account, s))
        l = s.split("\\n")
        self.logger("is_running(%s) l: %s" % (account, l))

        for e in l:
            if account in str(e):
                return str(True), 200
        return str(False), 200

    def start(self, account):
        ac = self.models.Account.query.filter_by(username=account).first()
        if ac:
            ac.started = True
            self.db.session.commit()

            self.logger("start with Settings: " + str(account.settings))
            subprocess.Popen(["./start_bot.sh"] +
                  [ac.settings, ac.username, ac.password, self.get_proxy(ac.username)])
            return "success", 200

        return "Account not found: %s" % account, 404

    def stop(self, account):
        ac = self.models.Account.query.filter_by(username=account).first()
        if ac:
            ac.started = False
            self.db.session.commit()

            self.run_cmd("./stop_bot_sh %s" % account)
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
