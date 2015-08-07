import unittest
import sqlite3
from twit import *

class TestTwit(unittest.TestCase):
    def setUp():
        self.conn = sqlite3.connect(":memory:")
        num_tweets_to_grab = 5
        retweet_count = 0
        self.twit = TwitterMain(conn, num_tweets_to_grab, retweet_count)

    def test_streaming_data():
        self.twit.get_streaming_data()
    def tearDown():
        self.conn.close()

