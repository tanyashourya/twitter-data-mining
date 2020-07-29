import os
import tweepy as tw
import pandas as pd
import mysql.connector
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="twitter_db"
)

# Fill the X's with the credentials obtained by  
# following the above mentioned procedure. 
consumer_key = "XXXX" 
consumer_secret = "XXXX"
access_token = "XXXX"
access_token_secret = "XXXX"
bearer_token="XXXX"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = "#hashtag"
date_since = "2020-07-20"

# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(20)

for tweet in tweets:
    print(tweet.text)
    mycursor = mydb.cursor()
    sql = "INSERT INTO twitter (id, tweet_list) VALUES (%s, %s)"
    val = (tweet.user.name,tweet.text)
    mycursor.execute(sql, val)
    mydb.commit()
    wr.writerow(tweets)