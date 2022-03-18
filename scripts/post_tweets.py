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

def parse():
    """ POST to Discord webhook """
    source = sys.stdin.readline()
    source = json.loads(source)
    
    tweets = source['data']
    users = {user['id']: user for user in source['includes']['users']}
    media = {medium['media_key']: medium for medium in source['includes']['media']}
    referrals = {tweet['id']: tweet for tweet in source['includes']['tweets']}
    
    for tweet in tweets:
        t = tweet
        text = t['text']

        if 'referenced_tweets' in tweet:
            key = tweet['referenced_tweets'][0]['id']
            t = referrals[key]
    
        attachments = [media[m] for m in t['attachments']['media_keys']]
        user = users[t['author_id']]

        print('username', '{} (@{})'.format(user['name'], user['username']))
        print('avatar_url', user['profile_image_url'])
        print('content', text)
        for a in attachments:
            print('embeds.image.url', a['url'])
        print('')


def post():
    """ POST to Discord webhook """
    url = ''
    
    for tweet in tweets:
        data = {
            "content": tweet['text'],
        }
        result = requests.post(url, json=data)
        if 200 <= result.status_code < 300:
            print(f"Webhook sent {result.status_code}")
        else:
            print(f"Not sent with {result.status_code}, response:\n{result.json()}")
        print(json.dumps(data, indent=2))


def main():
    """ Main entry point of the app """
    parse()
    # post()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

