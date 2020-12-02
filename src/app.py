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

# @app.route('/test')
# def test():
#     """Adding Docstring to satisfy github actions."""
#     return 'Hello, World!!!'

@app.route('/team/<member>')  # i.e /team/daniel
def team_page(member):
    """Route for team members.

    Each member is associated with their own route.
    """
    if member == "daniel":
        return "Daniel's page!"
    else:
        return "Unknown team member: {}".format(member)

@app.route('/register', methods = ['POST'])
def register():
    """Route for register"""
    data = request.get_json()
    username = data.get('username', None)
    hashed_password = data.get('password', None)

    # validation on argument
    if not username or not hashed_password:
        return "Invalid argument", 400

    user = User(username=username, hashed_password = hashed_password)
    scoped_session = db.create_scoped_session()
    res = db_manager.DBManager(scoped_session).add_user(user)

    if res == Result.Ok:
        return "you are registered {}".format(user.username), 200
    return "{}".format(res), 400

@app.route('/login/', methods = ['POST'])
def login():
    """Route for login"""
    data = request.get_json()
    username = data.get('username', None)
    hashed_password = data.get('password', None)
    
    # validation on argument
    if not username or not hashed_password:
        return "Invalid argument", 400
    
    user = User.query.filter_by(username=username).first()
    
    # user exist and password matched
    if not user or not user.check_password(hashed_password):
        return "User does not exist or password not matched", 400
    
    login_user(user)
    return flask.render_template('login.html', name=user.username)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for('/'))

@app.route('/test_register/<username>/<password>')
def test_register(username, password):
    """Route for test register"""
    user = User(username=username, hashed_password = int(password))
    scoped_session = db.create_scoped_session()
    res = db_manager.DBManager(scoped_session).add_user(user)

    if res == Result.Ok:
        return "you are registered {}".format(user.username), 200
    return "{}".format(res), 400

@app.route('/test_login/<username>/<password>')
def test_login(username, password):
    """Route for test login"""
    user = User.query.filter_by(username=username).first()
    
    # user exist and password matched
    if not user or not user.hashed_password == password:
        return "User does not exist or password not matched", 400
    login_user(user)
    return "Welcom back {}".format(user.username), 200

@app.route('/current_user')
def cur_user():
    return "{}".format(str(current_user))

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
