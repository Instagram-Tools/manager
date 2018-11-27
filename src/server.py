from flask import request

import models as appmod
from activity import Activity
from settings import db, app

activity = Activity(db=db, models=appmod, logger=app.logger.warning)


@app.route('/bot/<account>', methods=['GET'])
def is_running(account):
    app.logger.warning("GET /bot/%s" % account)
    try:
        return activity.is_running(account)
    except Exception as exc:
        return str(exc), 500


@app.route('/bot/stop/<account>', methods=['GET'])
def stop(account):
    app.logger.warning("GET /bot/stop/%s" % account)
    try:
        return activity.stop(account)
    except Exception as exc:
        return str(exc), 500


@app.route('/bot/start/<account>', methods=['GET'])
def start(account):
    app.logger.warning("GET /bot/start/%s" % account)
    try:
        return activity.start(account)
    except Exception as exc:
        return str(exc), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765)
