import module_dal

def get_categories_service(db):
    return module_dal.get_categories_dal(db.categories)