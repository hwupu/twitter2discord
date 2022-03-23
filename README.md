# My custom Twitter to Discord bot

still messy...

But, it can pull tweets every 15 minutes, and post to Discord via webhook. It will look at the Twitter IDs in `watchlist`, and grab the only the tweets that has image.

## Setup

1. `python3 -m venv venv`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`
1. Add Twitter API v2 token to `config.ymal`
1. Add Discord webhook URL to `watchlist.json`
1. Add your own favorite list of Twitter IDs to `watchlist.json`
1. `python -m scout`
