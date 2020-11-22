from sqlalchemy import create_engine
from habit_server.db_manager import DBManager
from habit_server.db_models import User, UserActivity, UserHabit
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from habit_server.app import db
import datetime
import time

def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory'
    db.init_app(app)
    app.app_context().push()
    return app


class DBManagerTestFixture():
    def __enter__(self):
        app = create_test_app()
        with app.app_context():
            db.create_all()
            return DBManager(db.session)

    def __exit__(self, exception_type, exception_value, traceback):
        db.session.remove()
        db.drop_all()


def test_add_user():
    with DBManagerTestFixture() as db_man:
        user1 = User(username='joe', password='pwd')
        user2 = User(username='mary', password='pwd')

        assert db_man.add_user(user1).ok()
        assert db_man.does_user_exist(user1.username)
        assert not db_man.does_user_exist(user2.username)
        assert not db_man.add_user(user1).ok()
        assert db_man.add_user(user2).ok()


def test_add_habit():
    with DBManagerTestFixture() as db_man:
        user = User(username='joe', password='pwd')
        habit1 = UserHabit(
            username='joe',
            habitname='running',
            habit_freq=1
        )
        habit2 = UserHabit(
            username='joe',
            habitname='sleeping',
            habit_freq=1
        )

        assert not db_man.add_habit(habit1).ok()
        assert db_man.add_user(user).ok()
        assert db_man.add_habit(habit1).ok()
        assert not db_man.add_habit(habit1).ok()
        assert db_man.add_habit(habit2).ok()

def test_delete_habit():
    with DBManagerTestFixture() as db_man:
        user = User(username='joe', password='pwd')
        habit = UserHabit(
            username='joe',
            habitname='running',
            habit_freq=1
        )
        assert db_man.add_user(user).ok()
        assert not db_man.delete_habit(habit).ok()
        assert db_man.add_habit(habit).ok()
        assert len(db_man.get_habits(user).unwrap())== 1
        assert db_man.delete_habit(habit).ok()
        assert len(db_man.get_habits(user).unwrap())== 0

def test_get_habits():
    with DBManagerTestFixture() as db_man:
        user = User(username='joe', password='pwd')
        habit1 = UserHabit(
            username='joe',
            habitname='running',
            habit_freq=1
        )
        habit2 = UserHabit(
            username='joe',
            habitname='sleeping',
            habit_freq=1
        )

        assert not db_man.get_habits(user).ok()
        assert db_man.add_user(user).ok()
        assert len(db_man.get_habits(user).unwrap())== 0
        assert db_man.add_habit(habit1).ok()
        assert len(db_man.get_habits(user).unwrap())== 1
        assert db_man.add_habit(habit2).ok()
        assert len(db_man.get_habits(user).unwrap())== 2


def test_add_and_get_activities():
    with DBManagerTestFixture() as db_man:
        user = User(username='joe', password='pwd')
        habit = UserHabit(
            username='joe',
            habitname='running',
            habit_freq=1
        )
        act1 = UserActivity(
            username='joe',
            habitname='running',
            timestamp=datetime.datetime.fromtimestamp(time.time())
        )
        act2 = UserActivity(
            username='joe',
            habitname='running',
            timestamp=datetime.datetime.fromtimestamp(time.time())
        )

        assert not db_man.add_activity(act1).ok()
        assert not db_man.get_activities(habit).ok()
        assert db_man.add_user(user).ok()
        assert not db_man.add_activity(act1).ok()
        assert db_man.add_habit(habit).ok()
        assert len(db_man.get_activities(habit).unwrap()) == 0
        assert db_man.add_activity(act1).ok()
        assert len(db_man.get_activities(habit).unwrap()) == 1
        assert db_man.add_activity(act2).ok()
        assert len(db_man.get_activities(habit).unwrap()) == 2
