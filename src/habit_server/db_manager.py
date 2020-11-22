from result.result import Result
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from habit_server.db_models import Base, User, UserActivity, UserHabit

Session = sessionmaker()


class DBManager():
    def __init__(self, db_engine):
        Base.metadata.create_all(db_engine)
        Session.configure(bind=db_engine)
        self._session = Session()

    def add_user(self, user):
        # check if user already exists
        if self.does_user_exist(user):
            return Result.Err("User with usename: '{}' already exists, cannot add".format(user.username))

        # add new user
        self._session.add(user)
        return Result.Ok()

    def does_user_exist(self, user):
        users = self._session.query(User).filter_by(username=user.username).all()

        if len(users) == 0:
            return False
        else:
            return True

    def add_habit(self, habit):
        if self.does_habit_exist(habit):
            return Result.Err("Habit already exists")

        self._session.add(habit)

    def get_habits(self, user): 
        # make sure user exists
        if not self.does_user_exist(user):
            return Result.Err("User does not exist, cannot get habits")

        habits = self._session.query(UserHabit).filter_by(username=user.name).all()
        return Result.Ok(habits)

    def delete_habit(self, habit):
        # make sure habit exists
        habits = self._session.query(UserHabit).filter_by(
            username=habit.username,
            habitname=habit.habitname
        ).all()

        if len(habits) == 0:
            return Result.Err("Habit does not exist, cannot delete")
        else:
            self._session.delete(habit)
            return Result.Ok()

    def does_habit_exist(self, habit):
        habits = self._session.query(UserHabit).filter_by(
            username=habit.username,
            habitname=habit.habitname
        ).all()

        if len(habits) == 0:
            return False
        else:
            return True

    def add_activity(self, activity):
        # make sure habit exists
        habits = self._session.query(UserHabit).filter_by(
            username=activity.username,
            habitname=activity.habitname
        ).all() 

        if len(habits) == 0:
            return Result.Err("Habit does not exist, cannot add activity")
        else:
            self.session.add(activity)
            return Result.Ok()

    def get_activities(self, habit):
        # make sure habit exists
        if not self.does_habit_exist(habit):
            return Result.Err("Habit does not exist, cannot get activities")

        activities = self._session.query(UserActivity).filter_by(
            username=habit.username,
            habitname=habit.habitname
        ).all() 

        return Result.Ok(activities)


if __name__ == "__main__":
    db = DBManager(create_engine('sqlite:///../habittracker.db', echo=True))
    user = User(username='jared', password='pwd')
    db.add_user(user)