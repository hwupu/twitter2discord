#!/usr/bin/env python3
"""
1. Take JSON string as input
2. Re-structure the data
3. POST to Discord webhook
"""

__author__ = "@hwupu"
__version__ = "0.0.1"
__license__ = "MIT"

import sys
import json
import requests
import sqlite3
from sqlite3 import Error

# Database connection
conn = None

# Webhook url
webhook_url = None

def parse():
    """ Prepare the data to post """
    source = sys.stdin.readline()
    source = json.loads(source)
    
    tweets = source['data']
    users = {user['id']: user for user in source['includes']['users']}
    media = {medium['media_key']: medium for medium in source['includes']['media'] if medium['type'] == 'photo'}
    referrals = {tweet['id']: tweet for tweet in source['includes']['tweets']}

    for tweet in tweets:
        t = tweet
        text = t['text']

        if 'referenced_tweets' in tweet:
            key = tweet['referenced_tweets'][0]['id']
            t = referrals[key]

        if hasTweetBeenPosted(t['id']):
            print('Tweet has been posted before: {}'.format(t['id']))
            continue
        else:
            attachments = [media[m] for m in t['attachments']['media_keys'] if m in media]
            if len(attachments) == 0:
                print('Tweet has no photo: {}'.format(t['id']))
                continue

            user = users[t['author_id']]
            
            print('')
            print('Posting tweet: {}'.format(t['id']))
            print('username', '{} (@{})'.format(user['name'], user['username']))
            print('avatar_url', user['profile_image_url'])
            print('content', text)
            for a in attachments:
                print('embeds.image.url', a['url'])

            payload = {
                'username': '{} (@{})'.format(user['name'], user['username']),
                'avatar_url': user['profile_image_url'],
                'content': text,
                'embeds': [ {'image': {'url': a['url']}} for a in attachments],
            } 
            post(payload)
            storeTweetToDatabse(t['id'])


def post(payload):
    """ POST to Discord webhook """
    result = requests.post(webhook_url, json=payload)
    if 200 <= result.status_code < 300:
        print(f"Webhook sent {result.status_code}")
    else:
        print(f"Not sent with {result.status_code}, response:\n{result.json()}")


def hasTweetBeenPosted(tweet_id: int):
    """ Check if tweet_id exist in database, return True if exist """
    cur = conn.cursor()
    cur.execute("SELECT id FROM posted_tweets WHERE id = ?", (tweet_id,))
    data=cur.fetchall()
    return len(data) != 0


def storeTweetToDatabse(tweet_id: int):
    """ Save tweet_id into database, except record doesn't exist """
    cur = conn.cursor()
    cur.execute("INSERT INTO  posted_tweets (id) VALUES (?)", (tweet_id,))
    conn.commit()


def connect_database():
    """ Create connection to database or initial one if empty """
    try:
        global conn
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS posted_tweets (id INT)")
        conn.commit()
    except Error as e:
        print(e)
        raise e


def close_databse():
    """ Close connection to database """
    if conn:
        conn.close()


def load_config():
    """ Load configurations """
    try:
        global webhook_url
        f = open('config.json', 'r')
        config = json.load(f)
        if 'webhook_url' in config:
            webhook_url = config['webhook_url']
        else:
            print('No webhook url found.')
            exit(-1)
    except IOError as e:
        print('Configuration can not be loaded.')
        raise e
    finally:
        if f:
            f.close()


def main():
    """ Main entry point of the app """
    load_config()
    connect_database()
    parse()
    close_databse()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

