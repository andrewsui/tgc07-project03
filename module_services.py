import module_dal

def service_users_get(db):
    return module_dal.dal_collection_get(db.users)


def service_category_get(db):
    return module_dal.dal_collection_get(db.categories)

def service_category_create_0(db, data):
    category_value = data.get('category')
    return module_dal.dal_category_create_0(db.categories, category_value)

def service_category_create_1(db, data, parent_id):
    category_value = data.get('category')
    return module_dal.dal_category_create_1(db.categories, category_value, parent_id)

def service_category_update_0(db, data, category_id):
    category_value = data.get('category')
    return module_dal.dal_category_update_0(db.categories, category_value, category_id)

def service_category_update_1(db, data, category_id):
    category_value = data.get('category')
    return module_dal.dal_category_update_1(db.categories, category_value, category_id)

def service_category_delete_0(db, category_id):
    return module_dal.dal_category_delete_0(db.categories, category_id)

def service_category_delete_1(db, category_id):
    return module_dal.dal_category_delete_1(db.categories, category_id)
