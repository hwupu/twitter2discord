# My custom Twitter to Discord bot

still messy...

## Setup

1. `python3 -m venv venv`
1. `source venv/bin/activate`
1. Add `.twitter_keys.ymal`
1. `python scripts/search_tweets.py --credential-file .twitter_keys.yaml | python scripts/post_tweets.py`
