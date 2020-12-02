"""Database manager for the habit server."""
import datetime
from result.result import Result
from sqlalchemy import and_
from habit_server.db_models import User, UserActivity, UserHabit
from habit_server.utils import is_valid_email_addr

class DBManager():
    """Database Manager for habit server."""

    def __init__(self, session):
        """:param session : databse session object."""
        self._session = session

    def add_user(self, user):
        """Add a new user to the database.
        :param user User: user to add
        :returns Result: operation result, Ok or Err.
        """
        # check that username is an email address
        if not is_valid_email_addr(user.username):
            return Result.Err(
                "Username '{}' is not an email address, cannot add user"
                .format(user.username)
            )

        # check if user already exists
        if self.does_user_exist(user.username):
            return Result.Err(
                "User with usename: '{}' already exists, cannot add"
                .format(user.username)
            )

        # add new user
        self._session.add(user)
        self._session.commit()

        return Result.Ok()

    def does_user_exist(self, username):
        """Check that a username exist in the database.
        :param username str: username to check.
        :returns bool: does user exist in database?
        """
        users = self._session.query(User).filter_by(username=username).all()

        if len(users) == 0:
            return False
        else:
            return True

    def add_habit(self, habit):
        """Add a habit to the databse for a particular user.
        :param habit UserHabit: habit to add
        :returns Result: operation result, Ok or Err
        """
        if not self.does_user_exist(habit.username):
            return Result.Err("User does not exist, cannot add habit")

        if self.does_habit_exist(habit):
            return Result.Err("Habit already exists")

        self._session.add(habit)
        self._session.commit()

        return Result.Ok()

    def get_habits(self, user):
        """Get habits for a particular user.
        :param user User: [description]
        :returns Result: operation result, Ok or Err
        """
        # make sure user exists
        if not self.does_user_exist(user.username):
            return Result.Err("User does not exist, cannot get habits")

        habits = self._session.query(UserHabit).filter_by(
                username=user.username
        ).all()

        return Result.Ok(habits)

    def delete_habit(self, habit):
        """Delete habit for a particular user.
        :param habit UserHabit: user habit to delete.
        :returns Result: operation result, Ok or Err
        """
        # make sure habit exists
        habits = self._session.query(UserHabit).filter_by(
            username=habit.username,
            habitname=habit.habitname
        ).all()

        if len(habits) == 0:
            return Result.Err("Habit does not exist, cannot delete")
        else:
            habit = self._session.query(UserHabit).filter_by(
            username=habit.username,
            habitname=habit.habitname
            ).first()
            self._session.delete(habit)
            self._session.commit()

            return Result.Ok()

    def does_habit_exist(self, habit):
        """Check whether a given habit exists for a given user.
        :param habit UserHabit: user habit to check existence for
        :returns bool: does the habit exist in the database?
        """
        habits = self._session.query(UserHabit).filter_by(
            username=habit.username,
            habitname=habit.habitname
        ).all()

        if len(habits) == 0:
            return False
        else:
            return True

    def add_activity(self, activity):
        """Add a new activity log for a given user and habit.
        :param activity UserActivity: activity to add
        :return Result: operation result, Ok or Err
        """
        # make sure habit exists
        habits = self._session.query(UserHabit).filter_by(
            username=activity.username,
            habitname=activity.habitname
        ).all()

        if len(habits) == 0:
            return Result.Err("Habit does not exist, cannot add activity")
        else:
            self._session.add(activity)
            self._session.commit()

            return Result.Ok()

    def get_activities(self, habit, trailing_days=100):
        """Get all the activities for a particular habit.
        :param habit UserHabit: grab all activities linked to this habit.
        :param trailing_days Optional[int]: filter the activities to last
            trailing_days number of days.
        :return Result: operation result, Ok or Err
        """
        # make sure habit exists
        if not self.does_habit_exist(habit):
            return Result.Err("Habit does not exist, cannot get activities")

        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=trailing_days)

        activities = self._session.query(UserActivity).filter(and_(
            UserActivity.username == habit.username,
            UserActivity.habitname == habit.habitname,
            UserActivity.timestamp > start_time,
            UserActivity.timestamp < end_time,
        )).all()

        return Result.Ok(activities)
