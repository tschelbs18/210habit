"""DBManagerTestFixture for the habit server."""
from src.db_manager import DBManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import uuid
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SECRET_KEY'] = uuid.uuid4().hex
db = SQLAlchemy(app)


class DBManagerTestFixture():
    """Database manager test fixture."""

    def __enter__(self):
        """Initialize test app, db manager, db session.

        :return DMManager: initialized database manager.
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()
            return DBManager(db.session)

    def __exit__(self, exception_type, exception_value, traceback):
        """Clean up database session.

        :param exception_type: unused
        :param exception_value: unused
        :param traceback: unused
        """
        db.session.remove()
        db.drop_all()
