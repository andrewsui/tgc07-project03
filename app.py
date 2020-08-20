from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from bson.objectid import ObjectId
from bson.json_util import dumps
from passlib.hash import pbkdf2_sha256
import os
import pymongo
import json
import datetime
import module_services

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
db = client['pc_forum']

# Home
@app.route('/')
def home():
    return "Test home page"

# Users
@app.route('/users')
def users():
    all_users = module_services.service_users_get_all(db)
    return render_template('users/all-users.html', users=all_users)

@app.route('/users/create', methods=['GET','POST'])
def create_user():
    if request.method == 'GET':
        return render_template('users/create-user.html')
    elif request.method == 'POST':
        module_services.service_users_create(db, request.form)
        return redirect(url_for('users'))

@app.route('/users/update/<user_id>', methods=['GET','POST'])
def update_user(user_id):
    if request.method == 'GET':
        previous_values = module_services.service_users_get_one(db, user_id)
        # print(previous_values)
        return render_template('users/update-user.html', previous_values=previous_values)
    elif request.method == 'POST':
        module_services.service_users_update(db, request.form, user_id)
        return redirect(url_for('users'))

@app.route('/users/delete/<user_id>', methods=['GET','POST'])
def delete_user(user_id):
    if request.method == 'GET':
        return render_template('users/delete-user.html')
    elif request.method == 'POST':
        module_services.service_users_delete(db, user_id)
        return redirect(url_for('users'))

# Categories
@app.route('/categories')
def categories():
    all_categories = module_services.service_categories_get_all(db)
    return render_template('categories/all-categories.html', categories=all_categories)

@app.route('/api/categories')
def api_categories():
    all_categories = module_services.service_categories_get_all(db)
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

# Forum threads
@app.route('/threads')
def threads():
    all_threads = module_services.service_threads_get_all(db)
    return render_template('threads/all-threads.html', threads=all_threads)

@app.route('/threads/create', methods=['GET','POST'])
def create_thread():
    if request.method == 'GET':
        return render_template('threads/create-thread.html')
    elif request.method == 'POST':
        module_services.service_threads_create(db, request.form)
        return redirect(url_for('threads'))

@app.route('/threads/update/<thread_id>', methods=['GET','POST'])
def update_thread(thread_id):
    if request.method == 'GET':
        previous_values = module_services.service_threads_get_one(db, thread_id)
        print(previous_values)
        return render_template('threads/update-thread.html', previous_values=previous_values)
    elif request.method == 'POST':
        module_services.service_threads_update(db, request.form, thread_id)
        return redirect(url_for('threads'))

@app.route('/threads/delete/<thread_id>', methods=['GET','POST'])
def delete_thread(thread_id):
    if request.method == 'GET':
        return render_template('threads/delete-thread.html')
    elif request.method == 'POST':
        module_services.service_threads_delete(db, thread_id)
        return redirect(url_for('threads'))

# App start point
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
