import sys
import json
import requests

source = sys.stdin.readline()
source = json.loads(source)

tweets = source['data']
users = {user['id']: user for user in source['includes']['users']}
media = {medium['media_key']: medium for medium in source['includes']['media']}
referrals = {tweet['id']: tweet for tweet in source['includes']['tweets']}

for tweet in tweets:
    t = tweet
    if 'referenced_tweets' in tweet:
        key = tweet['referenced_tweets'][0]['id']
        t = referrals[key]

    text = t['text']
    attachments = [media[m] for m in t['attachments']['media_keys']]
    user = users[t['author_id']]
    print(text, user, attachments)

exit()

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

