import models
from time import sleep

time = 10
print("sleep: " + str(time))
sleep(time)

try:
    for m in models.list():
        print(str(m))
        print(str(m.query.filter_by(id=1).first()))
except:
    print("DB ERROR")
    print("initDB now!")
    import create_db

    create_db
    print("initDB DONE")