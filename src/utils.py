"""Habit Server Utilities."""
from datetime import datetime, timedelta
import re
import json
from sqlalchemy.ext.declarative import DeclarativeMeta


def is_valid_email_addr(addr):
    """Validate whether an email address is syntactically valid.

    :param addr str: email addres
    :returns bool: is valid?
    """
    if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", addr):
        return True
    else:
        return False


def get_activity_streak(activities, current_date=datetime.now()):
    """Get the current activity streak.

    An activity streak is defined as the number of previous
    days in a row an activity has been logged.

    :param activities List[UserActivity]: list of activities
    :returns int: current activity streak
    """
    print('\nCalling get_activity_streak ', [act.timestamp for act in activities])

    # only conisder year, month, day of dates
    dates = [
        datetime.strptime(
            act.timestamp.strftime("%Y-%m-%d"), "%Y-%m-%d"
        ) for act in activities
    ]

    # remove duplicates and sort
    # it is possible that there could be two logs in a single day
    dates = list(filter(lambda date: date <= current_date, dates))
    dates = sorted(list(set(dates)), reverse=True)

    current_date = datetime.strptime(current_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
    day_to_check = current_date 
    streak = 0

    print('Dates', dates)
    print('Streak current date', current_date)
    for date in dates:
        if day_to_check - date == timedelta(days=0):
            # check that there is an activity entry for an expected day
            day_to_check -= timedelta(days=1)
        elif current_date - date == timedelta(days=1):
            # streak is still valid if we have not logged anything today
            # but there is a log from yesterday
            day_to_check -= timedelta(days=2)
        elif current_date == date:
            day_to_check -= timedelta(days=1)
        else:
            break

        streak += 1

    print('Streak', streak)

    return streak


class AlchemyEncoder(json.JSONEncoder):
    """AlchemyEncoder for habit server."""

    def default(self, obj):
        """Unwrap Result object and serialize to Json.

        :param result Result: returned result of db_manager
        :returns Json: Json object
        """
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith(
                    '_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values, like other
                    # classes
                    if field == 'timestamp':
                        data = data.strftime("%Y-%m-%d")
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)
