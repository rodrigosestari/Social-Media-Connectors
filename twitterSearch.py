import tweepy

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print
    tweet.text

from TwitterSearch import *

try:
    tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
    tso.set_keywords(['Guttenberg', 'Doktorarbeit'])  # let's define all words we would like to have a look for
    tso.set_language('de')  # we want to see German tweets only
    tso.set_include_entities(False)  # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key='aaabbb',
        consumer_secret='cccddd',
        access_token='111222',
        access_token_secret='333444'
    )

    # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

except TwitterSearchException as e:  # take care of all those ugly errors if there are some
    print(e)
