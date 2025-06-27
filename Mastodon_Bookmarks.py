from mastodon import Mastodon

# Config
mastodon = Mastodon(access_token = 'my_bookmarks.secret')


def get_mastodon_bookmarks_from_mastodon():
    # This function just queries all bookmaarks. I intend for this to be used infrequently with get_mastodon_bookmarks_from_mastodon_since_id preferred instead
    print('called get_mastodon_bookmarks_from_mastodon')
    bookmarks = mastodon.bookmarks()
    for bookmark in bookmarks:
        print(bookmark)


def get_mastodon_bookmarks_from_mastodon_since_id(bookmark_id):
    # This functions queries bookmarks since the specified bookmark_id and is intended to be the way I'll get incremental bookmark
    print('called get_mastodon_bookmarks_from_mastodon_since_id(bookmark_id)')

#get_mastodon_bookmarks_from_mastodon()