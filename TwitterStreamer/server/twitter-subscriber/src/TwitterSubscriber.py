import tweepy
from tweepy import Stream

"""The TwitterSubscriber sets up the connection to Twitter (including authentication, etc.) and subscribes to tweets."""


class TwitterSubscriber:

    def __init__(self, twitterListener, config):
        """Initialises Tweepy, the API we're using to Twitter-verse.
            :param: twitterListener: Handles all callbacks from Twitter, including on_connected, on_message,
                on_exception, etc.
            :param: config: dictionary that holds the configuration required for OAuth.
        """
        self.auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
        self.auth.secure = True
        self.auth.set_access_token(config["access_token"], config["access_token_secret"])
        self.api = tweepy.API(self.auth)
        self.twitterListener = twitterListener

    def subscribeTweets(self):
        """Starts subscribing to tweets which have one (or both) of the two hashtags: #Twitter and #RIPTwitter."""
        stream = Stream(self.auth, self.twitterListener)
        stream.filter(track=['#StarTrek'], languages=['en'])
