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
        out, err, errcode = run_cmd("./is_running.sh %s" % account)
        out = str(out).split("\\n")
        out = out[0][2:] + out[1:-2]
        return account in out

    def start(self, account):
        ac = self.models.Account.query.filter_by(username=account).first()
        if ac:
            ac.started = True
            self.db.session.commit()

            print("start with Settings: " + str(account.settings))
            Popen(["./start_bot.sh"] +
                  [ac.settings, ac.username, ac.password, self.get_proxy(ac.username)])
            return 200

        return "Account not found: %s" % account, 404

    def stop(self, account):
        ac = self.models.Account.query.filter_by(username=account).first()
        if ac:
            ac.started = False
            self.db.session.commit()

            run_cmd("./stop_bot_sh %s" % account)
            return 200

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
