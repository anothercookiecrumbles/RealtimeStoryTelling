##Background

This is the third assignment for the Realtime Storytelling class. 

There are over 50,000 edits made every hour across all Wikiepedia sites. These sites include en.wikipedia.org, fr.wikipedia.org and other regional/local sites. In addition, they also include wikibooks, wikidata and wikiquote. Pages are updated, categories are changed and new pages are added. For the most part, these changes are predictable and consistent. For example, it's hardly surprising that ~15% of all edits are made to en.wikipedia.org. But, where is the rest of the volume coming from? And, what does it mean if the edits on the English Wiki site drops down to 10% - where has the volume shifted? And is there an underlying reason as to why this trend has changed? 

For this assignment, we plug into the Wikipedia ["recent changes"](https://www.mediawiki.org/wiki/API:Recent_changes_stream) stream, and subscribe to changes across all Wikipedia sites, in order to identify where the changes are coming from, and to see what causes discrepencies to the what is considered to be "normal behaviour." For example, if the rate of change suddenly increases or decreases by a significant amount – what does that tell us? Or, if the entropy changes drastically? 

These items might just be numbers, but if we can contextualise the numbers and investigate them closer, it makes for the beginnings of an interesting story. After all, think of all the people who reference Wikipedia daily, irrespective of how reliable (or unreliable) the information is. 

From my observations while testing, the numbers are reasonably consistent at all times of the day on both, weekdays and weekends. This is across the many regional Wikipedia sites as well as the dedicated sites for books, data and quotes. Hence:
* I've used a ten-minute period for keys to expire in the Redis database, so our visibility into Wikipedia is always over the last ten minutes. This number was chosen arbitrarily after examining the data at different intervals at different points in time. There isn't much deviation in the numbers, which would lead me to believe that:
a) we won't glean anything significant from a twenty-minute window versus a ten-minute window;
b) any threshold breaches should be examined closely to determine the root cause
* The moving average has consistently been between 1 and 5, and hence I've chosen a breach threshold of +/- 10. A negative value indicates that there is more activity on Wikipedia than usual (or the rate of edits coming in are faster) whereas a positive rate indicates that there is less activity. 
* The entropy was consistently at 2, and hence the chosen breach level is 5, which indicates significantly higher entropy.
* For probabilities, I've flagged three Wikipedia sites that have always shown a consistent and reasonably high level of activitiy. There exists a dictionary that holds the expected probabilities and, on a breach, an alert is sent out. 

Like the previous assignment, alerts are sent out on a Slack channel. 


##Technical Specification 
The project was built using Python 3. 
It relies on the SocketIO client library that Wikipedia uses. To install it, you have to use version 0.5.6. You can install it with the following command:
sudo pip install "socketIO_client==0.5.6"
It also needs Flask, Redis and the official SlackClient for Python.


**Files**

Seven files exist in this project:
* wiki.py: This script opens the connection to the Wikipedia Recent Changes stream and receives a callback on a successful connection and on every single change. 
* diff.py: This scipt keeps track of the time deltas between edits, i.e. how much time has elapsed between the last edit message and the current one.
* insert_diff_into_redis.py: This script inserts the time deltas into Redis's default database (db=0)
* insert_dist_into_redis.py: For every single edit on every Wiki site, this script inserts an entry into Redis's database 1 (db=1)
* api.py: This script exposes a bunch of methods over HTTP, which clients can connect to, on port 5000. Methods include probability, entropy, hisogram and rate. 
* alert.py: This script flags an alert each time one (or more) of the specified thresholds for rate, entropy and probability have been breached. 
* slack.py: This script simply pushes out alerts to the given Slack channel. 

**Running the project**
* To get diffs into Redis:

`python wiki.py | python diff.py | python insert_diff_into_redis.py`

* To get the distribution into Redis:

`python wiki.py | python insert_dist_into_redis.py`

* To run the API:

`python api.py`

You can then run:
- http://localhost:5000 to get the distribution details.
- http://localhost:5000/entropy to get the entropy.
- http://localhost:5000/probability to get the probabilities across all the wikipedia sites 
- http://localhost:5000/probability/<site> to get the probability of a single site (e.g. http://localhost:5000/probability/commons.wikimedia.org)
- http://localhost:5000/rate to get the average of the deltas across messages 

* And to get alerts:

`python alert.py | python slack.py`

Note: To get the Slack integration to work, you'll have to enter your access token and channel – I could've added mine/driven it out of configuration, but then that would involve adding you to a(n) (ephemeral) channel. I wasn't sure if that was the right thing to do. 

##Additional Notes/Afterthoughts
For a lot of the Wiki sites, doing this project at an individual level would be significantly more interesting over a period of time. However, for the purpose of this assignment, I wanted a stream with a lot of data, which can't be guaranteed for the sites that are less frequently updated. Hence, the decision to use all sites in the Wikipedia realm. One could argue that you could narrow it down to a select twenty, but there's no telling at what point one of the sites will be doing something "interesting" and what that something "interesting" could be. 

##References/External Sources:
- https://github.com/mikedewar/RealTimeStorytelling/tree/master/
- https://docs.python.org/3.5/reference/
- http://redis.io/commands/
- https://www.mediawiki.org/wiki/API:Recent_changes_stream
- http://codepen.io/Krinkle/pen/laucI/?editors=101
- https://pypi.python.org/pypi/socketIO-client
- https://phabricator.wikimedia.org/T125059
- https://phabricator.wikimedia.org/T91393
- http://bl.ocks.org/Jverma/887877fc5c2c2d99be10
- http://stackoverflow.com/questions/19127035/what-is-the-difference-between-svgs-x-and-dx-attribute
