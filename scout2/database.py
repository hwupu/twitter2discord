# Store posted tweets ID to prevent depulicate posing
import sqlite3

def connect():
    """ Create connection to database or initial one if empty """
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS posted_tweets (id INT)")
    conn.commit()
    return conn

def hasTweetBeenPosted(tweet_id: int) -> bool:
    """ Check if tweet_id exist in database, return True if exist """
    cur = conn.cursor()
    cur.execute("SELECT id FROM posted_tweets WHERE id = ?", (tweet_id,))
    data=cur.fetchall()
    return len(data) != 0


def close(conn):
    """ Close connection to database """
    if conn:
        conn.close()
