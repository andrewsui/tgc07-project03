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

client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
db = client['pc_forum']

@app.route('/')
def home():
    return "Test home page"

@app.route('/users')
def users():
    all_users = module_services.service_users_get(db)
    return render_template('users/users.html', users=all_users)

@app.route('/users/create', methods=['GET','POST'])
def create_user():
    if request.method == 'GET':
        return render_template('users/create-user.html')
    elif request.method == 'POST':
        module_services.service_users_create(db, request.form)
        return redirect(url_for('users'))


@app.route('/categories')
def categories():
    all_categories = module_services.service_categories_get(db)
    return render_template('categories/categories.html', categories=all_categories)

@app.route('/api/categories')
def api_categories():
    all_categories = module_services.service_categories_get(db)
    return {
        'categories': json.loads(dumps(all_categories))
    }

@app.route('/categories/create-0', methods=['GET','POST'])
def create_category_0():
    if request.method == 'GET':
        return render_template('categories/create-category-0.html')
    elif request.method == 'POST':
        module_services.service_categories_create_0(db, request.form)
        return redirect(url_for('categories'))

@app.route('/categories/create-1/<parent_id>', methods=['GET','POST'])
def create_category_1(parent_id):
    if request.method == 'GET':
        return render_template('categories/create-category-1.html')
    elif request.method == 'POST':
        module_services.service_categories_create_1(db, request.form, parent_id)
        return redirect(url_for('categories'))

@app.route('/categories/update-0/<category_id>', methods=['GET','POST'])
def update_category_0(category_id):
    if request.method == 'GET':
        return render_template('categories/update-category-0.html')
    elif request.method == 'POST':
        module_services.service_categories_update_0(db, request.form, category_id)
        return redirect(url_for('categories'))

@app.route('/categories/update-1/<category_id>', methods=['GET','POST'])
def update_category_1(category_id):
    if request.method == 'GET':
        return render_template('categories/update-category-1.html')
    elif request.method == 'POST':
        module_services.service_categories_update_1(db, request.form, category_id)
        return redirect(url_for('categories'))

@app.route('/categories/delete-0/<category_id>', methods=['GET','POST'])
def delete_category_0(category_id):
    if request.method == 'GET':
        return render_template('categories/delete-category-0.html')
    elif request.method == 'POST':
        module_services.service_categories_delete_0(db, category_id)
        return redirect(url_for('categories'))

@app.route('/categories/delete-1/<category_id>', methods=['GET','POST'])
def delete_category_1(category_id):
    if request.method == 'GET':
        return render_template('categories/delete-category-1.html')
    elif request.method == 'POST':
        module_services.service_categories_delete_1(db, category_id)
        return redirect(url_for('categories'))


# App start point
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
