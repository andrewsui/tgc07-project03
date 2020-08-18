import module_dal

def service_category_get(db):
    return module_dal.dal_category_get(db.categories)

def service_category_create(db, data):
    category_value = data.get('category')
    return module_dal.dal_category_create(db.categories, category_value)

def service_category_create_1(db, data, parent_id):
    category_value = data.get('category')
    return module_dal.dal_category_create_1(db.categories, category_value, parent_id)
