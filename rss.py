import feedparser
import ssl
import csv
import itertools


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
