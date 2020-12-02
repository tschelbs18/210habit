"""habit_server package root."""
import os
import uuid
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SECRET_KEY'] = uuid.uuid4().hex
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
