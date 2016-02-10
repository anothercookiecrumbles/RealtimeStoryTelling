##Introduction  

The TwitterStreamer subscribes to messages from Twitter provided:
- the message has a hashtag with the name of one of the "FANG" (Facebook, Amazon, Netflix, Google) companies or Apple. 
- the tweet is considered to be in English in Twitterverse. 

On the server-side, these tweets go through another filter that ensures that only those with a geolocation are propagated to the client over websocket.

On the client-side, there's a world map on which circles appear and fade-out. The location of these circles correspond to the latitude and longitude present on the tweets, and the colour of the circles are dependent on the dominant colour of their logo. So, for example, tweets with the hashtag #Netflix are a shade of red whereas tweets with #Amazon are a shade of orange. Google/Alphabet, on the other hand, has a polychromatic logo, so its shade of green is used, as none of the other "AFANG" companies have green as the dominant colour.

##Technical Specification
The server-side of this application was built using Python 3.5 with two third-party libraries:  
**tweepy**   
Version: 3.5   
Install: pip install tweepy  

**websocket_server**  
Version: 0.4  
Install: pip install websocket_server  

The client-side of this application was built using HTML, CSS and JavaScript. Additionally, while not needed to run the client, the following libraries were used: 
- [gdal (Geospatial Data Abstraction Library)](http://www.gdal.org/)
- [topojson] (https://github.com/mbostock/topojson)

##Starting everything up (the instructions below are for python3):  

To start up the server, in a terminal emulator (e.g. Terminal on OS X), run:  

  `python3 /path/to/Bootstrap.py`


To start up the client, in a terminal emulator  (e.g. Terminal on OS X), run:  

  `cd /path/to/client/directory`  
  `python3 -m http.server 8000`  
And then, if you're on OS X, you can run:   
  `/usr/bin/open -a "/Applications/Google Chrome.app" 'http://localhost:8000/index.html'`  
  
Or alternatively, just start Chrome manually and enter the URL: `http://localhost:8000/index.html` 

##Console output
**Server-side**

On the server-side, there are three kinds of messages:
- A number count: 
  For every ten messages we receive from Twitter, we spew out the the total number of messages received and the total number of messages received with geolocation. 
  Example:   
  `The total number of messages received is 730 and the number of messages with geolocation is 10.`

- A geolocated message: 
  Whenever we receive a message from Twitter that has the geolocation, we log the tweet, the user, the city and the latitude-longitude.  
  Example:    
  Tweet: Wondering what to watch on #Netflix on this cold day in the Big #Apple and hoping a #Google search can help.  
 by: acc_playground  
 from: Malvinas Argentinas, Argentina  
 coordinates: [-64.057945, -31.402278]  
 hashtag: Netflix  

- Client connection/disconnection messages. 

- Any exceptions that occur while parsing the tweets. 

The client isn't sent the entire message that's logged on the server. Instead, it only receives the hashtag and the latitude-longitude. An example of the client's console log is: 
`The hashtag amazon was used in a tweet from the coordinates -64.057945,-31.402278`

##A Slightly More Detailed Explanation  

###What does the data represent? 

While Twitter is a great source of streaming data, a [2013 USC study] (https://pressroom.usc.edu/twitter-and-privacy-nearly-one-in-five-tweets-divulge-user-location-through-geotagging-or-metadata/) said that only 20% of tweets are geolocated. So, filtering geolocated tweets isn't representative of the whole population. In fact, *The Atlantic's City Lab* had an article last year about [why most Twitter maps can't be trusted](http://www.citylab.com/housing/2015/03/why-most-twitter-maps-cant-be-trusted/388586/). Additional to that, Twitter now allows users to manually enter their location, which makes the data even more unreliable. 

Taking all of this into account, each message, that appears in the client, represents a user (or a bot) using one (or more) of the hashtags listed above while tweeting, where the actual location of the tweeter may or may not be accurate. Also, some of the company names are homonymous with other words (alphabet, apple, Amazon), which means that the tweets might not actually be about the company but about some other topic. 

###Expected message count
Based on testing, on average, the expected number of messages coming in from Twitter will be around the 3,500 mark, and of these approximately 50 will have geolocation. This means, on average, one in every seventy tweets will have geolocation – this is significantly less than the one in five that the USC study found. One could speculate that tech tweeters are more likely to switch off the geotagging of their tweets? However, there are no statistics to back that up. 

###Caveats
- If a single tweet has multiple hashtags, the hashtag that appears first in the tweet is used. 
- Twitter doesn't seem to stream certain types of tweets. So, for example, if I just created a tweet with "#Amazon," I wouldn't see it entering the streaming server. 
- If a tweet fails to parse, for whatever reason, it's dropped. 

###A slight segue

The rationale behind using the A-FANG companies as hashtags stems from the fact that, probability-wise, people are using one of those hashtags, which means that testing or assessing this shouldn't need one to wait for copious amounts of time. There was temptation to include Twitter and Tesla as well (Twitter on Twitter would be quite meta), but I was running out of easily distinguashable colours to use in the front-end! 

##To-Dos and Nice-To-Haves
- Unit tests (is not a nice-to-have but essential!) 
- Perhaps include a chart that has the count of tweets for each of the hashtags irrespective of whether geotags exist or not.
- On the server-side, a lot can be done to categorise the tweets correctly. For example, the retail mammoth "Amazon" shouldn't be confused with the "Amazon" jungles. 
- Perhaps make the map more of a heat-map instead of projecting transient circles? 
- Address the TODOs and comments in the code itself – there are some edge-cases that should be considered and handled carefully.

## References/Disclaimers

Other than searching the internet for syntactical help or debugging specific issues, I used the following resources: 
- [How to create a topojson file](https://bost.ocks.org/mike/map/)
- [Help getting D3 to draw the map without inexplicable exceptions](http://stackoverflow.com/questions/25062902/path-not-showing-in-d3-js-topojson-graph)
- [The Wikipedia Recent Changes Map](http://rcmap.hatnote.com/#en)
