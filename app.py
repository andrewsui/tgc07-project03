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
import math
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
        user_object.is_admin = user['is_admin']
        user_object.username = user['username']
        user_object.email = user['email']
         # Return User object
        return user_object
    else:
        return None

# Home ######################################################### Add home page
@app.route('/')
def home():
    return redirect(url_for('threads'))
    # return render_template('index.html')

# Users
@app.route('/users/login', methods=['GET','POST'])
def login():
    errors = {}
    if request.method == 'GET':
        return render_template('users/login-user.html', errors=errors)
    elif request.method == 'POST':
        email = request.form.get('email')

        # If email not valid format, add error
        if not m_services.users_check_email(email):
            errors.update(invalid_email = "Please enter a valid email")

        # If password not valid, add error
        if not m_services.users_check_password(request.form.get('password')):
            errors.update(invalid_password = "Password must be a minimum of \
                eight characters, and have at least one letter and one \
                    number")

        # If email and/or password format invalid, show error messages
        if len(errors) > 0:
            return render_template('users/login-user.html', errors=errors)
        
        # If email and password formats are valid, check database
        else:
            user_db = db.users.find_one({ 'email': email })

            # If user exists, check if password matches
            if user_db and pbkdf2_sha256.verify(
                request.form.get('password'), user_db['password']):
                # If password matches, authorise user
                user_object = User()
                user_object.id = user_db['email']
                flask_login.login_user(user_object)

                # Redirect to a page and flash log in successful message
                flash("Log in successful", "success")
                return redirect(url_for('threads'))

            # If log in fails, return back to the log in page
            else:
                errors.update(invalid_email = "Either email or password was incorrect")
                errors.update(invalid_password = "Either email or password was incorrect")
                return render_template('users/login-user.html', errors=errors)

@app.route('/users/logout')
def logout():
    flask_login.logout_user()
    flash('Logged out', 'error')
    return redirect(url_for('login'))

@app.route('/users/signup', methods=['GET','POST'])
def create_user():
    errors = {}
    if request.method == 'GET':
        return render_template('users/create-user.html', errors=errors)
    elif request.method == 'POST':
        # Validate user input
        errors = m_services.users_validate_form(request.form)
        if len(errors) > 0:
            for key, value in request.form.items():
                errors[key] = value
            return render_template('users/create-user.html', errors=errors)
        
        else:
            m_services.users_create(db, request.form)
            user_object = User()
            user_object.id = request.form.get('email')
            if (flask_login.current_user.is_authenticated and
            flask_login.current_user.is_admin):
                # If admin user, redirect to all users template
                flash("Account created", "success")
                return redirect(url_for('users'))
            else:
                # If not admin user, log new user in
                # and redirect to all review threads template
                flask_login.login_user(user_object)
                flash("Sign up successful", "success")
                return redirect(url_for('threads'))

@app.route('/users/<user_id>/update', methods=['GET','POST'])
@flask_login.login_required
def update_user(user_id):
    errors = {}
    previous_values = m_services.users_get_one(db, user_id)
    if request.method == 'GET':
        if (str(flask_login.current_user._id)==user_id or
            flask_login.current_user.is_admin):
            return render_template(
                'users/update-user.html', previous_values=previous_values,
                errors=errors)
        else:
            flash("You do not have the required user privileges", "error")
            return redirect(url_for('threads'))
    elif request.method == 'POST':
        # Validate user input
        
        # If email not valid format, add error
        if not m_services.users_check_email(request.form.get('email')):
            errors.update(invalid_email = "Please enter a valid email")

        # If password not valid, add error
        if not m_services.users_check_password(request.form.get('password')):
            errors.update(invalid_password = "Password must be a minimum of \
                eight characters, and have at least one letter and one \
                    number")
        
        # If passwords are not same, add error
        if not m_services.users_check_password_same(
            request.form.get('password'), request.form.get('password_2')):
            errors.update(invalid_password_2 = "Passwords did not match")

        if len(errors) > 0:
            for key, value in request.form.items():
                errors[key] = value
            if request.form.get('marketing')==None:
                errors.update(marketing = "opt_out")
            return render_template(
                'users/update-user.html', previous_values=previous_values,
                errors=errors)
        else:
            # Update user details
            m_services.users_update(db, request.form, user_id)
            flash("Update account details successful", "success")
            return redirect(url_for('update_user', user_id=user_id))

@app.route('/users/<user_id>/delete', methods=['GET','POST'])
@flask_login.login_required
def delete_user(user_id):
    if request.method == 'GET':
        if (str(flask_login.current_user._id)==user_id or
            flask_login.current_user.is_admin):
            previous_values = m_services.users_get_one(db, user_id)
            return render_template(
                'users/delete-user.html', previous_values=previous_values)
        else:
            flash("You do not have the required user privileges", "error")
            return redirect(url_for('threads'))
    elif request.method == 'POST':
        m_services.users_delete(db, user_id)
        flash("Account deleted", "warning")
        if flask_login.current_user.is_admin:
            # If admin user, redirect to all users template
            return redirect(url_for('users'))
        else:
            # If not admin user, redirect to all review threads template
            return redirect(url_for('threads'))

@app.route('/users/<user_id>/threads', methods=['GET'])
def user_threads(user_id):
    if request.method == 'GET':
        errors = {}
        threads_by_user = m_services.users_threads_by_user(
            db, user_id, request.args)
        num_of_threads = threads_by_user.count()
        user_details = m_services.users_get_one(db, user_id)
        all_categories = m_services.categories_get_all(db)
        return render_template(
            'users/user-threads.html', user_id=user_id,
            threads=threads_by_user, num_of_threads=num_of_threads,
            categories=all_categories, errors=errors,
            user_details=user_details, previous_values = request.args)
    # POST not used, action of form points to create_thread() route

# Admin users
@app.route('/admin/users')
@flask_login.login_required
def users():
    if flask_login.current_user.is_admin:
        all_users = m_services.users_get_all(db)
        return render_template('admin-users/all-users.html', users=all_users)
    else:
        flash("You do not have the required user privileges", "error")
        return redirect(url_for('threads'))


@app.route('/admin/users/create', methods=['GET','POST'])
@flask_login.login_required
def admin_create_user():
    errors = {}
    if request.method == 'GET':
        if flask_login.current_user.is_admin:
            return render_template(
                'admin-users/admin-create-user.html', errors=errors)
        else:
            flash("You do not have the required user privileges", "error")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Validate user input
        errors = m_services.users_validate_form(request.form)

        if len(errors) > 0:
            return render_template(
                'admin-users/admin-create-user.html', errors=errors)
        
        else:
            m_services.users_create(db, request.form)
            user_object = User()
            user_object.id = request.form.get('email')
            flash("Sign up successful", "success")
            return redirect(url_for('users'))

@app.route('/admin/users/<user_id>/update', methods=['GET','POST'])
@flask_login.login_required
def admin_update_user(user_id):
    errors = {}
    previous_values = m_services.users_get_one(db, user_id)
    if request.method == 'GET':
        if flask_login.current_user.is_admin:
            return render_template(
                'admin-users/admin-update-user.html',
                previous_values=previous_values, errors=errors)
        else:
            flash("You do not have the required user privileges", "error")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Validate user input
        errors = m_services.users_validate_form(request.form)

        if len(errors) > 0:
            return render_template(
                'admin-users/admin-update-user.html',
                previous_values=previous_values, errors=errors)
        else:
            # Update user details
            m_services.admin_users_update(db, request.form, user_id)
            flash("Update account details successful", "success")
            return redirect(url_for('users'))

# Categories
@app.route('/categories', methods=['GET','POST'])
@flask_login.login_required
def categories():
    errors = {}
    all_categories = m_services.categories_get_all(db)
    if request.method == 'GET':
        if flask_login.current_user.is_admin:
            return render_template(
                'categories/all-categories.html', categories=all_categories,
                errors=errors)
        else:
            flash("You do not have the required user privileges", "error")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        if request.form.get('update_category'):
            if request.form.get('categories'):
                return redirect(url_for('update_category_0',
                category_id=request.form.get('categories')))
            else:
                errors.update(select_category="Please select a category")
        elif request.form.get('delete_category'):
            if request.form.get('categories'):
                return redirect(url_for('delete_category_0',
                category_id=request.form.get('categories')))
            else:
                errors.update(select_category="Please select a category")
        elif request.form.get('create_sub_category'):
            if request.form.get('categories'):
                return redirect(url_for('create_category_1',
                parent_id=request.form.get('categories')))
            else:
                errors.update(
                    select_category="Please select a parent category")
        elif request.form.get('update_sub_category'):
            if request.form.get('sub_categories'):
                return redirect(url_for('update_category_1',
                category_id=request.form.get('sub_categories')))
            else:
                errors.update(
                    select_sub_category="Please select a sub-category")
        elif request.form.get('delete_sub_category'):
            if request.form.get('sub_categories'):
                return redirect(url_for('delete_category_1',
                category_id=request.form.get('sub_categories')))
            else:
                errors.update(
                    select_sub_category="Please select a sub-category")
        if len(errors) > 0:
            return render_template(
                'categories/all-categories.html', categories=all_categories,
                errors=errors)
        else:
            return redirect(url_for('categories'))

@app.route('/api/categories')
def api_categories():
    all_categories = m_services.categories_get_all(db)
    return {
        'categories': json.loads(dumps(all_categories))
    }

@app.route('/categories/create-0', methods=['GET','POST'])
@flask_login.login_required
def create_category_0():
    errors = {}
    if request.method == 'GET':
        if flask_login.current_user.is_admin:
            return render_template('categories/create-category-0.html',
            errors=errors)
        else:
            flash("You do not have the required user privileges", "error")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        if len(request.form.get('category'))<3:
            errors.update(invalid_category="Please enter a valid category")
        if len(errors)>0:
            return render_template('categories/create-category-0.html',
            errors=errors)
        else:
            m_services.categories_create_0(db, request.form)
            return redirect(url_for('categories'))

@app.route('/categories/<parent_id>/create-1', methods=['GET','POST'])
@flask_login.login_required
def create_category_1(parent_id):
    errors = {}
    category = m_services.categories_get_one(db, parent_id)
    if request.method == 'GET':
        if flask_login.current_user.is_admin:
            return render_template('categories/create-category-1.html',
            category=category, errors=errors)
        else:
            flash("You do not have the required user privileges", "error")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        if len(request.form.get('sub_category'))<3:
            errors.update(
                invalid_sub_category = "Please enter a valid sub-category")
        if len(errors)>0:
            return render_template('categories/create-category-1.html',
            category=category, errors=errors)
        else:
            m_services.categories_create_1(db, request.form, parent_id)
            return redirect(url_for('categories'))

@app.route('/categories/<category_id>/update-0', methods=['GET','POST'])
@flask_login.login_required
def update_category_0(category_id):
    errors = {}
    previous_values = m_services.categories_get_one(db, category_id)
    if request.method == 'GET':
        if flask_login.current_user.is_admin:
            return render_template('categories/update-category-0.html',
            previous_values=previous_values, errors=errors)
        else:
            flash("You do not have the required user privileges", "error")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        if len(request.form.get('category'))<3:
            errors.update(invalid_category="Please enter a valid category")
        if len(errors)>0:
            return render_template('categories/update-category-0.html',
            previous_values=previous_values, errors=errors)
        else:
            m_services.categories_update_0(db, request.form, category_id)
            return redirect(url_for('categories'))

@app.route('/categories/<category_id>/update-1', methods=['GET','POST'])
@flask_login.login_required
def update_category_1(category_id):
    errors = {}
    previous_values = m_services.sub_categories_get_one(db, category_id)
    if request.method == 'GET':
        if flask_login.current_user.is_admin:
            return render_template('categories/update-category-1.html',
            previous_values=previous_values, errors=errors)
        else:
            flash("You do not have the required user privileges", "error")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        if len(request.form.get('sub_category'))<3:
            errors.update(
                invalid_sub_category="Please enter a valid sub_category")
        if len(errors)>0:
            return render_template('categories/update-category-1.html',
            previous_values=previous_values, errors=errors)
        else:
            m_services.categories_update_1(db, request.form, category_id)
            return redirect(url_for('categories'))

@app.route('/categories/<category_id>/delete-0', methods=['GET','POST'])
@flask_login.login_required
def delete_category_0(category_id):
    if request.method == 'GET':
        if flask_login.current_user.is_admin:
            previous_values = m_services.categories_get_one(db, category_id)
            return render_template('categories/delete-category-0.html',
            previous_values=previous_values)
        else:
            flash("You do not have the required user privileges", "error")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        m_services.categories_delete_0(db, category_id)
        return redirect(url_for('categories'))

@app.route('/categories/<category_id>/delete-1', methods=['GET','POST'])
@flask_login.login_required
def delete_category_1(category_id):
    if request.method == 'GET':
        if flask_login.current_user.is_admin:
            previous_values = m_services.sub_categories_get_one(
                db, category_id)
            return render_template('categories/delete-category-1.html',
            previous_values=previous_values)
        else:
            flash("You do not have the required user privileges", "error")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        m_services.categories_delete_1(db, category_id)
        return redirect(url_for('categories'))

@app.route('/api/categories/<category_id>/sub-categories')
def get_sub_categories(category_id):
    sub_categories = m_services.sub_categories_get(db, category_id)
    return {
        'results': json.loads(dumps(sub_categories))
    }

# Forum threads
@app.route('/threads')
def threads():
    all_categories = m_services.categories_get_all(db)
    previous_values = request.args

    results_per_page = 10
    number_of_results = m_services.threads_search(db, previous_values).count()
    number_of_pages = math.ceil(number_of_results/results_per_page)

    # Get current page number from args. If doesn't exist, set to 1
    page_number = int(previous_values.get('page') or 1)

    # Calculate how many results to skip depending current page number
    number_to_skip = (page_number-1) * results_per_page

    all_threads = m_services.threads_search(db, previous_values).skip(
        number_to_skip).limit(results_per_page)

    return render_template(
        'threads/all-threads.html', categories=all_categories,
        threads=all_threads, previous_values=previous_values,
                           page_number=page_number,
                           number_of_pages=number_of_pages,)

@app.route('/threads/<thread_id>', methods=['GET','POST'])
def display_thread(thread_id):
    errors = {}
    if request.method == 'GET':
        thread = m_services.threads_get_one(db, thread_id)
        return render_template(
            'threads/single-thread.html', thread=thread, errors=errors)
    elif request.method == 'POST':
        # Check user is logged in before being able to post comment
        if not flask_login.current_user.is_authenticated:
            errors.update(
                user_not_authenticated = "You must be logged in to post \
                    comments")
        # If logged in, check if form is empty
        elif request.form['comment'] == "":
            errors.update(empty = "Please enter your comments")
        # If any errors, give feedback
        if len(errors) > 0:
            thread = m_services.threads_get_one(db, thread_id)
            return render_template(
            'threads/single-thread.html', thread=thread, errors=errors)
        # If no errors, then post comment
        else:
            m_services.comments_create(db, request.form, thread_id)
            return redirect(url_for('display_thread', thread_id=thread_id))

@app.route('/threads/create', methods=['GET','POST'])
@flask_login.login_required
def create_thread():
    errors = {}
    all_categories = m_services.categories_get_all(db)
    if request.method == 'GET':
        return render_template(
            'threads/create-thread.html', categories=all_categories,
            errors=errors)
    elif request.method == 'POST':
        # Check for errors in form and capture relevant error messages
        errors = m_services.threads_validate_form(request.form)
        if len(errors)>0:
            # Capture user's input
            for key, value in request.form.items():
                errors[key] = value
            return render_template(
                'threads/create-thread.html', categories=all_categories,
                errors=errors)
        else:
            new_thread_id = m_services.threads_create(
                db,request.form).inserted_id
            return redirect(
                url_for('display_thread', thread_id=new_thread_id))

@app.route('/threads/<thread_id>/update', methods=['GET','POST'])
@flask_login.login_required
def update_thread(thread_id):
    errors = {}
    all_categories = m_services.categories_get_all(db)
    previous_values = m_services.threads_get_one(db, thread_id)
    if request.method == 'GET':
        return render_template(
            'threads/update-thread.html', categories=all_categories,
            previous_values=previous_values, errors=errors)
    elif request.method == 'POST':
        # Check for errors in form and capture relevant error messages
        errors = m_services.threads_validate_form(request.form)
        if len(errors)>0:
            # Capture user's input
            for key, value in request.form.items():
                errors[key] = value
            return render_template(
                'threads/update-thread.html', categories=all_categories,
                previous_values=previous_values, errors=errors)
        else:
            m_services.threads_update(db, request.form, thread_id)
            return redirect(url_for('display_thread', thread_id=thread_id))

@app.route('/threads/<thread_id>/delete', methods=['GET','POST'])
@flask_login.login_required
def delete_thread(thread_id):
    if request.method == 'GET':
        thread = m_services.threads_get_one(db, thread_id)
        return render_template('threads/delete-thread.html', thread=thread)
    elif request.method == 'POST':
        m_services.threads_delete(db, thread_id)
        return redirect(url_for('threads'))

@app.route('/threads/<thread_id>/comments/<comment_id>/update', methods=['GET','POST'])
@flask_login.login_required
def update_comment(thread_id, comment_id):
    errors = {}
    comment = m_services.comments_get_one(db, comment_id)
    if request.method == 'GET':
        return render_template(
            'threads/comments/update-comment.html', previous_values=comment,
            errors=errors)
    elif request.method == 'POST':
        # Check if form is empty
        if request.form['comment'] == "":
            errors.update(empty = "Please enter your comments")
        # If any errors, give feedback
        if len(errors) > 0:
            return render_template(
                'threads/comments/update-comment.html',
                previous_values=comment, errors=errors)
        else:
            m_services.comments_update(db, request.form, thread_id, comment_id)
            return redirect(url_for('display_thread', thread_id=thread_id))

@app.route('/threads/<thread_id>/comments/<comment_id>/delete', methods=['GET','POST'])
@flask_login.login_required
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
def vote_count(thread_id, up_or_down):
    votes = m_services.vote_count(db, thread_id, up_or_down)
    return {
        f'number_of_{up_or_down}_votes': json.loads(dumps(len(votes)))
    }


# App start point
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
