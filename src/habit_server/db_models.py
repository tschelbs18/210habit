from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from habit_server.app import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    password = Column(String)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class UserHabit(db.Model):
    __tablename__ = "user_habits"
    username = Column(String, primary_key=True)
    habitname = Column(String, primary_key=True)
    habit_freq = Column(Integer)  # are we still using this?


class UserActivity(db.Model):
    __tablename__ = "user_activities"
    username = Column(String, primary_key=True)
    habitname = Column(String, primary_key=True)
    timestamp = Column(DateTime)
