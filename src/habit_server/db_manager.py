from result.result import Result
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from habit_server.db_models import User, UserActivity, UserHabit


class DBManager():
    def __init__(self, session):
        self._session = session

    def add_user(self, user):
        # check if user already exists
        if self.does_user_exist(user.username):
            return Result.Err("User with usename: '{}' already exists, cannot add".format(user.username))

        # add new user
        self._session.add(user)
        return Result.Ok()

    def does_user_exist(self, username):
        users = self._session.query(User).filter_by(username=username).all()

        if len(users) == 0:
            return False
        else:
            return True

    def add_habit(self, habit):
        if not self.does_user_exist(habit.username):
            return Result.Err("User does not exist, cannot add habit")

        if self.does_habit_exist(habit):
            return Result.Err("Habit already exists")

        self._session.add(habit)
        return Result.Ok()

    def get_habits(self, user): 
        # make sure user exists
        if not self.does_user_exist(user.username):
            return Result.Err("User does not exist, cannot get habits")

        habits = self._session.query(UserHabit).filter_by(username=user.username).all()
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
            self._session.add(activity)
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
