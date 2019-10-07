from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
import json

import generalFunctions


app = Flask(__name__)

# # Use flask_pymongo to set up mongo connection
# mongodbCon = "mongodb+srv://generaluser:generaluser123@project2-ha8my.mongodb.net/movie_db?retryWrites=true&w=majority"
# app.config["MONGO_URI"] = mongodbCon
# # app.config["MONGO_URI"] = "mongodb://localhost:27017/dbscrape_app"
# mongo = PyMongo(app)

mongo = PyMongo(
    app, uri="mongodb+srv://generaluser:generaluser123@project2-ha8my.mongodb.net/movie_db?retryWrites=true&w=majority")


# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/internatianalGross")
def internatianalGross():
    listings = mongo.db.international_gross.find_one()
    result = json.loads(json_util.dumps(listings))
    return jsonify(result)


@app.route("/")
def init():
    return render_template("index.html")


@app.route("/filterLessEq_IG_Rank/<value>")
def filterRank(value):
    value = int(value)
    docs = []
    for doc in mongo.db.international_gross.find({'rank': {'$lte': value}}):
        doc.pop('_id')
        docs.append(doc)
    return jsonify(docs)


@app.route("/filterLessEq_IG_Dom/<value>")
def filterDomesticGross(value):
    value = int(value)
    docs = []
    for doc in mongo.db.international_gross.find({'domestic_total_gross': {'$lte': value}}):
        doc.pop('_id')
        docs.append(doc)
    return jsonify(docs)


@app.route("/filterLessEq_IG_Int/<value>")
def filterForeingGross(value):
    value = int(value)
    docs = []
    for doc in mongo.db.international_gross.find({'foreign_total_gross': {'$lte': value}}):
        doc.pop('_id')
        docs.append(doc)
    return jsonify(docs)


if __name__ == "__main__":
    app.run(debug=True)
