import markdown
import os
import shelve
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    return "Hello World"

habit_put_args = reqparse.RequestParser()
habit_put_args.add_argument("habit_name", type=str, help="habit name", required=True)
habits = {}

class Habit(Resource):

    def put(self, habit_id):
        args = habit_put_args.parse_args()
        habits[habit_id] = args
        return habits[habit_id], 201

    def delete(self, habit_id):
        del habits[habit_id]
        return '',204

api.add_resource(Habit,"/habits/<int:habit_id>")

if __name__ == "__main__":
    app.run()
