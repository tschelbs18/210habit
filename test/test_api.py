import os
import uuid
import pytest
from flask import Flask, session, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from src.db_models import User, UserActivity, UserHabit
from DBManagerTestFixture import DBManagerTestFixture

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SECRET_KEY'] = uuid.uuid4().hex
db = SQLAlchemy(app)

def test_user():
    with DBManagerTestFixture() as db_man:
        with app.test_client() as c:
            # register a new user
            response1 = c.post(
                '/users',
                data=json.dumps({'username': 'jane@gmail.com','password':'pwd'}),
                content_type='application/json',
                )
            assert response1.status_code == 200
            # add duplicate user
            response2 = c.post(
                '/users',
                data=json.dumps({'username': 'jane@gmail.com','password':'pwd'}),
                content_type='application/json',
                )
            assert response2.status_code == 404

            #login successful
            response3 = c.post(
                '/login',
                data=json.dumps({'username': 'jane@gmail.com','password':'pwd'}),
                content_type='application/json',
                )
            assert response3.status_code == 200

            # login with wrong pwd
            response4 = c.post(
                '/login',
                data=json.dumps({'username': 'jane@gmail.com','password':'wrongpwd'}),
                content_type='application/json',
                )
            assert response4.status_code == 404


def test_habit():
    with DBManagerTestFixture() as db_man:
        with app.test_client() as c:
            # register a new user
            response_user = c.post(
                '/users',
                data=json.dumps({'username': 'jane@gmail.com','password':'pwd'}),
                content_type='application/json',
                )
            assert response_user.status_code == 200
            # login
            response_login = c.post(
                '/login',
                data=json.dumps({'username': 'jane@gmail.com','password':'pwd'}),
                content_type='application/json',
                )
            assert response_login.status_code == 200
            # add a  habit
            response1 = c.post(
                '/api/habits',
                data=json.dumps({'habitname': 'reading'}),
                content_type='application/json',
            )
            assert response1.status_code == 200
            # get all habits
            response2 = c.get(
                '/api/habits',
                content_type='application/json',
            )
            assert response2.status_code == 200
            # delete a habit
            response3 = c.delete(
                '/api/habits',
                data=json.dumps({'habitname': 'reading'}),
                content_type='application/json',
            )
            assert response3.status_code == 200

def test_activity():
    with DBManagerTestFixture() as db_man:
        with app.test_client() as c:
            # register
            response_user = c.post(
                '/users',
                data=json.dumps({'username': 'jane@gmail.com','password':'pwd'}),
                content_type='application/json',
                )
            assert response_user.status_code == 200
            # login
            response_login = c.post(
                '/login',
                data=json.dumps({'username': 'jane@gmail.com','password':'pwd'}),
                content_type='application/json',
                )
            assert response_login.status_code == 200

            # add a habit
            response1 = c.post(
                '/api/habits',
                data=json.dumps({'habitname': 'reading'}),
                content_type='application/json',
            )
            assert response1.status_code == 200
            # add a activity
            response2 = c.post(
                '/api/habits/logs',
                data=json.dumps({'habitname': 'reading', 'timestamp': '2020-11-30'}),
                content_type='application/json',
            )
            assert response2.status_code == 200
            # get activity given a date
            response3 = c.get(
                'api/habits/logs',
                data=json.dumps({'habitname': 'reading', 'trailing_days':5}),
                content_type='application/json',
            )
            assert response3.status_code == 200
            # get all activity
            response4 = c.get(
                'api/habits/logs',
                data=json.dumps({'habitname': 'reading'}),
                content_type='application/json',
            )
            assert response3.status_code == 200
