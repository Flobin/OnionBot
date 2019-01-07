import feedparser
import ssl
import csv


ssl._create_default_https_context = ssl._create_unverified_context
d = feedparser.parse('https://www.theonion.com/rss')

headlines_list = []

# only get first 200 rows, that should be enough
with open('headlines.csv', 'r+').readlines()[0: 199] as headlines:
    
    # check all the headlines in the rss feed
    for entry in d['entries']:

        # get the headline
        headline = entry['title']

        reader = csv.reader(headlines, delimiter=',')

        # put headlines into list
        for row in reader:
            headlines_list.append(row[0])

        # add new headlines to csv file
        if headline in headlines_list:
            pass
        else:
            writer = csv.writer(headlines, delimiter=',')
            writer.writerow([headline])
