"""Habit Tracker Web Server entry point."""
import json
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, session
from habit_server.__init__ import app, db, login_manager
from habit_server.db_models import User, UserActivity, UserHabit
from habit_server.db_manager import DBManager
from habit_server.utils import AlchemyEncoder

db_manager = DBManager(db.session)

@login_manager.user_loader
def load_user(username):
    return User.get(username)

@app.route('/')
def hello_world():
    """Adding Docstring to satisfy github actions."""
    return 'Hello Habit Tracker'

@app.route('/api/habits', methods=['GET'])
def get_habits():
    user = User(username=session['username'], hashed_password = "")
    result = db_manager.get_habits(user)
    if result.ok():
        return json.dumps(result.unwrap(), cls=AlchemyEncoder), 200
    else:
        return "cannot add habit ", 404

@app.route('/api/habits', methods=['POST'])
def add_habit():
    new_habit = request.json['habitname']
    print(new_habit)
    userhabit = UserHabit(username = session['username'], habitname=new_habit)
    result = db_manager.add_habit(userhabit)
    if result.ok():
        return "add habit successful", 200
    else:
        return "cannot add habit ", 404

@app.route('/api/habits', methods=['DELETE'])
def delete_habit():
    new_habit = request.json['habitname']
    userhabit = UserHabit(username = session['username'], habitname = new_habit)
    result = db_manager.delete_habit(userhabit)
    if result.ok():
        return "delete habit successful", 200
    else:
        return "cannot delete habit ", 404

@app.route('/api/habits/logs', methods=['GET'])
def get_activites():
    data = request.json
    habitname = data['habitname']
    trailing_days = 100
    if data.get('trailing_days'):
        trailing_days = data['trailing_days']
    userhabit = UserHabit(username = session['username'], habitname = habitname)
    result = db_manager.get_activities(userhabit, trailing_days)
    if result.ok():
        return json.dumps(result.unwrap(), cls=AlchemyEncoder), 200
    else:
        return "cannot delete habit ", 404

@app.route('/api/habits/logs', methods=['POST'])
def add_activites():
    habitname = request.json['habitname']
    timestamp = request.json['timestamp']
    date_time = date.fromisoformat(timestamp)
    activity = UserActivity(username = session['username'], habitname = habitname, timestamp = date_time)
    result = db_manager.add_activity(activity)
    if result.ok():
        return "add activity successful", 200
    else:
        return "cannot add activity", 404

@app.route('/login', methods = ['POST'])
def login():
    data = request.json
    username = data.get('username', None)
    password = data.get('password', None)
    user = db_manager._session.query(User).filter_by(username=username).first()
    if not user or not user.check_password(password):
        return "login failed", 404
    session['username'] = username
    return render_template('login.html', name=user.username)

@app.route('/users', methods = ['POST'])
def register():
    data = request.json
    username = data.get('username', None)
    password = data.get('password', None)
    user = User(username = username, hashed_password = password)
    user.set_password(password)
    result = db_manager.add_user(user)
    if result.ok():
        return render_template('login.html', name=user.username)
    else:
        return "register failed", 404

# render
@app.route('/login', methods=['GET'])
def render_login():
    return render_template('login.html')

@app.route('/habits', methods=['GET'])
def render_habits():
    return render_template('habits.html')

@app.route('/progress', methods=['GET'])
def render_progress():
    return render_template('progress.html')


if __name__ == '__main__':
    app.run(debug = True)
