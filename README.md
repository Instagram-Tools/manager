# Manager 

## run via docker-compose
    docker-compose up
    
## init DataBase
    docker-compose run manager /usr/local/bin/python create_db.py

## reset venv

    rm -rf ./venv
    python -m venv --clear ./venv
    source venv/bin/activate

## install from requirements.txt
    pip install -r requirements.txt

## update requirements.txt
    pip freeze > requirements.txt
