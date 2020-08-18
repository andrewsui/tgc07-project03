

def dal_category_get(collection):
    return collection.find()

def dal_category_create(collection, category_value):
    new_record = {
        'category' : category_value,
        'sub_categories' : []
    }
    return collection.insert_one(new_record)

