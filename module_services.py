import module_dal

# Users
def service_users_get(db):
    return module_dal.dal_collection_get(db.users)

def service_users_get_one(db, user_id):
    return module_dal.dal_users_get_one(db.users, user_id)

def service_users_create(db, data):
    new_record = {
            'username': data.get('username'),
            'email': data.get('email'),
            'gender': None if data.get('gender')=="null" else data.get('gender'),
            'password': data.get('password'),
            'terms_and_conditions': False if data.get('terms_and_conditions')==None else True,
            'marketing': False if data.get('marketing')==None else True
        }
    return module_dal.dal_users_create(db.users, new_record)

def service_users_update(db, data, user_id):
    updated_record = {
            'username': data.get('username'),
            'email': data.get('email'),
            'gender': None if data.get('gender')=="null" else data.get('gender'),
            'password': data.get('password'),
            'terms_and_conditions': False if data.get('terms_and_conditions')==None else True,
            'marketing': False if data.get('marketing')==None else True
        }
    return module_dal.dal_users_update(db.users, updated_record, user_id)

def service_users_delete(db, user_id):
    return module_dal.dal_users_delete(db.users, user_id)

# Categories
def service_categories_get(db):
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
