"""habit_server package root."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SECRET_KEY'] = u'210habit'

# login
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "test"
login_manager.login_message = u"you must login to access this page"
login_manager.login_message_category = "message"

# config for db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../habit_tracker.db'
db = SQLAlchemy(app)