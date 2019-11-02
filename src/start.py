import models as appmod
from manager import Manager
from settings import db
import sys

manager = Manager(db, appmod)

try:
    manager.clear_running()
except Exception as exc:
    print("Exception during clear_running():")
    print(exc)

manager.loop()

sys.exit()
