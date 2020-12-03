from src.db_manager import DBManager
from src.db_models import User, UserActivity, UserHabit
from DBManagerTestFixture import DBManagerTestFixture
from flask import Flask
from habit_server.app import app, db
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
import uuid

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SECRET_KEY'] = uuid.uuid4().hex
db = SQLAlchemy(app)


def test_add_user():
    """Test the add_user method of the db manager."""
    with DBManagerTestFixture() as db_man:
        user1 = User(username='joe@gmail.com', hashed_password='pwd')
        user2 = User(username='mary@yahoo.com', hashed_password='pwd')
        user3 = User(username='jim', hashed_password='pwd')

        # attempt to add user with invalid username (not an email address)
        assert not db_man.add_user(user3).is_ok()

        # add valid user
        assert db_man.add_user(user1).is_ok()
        assert db_man.does_user_exist(user1.username)
        assert not db_man.does_user_exist(user2.username)

        # attempt to add duplicate user
        assert not db_man.add_user(user1).is_ok()

        # add another valid user
        assert db_man.add_user(user2).is_ok()


def test_add_habit():
    """Test the add_habit method of the db manager."""
    with DBManagerTestFixture() as db_man:
        user = User(username='joe@gmail.com', hashed_password='pwd')
        habit1 = UserHabit(
            username='joe@gmail.com',
            habitname='running',
        )
        habit2 = UserHabit(
            username='joe@gmail.com',
            habitname='sleeping',
        )

        # attempt to add habit with no associated user
        assert not db_man.add_habit(habit1).is_ok()

        # add user and associated habit
        assert db_man.add_user(user).is_ok()
        assert db_man.add_habit(habit1).is_ok()

        # attempt to add duplicate habit
        assert not db_man.add_habit(habit1).is_ok()

        # add another habit with the same associated user
        assert db_man.add_habit(habit2).is_ok()


def test_delete_habit():
    """Test the delete_habit method of the db manager."""
    with DBManagerTestFixture() as db_man:
        user = User(username='joe@gmail.com', hashed_password='pwd')
        habit = UserHabit(
            username='joe@gmail.com',
            habitname='running',
        )

        # attempt to delete non-existent habit
        assert db_man.add_user(user).is_ok()
        assert not db_man.delete_habit(habit).is_ok()

        # add and then delete habit
        assert db_man.add_habit(habit).is_ok()
        assert len(db_man.get_habits(user).unwrap()) == 1
        assert db_man.delete_habit(habit).is_ok()
        assert len(db_man.get_habits(user).unwrap()) == 0


def test_get_habits():
    """Test the get_habits method of the db manager."""
    with DBManagerTestFixture() as db_man:
        user = User(username='joe@gmail.com', hashed_password='pwd')
        habit1 = UserHabit(
            username='joe@gmail.com',
            habitname='running',
        )
        habit2 = UserHabit(
            username='joe@gmail.com',
            habitname='sleeping',
        )

        # attempt to get all habits from non-existent user
        assert not db_man.get_habits(user).is_ok()

        # add user, multiple habits, and grab all
        assert db_man.add_user(user).is_ok()
        assert len(db_man.get_habits(user).unwrap()) == 0
        assert db_man.add_habit(habit1).is_ok()
        assert len(db_man.get_habits(user).unwrap()) == 1
        assert db_man.add_habit(habit2).is_ok()
        assert len(db_man.get_habits(user).unwrap()) == 2


def test_add_and_get_activities():
    """Test the add_activity and get_activites methods of the db manager."""
    with DBManagerTestFixture() as db_man:
        user = User(username='joe@gmail.com', hashed_password='pwd')
        habit = UserHabit(
            username='joe@gmail.com',
            habitname='running',
        )
        act1 = UserActivity(
            username='joe@gmail.com',
            habitname='running',
            timestamp=datetime.datetime.now()
        )

        act2 = UserActivity(
            username='joe@gmail.com',
            habitname='running',
            timestamp=datetime.datetime.now() - datetime.timedelta(days=101)
        )

        # attempt to add/get activities with no associated user
        assert not db_man.add_activity(act1).is_ok()
        assert not db_man.get_activities(habit).is_ok()

        # attempt to add/get activities with no associated habit
        assert db_man.add_user(user).is_ok()
        assert not db_man.add_activity(act1).is_ok()
        assert not db_man.get_activities(habit).is_ok()

        # add habit and associated activities and get all
        assert db_man.add_habit(habit).is_ok()
        query_result = db_man.get_activities(habit, trailing_days=100)
        assert len(query_result.unwrap()) == 0

        assert db_man.add_activity(act1).is_ok()
        query_result = db_man.get_activities(habit, trailing_days=100)
        assert len(query_result.unwrap()) == 1

        assert db_man.add_activity(act2).is_ok()  # not in 100 day filter range
        query_result = db_man.get_activities(habit, trailing_days=100)
        assert len(query_result.unwrap()) == 1

        # no date filter, get all activities
        query_result = db_man.get_activities(habit, trailing_days=None)
        assert len(query_result.unwrap()) == 2


def test_get_activity_streak():
    with DBManagerTestFixture() as db_man:
        user = User(username='joe@gmail.com', hashed_password='pwd')
        habit = UserHabit(
            username='joe@gmail.com',
            habitname='running',
        )
        act1 = UserActivity(
            username='joe@gmail.com',
            habitname='running',
            timestamp=datetime.datetime.now() - datetime.timedelta(days=1)
        )
        act2 = UserActivity(
            username='joe@gmail.com',
            habitname='running',
            timestamp=datetime.datetime.now() - datetime.timedelta(days=2)
        )

        # try getting streak with no existing user or habit
        assert not db_man.get_activity_streak(habit).is_ok()

        # add user and habit
        assert db_man.add_user(user).is_ok()
        assert db_man.add_habit(habit).is_ok()

        # no activities, streak == 0
        streak = db_man.get_activity_streak(habit).unwrap()
        assert streak == 0

        # add activity. It is too old, streak still == 0
        assert db_man.add_activity(act2).is_ok()
        streak = db_man.get_activity_streak(habit).unwrap()
        assert streak == 0

        # add another activity, this time streak == 2
        assert db_man.add_activity(act1).is_ok()
        streak = db_man.get_activity_streak(habit).unwrap()
        assert streak == 2
