import json

"""
Class that "listens" to responses from the Twitter Streaming API once the {@class TwitterSubscriber} starts
subscribing to data in {@class TwitterSubscriber#subscribeTweets}.
As this assignment is relatively small and straightforward, as things stand, this class doesn't handle edge-cases,
failures or exceptions, which it really should.
All methods in this class are adhere to the interface mandated by Tweepy, i.e. the listener that's passed into Tweepy
expects an implementation of the below methods. Not all of these functions are needed by our application, but, to
avoid nasty crashes, simply adding empty implementations of all non-essential methods (for our purposes) supported by
the class StreamListener(object) in Tweepy's streaming module. Without these empty implementationz, there's a chance
of the dreaded AttributeErrors.
"""


class TwitterListener:

  def __init__(self, webSocketSender, hashtags):
    self.webSocketSender = webSocketSender
    self.hashtags = hashtags

  def on_data(self, data):
    """
    Invoked whenever a new message is streamed from Twitter.
    As the assignment intends to map the tweets, it pulls out the latitude-longitude from the tweet, provided the
    location is available. If not, the tweet is silently dropped -- mostly because, well, how do you map something
    sans latitude and longitude?
      :param data: The entire Twitter message in the JSON format. From here, we can extract whichever values we
        want to send to the front-end.
    """
    dataToSend = {}
    try:
      dataInJson = json.loads(data)
      if "place" in dataInJson and dataInJson["place"] is not None:
        coordinates = dataInJson["place"]["bounding_box"]["coordinates"][0][0]

        numberOfHashtags = len(dataInJson["entities"]["hashtags"])
        """Support for multiple hashtags in the same tweet. If there are multiple hashtags in a tweet, we'll iterate
        through all the hashtags present, and use the first hashtag that's in our array of HASHTAGS (i.e. the array
         of hashtags we subscribed to). This does mean that if multiple "hashtags of interest" exist on the tweet,
         the rest will be discarded. This is mostly because of how the UI handles the hashtag: Based on the company,
         the UI will put a point on the map, where the colour of the point is based on the dominant colour of the
         company's logo.
        """
        if (numberOfHashtags > 0):
          iterator = iter(dataInJson["entities"]["hashtags"])
          for tag in iterator:
            if ('#'+tag["text"].lower()) in self.hashtags:
              hashtag = tag["text"]
              break

        print("Tweet: {} \n by: {} \n from: {} \n coordinates: {} \n hashtag: {} \n"
                  .format(dataInJson["text"], dataInJson["user"]["screen_name"],
                          dataInJson["place"]["full_name"], coordinates, hashtag))

        dataToSend['coordinates'] = coordinates
        dataToSend['hashtag'] = hashtag
    except Exception as ex:
      print("Caught exception while parsing the tweet.")
      print(ex)
      pass

    try:
      if dataToSend:#empty dictionaries evaluate to false in Python.
        self.webSocketSender.send(json.dumps(dataToSend))
    except Exception as ex:
      print("Caught exception while attempting to send the tweet over websocket.")
      print(ex)
      pass

  def on_exception(self, error):
    """Simply prints out an exception if one occurs.
      :param error: The error string received from upstream (Twitter) when an exception occurs.
    """
    print("Exception occured on the Twitter stream: {}".format(error))

  def on_error(self, error):
    """Called when a non-200 status code is returned.
       :param error: The error string received from upstream (Twitter) when an error occurs.
    """
    print("Received error from Twitter: {}".format(error))

  def on_connect(self):
    """Once we successfully connect to Twitter, this prints out "Connected" in all its glory."""
    print("Connected.")

  def on_timeout(self):
    """Invoked when the connection to Twitter times out."""
    print("Connection to Twitter timed out.")

  def on_status(self, status):
    """Invoked when there's a status change -- not entirely sure when this will be invoked.
      :param status: The new status when a status changes. Is there a way to capture the old status?
    """
    print("Updating status to {}".format(status))

  def on_event(self, event):
    """Called when a new event arrives. Again, not entirely sure when this'll be invoked.
      :param event: The new event that occurs upstream.
    """
    print("Received an event from Twitter:{}".format(event))

  def on_direct_message(self, msg):
    """Called when a direct messaged is received.
      :param msg: Invoked when we receive a direct message from Twitter.
    """
    pass

  def on_limit(self, track):
    """Called when a limitation notice is received for a given track.
      :param track: The track (effectively hashtag) for which we've hit our limit.
    """
    print("Limitation notice received for {}".format(track))

  def on_disconnect(self, notice):
    """Called when the client disconnects from Twitter.
      :param notice: The notice from Twitter that accompanies the disconnect.
    """
    print("Disconnected from Twitter with notice: {}".format(notice))

  def on_warning(self, notice):
    """Called when a warning is received.
      :param notice: The warning message from Twitter.
    """
    print("Received warning from Twitter with notice: {}".format(notice))

  def keep_alive(self):
    pass
