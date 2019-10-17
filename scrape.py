import requests
from bs4 import BeautifulSoup
import csv
from time import sleep

# this is just to seed the first elements

headlines_list = []

base_url = 'https://www.theonion.com/'
extra = ''

headline_existing_count = 0
headline_new_count = 0

with open('headlines.csv', 'r+') as headlines:

    # put existing headlines in list
    reader = csv.reader(headlines, delimiter=',')
    for row in reader:
        headlines_list.append(row[0])

    # start looping the pages
    for counter in range(0,1000):
        response = requests.get(base_url + extra)
        html = response.content
        page_content = BeautifulSoup(html, "html.parser")

        # find all headlines
        headlines_on_page = page_content.select('.content-meta__headline h6, .content-meta__headline h3, .content-meta__headline__wrapper h5, article.js_post_item h1')

        # for each headline, get the text and add it if it doesn't exist yet
        for item in headlines_on_page:
            headline = item.text
            if headline in headlines_list:
                headline_existing_count += 1
                pass
            else:
                headline_new_count += 1
                writer = csv.writer(headlines, delimiter=',')
                writer.writerow([headline])

        # find the load more button to load the next page
        load_more_link = page_content.find(attrs={'data-ga': '[["Front page click","More stories click"]]'}).get('href')

        # increase the counter, build the next page link
        counter += 1
        if load_more_link is not None:
            extra = load_more_link
        # wait a little bit so I don't DDOS the onion
        print(counter)
        print('existing headlines: {}'.format(headline_existing_count))
        print('new headlines: {}'.format(headline_new_count))
        sleep(0.05)
