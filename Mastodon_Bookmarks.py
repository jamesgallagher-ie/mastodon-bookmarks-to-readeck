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
    try:
        result = mastodon_internal_identifiers.update_one({"type": "bookmark_min_id"}, { "$set": { "value": bookmark_min_id } } )
        if result.matched_count == 1 and result.modified_count == 1:
            success = True
    except Exception as e:
          print("An exception occurred ::", e)

    return success

def are_there_more_bookmarks(bookmark_pagination): 
    more = False
    more_pages_text = "_pagination_next"
    if more_pages_text in bookmark_pagination.keys():
        more = True    
    return more

def get_URIs_from_db():
    uris = []
    results = mongodb_mastodon_bookmarks.find({ "uri": { "$exists": True} })
    for result in results:
        uris.append(result['uri'])
    return uris

def parse_and_persist_bookmarks(bookmark_data):
  # Horrible duplicate checking
  # I'm thinking of using the URI and just getting a list of those already in the DB to check against
  bookmark_persist_success = True
  for bookmark in bookmark_data:
      if bookmark['uri'] not in current_URIs:
          try:
            results = mongodb_mastodon_bookmarks.insert_one(bookmark)
            current_URIs.append(bookmark['uri'])
          except Exception as e:
            print("An exception occurred ::", e)
            bookmark_persist_success = False
  return bookmark_persist_success  


more = True


while more:
  # MongoDB Query for existing URIs
  current_URIs = get_URIs_from_db()
  bookmark_min_id = get_min_id_from_db()
  # Mastodon Query 
  bookmarks = get_mastodon_bookmarks_from_mastodon_from_min_id(bookmark_min_id)
  # print(bookmarks)
  bookmark_json = json.loads(bookmarks)
  bookmark_data = bookmark_json['_mastopy_data']
  bookmark_pagination = bookmark_json['_mastopy_extra_data']

  bookmark_persist_success = parse_and_persist_bookmarks(bookmark_data)
  # update the bookmark_min_id value
  if (bookmark_persist_success):
      if bool(bookmark_pagination):
        update_min_id_on_db(bookmark_pagination['_pagination_prev']['min_id'])
      more = are_there_more_bookmarks(bookmark_pagination)
