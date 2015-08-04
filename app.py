from flask import Flask, render_template
app = Flask(__name__)
import sqlite3
import ast


def read_data():
    db = "./twit_data.db"

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * from lang_data LIMIT 1")

    result = c.fetchone()
    lang = ast.literal_eval(result['language'])
    top_lang = ast.literal_eval(result['top_language'])

    c.execute("SELECT * from twit_data LIMIT 1")
    result = c.fetchone()
    tweet = result['top_tweet']
    conn.close()

    return lang, top_lang, tweet



@app.route("/")
def main():

    language_data = []
    lang, top_lang, tweet = read_data()
    for l in lang:
        language_data.append([l[0], l[1], l[1]])
    return render_template('index.html', language_data = language_data, tweet = tweet)

if __name__ == "__main__":
    app.run(debug = True)


