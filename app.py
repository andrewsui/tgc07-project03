from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pymongo
from dotenv import load_dotenv
from bson.objectid import ObjectId
import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = "pc_forum"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

@app.route('/')
def home():
    return "Test home page"

@app.route('/categories')
def categories():
    all_categories = db.categories.find()
    return render_template('categories.html', categories=all_categories)



# App start point
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
