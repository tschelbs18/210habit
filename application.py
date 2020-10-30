"""Habit Tracker Web Server entry point."""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    ''' Adding Docstring to satisfy github actions '''
   return 'Hello, World!!'

if __name__ == '__main__':
   app.run()
