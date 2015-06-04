# -*- coding: utf-8 -*-

__author__ = 'Esther Seyffarth'
import tweepy
import random
import codecs
import time
import re
import config

def login():
    # for info on the tweepy module, see http://tweepy.readthedocs.org/en/

    # Authentication is taken from config.py
    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_token_secret = config.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api


def get_corpus_content(corpus_path):
    corpus = codecs.open(corpus_path, "r")
    content = []
    for line in corpus:
        line = line.strip()
        line = line.split("+++$+++")[-1]        # keep only text of current line
        line = re.sub("<[^<]+", "", line)       # remove formatting tags
        line = re.sub("\\'", "'", line)         # remove apostrophe encoding
        line = re.sub(u"\x92", "'", line)       # normalize apostrophes
        line = re.sub(u"\x93|\x94", '"', line)  # normalize quotation marks

        if line.endswith("?"):
            content.append(line)    # append only question lines to content

    return set(content)


def tweet_something(questions):
    api = login()
    output = random.sample(questions, 1)[0].strip()     # choose & clean up line before tweeting it
    if len(output) < 141:
        api.update_status(status=output)
        print output

corpus_path = "D:/Korpora/CornellMovieDialogsCorpus/movie_lines.txt"
questions = get_corpus_content(corpus_path)
while True:
    tweet_something(questions)
    time.sleep(1800)        # tweet once every half hour