from flask import json
from test.DBManagerTestFixture import DBManagerTestFixture
from app import app


def test_user():
    with DBManagerTestFixture():
        with app.test_client() as c:
            # register a new user
            response1 = c.post(
                '/api/users',
                data={'username': 'jane@gmail.com', 'password': 'pwd'},
                content_type='application/x-www-form-urlencoded'
            )
            assert response1.status_code == 200

            # add duplicate user
            response2 = c.post(
                '/api/users',
                data={'username': 'jane@gmail.com', 'password': 'pwd'},
                content_type='application/x-www-form-urlencoded'
            )
            assert response2.status_code == 404

            # login successful
            response3 = c.post(
                '/api/login',
                data={'username': 'jane@gmail.com', 'password': 'pwd'},
                content_type='application/x-www-form-urlencoded'
            )
            assert response3.status_code == 200

            # login with wrong pwd
            response4 = c.post(
                '/api/login',
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
                '/api/users',
                data={'username': 'jane@gmail.com', 'password': 'pwd'},
                content_type='application/x-www-form-urlencoded'
            )
            assert response_user.status_code == 200
            # login
            response_login = c.post(
                '/api/login',
                data={'username': 'jane@gmail.com', 'password': 'pwd'},
                content_type='application/x-www-form-urlencoded'
            )
            assert response_login.status_code == 200

            # add a  habit
            response1 = c.post(
                '/api/habits',
                data={'habitname': 'reading'},
                content_type='application/x-www-form-urlencoded'
            )
            assert response1.status_code == 201

            # get all habits
            response2 = c.get(
                '/api/habits',
                content_type='application/x-www-form-urlencoded'
            )
            assert response2.status_code == 200

            # delete a habit
            response3 = c.delete(
                '/api/habits/reading',
            )
            assert response3.status_code == 200


def test_activity():
    with DBManagerTestFixture():
        with app.test_client() as c:
            # register
            response_user = c.post(
                '/api/users',
                data={'username': 'jane@gmail.com', 'password': 'pwd'},
                content_type='application/x-www-form-urlencoded'
            )
            assert response_user.status_code == 200

            # login
            response_login = c.post(
                '/api/login',
                data={'username': 'jane@gmail.com', 'password': 'pwd'},
                content_type='application/x-www-form-urlencoded'
            )
            assert response_login.status_code == 302  # redirect to habits

            # add a  habit
            response1 = c.post(
                '/api/habits',
                data={'habitname': 'reading'},
                content_type='application/x-www-form-urlencoded'
            )
            assert response1.status_code == 201

            # add a activity
            response2 = c.post(
                '/api/habits/logs',
                data={'habitname': 'reading', 'day_to_log': '2020-11-30'},
                content_type='application/x-www-form-urlencoded'
            )
            assert response2.status_code == 200

            # get activity given a date
            response3 = c.get(
                'api/habits/logs',
                data={'habitname': 'reading', 'trailing_days': 5},
                content_type='application/x-www-form-urlencoded'
            )
            assert response3.status_code == 200

            # get all activity
            response4 = c.get(
                'api/habits/logs',
                data={'habitname': 'reading'},
                content_type='application/x-www-form-urlencoded'
            )
            assert response4.status_code == 200
