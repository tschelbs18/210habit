"""Habit Tracker Web Server entry point."""
from flask_login import login_user, logout_user, login_required, current_user


from flask import Flask
from flask_login import LoginManager
from User import User
import os
import sys
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SECRET_KEY'] = u'210habit'
# login
login_manager = LoginManager(app)
login_manager.init_app(app)
# login_manager.login_view = "/"
login_manager.login_message = 'You must login to access this page'

users = [User(1)]

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def hello_world():
   """Adding Docstring to satisfy github actions."""
   return 'Hello, World!!!'

@app.route('/team/<member>')  # i.e /team/daniel
def team_page(member):
    """Route for team members, each member is associated with their own route."""
    if member == "daniel":
        return "Daniel's page!"
    else:
        return "Unknown team member: {}".format(member)

@app.route('/login/<user_name>')
def login(user_name):
    global users
    print(users, file=sys.stderr)
    for u in users:
        if u.user_id == int(user_name):
            login_user(u)
            return "You are now logged as %s" % str(u)
    return "Unregistered user"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    print(type(current_user), file=sys.stderr)
    return "You are now logged out as %s" % str(current_user)

@app.route('/current_user')
@login_required
def cur_user():
    return str(current_user)

@app.route('/register/<user_name>')
def register(user_name):
    global users
    user = User(int(user_name))
    users.append(user)
    return "%s has registered" % str(user)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)