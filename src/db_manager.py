"""Database manager for the habit server."""
import datetime
from result.result import Result
from src.db_models import User, UserActivity, UserHabit
from src.utils import is_valid_email_addr, get_activity_streak


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

        :param user User: user to get habits from
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

        # delete any activities for that habit
        activities = self._session.query(UserActivity).filter_by(
            username=habit.username,
            habitname=habit.habitname
        ).all()

        if len(habits) == 0:
            return Result.Err("Habit does not exist, cannot delete")
        else:
            self._session.delete(habits[0])
            for activity in activities:
                self._session.delete(activity)
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

    def get_all_activities(self, user, trailing_days=100):
        """Get all the activities for a particular habit.

        :param user User: user to get habits from
        :return Result: operation result, Ok or Err
        """
        result = self.get_habits(user)

        if not result.is_ok():
            return result

        activities_and_streaks = []
        # Get all activities + streaks for all habits
        for habit in result.unwrap():
            activity_result = self.get_activities(habit, trailing_days=None)
            activities = activity_result.unwrap()

            for activity in activities:
                streak = get_activity_streak(
                    activities, current_date=activity.timestamp)
                activities_and_streaks.append((activity, streak))

        # filter for activities within last trailing_days
        cutoff_date = \
            datetime.datetime.now() - datetime.timedelta(days=trailing_days)

        activities_and_streaks = list(filter(
            lambda x: x[0].timestamp > cutoff_date, activities_and_streaks
        ))

        # Build dictionary of activity and streak in format that ZingGrid
        # expects
        activity_dict = {}
        for activity, streak in activities_and_streaks:
            if activity.habitname in activity_dict:
                activity_dict[activity.habitname].append(
                    (activity.timestamp.strftime("%Y-%m-%d"), streak))
            else:
                activity_dict[activity.habitname] = \
                    [(activity.timestamp.strftime("%Y-%m-%d"), streak)]

        for habit in result.unwrap():
            if habit.habitname not in activity_dict:
                activity_dict[habit.habitname] = [()]

        # remove duplicates
        for habitname, entries in activity_dict.items():
            activity_dict[habitname] = sorted(list(set(entries)))

        return Result.Ok(activity_dict)

    def get_activities(self, habit, trailing_days=100):
        """Get all the activities for a particular habit.

        :param habit UserHabit: grab all activities linked to this habit.
        :param trailing_days Optional[int]: filter the activities to last
            trailing_days number of days. If None, get all activities
        :return Result: operation result, Ok or Err
        """
        # make sure habit exists
        if not self.does_habit_exist(habit):
            return Result.Err("Habit does not exist, cannot get activities")

        query = self._session.query(UserActivity).filter(
            UserActivity.username == habit.username,
            UserActivity.habitname == habit.habitname,
        )

        if trailing_days is not None:
            end_time = datetime.datetime.now()
            start_time = end_time - datetime.timedelta(days=trailing_days)
            query = query.filter(
                UserActivity.timestamp > start_time,
                UserActivity.timestamp < end_time,
            )

        activities = query.all()

        return Result.Ok(activities)

    def get_activity_streak(self, habit):
        """Get the current activity streak for a given habit.

        :param habit UserHabit: user habit to get streak for
        :return Result: operation result, Ok or Err
        """
        result = self.get_activities(habit, trailing_days=None)

        if not result.is_ok():
            return result

        streak = get_activity_streak(result.unwrap())

        return Result.Ok(streak)
