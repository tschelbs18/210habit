from sqlalchemy import create_engine
from habit_server.db_manager import DBManager
from habit_server.db_models import User, UserActivity, UserHabit

def createDBManager():
    engine = create_engine('sqlite:///:memory:')
    return DBManager(engine)


def test_add_user():
    db = createDBManager()

    user1 = User(username='joe', password='pwd')
    user2 = User(username='mary', password='pwd')

    assert db.add_user(user1).ok()
    assert not db.add_user(user1).ok()
    assert db.add_user(user2).ok()

    # does user exist

def test_add_habit():
    pass

def test_delete_habit():
    pass

def test_get_habits():
    pass

def test_add_activity():
    pass

def test_get_activities():
    pass