from pytrends.request import TrendReq
import json

# https://trends.google.com/trends/explore?date=now%207-d&q=the%20most
# https://trends.google.com/trends/explore?date=now%201-d&q=the%20most
"""
 {"comparisonItem":[{"keyword":"the most","geo":"","time":"now 1-d"}],"category":0,"property":""}, 
 {"exploreQuery":"date=now%201-d&q=the%20most","guestPath":"https://trends.google.com:443/trends/embed/"} 
"""

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()
category = False

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
keys = ['When are', 'the most']
pytrend.build_payload(kw_list=keys, cat=632, geo='', timeframe='now 7-d')
if category:
    categories = pytrend.categories()
    with open('categories.json', 'w') as outfile:
        json.dump(categories, outfile, indent=2)

# Interest Over Time
interest_over_time_df = pytrend.interest_over_time()
print(interest_over_time_df.head())

# Interest by Region
interest_by_region_df = pytrend.interest_by_region(resolution="COUNTRY")
print(interest_by_region_df.sort_values(keys[0],ascending=False))

# Related Queries, returns a dictionary of dataframes
related_queries_dict = pytrend.related_queries()

print(related_queries_dict[keys[0]]["top"])
print(related_queries_dict[keys[0]]["rising"])

hist = pytrend.get_historical_interest(keys, year_start=2019)
print(hist)
# Get Google Keyword Suggestions
suggestions_dict = pytrend.suggestions(keyword="Milan")
print(suggestions_dict)

# Get Google Hot Trends data
# trending_searches_df = pytrend.trending_searches()
# print(trending_searches_df.head())

# Get Google Top Charts
# top_charts_df = pytrend.top_charts(cid='actors', date=201611)
# print(top_charts_df.head())
