import tweepy
from pprint import pprint
from time import sleep
from credentials import *
import markovify
import csv
import datetime

def make_headline():
    # Get raw text as string.
    with open("headlines.csv") as f:
        text = f.read()

    # Build the model.
    text_model = markovify.NewlineText(text, state_size=3)

    # make a new headline no more than 280 characters long
    return text_model.make_short_sentence(280)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def update_status():
    tweet = make_headline()
    try:
        api.update_status(tweet)
        log_write = open("log.txt", "w")
        log_write.write(str(now + ' - ' + tweet))
        log_write.close()
    except tweepy.TweepError as e:
        log_write = open("log.txt", "w")
        log_write.write(str(now + ' - ' + e.reason))
        log_write.close()

update_status()
