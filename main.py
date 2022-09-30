import secret
import re
import numpy as np
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
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
    r = [w for w in r]
    r = " ".join(word for word in r)
    return r

cleaned = [clean_tweet(tw) for tw in tweet_list]
#print('\n', cleaned)
#for t in cleaned:
    #print()
    #print(t)


#Define sentiments using textblob
sentiment_obj = [TextBlob(tweet) for tweet in cleaned]
sentiment_obj[0].polarity, sentiment_obj[0]

#Create a list
sentiment_val = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_obj]
#print(sentiment_val[0])

sentiemnt_dataframe = pd.DataFrame(sentiment_val, columns=['Polarity', 'Tweet'])

#print(sentiemnt_dataframe)

polarity_col = sentiemnt_dataframe['Polarity']
m = pd.Series(polarity_col)

pos_count = 0
neg_count = 0
neu_count = 0

for items in m:
    if items>0:
        print('Positive')
        pos_count += 1
    elif items < 0 :
        print('Negative')
        neg_count += 1
    else:
        print('Neutral')
        neu_count += 1

print(pos_count,neg_count,neu_count)

pie_labels = ["Positive", "Negative", "Neutral"]
population_share = [pos_count, neg_count, neu_count]

figureObject, axesObject = plt.subplots()

axesObject.pie(population_share, labels = pie_labels, autopct='%1.2f', startangle = 90)

axesObject.axis('equal')
plt.show()