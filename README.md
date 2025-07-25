# mastodon-bookmarks-to-readeck
Extract bookmarks from Mastodon and insert them to Readeck 

# Intro
This is pretty horrible code - I don't write code day-to-day but this was especially lazy as I was writing bit-by-bit in a "does this work" fashion. So there's duplication of code, lack of error handling and bad design (I'm not proud of my duplicate checking approaches :D ). But here it is anyway.

# Flow
## Mastodon_Bookmarks
Mastodon_Bookmarks fetches the bookmarks from Mastodon and dumps them into a MongoDB collection - I did this because I figured I may want to do other things with the data later. I also persist a Mastodon internal identifier so I can get incremental updates of the bookmarks. 
```
{
  "_id": {
    "$oid": "6876c1b9320ed56f4b1e31cd"
  },
  "type": "bookmark_min_id",
  "value": 185
}
```
The internal identifiers are confusing to me - there's no way to get individual identifiers (see the note [here](https://docs.joinmastodon.org/methods/bookmarks/)) and I found the way `since_id`, `min_id` and `max_id` work confusing too. 

## Send_Mastodon_Bookmarks_to_Readeck
Send_Mastodon_Bookmarks_to_Readeck then fetches the URLs of bookmarks I've stored in MongoDB and creates a Readeck bookmark with the label `mastodon_bookmarks` so I can create a Readeck collection by filtering on that label. Because I'm just using Readeck to store these bookmarks for future reference I added functions afterwards to set them as read and to archive them so they don't show up in my Readeck unread items. I'm still learning Readeck and thinking about how I'll use it. I'll likely refactor my code to mark them bookmark as read and archived when I'm creating the bookmark
