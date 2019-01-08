import tweepy
from pprint import pprint
from time import sleep
# from credentials import *
import markovify
import datetime
import feedparser
import ssl
import csv
from os import environ
import requests
from bs4 import BeautifulSoup

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
            for row in reader:
                headlines_list.append(row[0])

            # add new headlines to csv file
            if headline in headlines_list:
                pass
            else:
                writer = csv.writer(headlines, delimiter=',')
                writer.writerow([headline])
                headlines_list.append(headline) # have to put it in headlines_list as well otherwise you get doubles


def scrape_site():
    base_url = 'https://www.theonion.com/'
    extra = ''

    headlines_list = []

    with open('headlines.csv', 'r+') as headlines:

        # put existing headlines in list
        reader = csv.reader(headlines, delimiter=',')
        for row in reader:
            headlines_list.append(row[0])

        # start looping the pages
        for counter in range(0,2):
            response = requests.get(base_url + extra)
            html = response.content
            page_content = BeautifulSoup(html, "html.parser")

            # find all headlines
            headlines_data = page_content.find_all(attrs={'data-contenttype': 'Headline'})
            headlines_class = page_content.find_all(class_='headline')

            # for each headline, get the text and add it if it doesn't exist yet
            for item in headlines_data:
                headline = item.text
                if headline in headlines_list:
                    pass
                else:
                    writer = csv.writer(headlines, delimiter=',')
                    writer.writerow([headline])

            for item in headlines_class:
                headline = item.text
                if headline in headlines_list:
                    pass
                else:
                    writer = csv.writer(headlines, delimiter=',')
                    writer.writerow([headline]) # have to put it in headlines_list as well otherwise you get doubles

            # find the load more button to load the next page
            load_more_button = page_content.find(attrs={'class': 'load-more__button'})
            load_more_link = load_more_button.find('a').get('href')

            # increase the counter, build the next page link
            counter += 1
            extra = load_more_link


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
scrape_site()
update_status()
