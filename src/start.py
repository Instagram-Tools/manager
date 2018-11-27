import models as appmod
from manager import Manager
from settings import db

Manager(db, appmod).run()
