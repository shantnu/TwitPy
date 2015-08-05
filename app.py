from flask import Flask, render_template
app = Flask(__name__)
import sqlite3
import ast


def read_data():
    db = "./twit_data.db"

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * from lang_data ORDER BY datetime DESC LIMIT 1")

    result = c.fetchone()
    lang = ast.literal_eval(result['language'])
    top_lang = ast.literal_eval(result['top_language'])

    c.execute("SELECT * from twit_data  ORDER BY top_tweet DESC LIMIT 10")
    result = c.fetchall()
    tweets = []

    for tweet in result:
        tweets.append(tweet['top_tweet'])


    c.execute("SELECT * from love_data ORDER BY datetime DESC LIMIT 1")

    result = c.fetchone()
    love_words = result['love_words']
    swear_words = result['swear_words']

    c.execute("SELECT * from country_data ORDER BY datetime DESC LIMIT 1")

    result = c.fetchone()
    country = ast.literal_eval(result['country'])

    trend = []
    trend_tweet = []

    c.execute("SELECT * from trend_data ORDER BY datetime DESC LIMIT 5") 
    result = c.fetchall()

    for r in result:
        trend.append(r['trend'])
        trend_tweet.append(r['trend_id1'])
        trend_tweet.append(r['trend_id2'])
        trend_tweet.append(r['trend_id3'])

    conn.close()

    return lang, top_lang, tweets, love_words, swear_words, country, trend, trend_tweet



@app.route("/")
def main():

    language_data = []
    top_language_data = []
    words_data = []
    words_data_gauge = []
    country_data = []


    lang, top_lang, tweets, love_words, swear_words, country, trend, trend_tweet = read_data()
    for l in lang:
        language_data.append([l[0], l[1], l[1]])

    for t in top_lang:
        top_language_data.append([t[0], t[1], t[1]])

    words_data.append(['love_words', love_words, love_words])
    words_data.append(['swear_words', swear_words, swear_words])

    words_data_gauge.append(['Label', 'Value'])
    words_data_gauge.append(['love_words', love_words])
    words_data_gauge.append(['swear_words', swear_words])

    country_data.append(['Country', 'Popularity'])

    for coun in country:
        country_data.append([coun[0], coun[1]])


    return render_template('index.html', language_data = language_data, top_language_data = top_language_data, tweets = tweets, words_data = words_data, \
                            words_data_gauge = words_data_gauge, country_data = country_data,  trend = trend, trend_tweet = trend_tweet)

if __name__ == "__main__":
    app.run(debug = True)


