import csv
from selenium import webdriver
import time
import sys


# sys.setdefaultencoding('utf-8')

def scrape(hashtag):
    '''
    Extract tweets using the specified hashtag.
    Results are saved in a file <candidate>.csv
    '''

    browser = webdriver.Chrome(executable_path='/usr/local/Cellar/chromedriver/2.24/bin/chromedriver')
    url = 'https://twitter.com/search?l=&q=%23' + hashtag + '%20since%3A2016-11-01%20until%3A2016-11-08&src=typd&lang=en'
    browser.get(url)

    numberTweets = 0

    for i in range(0, 2):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        texts = browser.find_elements_by_css_selector('p.TweetTextSize.js-tweet-text.tweet-text')
        timestamps = browser.find_elements_by_css_selector('span._timestamp.js-short-timestamp')

        tweet_text = [t.text.encode("utf8") for t in texts]
        tweet_timestamp = [ts.text.encode("utf8") for ts in timestamps]

        numberTweets = len(tweet_text)

        with open('../gen/' + hashtag + '.csv', 'wb') as csvfile:
            fieldnames = ['text', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for text, timestamp in zip(tweet_text, tweet_timestamp):
                writer.writerow({'text': text, 'timestamp': timestamp})
    return numberTweets


def getTweets(hashtags, frame):
    n = 0
    for hashtag in hashtags:
        m = scrape(hashtag)
        n += m
    s = str(n) + " tweets extracted"
    frame.config(text=s)