from habit_server.db_manager import DBManager
from habit_server.db_models import User, UserActivity, UserHabit
from flask import Flask
from habit_server.app import db
import datetime


def create_test_app():
    """ Create a test flask app.

    :return Flask: initialized test flask app
    """
    app = Flask(__name__)
    app.config['TESTING'] = True
    # use in-memory sqllite database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    app.app_context().push()

    return app


class DBManagerTestFixture():
    """Database manager test fixture."""
    def __enter__(self):
        """Initialize test app, db manager, db session.

        :return DMManager: initialized database manager.
        """
        app = create_test_app()
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


def test_add_user():
    """Test the add_user method of the db manager."""
    with DBManagerTestFixture() as db_man:
        user1 = User(username='joe@gmail.com', hashed_password='pwd')
        user2 = User(username='mary@yahoo.com', hashed_password='pwd')
        user3 = User(username='jim', hashed_password='pwd')

        # attempt to add user with invalid username (not an email address)
        assert not db_man.add_user(user3).ok()

        # add valid user
        assert db_man.add_user(user1).ok()
        assert db_man.does_user_exist(user1.username)
        assert not db_man.does_user_exist(user2.username)

        # attempt to add duplicate user
        assert not db_man.add_user(user1).ok()

        # add another valid user
        assert db_man.add_user(user2).ok()


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
        assert not db_man.add_habit(habit1).ok()

        # add user and associated habit
        assert db_man.add_user(user).ok()
        assert db_man.add_habit(habit1).ok()

        # attempt to add duplicate habit
        assert not db_man.add_habit(habit1).ok()

        # add another habit with the same associated user
        assert db_man.add_habit(habit2).ok()


def test_delete_habit():
    """Test the delete_habit method of the db manager."""
    with DBManagerTestFixture() as db_man:
        user = User(username='joe@gmail.com', hashed_password='pwd')
        habit = UserHabit(
            username='joe@gmail.com',
            habitname='running',
        )

        # attempt to delete non-existent habit
        assert db_man.add_user(user).ok()
        assert not db_man.delete_habit(habit).ok()

        # add and then delete habit
        assert db_man.add_habit(habit).ok()
        assert len(db_man.get_habits(user).unwrap()) == 1
        assert db_man.delete_habit(habit).ok()
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
        assert not db_man.get_habits(user).ok()

        # add user, multiple habits, and grab all
        assert db_man.add_user(user).ok()
        assert len(db_man.get_habits(user).unwrap()) == 0
        assert db_man.add_habit(habit1).ok()
        assert len(db_man.get_habits(user).unwrap()) == 1
        assert db_man.add_habit(habit2).ok()
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
            timestamp=datetime.datetime.now() - datetime.timedelta(days=50)
        )

        act2 = UserActivity(
            username='joe@gmail.com',
            habitname='running',
            timestamp=datetime.datetime.now() - datetime.timedelta(days=101)
        )

        # attempt to add/get activities with no associated user
        assert not db_man.add_activity(act1).ok()
        assert not db_man.get_activities(habit).ok()

        # attempt to add/get activities with no associated habit
        assert db_man.add_user(user).ok()
        assert not db_man.add_activity(act1).ok()
        assert not db_man.get_activities(habit).ok()

        # add habit and associated activities and get all
        assert db_man.add_habit(habit).ok()
        query_result = db_man.get_activities(habit, trailing_days=100)
        assert len(query_result.unwrap()) == 0

        assert db_man.add_activity(act1).ok()
        query_result = db_man.get_activities(habit, trailing_days=100)
        assert len(query_result.unwrap()) == 1

        assert db_man.add_activity(act2).ok()  # not in 100 day filter range
        query_result = db_man.get_activities(habit, trailing_days=100)
        assert len(query_result.unwrap()) == 1

        query_result = db_man.get_activities(habit, trailing_days=200)
        assert len(query_result.unwrap()) == 2

        query_result = db_man.get_activities(habit, trailing_days=None)  # no filter
        assert len(query_result.unwrap()) == 2