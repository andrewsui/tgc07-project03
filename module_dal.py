from bson.objectid import ObjectId

# Get entire collection from database
def dal_collection_get(collection):
    return collection.find()

# Users
def dal_users_get_one(collection, user_id):
    return collection.find_one({
        '_id': ObjectId(user_id)
    })

def dal_users_create(collection, new_record):
    return collection.insert_one(new_record)

def dal_users_update(collection, updated_record, user_id):
    return collection.update_one({
        '_id': ObjectId(user_id)
    }, {
        '$set': updated_record
    })

def dal_users_delete(collection, user_id):
    return collection.remove({
        '_id': ObjectId(user_id)
        })

# Categories
def dal_categories_create_0(collection, category_value):
    new_record = {
        'category': category_value,
        'sub_categories': []
    }
    return collection.insert_one(new_record)

def dal_categories_create_1(collection, category_value, parent_id):
    return collection.update_one({
        '_id': ObjectId(parent_id)
    }, {
        '$push': {
            'sub_categories': {
                '_id': ObjectId(),
                'category': category_value,
                'sub_categories': []
            }
        }
    })

def dal_categories_update_0(collection, category_value, category_id):
    return collection.update_one({
        '_id': ObjectId(category_id)
    }, {
        '$set': {
            'category': category_value
            }
    })

def dal_categories_update_1(collection, category_value, category_id):
    return collection.update_one({
            'sub_categories._id': ObjectId(category_id)
        }, {
            '$set': {
                'sub_categories.$.category': category_value
            }
        })

def dal_categories_delete_0(collection, category_id):
    return collection.remove({
        '_id': ObjectId(category_id)
        })

def dal_categories_delete_1(collection, category_id):
    return collection.update_one({
        'sub_categories._id': ObjectId(category_id)
        }, {
            '$pull': {
                'sub_categories': {
                    '_id': ObjectId(category_id)
                }
            }
        })


