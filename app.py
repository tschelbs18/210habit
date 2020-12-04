"""Habit Tracker Web Server entry point."""
import json
from datetime import date
import os
import uuid
from flask import render_template, request, session, redirect, Flask, flash
from flask_login import login_user, current_user, LoginManager
from src.db_models import User, UserActivity, UserHabit, db
from src.db_manager import DBManager
from src.utils import AlchemyEncoder

# Flask App init
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SECRET_KEY'] = uuid.uuid4().hex
db.init_app(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)

db.create_all()
db_manager = DBManager(db.session)


@login_manager.user_loader
def load_user(username):
    """Retrive current user."""
    return User.query.get(username)


@app.route('/api/habits', methods=['GET'])
def get_habits():
    """Get habits for a user."""
    result = db_manager.get_habits(current_user)
    if not result.is_ok():
        return "cannot get habits", 400

    # package up habit names and streaks for return
    resp_data = {'habits': [], 'streaks': []}
    habits = result.unwrap()
    for habit in habits:
        resp_data['habits'].append(habit.habitname)
        resp_data['streaks'].append(
            db_manager.get_activity_streak(habit).unwrap())

    return json.dumps(resp_data), 200


@app.route('/api/habits', methods=['POST'])
def add_habit():
    """Add a habit."""
    userhabit = UserHabit(
        username=current_user.username,
        habitname=request.form['habitname']
    )
    result = db_manager.add_habit(userhabit)
    if result.is_ok():
        return "add habit successful", 201
    else:
        return "cannot add habit ", 404


@app.route('/api/habits/<habitname>', methods=['DELETE'])
def delete_habit(habitname):
    """Delete a habit.

    :param habitname str: name of habit to delete
    """
    userhabit = UserHabit(
        username=current_user.username,
        habitname=habitname
    )
    result = db_manager.delete_habit(userhabit)
    if result.is_ok():
        return "delete habit successful", 200
    else:
        return "cannot delete habit ", 404


@app.route('/api/habits/logs', methods=['GET'])
def get_activites():
    """Get activities for a user."""
    userhabit = UserHabit(
        username=current_user.username,
        habitname=request.form.get('habitname')
    )
    trailing_days = request.form.get('trailing_days') or 100
    result = db_manager.get_activities(
        userhabit, trailing_days=int(trailing_days))
    if result.is_ok():
        return json.dumps(result.unwrap(), cls=AlchemyEncoder), 200
    else:
        return "cannot get habit logs", 404


@app.route('/api/habits/logs', methods=['POST'])
def add_activites():
    """Add activities for a habit."""
    timestamp = date.fromisoformat(
        request.form['day_to_log']
    )
    activity = UserActivity(
        username=current_user.username,
        habitname=request.form['habitname'],
        timestamp=timestamp
    )
    result = db_manager.add_activity(activity)
    if result.is_ok():
        return "add activity successful", 200
    else:
        return "cannot add activity", 404


@app.route('/api/login', methods=['POST'])
def login():
    """Login a user."""
    data = request.form
    username = data.get('username')
    password = data.get('password')
    user = db_manager._session.query(User).filter_by(username=username).first()
    if not user or not user.check_password(password):
        flash('Login failed')
        return render_template('login.html')
    session['username'] = username
    login_user(user)

    return redirect('/habits')


@app.route('/api/users', methods=['POST'])
def register():
    """Register a user."""
    data = request.form
    username = data.get('username')
    password = data.get('password')
    user = User(username=username, hashed_password=password)
    user.set_password(password)
    result = db_manager.add_user(user)
    if result.is_ok():
        return render_template('login.html', name=user.username)
    else:
        flash('Registration failed')
        return render_template('login.html')


@app.route('/', methods=['GET'])
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
