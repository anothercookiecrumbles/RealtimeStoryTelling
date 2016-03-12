from socketIO_client import SocketIO, BaseNamespace

import sys

"""
Sets up a subscription to Wikipedia to get the "recent changes."
The instructions on how to set up the "Recent Changes" stream are here:
  https://www.mediawiki.org/wiki/API:Recent_changes_stream
Additionally, a JavaScript example, which I've referenced pretty heavily, is here:
  http://codepen.io/Krinkle/pen/laucI/?editors=101
I've also referenced the SocketIO Python library, which is here:
  https://pypi.python.org/pypi/socketIO-client
There is an incompatibility in the latest version of SocketIO and an earlier
version must be used. To install the compatible version, use this command:
  sudo pip install "socketIO_client==0.5.6"
More details about the SocketIO compatibility issue can be found here:
  https://phabricator.wikimedia.org/T125059
  https://phabricator.wikimedia.org/T91393
"""
class Wiki(BaseNamespace):
  #Invoked each time an edit occurs on any wiki page, with details about the
  #change.
  def on_change(self, change):
    try:
      if ("server_name" in change) and ("timestamp" in change):
        print('{"wiki": "%(server_name)s", "timestamp": "%(timestamp)s"}' % change)
        sys.stdout.flush()
    except Exception as ex:
      pass

  #Invoked when we successfully connect to the wikipedia stream.
  def on_connect(self):
    #On successful connection, we need to specify which sites we want to
    #subscribe to. For the sake of this assignment, we are subscribing to all
    #sites. e.g.: wikibooks, wikimedia, and all the different regional
    #wikipedias.
    self.emit('subscribe', '*')

#Setsup connection to the "recent changes" Wikipedia stream. Instructions can be
#found here: https://www.mediawiki.org/wiki/API:Recent_changes_stream. The Wiki
#class is added as the callback, such that any message from the stream can be
#processed by the Wiki class.
socketIO = SocketIO('stream.wikimedia.org', 80, Wiki)
#Defines the channel we are subscribing to. "rc" means "recent changes."
socketIO.define(Wiki, '/rc')
socketIO.wait(seconds=1000)
