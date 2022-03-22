import schedule
import signal
import time
from subprocess import check_output
import requests
import json

from . import initializer

alive = True
watchlist = None
webhook_url = None
conn = None
query = None

def parse(raw_json):
    """ Prepare the data to post """
    source = json.loads(raw_json)
    
    tweets = source['data']
    users = {user['id']: user for user in source['includes']['users']}
    if 'media' in source['includes']:
        media = {medium['media_key']: medium for medium in source['includes']['media'] if medium['type'] == 'photo'}
    else:
        media = {}
    if 'tweets' in source['includes']:
        referrals = {tweet['id']: tweet for tweet in source['includes']['tweets']}
    else:
        referrals = {}

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
            
            #print('')
            print('Posting tweet: {}'.format(t['id']))
            #print('username', '{} (@{})'.format(user['name'], user['username']))
            #print('avatar_url', user['profile_image_url'])
            #print('content', text)
            #for a in attachments:
            #    print('embeds.image.url', a['url'])

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

def job1():
    out = check_output(["python",
                        "scout/search_tweets.py",
                        "--credential-file",
                        "config.yaml",
                        "--config-file",
                        "config.yaml",
                        "--query",
                        "({}) -is:reply has:media".format(query),
                        "--start-time",
                        "16m"])

    if out:
        parse(out)
    else:
        print('No new tweet found.')


def stop(self, *args):
    initializer.close_databse(conn)
    schedule.clear()
    
    global alive
    alive = False


def main():
    global watchlist
    global webhook_url
    global conn
    global query
    
    (watchlist, webhook_url) = initializer.get_watchlist()
    conn = initializer.connect_database()
    query = ' OR '.join(['from:{}'.format(w) for w in watchlist])
    
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    print('Start polling Twitters from watchlist every 15 minutes...')
    schedule.every(15).minutes.do(job1)
    schedule.run_all()

    while alive:
        schedule.run_pending()
        time.sleep(1)


