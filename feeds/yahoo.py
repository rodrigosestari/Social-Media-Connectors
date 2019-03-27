news_rss_url = "http://rss.ent.yahoo.com/movies/thisweek.xml"
import feedparser
import datetime

info = feedparser.parse(news_rss_url)

info.feed.title
info.feed.link
for entry in info.entries:
    print(entry.title)

entry = info.entries[0]

entry.modified_parsed
datetime.datetime.fromtimestamp(datetime.time.mktime(entry.modified_parsed))

entry.modified_parsed
timetuple = list(entry.modified_parsed[0:8]) + [-1]
datetime.datetime.fromtimestamp(datetime.time.mktime(timetuple))
