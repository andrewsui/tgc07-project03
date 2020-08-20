from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import datetime
import flask_login
import module_dal

# Users
def service_users_get_all(db):
    return module_dal.dal_collection_get(db.users)

def service_users_get_one(db, user_id):
    return module_dal.dal_document_get(db.users, user_id)

def service_users_create(db, data):
    new_record = {
            'username': data.get('username'),
            'email': data.get('email'),
            'gender': None if data.get('gender')=="null" else data.get('gender'),
            'password': pbkdf2_sha256.hash(data.get('password')),
            'terms_and_conditions': False if data.get('terms_and_conditions')==None else True,
            'marketing': False if data.get('marketing')==None else True
        }
    return module_dal.dal_users_create(db.users, new_record)

def service_users_update(db, data, user_id):
    updated_record = {
            'username': data.get('username'),
            'email': data.get('email'),
            'gender': None if data.get('gender')=="null" else data.get('gender'),
            'password': pbkdf2_sha256.hash(data.get('password')),
            'terms_and_conditions': False if data.get('terms_and_conditions')==None else True,
            'marketing': False if data.get('marketing')==None else True
        }
    return module_dal.dal_users_update(db.users, updated_record, user_id)

def service_users_delete(db, user_id):
    return module_dal.dal_users_delete(db.users, user_id)

# Categories
def service_categories_get_all(db):
    return module_dal.dal_collection_get(db.categories)

def service_categories_create_0(db, data):
    category_value = data.get('category')
    return module_dal.dal_categories_create_0(db.categories, category_value)

def service_categories_create_1(db, data, parent_id):
    category_value = data.get('category')
    return module_dal.dal_categories_create_1(db.categories, category_value, parent_id)

def service_categories_update_0(db, data, category_id):
    category_value = data.get('category')
    return module_dal.dal_categories_update_0(db.categories, category_value, category_id)

def service_categories_update_1(db, data, category_id):
    category_value = data.get('category')
    return module_dal.dal_categories_update_1(db.categories, category_value, category_id)

def service_categories_delete_0(db, category_id):
    return module_dal.dal_categories_delete_0(db.categories, category_id)

def service_categories_delete_1(db, category_id):
    return module_dal.dal_categories_delete_1(db.categories, category_id)

# Threads
def service_threads_get_all(db):
    return module_dal.dal_collection_get(db.threads)

def service_threads_get_one(db, thread_id):
    return module_dal.dal_document_get(db.threads, thread_id)

def service_threads_create(db, data):
    new_record = {
        'datetime': datetime.datetime.utcnow(),
        'user': {
            # 'user_id': ObjectId(data.get('user_id')),
            # 'username': data.get('username')
            'user_id': ObjectId(flask_login.current_user._id),
            'username': flask_login.current_user.username
        },
        'category': {
            'category_id': ObjectId(data.get('category_id')),
            'category_name': [data.get('category_name')]
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
    # print(new_record)
    return module_dal.dal_threads_create(db.threads, new_record)

def service_threads_update(db, data, thread_id):
    updated_record = {
        'datetime': datetime.datetime.utcnow(),
        'user': {
            # 'user_id': data.get('user_id').strip(),
            # 'username': data.get('username')
            'user_id': ObjectId(flask_login.current_user._id),
            'username': flask_login.current_user.username
        },
        'category': {
            'category_id': data.get('category_id').strip(),
            'category_name': [data.get('category_name')]
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
    # print(updated_record)
    return module_dal.dal_threads_update(db.threads, updated_record, thread_id)

def service_threads_delete(db, thread_id):
    return module_dal.dal_threads_delete(db.threads, thread_id)
