import os

import tweepy
#https://github.com/R3l3ntl3ss/HeavyMind_Bot
#https://medium.com/datadriveninvestor/how-i-created-a-twitter-bot-using-python-a68b917d133
#https://python-twitter.readthedocs.io/en/latest/index.html
#https://gist.github.com/gdsaxton/b0d36c10bbdb80e26b692a1d1a3e11de

consumer_key = str(os.environ.get('consumer_key', ''))
consumer_secret = str(os.environ.get('consumer_secret', ''))
access_token = str(os.environ.get('access_token', ''))
access_token_secret = str(os.environ.get('access_token_secret', ''))

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

import tweepy


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)


myStreamListener = MyStreamListener()
#myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
#myStream.filter(track=['influenza'])

from TwitterSearch import *

try:
    tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
    tso.set_keywords(['vaccines', 'cause', 'autism'])  # let's define all words we would like to have a look for
    # tso.set_language('en')  # we want to see German tweets only
    tso.set_include_entities(True)  # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

except TwitterSearchException as e:  # take care of all those ugly errors if there are some
    print(e)
