from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import datetime
import flask_login
import re
import m_dal

# Users
def users_get_all(db):
    return m_dal.collection_get(db.users)

def users_get_one(db, user_id):
    return m_dal.document_get(db.users, user_id)

def users_create(db, data):
    new_record = {
            'username': data.get('username'),
            'email': data.get('email'),
            'gender': None if data.get('gender')=="null" else data.get(
                'gender'),
            'password': pbkdf2_sha256.hash(data.get('password')),
            'terms_and_conditions': False if data.get(
                'terms_and_conditions')==None else True,
            'marketing': False if data.get('marketing')==None else True,
            'is_admin': False if data.get('is_admin')==None else True
        }
    return m_dal.users_create(db.users, new_record)

def users_update(db, data, user_id):
    updated_record = {
            # 'username': data.get('username'),
            'email': data.get('email'),
            'gender': None if data.get('gender')=="null" else data.get(
                'gender'),
            'password': pbkdf2_sha256.hash(data.get('password')),
            # 'terms_and_conditions': False if data.get(
            #     'terms_and_conditions')==None else True,
            'marketing': False if data.get('marketing')==None else True,
            'is_admin': False if data.get('is_admin')==None else True
        }
    return m_dal.users_update(db.users, updated_record, user_id)

def users_delete(db, user_id):
    return m_dal.users_delete(db.users, user_id)

def users_threads_by_user(db, user_id):
    search_criteria = {}
    search_criteria['user.user_id'] = ObjectId(user_id)
    return m_dal.users_threads_by_user(db.threads, search_criteria)

def users_check_email(email):
    # https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    return re.search(regex, email)

def users_check_username(username):
    # If doesn't start with letter, followed by 3-20 alphanumeric
    if not re.search('^[a-z]+[a-z0-9]{3,20}', username):
        return False
    # If has whitespace, comma, fullstop, underscore, hyphen
    elif re.search('[\s,._-]', username):
        return False
    # If greater than length 20
    elif len(username) > 20:
        return False
    # If none of the above, then valid username
    else:
        return True

def users_check_password(password):
    # https://stackoverflow.com/questions/19605150/regex-for-password-must-contain-at-least-eight-characters-at-least-one-number-a
    return re.search('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password)

def users_check_password_same(password_1, password_2):
    return password_1==password_2

def users_validate_form(data):
    errors = {}
    # If username not valid, add error
    if not users_check_username(data.get('username')):
        errors.update(invalid_username = "Username must start with a \
            letter, be alphanumeric and be between 4 and 20 characters \
                long")
    # If email not valid, add error
    if not users_check_email(data.get('email')):
        errors.update(invalid_email = "Please enter a valid email")
    # If password not valid, add error
    if not users_check_password(data.get('password')):
        errors.update(invalid_password = "Password must be a minimum of \
            eight characters, and have at least one letter and one \
                number")
    # If passwords are not same, add error
    if not users_check_password_same(
        data.get('password'), data.get('password_2')):
        errors.update(invalid_password_2 = "Passwords did not match")
    # If T&Cs not agreed to, add error
    if not data.get('terms_and_conditions'):
        errors.update(invalid_terms_and_conditions = "You must agree to \
            our terms and conditions to create a user account")
    return errors

# Admin users
def admin_users_update(db, data, user_id):
    updated_record = {
            'username': data.get('username'),
            'email': data.get('email'),
            'gender': None if data.get('gender')=="null" else data.get(
                'gender'),
            'password': pbkdf2_sha256.hash(data.get('password')),
            'terms_and_conditions': False if data.get(
                'terms_and_conditions')==None else True,
            'marketing': False if data.get('marketing')==None else True,
            'is_admin': False if data.get('is_admin')==None else True
        }
    return m_dal.admin_users_update(db.users, updated_record, user_id)

# Categories
def categories_get_all(db):
    return m_dal.collection_get(db.categories)

def categories_get_one(db, category_id):
    return m_dal.document_get(db.categories, category_id)

def categories_create_0(db, data):
    category_value = data.get('category')
    return m_dal.categories_create_0(db.categories, category_value)

def categories_create_1(db, data, parent_id):
    category_value = data.get('sub_category')
    return m_dal.categories_create_1(db.categories, category_value, parent_id)

def categories_update_0(db, data, category_id):
    category_value = data.get('category')
    return m_dal.categories_update_0(
        db.categories, category_value, category_id)

def categories_update_1(db, data, category_id):
    category_value = data.get('sub_category')
    return m_dal.categories_update_1(
        db.categories, category_value, category_id)

def categories_delete_0(db, category_id):
    return m_dal.categories_delete_0(db.categories, category_id)

def categories_delete_1(db, category_id):
    return m_dal.categories_delete_1(db.categories, category_id)

def sub_categories_get(db, parent_id):
    return m_dal.sub_categories_get(db.categories, parent_id)

def sub_categories_get_one(db, sub_category_id):
    return m_dal.sub_categories_get_one(db.categories, sub_category_id)

# Threads
def threads_get_all(db):
    return m_dal.collection_get(db.threads)

def threads_get_one(db, thread_id):
    return m_dal.document_get(db.threads, thread_id)

def threads_search(db, data):
    user_input = {
        'category_id': data.get('categories'),
        'sub_category_id': data.get('sub_categories'),
        'search_box': data.get('search-box')
    }
    return m_dal.threads_search(db.threads, user_input)

def threads_create(db, data):
    category_id = data.get('categories')
    category_name = m_dal.category_name_get(db.categories, category_id)
    if data.get('sub_categories'):
        sub_category_id = ObjectId(data.get('sub_categories'))
        sub_category_name = m_dal.sub_category_name_get(
            db.categories, data.get('sub_categories'))
    else:
        sub_category_id = ""
        sub_category_name = ""
    new_record = {
        'datetime': datetime.datetime.utcnow(),
        'user': {
            'user_id': ObjectId(flask_login.current_user._id),
            'username': flask_login.current_user.username
        },
        'category': {
            'category_id': ObjectId(category_id),
            'category_name': category_name,
            'sub_category_id': sub_category_id,
            'sub_category_name': sub_category_name
        },
        'product_name': data.get('product_name'),
        'price': float(data.get('price')),
        'image': data.get('image'),
        'affiliate': data.get('affiliate'),
        'description': data.get('description'),
        'votes': {
            'up_votes': [],
            'down_votes': []
        },
        'sub_posts': []
    }
    return m_dal.threads_create(db.threads, new_record)

def threads_update(db, data, thread_id):
    category_id = data.get('categories')
    category_name = m_dal.category_name_get(db.categories, category_id)
    if data.get('sub_categories'):
        sub_category_id = ObjectId(data.get('sub_categories'))
        sub_category_name = m_dal.sub_category_name_get(
            db.categories, data.get('sub_categories'))
    else:
        sub_category_id = ""
        sub_category_name = ""
    updated_record = {
        'category': {
            'category_id': ObjectId(data.get('categories')),
            'category_name': category_name,
            'sub_category_id': sub_category_id,
            'sub_category_name': sub_category_name
        },
        'product_name': data.get('product_name'),
        'price': float(data.get('price')),
        'image': data.get('image'),
        'affiliate': data.get('affiliate'),
        'description': data.get('description'),
        'votes': {
            'up_votes': [],
            'down_votes': []
        },
        'sub_posts': []
    }
    return m_dal.threads_update(db.threads, updated_record, thread_id)

# def threads_update_username(db, username, user_id):
#     return m_dal.threads_update_username(db.threads, username, user_id)

def threads_delete(db, thread_id):
    return m_dal.threads_delete(db.threads, thread_id)

# Thread comments
def comments_get_one(db, comment_id):
    return m_dal.comments_get_one(db.threads, comment_id)['sub_posts'][0]

def comments_create(db, data, thread_id):
    new_record = {
        'datetime': datetime.datetime.utcnow(),
        'user': {
            'user_id': ObjectId(flask_login.current_user._id),
            'username': flask_login.current_user.username
        },
        'comment': data.get('comment'),
        'quote': None
    }
    return m_dal.comments_create(db.threads, new_record, thread_id)

def comments_update(db, data, thread_id, comment_id):
    updated_record = {
        # 'datetime': datetime.datetime.utcnow(),
        'user': {
            'user_id': ObjectId(flask_login.current_user._id),
            'username': flask_login.current_user.username
        },
        'comment': data.get('comment'),
        'quote': None
    }
    return m_dal.comments_update(
        db.threads, updated_record, thread_id, comment_id)

# def comments_update_username(db, username, user_id):
#     return m_dal.comments_update_username(db.threads, username, user_id)

def comments_delete(db, comment_id):
    return m_dal.comments_delete(db.threads, comment_id)

def comments_count(db, thread_id):
    return m_dal.comments_count(db.threads, thread_id)

# Voting
def vote_up(db, thread_id):
    return m_dal.vote_up(db.threads, thread_id)

def vote_down(db, thread_id):
    return m_dal.vote_down(db.threads, thread_id)

def vote_up_check(db, thread_id):
    return m_dal.vote_up_check(db.threads, thread_id)

def vote_down_check(db, thread_id):
    return m_dal.vote_down_check(db.threads, thread_id)

def vote_up_remove(db, thread_id):
    return m_dal.vote_up_remove(db.threads, thread_id)

def vote_down_remove(db, thread_id):
    return m_dal.vote_down_remove(db.threads, thread_id)

def vote_count(db, thread_id, up_or_down):
    return m_dal.vote_count(db.threads, thread_id, up_or_down)

