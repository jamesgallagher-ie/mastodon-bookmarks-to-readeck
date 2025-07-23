import json
import requests
from dotenv import dotenv_values

# Establish a connection to Readeck to get my Mastodon Bookmarks collection, find bookmarks already added and then add new ones
readeck_env = dotenv_values(".readeck_env")
READECK_API_TOKEN=readeck_env['READECK_API_TOKEN']
READECK_API_URL=readeck_env['READECK_API_URL']
READECK_MASTODON_BOOKMARKS_COLLECTION_ID=readeck_env['READECK_MASTODON_BOOKMARKS_COLLECTION_ID']


def get_existing_readeck_mastodon_bookmark_urls():
    bookmark_urls=[]
    if READECK_API_TOKEN is not None or READECK_API_TOKEN != "":
        if READECK_API_URL is not None or READECK_API_URL != "":
            if READECK_MASTODON_BOOKMARKS_COLLECTION_ID is not None or READECK_MASTODON_BOOKMARKS_COLLECTION_ID != "":
                # ready to make API calls
                READECK_BOOKMARK_LIST_URL = READECK_API_URL + "/bookmarks" + "?" + "collection=" + READECK_MASTODON_BOOKMARKS_COLLECTION_ID
                headers = {
                    'Authorization': 'Bearer ' + READECK_API_TOKEN
                }
                response = requests.get(READECK_BOOKMARK_LIST_URL, headers=headers)
                if response.status_code == 200:
                    if "application/json" in response.headers['Content-Type']:
                        bookmarks = response.json()
                        for bookmark in bookmarks:
                            bookmark_urls.append(bookmark['url'])
    return bookmark_urls


existing_readeck_bookmark_urls = get_existing_readeck_mastodon_bookmark_urls()

def get_mastodon_bookmark_urls():
    mastodon_bookmark_urls = []
    # connect to MongoDB and retrieve the URLs


    return mastodon_bookmark_urls

