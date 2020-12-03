"""Habit Tracker Web Server entry point."""
import json
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, session, flash, redirect, url_for
from habit_server.__init__ import app, db, login_manager
from habit_server.db_models import User, UserActivity, UserHabit
from habit_server.db_manager import DBManager
from habit_server.utils import AlchemyEncoder
from flask_login import login_user, logout_user, login_required, current_user
import flask_login

db.create_all()
db_manager = DBManager(db.session)

@login_manager.user_loader
def load_user(username):
    """Retrive current user."""    
    return User.query.get(username)

@app.route('/')
def hello_world():
    """Adding Docstring to satisfy github actions."""
    return 'Hello Habit Tracker'

@app.route('/api/habits', methods=['GET'])
def get_habits():
    """Get habits for a user.""" 
    # user = User(username=session['username'], hashed_password = "")
    result = db_manager.get_habits(flask_login.current_user)
    if not result.is_ok():
        return "cannot get habits", 400

    habits = result.unwrap()

    return_dict = {'habits':[], 'streaks':[]}
    for habit in habits:
        return_dict['habits'].append(habit.habitname)
        return_dict['streaks'].append(db_manager.get_activity_streak(habit).unwrap())

    return json.dumps(return_dict), 200

@app.route('/api/habits', methods=['POST'])
def add_habit():
    """Add a habit.

    :param habitname str: habit to add
    """ 
    new_habit = request.form['habitname']
    username = flask_login.current_user.username
    userhabit = UserHabit(username = username, habitname=new_habit)
    result = db_manager.add_habit(userhabit)
    if result.is_ok():
        return "add habit successful", 201
    else:
        return "cannot add habit ", 404

@app.route('/api/habits', methods=['DELETE'])
def delete_habit():
    """Delete a habit.

    :param habitname str: habit to delete
    """ 
    new_habit = request.json['habitname']
    userhabit = UserHabit(username = session['username'], habitname = new_habit)
    result = db_manager.delete_habit(userhabit)
    if result.is_ok():
        return "delete habit successful", 200
    else:
        return "cannot delete habit ", 404

@app.route('/api/habits/logs', methods=['GET'])
def get_activites():
    """Get activities for a user.

    :param habitname str: habit for the activity 
    """ 
    data = request.json
    habitname = data['habitname']
    trailing_days = 100
    if data.get('trailing_days'):
        trailing_days = data['trailing_days']
    userhabit = UserHabit(username = session['username'], habitname = habitname)
    result = db_manager.get_activities(userhabit, trailing_days)
    if result.is_ok():
        return json.dumps(result.unwrap(), cls=AlchemyEncoder), 200
    else:
        return "cannot get habit logs", 404

@app.route('/api/habits/logs', methods=['POST'])
def add_activites():
    """Add activities for a habit.

    :param habitname str: habit for the activity 
    :param habitname str: timestamp for the activity 
    """ 
    habitname = request.json['habitname']
    timestamp = request.json['timestamp']
    date_time = date.fromisoformat(timestamp)
    activity = UserActivity(username = session['username'], habitname = habitname, timestamp = date_time)
    result = db_manager.add_activity(activity)
    if result.is_ok():
        return "add activity successful", 200
    else:
        return "cannot add activity", 404

@app.route('/api/login', methods = ['POST'])
def login():
    """Login a user.

    :param username str: username for the user 
    :param password str: password for the user 
    """ 
    data = request.form
    username = data.get('username', None)
    password = data.get('password', None)
    user = db_manager._session.query(User).filter_by(username=username).first()
    if not user or not user.check_password(password):
        return "login failed", 404
    session['username'] = username
    login_user(user)
    flash('Logged in successfully!!!')
    # return render_template('login.html', name=user.username)
    # return "login successful", 200
    return redirect(url_for('render_habits'))

@app.route('/api/users', methods = ['POST'])
def register():
    """Register a user.

    :param username str: username for the user 
    :param password str: password for the user 
    """ 
    data = request.form
    username = data.get('username', None)
    password = data.get('password', None)
    user = User(username = username, hashed_password = password)
    user.set_password(password)
    result = db_manager.add_user(user)
    if result.is_ok():
        return render_template('login.html', name=user.username)
    else:
        return "register failed", 404

@app.route('/login', methods=['GET'])
def render_login():
    """Render login page.""" 
    return render_template('login.html')

@app.route('/habits', methods=['GET'])
def render_habits():
    """Render habits page.""" 
    return render_template('habits.html')

@app.route('/progress', methods=['GET'])
def render_progress():
    """Render progress page.""" 
    return render_template('progress.html')


if __name__ == '__main__':
    app.run()
