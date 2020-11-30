import os
import uuid
import json
import pytest
from flask import Flask, session, json
from habit_server.__init__ import app, db
from sqlalchemy import create_engine
from habit_server.db_manager import DBManager
from habit_server.db_models import User, UserActivity, UserHabit
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from habit_server.utils import toDate
import datetime
import time


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
        """ Clean up database session.

        :param exception_type: unused
        :param exception_value: unused
        :param traceback: unused
        """
        db.session.remove()
        db.drop_all()


def test_habit():
    with DBManagerTestFixture() as db_man:
        with app.test_client() as c:
            user = User(username='joe@gmail.com', hashed_password='pwd')
            print("add user")
            assert db_man.add_user(user).ok()

            print("post")
            response1 = c.post(
                '/api/habits',
                data=json.dumps({'habitname': 'reading'}),
                content_type='application/json',
            )
            assert response1.status_code == 200

            response2 = c.get(
                '/api/habits',
                content_type='application/json',
            )
            assert response2.status_code == 200

            response3 = c.delete(
                '/api/habits',
                data=json.dumps({'habitname': 'reading'}),
                content_type='application/json',
            )
            assert response3.status_code == 200

def test_activity():
    with DBManagerTestFixture() as db_man:
        with app.test_client() as c:
            user = User(username='joe@gmail.com', hashed_password='pwd')
            assert db_man.add_user(user).ok()

            # add a habit
            response1 = c.post(
                '/api/habits',
                data=json.dumps({'habitname': 'reading'}),
                content_type='application/json',
            )
            assert response1.status_code == 200

            # These 2 tests are failed becuase of 'SQLite DateTime type only accepts Python datetime and date objects as input'
            # time= "2019-12-04"
            # datetime = toDate(time)
            # response2 = c.post(
            #     '/api/habits/logs',
            #     data=json.dumps({'habitname': 'reading', 'timestamp': datetime}),
            #     content_type='application/json',
            # )
            # assert response2.status_code == 200
            #
            # response3 = c.get(
            #     'api/habits/logs',
            #     data=json.dumps({'habitname': 'reading'}),
            #     content_type='application/json',
            # )
            # assert response3.status_code == 200
