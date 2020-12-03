from flask import json
from test.DBManagerTestFixture import DBManagerTestFixture
from app import app


def test_user():
    with DBManagerTestFixture():
        with app.test_client() as c:
            # register a new user
            response1 = c.post(
                '/users',
                data=json.dumps(
                    {'username': 'jane@gmail.com', 'password': 'pwd'}),
                content_type='application/json',
            )
            assert response1.status_code == 200
            # add duplicate user
            response2 = c.post(
                '/users',
                data=json.dumps(
                    {'username': 'jane@gmail.com', 'password': 'pwd'}),
                content_type='application/json',
            )
            assert response2.status_code == 404

            # login successful
            response3 = c.post(
                '/login',
                data=json.dumps(
                    {'username': 'jane@gmail.com', 'password': 'pwd'}),
                content_type='application/json',
            )
            assert response3.status_code == 200

            # login with wrong pwd
            response4 = c.post(
                '/login',
                data=json.dumps(
                    {'username': 'jane@gmail.com', 'password': 'wrongpwd'}),
                content_type='application/json',
            )
            assert response4.status_code == 404


def test_habit():
    with DBManagerTestFixture():
        with app.test_client() as c:
            # register a new user
            response_user = c.post(
                '/users',
                data=json.dumps(
                    {'username': 'jane@gmail.com', 'password': 'pwd'}),
                content_type='application/json',
            )
            assert response_user.status_code == 200
            # login
            response_login = c.post(
                '/login',
                data=json.dumps(
                    {'username': 'jane@gmail.com', 'password': 'pwd'}),
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
    with DBManagerTestFixture():
        with app.test_client() as c:
            # register
            response_user = c.post(
                '/users',
                data=json.dumps(
                    {'username': 'jane@gmail.com', 'password': 'pwd'}),
                content_type='application/json',
            )
            assert response_user.status_code == 200
            # login
            response_login = c.post(
                '/login',
                data=json.dumps(
                    {'username': 'jane@gmail.com', 'password': 'pwd'}),
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
                data=json.dumps(
                    {'habitname': 'reading', 'timestamp': '2020-11-30'}),
                content_type='application/json',
            )
            assert response2.status_code == 200
            # get activity given a date
            response3 = c.get(
                'api/habits/logs',
                data=json.dumps({'habitname': 'reading', 'trailing_days': 5}),
                content_type='application/json',
            )
            assert response3.status_code == 200
            # get all activity
            response4 = c.get(
                'api/habits/logs',
                data=json.dumps({'habitname': 'reading'}),
                content_type='application/json',
            )
            assert response4.status_code == 200
