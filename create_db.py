import sqlite3

db = "./twit_db.db"

conn = sqlite3.connect(db)
c = conn.cursor()

cmd = "CREATE TABLE twrend_data (trend TEXT, trend_tweet TEXT, last_updated_time TEXT)"
c.execute(cmd)


cmd = "CREATE TABLE twit_data (top_tweet TEXT, last_updated_time TEXT)"
c.execute(cmd)


cmd = "CREATE TABLE lang_data (language TEXT, top_language TEXT, last_updated_time TEXT)"
c.execute(cmd)

conn.commit()

conn.close()