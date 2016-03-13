#This script uses Flask, a web framework, that easily allows us to route http
#requests.
#It exposes an  API which others can access over http (http://<server_name>:5000)
#to get some information about the streaming dataset. The server_name here is the
#server on which this is running.  This API exposes the following methods:
#i) histogram(): This shows the shape of the distribution. It is the ratio
#between the number of edits made for a certain wiki to the number of edits
#made across all wikis. This function is based on the instructions we received
#in class. It can be accessed by: http://<server_name>:5000/histogram.
#ii) entropy(): This shows the predictability of the underlying data. While for
#the most part, the data should be fairly predictable, any spikes or troughs
#could indicate that a certain wiki has unusually high or low activity, which
#can consequently be investigated. Like histogram(), this function is based on
#instructions received in class. It can be accessed by:
#http://<server_name>:5000/entropy
#iii) probability(): The probability of each of each edit belonging to a certain
#wiki against the whole universe of wikis. Again, this is based on the
#instructions received in class and can be accessed over:
#http://<server_name>:5000/probability
#iv) probability_site(): Retrieves probability for a single site. So, for
#example, you can call probability_site('en.wikipedia.org') and it'll return
#the probability that the site is en.wikipedia.org.
#
#The corresponding API script from class that was referred to can be found here:
#https://github.com/mikedewar/RealTimeStorytelling/blob/master/3/city-bot-api.py
#
#This dataset is dominated by edits to en.wikipedia.org (which has 15-20% of
#the edits). However, commons.wikipedia.org and www.wikidata.org isn't that
#far behind with 14-17% of all edits.

import flask
from flask import request, render_template

import redis

import json
import numpy as np
import collections
from collections import defaultdict

#Initialises the Flask web application, i.e. once this piece of code is run,
#the Flask webserver is up and running. This is invoked by the main method at
#the bottom of this class.
app = flask.Flask(__name__)

#Opens the connection to the two Redis databases: db1, which holds data that
#helps determine the moving average; and db2, which holds details of the
#distribution and therefore allows us to calculate the entropy and  probability.
db1 = redis.Redis(db=0)
db2 = redis.Redis(db=1)

#Builds a histogram, i.e. uses the data in db2 to get the shape of the data
#present in the database. The X-Axis of this data is the unique wiki sites
#that exist at the given point in time. The Y-Axis is the ratio of that count
#to the total number of wiki edits.
def build_histogram():
  #Retrieves all the keys from the database. The keys here are a unique
  #arbitrary identifier, so using the keys along, we can't really do that much.
  keys = db2.keys()
  #A defaultdict defaults the value of the keys if no value exists. In plainer
  #terms, when we add a key to the dictionary, it'll automatically initialise
  #it to a zero value. For more details:
  #https://docs.python.org/2/library/collections.html#collections.defaultdict
  #This data defaultdict is used to collect the count of edits against each
  #wiki, where the key is the wiki servername and the value is the number of
  #edits.
  data = defaultdict(int)
  #Iterates through all the keys in order to get the wiki site. The site hasn't
  #been stored as tthe key as we need the key to expire every 30 minutes, and
  #the Redis key expiry policy doesn't allow that.
  for key in keys:
    #Retrieves the key from Redis and then pulls out the "site" field, which
    #contains the wiki site.
    item = db2.hget(key, "site")
    #Increments the counter for the given site by 1, thereby allowing us to keep
    #count of the edits made to that particular wiki.
    if (item != None):
      data[item.decode("utf-8")] += 1
  #Calculates all the edits made across all wikis (data.values() has the edits
  #made for every single wiki, so we can simply sum it up to get a count of  all edits.
  summed = sum(data.values())
  #Returns the ratio of the edits of each wiki against the total number of
  #edits.
  return {k:v/float(summed) for k,v in data.items()}

#When a client calls http://<server_name>:5000 or
#http://<server_name>:5000/histohtam, this returns a JSON representation
#of the data in the db2 database. All it does is invoke the build_
#histogram() function, and returns the output.
@app.route("/")
@app.route("/probability")
def histogram():
  return render_template('index.html')

#Returns a JSON list of site-frequency dictionaries, which is used to render
#the barchart at the front-end.
@app.route("/histogram")
def get_histogram():
  #First, we get all the data.
  data = build_histogram()
  items = []
  keys = data.keys()
  #...and then we iterate through the keys to find data with a higher frequency
  #than 0.001. The number was chosen arbitrarily. However, if we skipped this or
  #didn't do this, the chart looked cluttered and visually unappealing.
  for key in keys:
    frequency = data[key]
    if (frequency < 0.001):
      continue
    #Creates the list in the format we need the front-end to receive this data.
    items.append({"site":key, "frequency": data[key]})
  return json.dumps(items)

#When a client calls http://<server_name>:5000/entropy, this returns the
#current entropy across the entire dataset in db2.
@app.route("/entropy")
def entropy():
  histogram = build_histogram()
  #The formula used to calculate the entropy here is the one used in class.
  #This is based on Shannon's Theorem, which is explained in more detail here:
  #https://en.wikipedia.org/wiki/Entropy_(information_theory)
  return json.dumps({"entropy":(-sum([p*np.log(p) for p in
    histogram.values()]))})

#Returns the probability of each of the wiki entries based on the total number
#of wiki edits. This is invoked when a client calls http://<server_name>:5000/
#probability
def probability():
  histogram=build_histogram()
  #The total number of edits, as the sum of all edits against each wiki will
  #give you the count of the total edits.
  total = sum(histogram.values())
  #Creates a dictionary where the key is the wikiname and the value is the
  #probability for that specific key.
  data = {k: v/total for k,v in histogram.items()}
  return json.dumps(data)

@app.route('/probability/<site>')
def probability_site(site):
  site = site.strip()
  print('Getting probability for ' + site)
  probabilities = probability()
  probability_map = json.loads(probabilities)
  if site in probability_map:
    prob = probability_map.get(site)
    return "Probability is {0}".format(str(prob))
  else:
    return "Site {0} doesn't exist in the distribution.".format(site)


def probability_table():
  prob_map = json.loads(probability())
  keys = prob_map.keys()
  items = []
  #...and then we iterate through the keys to find the probability of each site
  for key in keys:
    prob = prob_map[key]
    #Creates the list in the format we need the front-end to receive this data.
    items.append({"site":key, "probability": prob_map[key]})
  return json.dumps(items)

#Invoked when a client calls http://<server_name>:5000/rate. This returns the
#rate of the distribution, i.e. the average difference between edit entries
#in milliseconds. This is done over a rolling period of 10 minutes.
#The chosen 10 minutes is arbitrary, but it seems like it is a sufficient amount
#of time to get a good idea of what the regular rate is.
@app.route("/rate")
def rate():
  #Retrieves all keys from the database that contains the deltas/diffs.
  keys = db1.keys()
  #Simply initialises the rate to 0 - mostly avoiding multiple else statements
  #in case anything goes awry. Here, in the worst-case (lack of data or zero
  #values), the rate will be 0... which is accurate.
  rate = 0
  #We only need to calculate the average if there is any data in the database.
  if len(keys):
    #Pulls out all the deltas from the database for each of the keys present.
    values = db1.mget(keys)
    #...and converts them into floats.
    deltas = [float(v) for v in values]
    #If there are any deltas present, then we can calculate the average rate.
    if (len(deltas)):
      #...and then we can calculate the average.
      rate = sum(deltas)/float(len(deltas))
  #For convenience, we always return in JSON format.
  return json.dumps({"rate":rate})

if __name__ == "__main__":
  app.run(debug = True)
