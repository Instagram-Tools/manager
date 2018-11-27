from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
from manager import Manager

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)