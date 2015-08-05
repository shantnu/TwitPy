import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import pdb
import json
from collections import Counter
import sqlite3
from local_config import *

langs = \
{'ar': 'Arabic',
 'bg': 'Bulgarian',
 'ca': 'Catalan',
 'cs': 'Czech',
 'da': 'Danish',
 'de': 'German',
 'el': 'Greek',
 'en': 'English',
 'es': 'Spanish',
 'et': 'Estonian',
 'fa': 'Persian',
 'fi': 'Finnish',
 'fr': 'French',
 'hi': 'Hindi',
 'hr': 'Croatian',
 'hu': 'Hungarian',
 'id': 'Indonesian',
 'is': 'Icelandic',
 'it': 'Italian',
 'iw': 'Hebrew',
 'ja': 'Japanese',
 'ko': 'Korean',
 'lt': 'Lithuanian',
 'lv': 'Latvian',
 'ms': 'Malay',
 'nl': 'Dutch',
 'no': 'Norwegian',
 'pl': 'Polish',
 'pt': 'Portuguese',
 'ro': 'Romanian',
 'ru': 'Russian',
 'sk': 'Slovak',
 'sl': 'Slovenian',
 'sr': 'Serbian',
 'sv': 'Swedish',
 'th': 'Thai',
 'tl': 'Filipino',
 'tr': 'Turkish',
 'uk': 'Ukrainian',
 'ur': 'Urdu',
 'vi': 'Vietnamese',
 'zh_CN': 'Chinese (simplified)',
 'zh_TW': 'Chinese (traditional)'
 }

swear_words = ["fuck", "shit", "bitch", "idiot"]

love_words = ["love", "thank", "happy", "bless"]


class Twit_utils():

    def __init__(self, api):
        self.api = api


    def get_tweet_html(self, id):
        oembed = api.get_oembed(id=id, hide_media = True, hide_thread = True)

        tweet_html = oembed['html'].strip("\n")

        return tweet_html


class stats():

    def __init__(self):
        self.lang = []
        self.top_lang = []
        self.love_words = 0
        self.swear_words = 0
        self.top_tweets = []

    def add_lang(self, lang):
        self.lang.append(lang)

    def add_top_lang(self, top_lang):
        self.top_lang.append(top_lang)

    def love_word_found(self):
        self.love_words += 1

    def swear_word_found(self):
        self.swear_words += 1

    def save_top_tweets(self, tweet_html):
        self.top_tweets.append(tweet_html)

    def get_stats(self):
        return self.lang, self.top_lang, self.love_words, self.swear_words, self.top_tweets

class listener(StreamListener):

    def __init__(self, stats_obj, twit_utils):
        self.count = 0
        self.stats_obj = stats_obj
        self.twit_utils = twit_utils

    def on_data(self, data):
        try:            
            json_data = json.loads(data)
            #print(json_data)

            tweet = json_data["text"]

            for l in love_words:
                if l in tweet.lower():
                    self.stats_obj.love_word_found()

            for l in swear_words:
                if l in tweet.lower():
                    self.stats_obj.swear_word_found()

            retweet_count = json_data["retweeted_status"]["retweet_count"]

            self.stats_obj.add_lang(langs[json_data["lang"]])

            if retweet_count > 10000:
                print (tweet, retweet_count, langs[json_data["lang"]])
                self.stats_obj.add_top_lang(langs[json_data["lang"]])
                tweet_html = self.twit_utils.get_tweet_html(json_data['id'])
                self.stats_obj.save_top_tweets(tweet_html)

            self.count += 1

            if self.count == 500:
                return False

            return True

        except:
            #print("SHAN ERR")
            #pdb.set_trace()
            pass
                 

    def on_error(self, status):
        print("IN on error")
        pdb.set_trace()
        print(status)
        
auth = tweepy.OAuthHandler(cons_tok, cons_sec)
auth.set_access_token(app_tok, app_sec)

api = tweepy.API(auth)
twit_utils = Twit_utils(api)

db = "./twit_data.db"

conn = sqlite3.connect(db)
c = conn.cursor()

s = stats()
try:
    twitterStream = Stream(auth, listener(s, twit_utils))
    twitterStream.sample()
except Exception as e:
        print("Error. Restarting Stream.... Error: ")
        print(e.__doc__)
        #print(e.message)

lang, top_lang,love_words, swear_words, top_tweets = s.get_stats()

print(Counter(lang))
print(Counter(top_lang))
print("Love Words {} Swear Words {}".format(love_words, swear_words))

c.execute("INSERT INTO lang_data VALUES (?,?, DATETIME('now'))", (str(list(Counter(lang).items())), str(list(Counter(top_lang).items()))))

c.execute("INSERT INTO love_data VALUES (?,?, DATETIME('now'))", (love_words, swear_words))

for t in top_tweets:
    c.execute("INSERT INTO twit_data VALUES (?, DATETIME('now'))", (t,))

conn.commit()
conn.close()


#twitterStream.filter(languages=["en"])

#tt = tweepy.Cursor(api.search, q = "python", since_id = 623488361030750208).items(5)

#for t in tt:
    #print(t.text)



db = "./twit_data.db"

conn = sqlite3.connect(db)
c = conn.cursor()

trends = api.trends_place(1)
trend_data = []

for trend in trends[0]["trends"][:5]:
    #print(trend['name'])
    trend_tweets = []
    trend_tweets.append(trend['name'])
    tt = tweepy.Cursor(api.search, q = trend['name']).items(3)

    

    for t in tt:
        tweet_html = twit_utils.get_tweet_html(t.id)
        trend_tweets.append(tweet_html)
        #print(tweet_html)

    trend_data.append(tuple(trend_tweets))

c.executemany("INSERT INTO trend_data VALUES (?,?,?,?, DATETIME('now'))", trend_data)



conn.commit()
conn.close()

'''
api.get_oembed(id=626415779202920448)
Out[76]: 
{'author_name': 'Cerise || Rabbit',
 'author_url': 'https://twitter.com/AylinTheMuffin',
 'cache_age': '3153600000',
 'height': None,
 'html': '<blockquote class="twitter-tweet"><p lang="de" dir="ltr">straub was bald <a href="https://twitter.com/hashtag/TodaysCubeFansWillNeverKnow?src=hash">#TodaysCubeFansWillNeverKnow</a></p>&mdash; kay (@frickgraser) <a href="https://twitter.com/frickgraser/status/626088782790443008">July 28, 2015</a></blockquote>\n<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>',
 'provider_name': 'Twitter',
 'provider_url': 'https://twitter.com',
 'type': 'rich',
 'url': 'https://twitter.com/AylinTheMuffin/statuses/626415779202920448',
 'version': '1.0',
 'width': 550}
'''
'''
1. Most pop tweets
2. Lang of all tweets as bar
3. Lang of top tweets as pie 
4.  Swear vs kind words as donut chart
Something with gauge chart- cool! Maybe swear vs good- show in both donut and gague
'''    