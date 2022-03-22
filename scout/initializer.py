import os
import json
import yaml
import sqlite3

def get_watchlist():
    """ Load configurations """
    f = None
    try:
        f = open('watchlist.json', 'r')
        j = json.load(f)
        return (j['watchlist'], j['webhook_url'])
    except FileNotFoundError as e:
        print('\033[1;31mConfiguration not found.\033[m')
        raise e
    except IOError as e:
        print('\033[1;31mConfiguration can not be loaded.\033[m')
        raise e
    finally:
        if f:
            f.close()


def connect_database():
    """ Create connection to database or initial one if empty """
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS posted_tweets (id INT)")
    conn.commit()
    return conn


def close_databse(conn):
    """ Close connection to database """
    if conn:
        conn.close()
