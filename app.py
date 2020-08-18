from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pymongo
from dotenv import load_dotenv
from bson.objectid import ObjectId
from bson.json_util import dumps
import json
import datetime
import module_services

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
    all_categories = module_services.service_category_get(db)
    return render_template('categories.html', categories=all_categories)

@app.route('/api/categories')
def api_categories():
    all_categories = module_services.service_category_get(db)
    return {
        'categories': json.loads(dumps(all_categories))
    }

@app.route('/categories/create', methods=['GET','POST'])
def create_category():
    if request.method == 'GET':
        return render_template('create-category.html')
    elif request.method == 'POST':
        module_services.service_category_create(db, request.form)
        return redirect(url_for('categories'))

# App start point
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
