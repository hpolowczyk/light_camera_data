from flask import Flask, render_template
import pymongo
from flask_pymongo import PyMongo

app = Flask(__name__)

# setup mongo connection
mongo = PyMongo(app, uri="mongodb+srv://generaluser:generaluser123@project2-ha8my.mongodb.net/db?retryWrites=true&w=majority")


@app.route("/")

def index():
    # write a statement that finds all the items in the db and sets it to a variable
    inventory = mongo.db.trial.find()
    print(inventory)

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", inventory=inventory)


if __name__ == "__main__":
    app.run(debug=True)
