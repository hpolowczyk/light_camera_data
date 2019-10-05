from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
import json

import generalFunctions


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongodbCon = "mongodb+srv://generaluser:generaluser123@project2-ha8my.mongodb.net/movie_db?retryWrites=true&w=majority"
app.config["MONGO_URI"] = mongodbCon
# app.config["MONGO_URI"] = "mongodb://localhost:27017/dbscrape_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/internatianalGross")
def index():
    listings = mongo.db.international_gross.find_one()
    result = json.loads(json_util.dumps(listings))
    return jsonify(result)


@app.route("/map")
def test():
    listings = mongo.db.merged.find_one()
    return render_template("pages/test.html", listings=listings)


@app.route("/collectionBoth")
def collectionBoth():
    pass
    # listings = mongo.db.listings
    # listings.remove()
    # listings_data = scrape_mars.scrape()
    # listings.insert(listings_data)
    # return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
