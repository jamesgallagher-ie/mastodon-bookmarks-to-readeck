import json
import requests
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo import errors


# Establish a connection to Readeck to get my Mastodon Bookmarks collection, find bookmarks already added and then add new ones
READECK_API_TOKEN = ""
READECK_API_URL = ""
READECK_MASTODON_BOOKMARKS_COLLECTION_ID = ""
readeck_env = dotenv_values(".readeck_env")
if readeck_env:
    READECK_API_TOKEN=readeck_env['READECK_API_TOKEN']
    READECK_API_URL=readeck_env['READECK_API_URL']
    READECK_MASTODON_BOOKMARKS_COLLECTION_ID=readeck_env['READECK_MASTODON_BOOKMARKS_COLLECTION_ID']

mongodb_config = dotenv_values(".env")
# mongodb+srv://<username>:<password>@cluster0-hars.tkhxr.mongodb.net/?retryWrites=true&w=majority
mongo_connection_protocol = 'mongodb://'
mongo_connection_string = (mongo_connection_protocol + mongodb_config['MONGO_USER'] + ':'
 + mongodb_config['MONGO_PASSWORD'] + '@' + mongodb_config["MONGO_URI"] )

def have_all_readeck_config():
    all_config_available = False
    if READECK_API_TOKEN is not None or READECK_API_TOKEN != "":
        if READECK_API_URL is not None or READECK_API_URL != "":
            if READECK_MASTODON_BOOKMARKS_COLLECTION_ID is not None or READECK_MASTODON_BOOKMARKS_COLLECTION_ID != "":
                all_config_available = True
    return all_config_available


def get_existing_readeck_mastodon_bookmark_urls():
    bookmark_urls=[]
    more = True
    offset = 0
    if have_all_readeck_config():
        # ready to make API calls
        headers = {
            'Authorization': 'Bearer ' + READECK_API_TOKEN
        }
        while more:
            READECK_BOOKMARK_LIST_URL = READECK_API_URL + "/bookmarks" + "?" + "collection=" + READECK_MASTODON_BOOKMARKS_COLLECTION_ID + "&" + "offset=" + str(offset)
            response = requests.get(READECK_BOOKMARK_LIST_URL, headers=headers)
            if response.status_code == 200:
                if "application/json" in response.headers['Content-Type']:
                    bookmarks = response.json()
                    for bookmark in bookmarks:
                        bookmark_urls.append(bookmark['url'])
                total_count = response.headers.get('Total-Count', None)
                count_of_bookmarks = len(bookmark_urls)
                # print(count_of_bookmarks, total_count)
                if count_of_bookmarks < int(total_count):
                    offset = offset + 50
                    more = True
                elif count_of_bookmarks >= int(total_count):  
                    more = False
    return bookmark_urls

def get_URLs_from_db():
    # DB Connections
    client = MongoClient(mongo_connection_string)
    db = client.mastodon_bookmarks
    mongodb_mastodon_bookmarks = db.bookmarks
    urls = []
    results = mongodb_mastodon_bookmarks.find({ "url": { "$exists": True} })
    for result in results:
        urls.append(result['url'])
    return urls

def filter_existing_urls_in_readeck(readeck_urls, mastodon_urls):
    filtered_urls = []
    for m in mastodon_urls:
        if m not in readeck_urls:
            filtered_urls.append(m)
    return filtered_urls

def create_readeck_bookmark(url):
    READECK_BOOKMARK_LIST_URL = READECK_API_URL + "/bookmarks"
    labels = ['mastodon_bookmarks']
    payload = { 'labels': labels, 'url': url}
    headers = {
         'Authorization': 'Bearer ' + READECK_API_TOKEN
         }
    response = requests.post(READECK_BOOKMARK_LIST_URL, headers=headers, data=payload)

def get_existing_readeck_mastodon_bookmark_uids(filter_errored_bookmarks=None):
    bookmark_uids=[]
    more = True
    offset = 0
    if filter_errored_bookmarks:
        filter_errored = 'true'
    elif not filter_errored_bookmarks:
        filter_errored = 'false'
        
    if have_all_readeck_config():
        # ready to make API calls
        headers = {
            'Authorization': 'Bearer ' + READECK_API_TOKEN
        }
        while more:
            READECK_BOOKMARK_LIST_URL = READECK_API_URL + "/bookmarks" + "?" + "collection=" + READECK_MASTODON_BOOKMARKS_COLLECTION_ID + "&" + "offset=" + str(offset)
            if filter_errored_bookmarks:
                READECK_BOOKMARK_LIST_URL = READECK_BOOKMARK_LIST_URL + "&" + "has_errors=" + filter_errored
            response = requests.get(READECK_BOOKMARK_LIST_URL, headers=headers)
            if response.status_code == 200:
                if "application/json" in response.headers['Content-Type']:
                    bookmarks = response.json()
                    for bookmark in bookmarks:
                        bookmark_uids.append(bookmark['id'])
                total_count = response.headers.get('Total-Count', None)
                count_of_bookmarks = len(bookmark_uids)
                # print(count_of_bookmarks, total_count)
                if count_of_bookmarks < int(total_count):
                    offset = offset + 50
                    more = True
                elif count_of_bookmarks >= int(total_count):  
                    more = False
    
    return bookmark_uids

def get_existing_readeck_mastodon_bookmarks_details(uid):
    bookmark_details = {}

    return bookmark_details

def mark_bookmark_as_read(uid):
    READECK_BOOKMARK_LIST_URL = READECK_API_URL + "/bookmarks/" + uid
    headers = { 'Authorization': 'Bearer ' + READECK_API_TOKEN }
    payload = { 'read_progress': 100 }
    response = requests.patch(READECK_BOOKMARK_LIST_URL, headers=headers, data=payload)
    if response.status_code == 200:
        if "application/json" in response.headers['Content-Type']:
            r = response.json()

def archive_bookmark(uid):
    READECK_BOOKMARK_LIST_URL = READECK_API_URL + "/bookmarks/" + uid
    headers = { 'Authorization': 'Bearer ' + READECK_API_TOKEN }
    payload = { 'is_archived': 'true' }
    response = requests.patch(READECK_BOOKMARK_LIST_URL, headers=headers, data=payload)
    if response.status_code == 200:
        if "application/json" in response.headers['Content-Type']:
            r = response.json()
    else:
        print("there was an error")

existing_readeck_bookmark_urls = get_existing_readeck_mastodon_bookmark_urls()

mastodon_bookmark_urls = get_URLs_from_db()
urls_for_creation = filter_existing_urls_in_readeck(existing_readeck_bookmark_urls, mastodon_bookmark_urls)
for url in urls_for_creation:
    create_readeck_bookmark(url)

# errored_uids = get_existing_readeck_mastodon_bookmark_uids(filter_errored_bookmarks=True)
# all_uids = get_existing_readeck_mastodon_bookmark_uids(filter_errored_bookmarks=False)

# for uid in all_uids:
#     if uid not in errored_uids:
#         archive_bookmark(uid)