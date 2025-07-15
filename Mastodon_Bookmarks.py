from mastodon import Mastodon
from datetime import datetime
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo import errors

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
    # This function just queries all bookmaarks. I intend for this to be used infrequently with get_mastodon_bookmarks_from_mastodon_since_id preferred instead
    print('called get_mastodon_bookmarks_from_mastodon')
    bookmarks = mastodon.bookmarks(limit = 40, min_id = 1)

    return bookmarks


def get_mastodon_bookmarks_from_mastodon_since_id(bookmark_internal_id):
    # This functions queries bookmarks since the specified internal bookmark_id and is intended to be the way I'll get incremental bookmark
    print('called get_mastodon_bookmarks_from_mastodon_since_id(bookmark_id)')
    # 114719202162983446
    bookmarks = mastodon.bookmarks(min_id = bookmark_internal_id, limit = 40)

    return bookmarks


# bookmarks = get_mastodon_bookmarks_from_mastodon()
# # bookmarks = get_mastodon_bookmarks_from_mastodon_since_id('46')
# print(bookmarks._pagination_prev)
# print(bookmarks._pagination_next)
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