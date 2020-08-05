import os
import tweepy as tw
import mysql.connector
import json
import re
from textblob import TextBlob 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="twitter_db"
)

# Fill the X's with the credentials obtained by  
# following the above mentioned procedure. 
access_token = "XXXX" 
access_token_secret = "XXXX"
consumer_key = "XXXX"
consumer_secret = "XXXX"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = "#dell"
date_since = "2020-07-01"

# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(500)

tweet_list = [tweet for tweet in tweets]

for tweet in tweet_list:
  username = tweet.user.screen_name
  location = tweet.user.location
  retweetcount = tweet.retweet_count
  hashtags = tweet.entities['hashtags']
  hashtags_str = ' '.join([str(elem) for elem in hashtags])
  text = tweet.text
  # text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
  analysis = TextBlob(str(text))
  if analysis.sentiment.polarity > 0: 
    sentiment = 'positive'
  elif analysis.sentiment.polarity == 0: 
    sentiment = 'neutral'
  else: 
    sentiment = 'negative'
  print(sentiment)
  mycursor = mydb.cursor()
  sql = "INSERT INTO twitter (id, tweet_list, location, retweet, hashtags, sentiment ) VALUES (%s, %s, %s, %s, %s, %s)"
  val = (username,text,location,retweetcount, hashtags_str, sentiment)
  mycursor.execute(sql, val)
  mydb.commit()

print('Scraping has completed!')