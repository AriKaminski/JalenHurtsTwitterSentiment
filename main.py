import secret
import re
import numpy as np
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib as plt
import pandas as pd
from wordcloud import STOPWORDS, wordcloud
from better_profanity import profanity


#Access twitter data

auth = tweepy.OAuthHandler(secret.TWITTER_API_KEY, secret.TWITTER_API_KEY_SECRET)
auth.set_access_token(secret.TWITTER_ACCESS_TOKEN, secret.TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

query = input("Enter your criteria: ")

#Remove retweets
filtered = query + "-filter:retweets"

#Generate latest tweets
tweets = tweepy.Cursor(api.search_tweets, q=filtered, lang="en").items(100)

#Create a list of tweets gathered
list1 = [[tweet.text, tweet.user.screen_name, tweet.user.location] for tweet in tweets]

#List into dataframe
dframe = pd.DataFrame(data=list1, columns=['tweets','user','location'])

#Convert tweets into a list
tweet_list = dframe.tweets.to_list()


def clean_tweet(tweet):
    if type(tweet) == np.float64:
        return ""
    r = tweet.lower()
    r = profanity.censor(r)
    r = re.sub("'", "", r)
    r = re.sub("@[A-Za-z0-9_]+","", r)
    r = re.sub("#[A-Za-z0-9_]+","", r)
    r = re.sub(r'http\S+', '', r)
    r = re.sub('[()!?]', ' ', r)
    r = re.sub('\[.*?\]',' ', r)
    r = re.sub("[^a-z0-9]"," ", r)
    r = r.split()
    STOPWORDS = ["for", "on", "an", "a", "of", "and", "in", "the", "to", "from"]
    r = [w for w in r if not w in STOPWORDS]
    r = " ".join(word for word in r)
    return r

cleaned = [clean_tweet(tw) for tw in tweet_list]
print(cleaned)