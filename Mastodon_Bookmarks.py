from mastodon import Mastodon
from datetime import datetime
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo import errors
import json

# Config
  # Mastodon
mastodon = Mastodon(access_token = 'my_bookmarks.secret')
# MongoDB 
mongodb_config = dotenv_values(".env")
# mongodb+srv://<username>:<password>@cluster0-hars.tkhxr.mongodb.net/?retryWrites=true&w=majority
mongo_connection_protocol = 'mongodb://'
mongo_connection_string = (mongo_connection_protocol + mongodb_config['MONGO_USER'] + ':'
 + mongodb_config['MONGO_PASSWORD'] + '@' + mongodb_config["MONGO_URI"] )
# End of config

# DB Connections
client = MongoClient(mongo_connection_string)
db = client.mastodon_bookmarks
mastodon_internal_identifiers = db.internal_identifiers
mongodb_mastodon_bookmarks = db.bookmarks
# End of DB connections

rough_date = datetime(2022, 1, 1, 0, 0, 0)

def get_mastodon_bookmarks_from_mastodon():
    # This function just queries all bookmarks. I intend for this to be used infrequently with get_mastodon_bookmarks_from_mastodon_since_id preferred instead
    bookmarks = get_mastodon_bookmarks_from_mastodon_from_min_id(0)
    return bookmarks


def get_mastodon_bookmarks_from_mastodon_from_min_id(bookmark_min_id, bookmark_limit=40, bookmark_max_id=None):
    # This functions queries bookmarks after this internal min_id and is intended to be the way I'll get incremental bookmarks
    if bookmark_max_id is not None:
        bookmarks = mastodon.bookmarks(min_id = bookmark_min_id, max_id = bookmark_max_id)
    else:
        bookmarks = mastodon.bookmarks(min_id = bookmark_min_id, limit = bookmark_limit)
    return bookmarks.to_json()

def get_min_id_from_db():
    bookmark_min_id = 0
    result = mastodon_internal_identifiers.find_one({"type": "bookmark_min_id"})
    if result is not None:
        bookmark_min_id = result['value']
    return bookmark_min_id

def update_min_id_on_db(bookmark_min_id):
    success = False

    return success

def are_there_more_bookmarks(bookmark_pagination): 
    more = False
    more_pages_text = "_pagination_next"
    if more_pages_text in bookmark_pagination.keys():
        more = True    
    return more

    



bookmark_min_id = get_min_id_from_db()

# Mastodon Query 
bookmarks = get_mastodon_bookmarks_from_mastodon_from_min_id(bookmark_min_id, bookmark_limit=5)
print(bookmarks)
bookmark_json = json.loads(bookmarks)
bookmark_data = bookmark_json['_mastopy_data']
bookmark_pagination = bookmark_json['_mastopy_extra_data']

more = are_there_more_bookmarks(bookmark_pagination)

# persist the results
# result = mongodb_mastodon_bookmarks.insert_many(bookmark_data)
# print(result)

# update the bookmark_min_id value




# bookmarks = get_mastodon_bookmarks_from_mastodon()
# print(bookmarks._pagination_prev)
# print(bookmarks._pagination_next)
# print(bookmarks)


# print(len(bookmarks))
# for bookmark in bookmarks:
#     # print(bookmark)
# #     # print(bookmark['content'])
#     # print("\n")
# #     # print(bookmark['url'], bookmark['content'])
#     print(bookmark['id'], bookmark['url'])

# # statuses = get_statuses()
# # print(statuses._pagination_prev)
# print("next")
# next = mastodon.fetch_next(previous_page = bookmarks._pagination_next)
# for b in next:
#     print(b['id'], b['url'])
# previous = mastodon.fetch_previous(next_page = bookmarks._pagination_next)
# print(previous._pagination_next)
# again = mastodon.fetch_previous(next_page = previous._pagination_next)
# print(again._pagination_next)
# again2 = mastodon.fetch_previous(next_page = again._pagination_next)
# print(again2._pagination_next)