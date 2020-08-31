from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from bson.objectid import ObjectId
from bson.json_util import dumps
from passlib.hash import pbkdf2_sha256
import flask_login
import os
import pymongo
import json
import datetime
import m_services

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
db = client['pc_forum']

class User(flask_login.UserMixin):
    pass

# Initialise flask-login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(email):
    user = db.users.find_one({
        'email': email
    })

    # Check if user exists based on email
    if user:
        # Create User object
        user_object = User()
        user_object._id = user['_id']
        user_object.username = user['username']
        user_object.email = user['email']
         # Return User object
        return user_object
    else:
        # If email does not exist in database, report an error
        return None

# Home
@app.route('/')
def home():
    # print(flask_login.current_user.is_authenticated)
    return redirect(url_for('threads'))
    # return render_template('index.html')

# Users
@app.route('/users')
def users():
    all_users = m_services.users_get_all(db)
    return render_template('users/all-users.html', users=all_users)

@app.route('/users/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login-user.html')
    elif request.method == 'POST':
        user = db.users.find_one({
            'email': request.form.get('email')
        })

        # If user exists, check if password matches
        if user and pbkdf2_sha256.verify(
            request.form.get('password'), user['password']):
            # If password matches, authorise user
            user_object = User()
            user_object.id = user['email']
            flask_login.login_user(user_object)

            # Redirect to a page that says login is successful
            # flash("Login successful", "success")
            return redirect(url_for('threads'))

        # If login fails, return back to the login page
        else:
            # flash("Wrong email or password", "danger")
            return redirect(url_for('login'))

@app.route('/users/logout')
def logout():
    flask_login.logout_user()
    # flash('Logged out', 'success')
    return redirect(url_for('login'))

@app.route('/users/signup', methods=['GET','POST'])
def create_user():
    if request.method == 'GET':
        return render_template('users/create-user.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        m_services.users_create(db, request.form)
        user_object = User()
        user_object.id = email
        flask_login.login_user(user_object)
        return redirect(url_for('users'))

@app.route('/users/<user_id>/update', methods=['GET','POST'])
def update_user(user_id):
    if request.method == 'GET':
        previous_values = m_services.users_get_one(db, user_id)
        # print(previous_values)
        return render_template(
            'users/update-user.html', previous_values=previous_values)
    elif request.method == 'POST':
        m_services.users_update(db, request.form, user_id)
        # ADD flash message
        return redirect(url_for('update_user', user_id=user_id))

@app.route('/users/<user_id>/delete', methods=['GET','POST'])
def delete_user(user_id):
    if request.method == 'GET':
        previous_values = m_services.users_get_one(db, user_id)
        return render_template('users/delete-user.html', previous_values=previous_values)
    elif request.method == 'POST':
        m_services.users_delete(db, user_id)
        return redirect(url_for('threads'))

@app.route('/users/<user_id>/threads', methods=['GET','POST'])
def user_threads(user_id):
    if request.method == 'GET':
        search_criteria = {}
        search_criteria['user.user_id'] = ObjectId(user_id)
        threads_by_user = db.threads.find(search_criteria)
        num_of_threads = threads_by_user.count()
        all_categories = m_services.categories_get_all(db)
        return render_template(
            'users/user-threads.html', threads=threads_by_user,
            num_of_threads=num_of_threads, categories=all_categories)
    # POST not used, action of form points to create_thread() route

# Categories
@app.route('/categories')
def categories():
    all_categories = m_services.categories_get_all(db)
    return render_template(
        'categories/all-categories.html', categories=all_categories)

@app.route('/api/categories')
def api_categories():
    all_categories = m_services.categories_get_all(db)
    return {
        'categories': json.loads(dumps(all_categories))
    }

@app.route('/categories/create-0', methods=['GET','POST'])
def create_category_0():
    if request.method == 'GET':
        return render_template('categories/create-category-0.html')
    elif request.method == 'POST':
        m_services.categories_create_0(db, request.form)
        return redirect(url_for('categories'))

@app.route('/categories/<parent_id>/create-1', methods=['GET','POST'])
def create_category_1(parent_id):
    if request.method == 'GET':
        return render_template('categories/create-category-1.html')
    elif request.method == 'POST':
        m_services.categories_create_1(db, request.form, parent_id)
        return redirect(url_for('categories'))

@app.route('/categories/<category_id>/update-0', methods=['GET','POST'])
def update_category_0(category_id):
    if request.method == 'GET':
        return render_template('categories/update-category-0.html')
    elif request.method == 'POST':
        m_services.categories_update_0(db, request.form, category_id)
        return redirect(url_for('categories'))

@app.route('/categories/<category_id>/update-1', methods=['GET','POST'])
def update_category_1(category_id):
    if request.method == 'GET':
        return render_template('categories/update-category-1.html')
    elif request.method == 'POST':
        m_services.categories_update_1(db, request.form, category_id)
        return redirect(url_for('categories'))

@app.route('/categories/<category_id>/delete-0', methods=['GET','POST'])
def delete_category_0(category_id):
    if request.method == 'GET':
        return render_template('categories/delete-category-0.html')
    elif request.method == 'POST':
        m_services.categories_delete_0(db, category_id)
        return redirect(url_for('categories'))

@app.route('/categories/<category_id>/delete-1', methods=['GET','POST'])
def delete_category_1(category_id):
    if request.method == 'GET':
        return render_template('categories/delete-category-1.html')
    elif request.method == 'POST':
        m_services.categories_delete_1(db, category_id)
        return redirect(url_for('categories'))

@app.route('/api/sub-categories/<parent_id>')
def get_sub_categories(parent_id):
    sub_categories = m_services.sub_categories_get(db, parent_id)
    return {
        'results': json.loads(dumps(sub_categories))
    }

# Forum threads
@app.route('/threads')
def threads():
    all_categories = m_services.categories_get_all(db)
    all_threads = m_services.threads_search(db, request.args)
    previous_values = request.args
    return render_template(
        'threads/all-threads.html', categories=all_categories,
        threads=all_threads, previous_values=previous_values)

@app.route('/threads/<thread_id>', methods=['GET','POST'])
def display_thread(thread_id):
    if request.method == 'GET':
        thread = m_services.threads_get_one(db, thread_id)
        return render_template('threads/single-thread.html', thread=thread)
    elif request.method == 'POST':
        if flask_login.current_user.is_authenticated:
            m_services.comments_create(db, request.form, thread_id)
            return redirect(url_for('display_thread', thread_id=thread_id))
        else:
            # ADD flash message
            return redirect(url_for('display_thread', thread_id=thread_id))

@app.route('/threads/create', methods=['GET','POST'])
@flask_login.login_required
def create_thread():
    if request.method == 'GET':
        all_categories = m_services.categories_get_all(db)
        return render_template(
            'threads/create-thread.html', categories=all_categories)
    elif request.method == 'POST':
        # m_services.threads_create(db, request.form)
        new_thread_id = m_services.threads_create(db,request.form).inserted_id
        return redirect(url_for('display_thread', thread_id=new_thread_id))

@app.route('/threads/<thread_id>/update', methods=['GET','POST'])
@flask_login.login_required
def update_thread(thread_id):
    if request.method == 'GET':
        all_categories = m_services.categories_get_all(db)
        previous_values = m_services.threads_get_one(db, thread_id)
        # print(previous_values)
        return render_template(
            'threads/update-thread.html', categories=all_categories,
            previous_values=previous_values)
    elif request.method == 'POST':
        m_services.threads_update(db, request.form, thread_id)
        return redirect(url_for('display_thread', thread_id=thread_id))

@app.route('/threads/<thread_id>/delete', methods=['GET','POST'])
def delete_thread(thread_id):
    if request.method == 'GET':
        thread = m_services.threads_get_one(db, thread_id)
        return render_template('threads/delete-thread.html', thread=thread)
    elif request.method == 'POST':
        m_services.threads_delete(db, thread_id)
        return redirect(url_for('threads'))

# @app.route('/threads/<thread_id>/comments/create', methods=['GET','POST'])
# @flask_login.login_required
# def create_comment(thread_id):
#     if request.method == 'GET':
#         return render_template('threads/comments/create-comment.html')
#     elif request.method == 'POST':
#         m_services.comments_create(db, request.form, thread_id)
#         return redirect(url_for('display_thread', thread_id=thread_id))

@app.route('/threads/<thread_id>/comments/<comment_id>/update', methods=['GET','POST'])
@flask_login.login_required
def update_comment(thread_id, comment_id):
    if request.method == 'GET':
        return render_template('threads/comments/update-comment.html')
    elif request.method == 'POST':
        m_services.comments_update(db, request.form, thread_id, comment_id)
        return redirect(url_for('display_thread', thread_id=thread_id))

@app.route('/threads/<thread_id>/comments/<comment_id>/delete', methods=['GET','POST'])
def delete_comment(thread_id, comment_id):
    if request.method == 'GET':
        comment = m_services.comments_get_one(db, comment_id)
        return render_template(
            'threads/comments/delete-comment.html', comment=comment)
    elif request.method == 'POST':
        m_services.comments_delete(db, comment_id)
        return redirect(url_for('display_thread', thread_id=thread_id))

@app.route('/api/threads/<thread_id>/comments/count')
def count_comments(thread_id):
    comments = m_services.comments_count(db, thread_id)
    return {
        'comments': json.loads(dumps(len(comments)))
    }

# Voting
@app.route('/api/threads/<thread_id>/vote-up', methods=['PATCH'])
def vote_up(thread_id):
    if flask_login.current_user.is_authenticated:
        m_services.vote_up(db, thread_id)
        return { "status": 200 }
    else:
        return "0"

@app.route('/api/threads/<thread_id>/vote-down', methods=['PATCH'])
def vote_down(thread_id):
    if flask_login.current_user.is_authenticated:
        m_services.vote_down(db, thread_id)
        return { "status": 200 }
    else:
        return "0"

@app.route('/api/threads/<thread_id>/vote-up-check')
def vote_up_check(thread_id):
    if flask_login.current_user.is_authenticated:
        return { "response": m_services.vote_up_check(db, thread_id) }
    else:
        return "0"

@app.route('/api/threads/<thread_id>/vote-down-check')
def vote_down_check(thread_id):
    if flask_login.current_user.is_authenticated:
        return { "response": m_services.vote_down_check(db, thread_id) }
    else:
        return "0"

@app.route('/api/threads/<thread_id>/vote-up-remove', methods=['PATCH'])
def vote_up_check_remove(thread_id):
    if flask_login.current_user.is_authenticated:
        m_services.vote_up_remove(db, thread_id)
        return { "status": 200 }
    else:
        return { "response": False }

@app.route('/api/threads/<thread_id>/vote-down-remove', methods=['PATCH'])
def vote_down_check_remove(thread_id):
    if flask_login.current_user.is_authenticated:
        m_services.vote_down_remove(db, thread_id)
        return { "status": 200 }
    else:
        return { "response": False }

@app.route('/api/threads/<thread_id>/vote-count/<up_or_down>')
def test(thread_id, up_or_down):
    votes = m_services.vote_count(db, thread_id, up_or_down)
    return {
        f'number_of_{up_or_down}_votes': json.loads(dumps(len(votes)))
    }


# App start point
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
