"""Habit Tracker Web Server entry point."""
import json
from datetime import date
import os
import uuid
from flask import render_template, request, redirect, Flask, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import LoginManager
from src.db_models import User, UserActivity, UserHabit, db
from src.db_manager import DBManager
from src.utils import AlchemyEncoder

# Flask App init
app = Flask(__name__)
app.config['SECRET_KEY'] = uuid.uuid4().hex
app.app_context().push()

# login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"
login_manager.login_message = u"you must login to access this page"
login_manager.login_message_category = "message"


# db
db.init_app(app)
db.create_all()
# TODO using a local db.session might be a better idea
db_manager = DBManager(db.session)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')


@login_manager.unauthorized_handler
def unauthorized_callback():
    """Redirect to login page if not logged in."""
    return redirect('/login')


@login_manager.user_loader
def load_user(username):
    """Retrive current user."""
    user = User.query.filter_by(username=username).first()
    return user


@app.route('/api/habits', methods=['GET'])
@login_required
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
@login_required
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


@app.route('/api/habits', methods=['DELETE'])
def delete_habit():
    """Delete a habit.

    :param habitname str: name of habit to delete
    """
    userhabit = UserHabit(
        username=current_user.username,
        habitname=request.form['habitname']
    )
    result = db_manager.delete_habit(userhabit)
    if result.is_ok():
        return "delete habit successful", 200
    else:
        return "cannot delete habit ", 404


@app.route('/api/habits/all_logs', methods=['GET'])
def get_all_activites():
    """Get all activities for a user."""
    username = current_user.username
    result = db_manager.get_all_activities(username)
    if result.is_ok():
        return result.unwrap()
    else:
        return "Cannot get habit logs", 404


@app.route('/api/habits/logs', methods=['GET'])
@login_required
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
@login_required
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
        return render_template('login.html'), 404
    login_user(user)

    return redirect('/habits')


@app.route('/api/users', methods=['POST'])
def register():
    """Register a user."""
    data = request.form
    # TODO we might need also to check if data has username or password
    username = data.get('username')
    password = data.get('password')

    if len(password) < 6:
        flash('Registration failed: Password too short. Must be 6 characters')
        return render_template('login.html'), 404

    user = User(username=username, hashed_password=password)
    user.set_password(password)
    result = db_manager.add_user(user)

    if result.is_ok():
        return render_template('login.html', name=user.username)
    else:
        flash('Registration failed: ' + result.err())
        return render_template('login.html'), 404


@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def render_login():
    """Render login page."""
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logout a user."""
    logout_user()
    return redirect('/')


@app.route('/test/register/<username>/<password>')
def test_register(username, password):
    """Route for test register."""
    user = User(username=username, hashed_password=int(password))
    scoped_session = db.create_scoped_session()
    res = db_manager.DBManager(scoped_session).add_user(user)

    if res.is_ok():
        return "you are registered {}".format(user.username), 200
    return "{}".format(res), 400


@app.route('/test/login/<username>/<password>')
def test_login(username, password):
    """Route for test login."""
    user = User.query.filter_by(username=username).first()

    # user exist and password matched
    if not user or not user.hashed_password == password:
        return "User does not exist or password not matched", 400
    login_user(user)
    return "Welcom back {}".format(user.username), 200


@app.route('/test/current_user')
def cur_user():
    """Test api for current_user."""
    return "{}".format(current_user.username)


@app.route('/habits', methods=['GET'])
@login_required
def render_habits():
    """Render habits page."""
    return render_template('habits.html')


@app.route('/progress', methods=['GET'])
@login_required
def render_progress():
    """Render progress page."""
    return render_template('progress.html')


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
