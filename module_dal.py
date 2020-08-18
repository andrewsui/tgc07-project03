from bson.objectid import ObjectId

def dal_category_get(collection):
    return collection.find()

def dal_category_create(collection, category_value):
    new_record = {
        'category' : category_value,
        'sub_categories' : []
    }
    return collection.insert_one(new_record)

def dal_category_create_1(collection, category_value, parent_id):
    return collection.update_one({
        '_id': ObjectId(parent_id)
    }, {
        '$push': {
            'sub_categories': {
                '_id': ObjectId(),
                'category' : category_value,
                'sub_categories': []
            }
        }
    })