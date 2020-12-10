"""Helper util to add activity logs into the DB for any day."""
import requests

def add_activity_to_db(username, password, habitname, day_to_log):
    """Post an activity log to the habit server API.

    :param username: username of user
    :param password: password of user
    :param habitname: habit to post activity to
    :param day_to_log: day to post activity to
    """
    with requests.Session() as s:
        data = {"username": username, "password": password}
        s.post("http://127.0.0.1:5000/api/login", data)

        data = {'habitname': habitname, 'day_to_log': day_to_log}
        resp = s.post("http://127.0.0.1:5000/api/habits/logs", data)
        print(resp, resp.content)


if __name__ == '__main__':
    username = ''
    password = ''
    habitname = ''
    day_to_log = '2020-12-10'

    add_activity_to_db(username, password, habitname, day_to_log)
