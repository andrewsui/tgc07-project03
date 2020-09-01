from bson.objectid import ObjectId
import flask_login

# Generic database queries
def collection_get(collection):
    return collection.find()

def document_get(collection, document_id):
    return collection.find_one({
        '_id': ObjectId(document_id)
    })

# Users
def users_create(collection, new_record):
    return collection.insert_one(new_record)

# def users_update(collection, updated_record, user_id):
#     return collection.update_one({
#         '_id': ObjectId(user_id)
#     }, {
#         '$set': updated_record
#     })

def users_update(collection, updated_record, user_id):
    return collection.update_one({
        '_id': ObjectId(user_id)
    }, {
        '$set': {
            'email': updated_record['email'],
            'password': updated_record['password'],
            'gender': updated_record['gender'],
            'marketing': updated_record['marketing'],
        }
    })

def users_delete(collection, user_id):
    return collection.remove({
        '_id': ObjectId(user_id)
        })

def users_threads_by_user(collection, search_criteria):
    return collection.find(search_criteria)

# Categories
def category_name_get(collection, category_id):
    return collection.find_one({
        '_id': ObjectId(category_id)
    },
    {
        'category': 1
    })['category']

def sub_category_name_get(collection, sub_category_id):
    return collection.find_one({
        'sub_categories._id': ObjectId(sub_category_id)
    },
    {
        'sub_categories.$.category': 1
    })['sub_categories'][0]['category']

def categories_create_0(collection, category_value):
    new_record = {
        'category': category_value,
        'parent': None,
        'sub_categories': []
    }
    return collection.insert_one(new_record)

def categories_create_1(collection, category_value, parent_id):
    return collection.update_one({
        '_id': ObjectId(parent_id)
    }, {
        '$push': {
            'sub_categories': {
                '_id': ObjectId(),
                'category': category_value,
                'parent': ObjectId(parent_id),
                'sub_categories': []
            }
        }
    })

def categories_update_0(collection, category_value, category_id):
    return collection.update_one({
        '_id': ObjectId(category_id)
    }, {
        '$set': {
            'category': category_value
            }
    })

def categories_update_1(collection, category_value, category_id):
    return collection.update_one({
            'sub_categories._id': ObjectId(category_id)
        }, {
            '$set': {
                'sub_categories.$.category': category_value
            }
        })

def categories_delete_0(collection, category_id):
    return collection.remove({
        '_id': ObjectId(category_id)
        })

def categories_delete_1(collection, category_id):
    return collection.update_one({
        'sub_categories._id': ObjectId(category_id)
        }, {
            '$pull': {
                'sub_categories': {
                    '_id': ObjectId(category_id)
                }
            }
        })

def sub_categories_get(collection, parent_id):
    return collection.find({
        '_id': ObjectId(parent_id)
    }, {
        'sub_categories': 1
    })

# Threads
def threads_search(collection, user_input):
    search_criteria = {}
    # Search by category
    if user_input['category_id']:
        search_criteria['category.category_id'] = ObjectId(
            user_input['category_id'])
    # Search by sub-category
    if user_input['sub_category_id']:
        search_criteria['category.sub_category_id'] = ObjectId(
            user_input['sub_category_id'])
    # Search box queries
    if user_input['search_box']:
        search_criteria['$or'] = [
            {
                'product_name': {
                    '$regex': user_input['search_box'],
                    '$options': 'i'
                }
            },
            {
                'description': {
                    '$regex': user_input['search_box'],
                    '$options': 'i'
                }
            },
            {
                'sub_posts.comment': {
                    '$regex': user_input['search_box'],
                    '$options': 'i'
                }
            }
        ]
    return collection.find(search_criteria)

def threads_create(collection, new_record):
    return collection.insert_one(new_record)

def threads_update(collection, updated_record, thread_id):
    return collection.update_one({
        '_id': ObjectId(thread_id)
    }, {
        '$set': {
            'category': {
                'category_id': updated_record['category']['category_id'],
                'category_name': updated_record['category']['category_name'],
                'sub_category_id': updated_record['category'][
                    'sub_category_id'],
                'sub_category_name': updated_record['category'][
                    'sub_category_name']
            },
            'product_name': updated_record['product_name'],
            'price': updated_record['price'],
            'image': updated_record['image'],
            'affiliate': updated_record['affiliate'],
            'description': updated_record['description']
        }
    })

# def threads_update_username(collection, username, user_id):
#     return collection.update_many({
#             'user.user_id': ObjectId(user_id)
#         },{
#             '$set': {
#                 'user.username': username
#             }
#         })

def threads_delete(collection, thread_id):
    return collection.remove({
        '_id': ObjectId(thread_id)
        })

# Thread comments
def comments_get_one(collection, comment_id):
    return collection.find_one({
        'sub_posts._id': ObjectId(comment_id)
    }, {
        'sub_posts.$': 1
    })

def comments_create(collection, updated_record, thread_id):
    return collection.update_one({
        '_id': ObjectId(thread_id)
    }, {
        '$push': {
            'sub_posts': {
                '_id': ObjectId(),
                'parent': ObjectId(thread_id),
                'datetime': updated_record['datetime'],
                'user': {
                    'user_id': ObjectId(updated_record['user']['user_id']),
                    'username': updated_record['user']['username']
                },
                'comment': updated_record['comment'],
                'quote': updated_record['quote']
            }
        }
    })

def comments_update(collection, updated_record, thread_id, comment_id):
    return collection.update_one({
            'sub_posts._id': ObjectId(comment_id)
        }, {
            '$set': {
                'sub_posts.$.comment': updated_record['comment']
            }
        })

def comments_delete(collection, comment_id):
    return collection.update_one({
        'sub_posts._id': ObjectId(comment_id)
        }, {
            '$pull': {
                'sub_posts': {
                    '_id': ObjectId(comment_id)
                }
            }
        })

def comments_count(collection, thread_id):
    return collection.find_one({
            '_id': ObjectId(thread_id)
        }, {
            'sub_posts': 1
        })['sub_posts']

# def comments_update_username(collection, username, user_id):
#     return collection.update_many({
#             'sub_posts.user': {
#                 '$elemMatch': {
#                     'user_id': ObjectId(user_id)
#                 }
#             }
#         },{
#             '$set': {
#                 'sub_posts.$.user.username': username
#             }
#         })

# Voting
def vote_up(collection, thread_id):
    return collection.update_one({
            '_id': ObjectId(thread_id)
        }, {
            '$addToSet': {
                'votes.up_votes': ObjectId(flask_login.current_user._id)
            }
        })

def vote_down(collection, thread_id):
    return collection.update_one({
            '_id': ObjectId(thread_id)
        }, {
            '$addToSet': {
                'votes.down_votes': ObjectId(flask_login.current_user._id)
            }
        })

def vote_up_check(collection, thread_id):
    return collection.find({
            '_id': ObjectId(thread_id),
            'votes.up_votes': {
                 '$in': [ObjectId(flask_login.current_user._id)]
                 }
        }).count()

def vote_down_check(collection, thread_id):
    return collection.find({
            '_id': ObjectId(thread_id),
            'votes.down_votes': {
                '$in': [ObjectId(flask_login.current_user._id)]
                }
        }).count()

def vote_up_remove(collection, thread_id):
    return collection.update_one({
            '_id': ObjectId(thread_id)
        }, {
            '$pull': {
                'votes.up_votes': ObjectId(flask_login.current_user._id)
            }
        })

def vote_down_remove(collection, thread_id):
    return collection.update_one({
            '_id': ObjectId(thread_id)
        }, {
            '$pull': {
                'votes.down_votes': ObjectId(flask_login.current_user._id)
            }
        })

def vote_count(collection, thread_id, up_or_down):
    return collection.find_one({
        '_id': ObjectId(thread_id)
    }, {
        f'votes.{up_or_down}_votes': 1
    })['votes'][f'{up_or_down}_votes']
