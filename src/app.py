"""Habit Tracker Web Server entry point."""
from flask import Flask
import flask
import sys
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from habit_server import app, db
from habit_server.db_models import User
from habit_server import db_manager
from result.result import Result

@app.route('/')
def hello_world():
    """Adding Docstring to satisfy github actions."""
    return 'Hello, World!!!'


@app.route('/team/<member>')  # i.e /team/daniel
def team_page(member):
    """Route for team members.

    Each member is associated with their own route.
    """
    if member == "daniel":
        return "Daniel's page!"
    else:
        return "Unknown team member: {}".format(member)

@app.route('/register', methods = ['POST', 'GET'])
def register():
    """Route for register"""
    data = request.get_json()
    scoped_session = db.create_scoped_session()
    user = User(username = data.get('username', None), hashed_password = data.get('password', None))
    # TODO how to user db_manager
    # TODO db_manager might need to call 'commit' method of _session
    res = db_manager.DBManager(scoped_session).add_user(user)
    if res == Result.Ok:
        return "you are registered"
    else:
        return "{}".format(res)

@app.route('/login', methods = ['POST'])
def login():
    """Route for login"""
    data = request.get_json()
    username = data.get('username', None)
    hashed_password = data.get('password', None)
    user = User.query.filter_by(username=username)
    
    if not user or not user.check_password(hashed_password):
        return "logint failed"

    return flask.render_template('login.html', name=user.username)

@app.route('/logout', methods = ['POST'])
@login_required
def logout():
    logout_user()
    return "you are logged out"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
