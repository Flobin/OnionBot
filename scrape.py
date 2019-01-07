import requests
from bs4 import BeautifulSoup
import csv
from time import sleep

# this is just to seed the first elements

headlines_list = []

base_url = 'https://www.theonion.com/'
extra = ''

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
        headlines_class = page_content.find_all(class_='headline')

        # for each headline, get the text and add it if it doesn't exist yet
        for item in headlines_class:
            headline = item.text
            if headline in headlines_list:
                pass
            else:
                writer = csv.writer(headlines, delimiter=',')
                writer.writerow([headline])

        # find the load more button to load the next page
        load_more_button = page_content.find(attrs={'class': 'load-more__button'})
        load_more_link = load_more_button.find('a').get('href')

        # increase the counter, build the next page link
        counter += 1
        extra = load_more_link
        # wait a little bit so I don't DDOS the onion
        sleep(0.05)
