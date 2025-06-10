import feedparser

def fetch_feed(url: str):
    feed = feedparser.parse(url)
    return feed.entries