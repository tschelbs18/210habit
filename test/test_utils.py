from datetime import datetime, timedelta
from src.db_models import UserActivity
from src.utils import (
    is_valid_email_addr,
    get_activity_streak
)


def generate_activities(timestamps):
    # generate a list of activities
    return [
            UserActivity(
                username='joe@gmail.com',
                habitname='running',
                timestamp=timestamp
            ) for timestamp in timestamps
    ]


def test_valid_email_addr():
    """ test that an email address is syntactically valid """
    assert not is_valid_email_addr('joe')
    assert not is_valid_email_addr('joe@')
    assert not is_valid_email_addr('joe@gmail')
    assert not is_valid_email_addr('@gmail.com')
    assert is_valid_email_addr('joe@gmail.com')


def test_get_activity_streak():
    """ test that the activitiy streak util works """

    # test 10 day streak (including today)
    timestamps = [
        datetime.now() - timedelta(days=i) for i in range(10)
    ]
    assert get_activity_streak(generate_activities(timestamps)) == 10

    # test 10 day streak (no log today, but there is a log yesterday)
    timestamps = [
        datetime.now() - timedelta(days=i) for i in range(1, 11)
    ]
    assert get_activity_streak(generate_activities(timestamps)) == 10

    # test break in streak
    timestamps = [
        datetime.now() - timedelta(days=i) for i in [1, 2, 3, 5, 6, 7]
    ]
    assert get_activity_streak(generate_activities(timestamps)) == 3

    # test break in streak
    timestamps = [
        datetime.now() - timedelta(days=i) for i in [2, 3, 4]
    ]
    assert get_activity_streak(generate_activities(timestamps)) == 0

    # test duplicate log entries per day, should only count as 1
    # in a streak
    timestamps = [
        datetime.now() - timedelta(days=i) for i in [0, 1, 2, 2, 3, 3]
    ]
    assert get_activity_streak(generate_activities(timestamps)) == 4

    # test out of order streak
    timestamps = [
        datetime.now() - timedelta(days=i) for i in [3, 1, 2, 0]
    ]
    assert get_activity_streak(generate_activities(timestamps)) == 4
