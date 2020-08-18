import module_dal

def service_category_get(db):
    return module_dal.dal_category_get(db.categories)