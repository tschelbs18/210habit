from src.db_models import User, UserActivity, UserHabit
import requests

# def add_activity_to_db(username, password, habitname, date):
def add_activity_to_db(username, password, habitname, day_to_log):
    with requests.Session() as s:
        data = {"username":username, "password": password}
        s.post("http://127.0.0.1:5000/api/login", data)

        data = {'habitname':habitname, 'day_to_log':day_to_log}
        resp = s.post("http://127.0.0.1:5000/api/habits/logs", data)
        print(resp, resp.content)


if __name__ == '__main__':
    username = 'abc@gmail.com'
    password = 'abc@gmail.com'
    add_activity_to_db(username, password, 'abc', '2020-12-18')
