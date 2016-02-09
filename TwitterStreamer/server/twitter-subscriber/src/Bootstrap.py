from src.TwitterSubscriber import TwitterSubscriber
from src.TwitterListener import TwitterListener
from src.WebSocketSender import WebSocketSender

"""As the name suggests, the bootstrapper."""

"""The configuration file that holds configuration in key-value pairs. An example entry is "Port=8080".
Note: Leading/trailing whitespaces will be stripped, so you could easily have: "Port = 8000" as well."""
CONFIG_FILE="../config/config.cfg"

def main():
    """Initialises the WebSocketSender, which creates the WebSocket connection and streams data down."""
    sender = WebSocketSender()

    """Initialises the TwitterListener, which has a reference to the WebSocketSender, simply to be able to _send_
    messages down to the client(s)."""
    listener = TwitterListener(sender)

    """Pulls out OAuth keys from the configuration file, which is needed to authenticate with Twitter.
    TODO: Should really look into making this more elegant. For example, if any of the keys or values had an "=",
    this wouldn't work as expected. For now, this isn't the case, so something to come back to."""
    oauthKeys = {}
    try:
        with open(CONFIG_FILE) as config:
            for line in config:
                if not line.strip():
                    (key, value) = line.split("=")
                    oauthKeys[key.strip()] = value.strip()
    except FileNotFoundError as ex:
        print("Unable to find the configuration {}. Please ensure that it exists in the correct location."
              .format(CONFIG_FILE))
        raise FileNotFoundError("No file exists: {}".format(CONFIG_FILE))

    """Create the TwitterSubscriber object, which in turn initializes Tweepy, which in turn authorises the connection
    with Twitter."""
    subscriber = TwitterSubscriber(listener, oauthKeys)

    """Subscribe to tweets. Perhaps it might be nice to allow users to input the "track" they're interested in, and
    stream the data accordingly?"""
    subscriber.subscribeTweets()

if __name__ == "__main__":
    main()