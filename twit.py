import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import pdb
import json
from collections import Counter
import sqlite3
from local_config import *
import re

db = "./twit_data.db"
countries_list = ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina', 'Burundi', 'Cameroon', 'Cape Verde', 'Central African Republic', 'Chad', 'Comoros', 'Congo', '"Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Swaziland', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe', 'Afghanistan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Burma (Myanmar)', 'Cambodia', 'China', 'East Timor', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', '"Korea', '"Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Nepal', 'Oman', 'Pakistan', 'Philippines', 'Qatar', 'Russian Federation', 'Saudi Arabia', 'Singapore', 'Sri Lanka', 'Syria', 'Tajikistan', 'Thailand', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Yemen', 'Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 'Vatican City', 'Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States', 'Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Nauru', 'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu', 'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela']
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
        oembed = self.api.get_oembed(id=id, hide_media = True, hide_thread = True)

        tweet_html = oembed['html'].strip("\n")

        return tweet_html


class stats():

    def __init__(self):
        self.lang = []
        self.top_lang = []
        self.love_words = 0
        self.swear_words = 0
        self.top_tweets = []
        self.countries = []

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

    def add_country(self, country):
        self.countries.append(country)

    def get_stats(self):
        return self.lang, self.top_lang, self.love_words, self.swear_words, self.top_tweets, self.countries

class listener(StreamListener):

    def __init__(self, stats_obj, twit_utils, num_tweets_to_grab, retweet_count):
        self.count = 0
        self.stats_obj = stats_obj
        self.twit_utils = twit_utils
        self.num_tweets_to_grab = num_tweets_to_grab
        self.retweet_count = retweet_count

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

            for country in countries_list:
                country_local = "\\b" + country + "\\b"
                if re.findall(country_local, tweet, flags = re.IGNORECASE):
                    self.stats_obj.add_country(country)

            # Hack for USA & UK, since no one uses its full name on Twitter
            # Yes, it's unfair I'm not doing this for all countries.
            if re.findall("\\busa\\b", tweet, flags = re.IGNORECASE):
                    self.stats_obj.add_country("United States")

            if re.findall("\\bbritain\\b", tweet, flags = re.IGNORECASE):
                    self.stats_obj.add_country("United Kingdom")

            retweet_count = json_data["retweeted_status"]["retweet_count"]

            self.stats_obj.add_lang(langs[json_data["lang"]])

            if retweet_count > self.retweet_count:
                print (tweet, retweet_count, langs[json_data["lang"]])
                self.stats_obj.add_top_lang(langs[json_data["lang"]])
                tweet_html = self.twit_utils.get_tweet_html(json_data['id'])
                self.stats_obj.save_top_tweets(tweet_html)

            self.count += 1

            if self.count == self.num_tweets_to_grab:
                return False

            return True

        except:
            #print("SHAN ERR")
            #pdb.set_trace()
            pass
                 

    def on_error(self, status):
        print("IN on error")
        #pdb.set_trace()
        print(status)

class TwitterMain():
    def __init__(self, conn, num_tweets_to_grab, retweet_count):
        '''
        num_tweets_to_grab: The number of tweets to grab. If this number is too big, Twitter blocks you temporarily, so keep it small.
        retweet_count: The number of times a tweet must have been retweeted for us to save it.
        '''
        self.auth = tweepy.OAuthHandler(cons_tok, cons_sec)
        self.auth.set_access_token(app_tok, app_sec)

        self.api = tweepy.API(self.auth)
        self.twit_utils = Twit_utils(self.api)

        self.conn = conn
        self.c = self.conn.cursor()

        self.s = stats()

        self.num_tweets_to_grab = num_tweets_to_grab
        self.retweet_count = retweet_count


    def get_streaming_data(self):
        try:
            twitterStream = Stream(self.auth, listener(self.s, self.twit_utils, self.num_tweets_to_grab, self.retweet_count))
            twitterStream.sample()
        except Exception as e:
                print("Error. Restarting Stream.... Error: ")
                print(e.__doc__)
                #print(e.message)

        lang, top_lang,love_words, swear_words, top_tweets, countries = self.s.get_stats()

        print(Counter(lang))
        print(Counter(top_lang))
        print("Love Words {} Swear Words {}".format(love_words, swear_words))
        print(Counter(countries))

        self.c.execute("INSERT INTO lang_data VALUES (?,?, DATETIME('now'))", (str(list(Counter(lang).items())), str(list(Counter(top_lang).items()))))

        self.c.execute("INSERT INTO love_data VALUES (?,?, DATETIME('now'))", (love_words, swear_words))

        for t in top_tweets:
            self.c.execute("INSERT INTO twit_data VALUES (?, DATETIME('now'))", (t,))

        self.c.execute("INSERT INTO country_data VALUES (?, DATETIME('now'))", (str(list(Counter(countries).items())),))

        self.conn.commit()



    def get_trends(self):
        trends = self.api.trends_place(1)
        trend_data = []

        for trend in trends[0]["trends"]:
            #print(trend['name'])
            trend_tweets = []
            trend_tweets.append(trend['name'])
            tt = tweepy.Cursor(self.api.search, q = trend['name']).items(3)
         
            for t in tt:
                tweet_html = self.twit_utils.get_tweet_html(t.id)
                trend_tweets.append(tweet_html)
                print(tweet_html)

            trend_data.append(tuple(trend_tweets))

        self.c.executemany("INSERT INTO trend_data VALUES (?,?,?,?, DATETIME('now'))", trend_data)

        self.conn.commit()


if __name__ == "__main__":
    num_tweets_to_grab = 2000
    retweet_count = 10000
    try:
        conn = sqlite3.connect(db)
        twit = TwitterMain(conn, num_tweets_to_grab, retweet_count)
        #twit.get_streaming_data()
        twit.get_trends()

    except Exception as e:
        print(e.__doc__)

    finally:
        conn.close()

