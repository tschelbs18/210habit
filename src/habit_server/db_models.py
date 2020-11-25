"""Databse ORM models."""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from habit_server.app import db


class User(db.Model, UserMixin):
    """Database ORM model representing a User."""

    __tablename__ = "users"
    username = db.Column(db.String, primary_key=True)
    hashed_password = db.Column(db.String)

    def set_password(self, password):
        """Set hashed password for a user.

        :param password str: password to hash and set.
        """
        self.hashed_password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, hashed_password):
        """Check that hashed password matches expected hashed password.

        :param hased_password str: hashed password to check
        """
        return check_password_hash(self.hashed_password, hashed_password)


class UserHabit(db.Model):
    """Database ORM model representing a single user habit."""

    __tablename__ = "user_habits"
    username = db.Column(db.String, primary_key=True)
    habitname = db.Column(db.String, primary_key=True)


class UserActivity(db.Model):
    """Databse ORM model representing a single activity."""

    __tablename__ = "user_activities"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    habitname = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
