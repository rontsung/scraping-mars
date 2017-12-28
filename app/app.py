from flask import Flask, jsonify, render_template, request, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pandas as pd

# Flask setup
app = Flask(__name__)

mongo = PyMongo(app)

# Home route
@app.route("/")
def home():
    df = pd.read_csv('df.csv')
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


# Fomr Route that will post the data on submissions
@app.route("/scrape")
def send():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    print("about to redirect")
    return redirect("http://localhost:5000/", code=302)

if __name__ == '__main__':
    app.run(debug=False)
