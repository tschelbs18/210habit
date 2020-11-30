"""Habit Tracker Web Server entry point."""

from flask import Flask, render_template, request, jsonify, session
from habit_server.__init__ import app, session
from habit_server.db_models import User, UserActivity, UserHabit
from habit_server.db_manager import DBManager, db
from habit_server.utils import toDate, AlchemyEncoder
import json
db_manager = DBManager(db.session)
cur_user = User(username='joe@gmail.com', hashed_password='pwd')


@app.route('/')
def hello_world():
    """Adding Docstring to satisfy github actions."""
    return 'Hello, World!'

@app.route('/team/<member>')  # i.e /team/daniel
def team_page(member):
    """Route for team members.
    Each member is associated with their own route.
    """
    if member == "daniel":
        return "Daniel's page!"
    else:
        return "Unknown team member: {}".format(member)

@app.route('/api/habits', methods=['GET'])
def get_habits():
    user = User(username=cur_user.username, hashed_password=cur_user.hashed_password)
    print("here")
    result = db_manager.get_habits(user)
    if result.ok():
        return json.dumps(result.unwrap(), cls=AlchemyEncoder), 200
    else:
        return "cannot add habit ", 404

@app.route('/api/habits', methods=['POST'])
def add_habit():
    new_habit = request.json['habitname']
    print(new_habit)
    userhabit = UserHabit(username=cur_user.username, habitname=new_habit)
    result = db_manager.add_habit(userhabit)
    if result.ok():
        return "add habit successful", 200
    else:
        return "cannot add habit ", 404

@app.route('/api/habits', methods=['DELETE'])
def delete_habit():
    new_habit = request.json['habitname']
    userhabit = UserHabit(username = cur_user.username, habitname = new_habit)
    result = db_manager.delete_habit(userhabit)
    if result.ok():
        return "delete habit successful", 200
    else:
        return "cannot delete habit ", 404

@app.route('/api/habits/logs', methods=['GET'])
def get_activites():
    habitname = request.json['habitname']
    print("here")
    start = request.json['start']
    print("here2")
    end = request.json['end']

    if start != None and end != None:
        startDay = request.args.get('start', type = toDate)
        endDay = request.args.get('end', type = toDate)
    if (startDay != None and endDay != None):
        print("TODO")
        # get activity with start and end day
    else:
        userhabit = UserHabit(username = cur_user.username, habitname = habitname)
        return db_manager.get_activites(userhabit)

@app.route('/api/habits/logs', methods=['POST'])
def add_activites():
    habitname = request.json['habitname']
    timestamp = request.json['timestamp']
    activity = UserActivity(username = cur_user.username, habitname = habitname, timestamp = timestamp)
    return db_manager.add_activity(activity)

# render
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/habits', methods=['GET'])
def habits():
    return render_template('habits.html')

@app.route('/progress', methods=['GET'])
def progress():
    return render_template('progress.html')


if __name__ == '__main__':
    app.run(debug = True)
