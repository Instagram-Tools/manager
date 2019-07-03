import json
from flask import request

import models as appmod
from activity import Activity
from settings import db, app

activity = Activity(db=db, models=appmod, logger=app.logger)


@app.route('/bot/running/<account>', methods=['GET'])
def is_running(account):
    app.logger.info("GET /bot/%s" % account)
    try:
        if account:
            return str(activity.is_running(account)), 200
        else:
            app.logger.error("GET /bot/%s return: 501" % account)
            return "Not found: %s" % account, 501  # Not Implemented
    except Exception as exc:
        app.logger.error("GET /bot/%s Exception: %s" % (account, exc))
        return str(exc), 500


@app.route('/bot/stop/<account>', methods=['GET'])
def stop(account):
    app.logger.warning("GET /bot/stop/%s" % account)
    try:
        return activity.stop(account)
    except Exception as exc:
        app.logger.error("GET /bot/%s Exception: %s" % (account, exc))
        return str(exc), 500


@app.route('/bot/start/<account>', methods=['GET'])
def start(account):
    app.logger.warning("GET /bot/start/%s" % account)
    try:
        return activity.start(account)
    except Exception as exc:
        app.logger.error("GET /bot/%s Exception: %s" % (account, exc))
        return str(exc), 500


@app.route('/bot/login/', methods=['POST'])
def try_login():
    data = json.loads(request.data)
    app.logger.warning("POST /bot/login: %s" % data)
    try:
        return activity.start_try_login(username=data.get("username", "").lower(),
                                        password=data.get('password'),
                                        email=data.get('email'),
                                        sec_code=data.get('sec_code'))
    except Exception as exc:
        app.logger.error("POST /bot/login Exception: %s" % (exc))
        return str(exc), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765)
