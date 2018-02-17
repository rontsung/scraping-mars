from flask import Flask, jsonify, render_template, request, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
# from flask_pymongo import PyMongo
import scrape_mars
import pandas as pd

# Flask setup
app = Flask(__name__)

# mongo = PyMongo(app)
client = MongoClient("mongodb://mars:rams@ds243345.mlab.com:43345/heroku_m5kl8br7")
db =  client.heroku_m5kl8br7
mars = db.mars

# Home route
@app.route("/")
def home():
    # mars = mongo.db.mars.find_one()
    mars = mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def send():
    mars = db.mars
    # mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    print("about to redirect")
    # return redirect("http://localhost:5000/", code=302)
    return redirect("https://mongo-.herokuapp.com/", code=302)

if __name__ == '__main__':
    app.run(debug=False)
