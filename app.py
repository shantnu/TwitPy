from flask import Flask, render_template
app = Flask(__name__)
import sqlite3
import ast

langs = [('Turkish', 6),
 ('Portuguese', 1),
 ('Arabic', 3),
 ('Korean', 1),
 ('French', 1),
 ('Russian', 1),
 ('English', 11),
 ('Spanish', 7),
 ('Polish', 1),
 ('Japanese', 11),
 ('Bulgarian', 1),
 ('Thai', 6)]


def read_data():
    db = "./twit_data.db"

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * from lang_data LIMIT 1")

    result = c.fetchone()
    lang = ast.literal_eval(result['language'])
    top_lang = ast.literal_eval(result['top_language'])    
    conn.close()

    return lang, top_lang



@app.route("/")
def main():

    language_data = []
    lang, top_lang = read_data()
    for l in lang:
        language_data.append([l[0], l[1], l[1]])
    return render_template('index.html', language_data = language_data)

if __name__ == "__main__":
    app.run(debug = True)


