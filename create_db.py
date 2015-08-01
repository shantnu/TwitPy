import sqlite3

db = "./twit_data.db"

conn = sqlite3.connect(db)
c = conn.cursor()

try:
    c.execute("drop table trend_data")
    c.execute("drop table twit_data")
    c.execute("drop table lang_data")
    c.execute("drop table love_data")
except:
    # Nothing to drop, do nothing.
    pass

cmd = "CREATE TABLE trend_data (trend TEXT, trend_id1 INT, trend_id2 INT, trend_id3 INT)"
c.execute(cmd)


cmd = "CREATE TABLE twit_data (top_tweet_id INT)"
c.execute(cmd)


cmd = "CREATE TABLE lang_data (language TEXT, top_language TEXT)"
c.execute(cmd)

cmd = "CREATE TABLE love_data (love_words INT, swear_words INT)"
c.execute(cmd)

conn.commit()

conn.close()