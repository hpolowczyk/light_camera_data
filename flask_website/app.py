from flask import Flask, render_template,jsonify
import pymongo
from flask_pymongo import PyMongo

app = Flask(__name__)

# setup mongo connection
mongo = PyMongo(app, uri="mongodb+srv://generaluser:generaluser123@project2-ha8my.mongodb.net/movie_db?retryWrites=true&w=majority")

@app.route('/json')
def jsonified():
    docs = []
    for doc in mongo.db.movie_detail.find():
        doc.pop('_id') 
        docs.append(doc)
    return jsonify(docs)

@app.route('/movie_ring')
def movie_ring():
    # write a statement that finds all the items in the db and sets it to a variable
    inventory = list(mongo.db.movie_detail.find())

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("movie_ring.html", inventory=inventory)

@app.route('/')
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    inventory = list(mongo.db.movie_detail.find())

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("about.html", inventory=inventory)


if __name__ == "__main__":
    app.run(debug=True)
