import tweepy
from pprint import pprint
from time import sleep
# from credentials import *
import markovify
import datetime
import feedparser
import ssl
import csv
import itertools
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']

def check_rss():
    ssl._create_default_https_context = ssl._create_unverified_context
    d = feedparser.parse('https://www.theonion.com/rss')

    headlines_list = []

    with open('headlines.csv', 'r+') as headlines:
        
        # check all the headlines in the rss feed
        for entry in d['entries']:

            # get the headline
            headline = entry['title']

            reader = csv.reader(headlines, delimiter=',')

            # put first 1000 headlines into list, should be enough
            for row in itertools.islice(reader, 1000):
                headlines_list.append(row[0])

            # add new headlines to csv file
            if headline in headlines_list:
                pass
            else:
                writer = csv.writer(headlines, delimiter=',')
                writer.writerow([headline])


def make_headline():
    # Get raw text as string.
    with open("headlines.csv") as headlines:
        text = headlines.read()

    # Build the model.
    text_model = markovify.NewlineText(text, state_size=3)

    # make a new headline no more than 280 characters long
    return text_model.make_short_sentence(280)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
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

check_rss()
update_status()
