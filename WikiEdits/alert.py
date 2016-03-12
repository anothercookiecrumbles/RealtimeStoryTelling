#This script uses the API built to alert a system incase there's a breach in the
#rate threshold, entropy threshold, or if the behaviour is more unlikely than
#that expected. Instead of polling Redis, this script will simply call api.py,
#which already calculates the rate, entropy and probability. This avoids code
#duplication and maintenence, which is nice.

import json
import sys
import time

import urllib.request

#This URL exposes the API that we are interested in.
geturl = "http://localhost:5000/"

#The rate threshold, i.e. if the rate is less than or more than this, we should
#get an alert as something funky is going on. The rate threshold has been
#determined by observed movements in the rate across multiple times of the day,
#over weekends and weekdays.
rate_threshold = 10

#The entropy threshold, i.e. if the entropy is less than this, it means that the
#behaviour is becoming more random. The entropy threshold has been determined by
#observed entropies at random points in time, across multiple times of the day
#and over weekdays and weekends.
entropy_threshold = 5

#There are tons of pages in the Wikipedia realm. For the purpose of tracking
#probabilities, I've identified the three most editted pages. If the probability
#of any of these three go down, an alert will be dispatched. The rates have been
#determined based on the observed probabilities over a period of an hour at
#multiple times of the day, and across weekdays and weekends.
likely_probabilities = {"en.wikipedia.org":0.13, "commons.wikimedia.org":0.10,
"www.wikidata.org":0.10}

#Simply a helper method that is invoked with a slug. It returns a properly
#decoded, i.e. a readable, JSON object.
def get_data(slug):
  #Makes an API call with the slug passed in. This can be: histogram, entropy
  #and rate.
  item = urllib.request.urlopen(geturl+slug).read()
  #Returns a properly formatted JSON object that has parsed the response into a
  #readable format.
  return json.loads(item.decode('utf-8'))

#Method that checks if the rate threshold has been breached, and if it has, it
#sends a message out. This can then be piped into any "alerter," i.e. any script
#that is reading lines in, and alerting some client-facing frontend. We use
#Slack.
def alert_on_rate_threshold_breach():
  #Retrieves the rate from the API.
  item = get_data("rate")
  #Only if the rate exists in the JSON object do we carry on. Else, we do
  #nothing.
  if "rate" in item:
    rate = item["rate"]
    #Checks if the rate threshold has been breached. The abs returns the
    #absolute value of the rate, i.e. irrespective of whether the value is
    #positive or negative, the value is _always_ positive. This is because
    #a change, positive or negative, can be inferred as unusual activity.
    if abs(rate) >= rate_threshold:
      print(json.dumps({"message":
        ("Rate alert of {0}  breached. Current rate is {1}".format(
          rate_threshold, rate))}))
      sys.stdout.flush()

#Method that checks if the entropy threshold has been breached, and if it has, it
#sends a message out. This can then be piped into any "alerter," i.e. any script
#that is reading lines in, and alerting some client-facing frontend. We use
#Slack.
def alert_on_entropy_threshold_breach():
  #Retrieves the entropy after invoking the API.
  item = get_data("entropy")
  if "entropy" in item:
    entropy = item["entropy"]
    #Checks if the entropy is less than the threshold, and if it is, send out an
    #alert.
    if entropy >= entropy_threshold:
      print(json.dumps({"message":
      "Entropy alert of {0} breached. Entropy is now at {1}".format(entropy_threshold, entropy)})
      )
      sys.stdout.flush()

#Method that checks if there is observed unlikely behaviour, and if it has, it
#sends a message out. This can then be piped into any "alerter," i.e. any script
#that is reading lines in, and alerting some client-facing frontend. We use
#Slack.
def alert_on_unlikeliness_breach():
  #Invokes the API to retrieve the probability.
  item = get_data("probability")
  #Gets all the urls that have a "likely" probability associated with them.
  #We can then examine the probabilities returned from the API against the
  #expected probabilities defined.
  likeliness_keys = likely_probabilities.keys()
  #Iterate through all the keys that have a corresponding likelihood...
  for key in likeliness_keys:
    #...and compare each key's actual probability against what is expected based
    #on what is defined in the likely_probabilies dict..
    actual_probability = item[key]
    #If the probability is less than what's expected, send out an alert.
    likely_probability = likely_probabilities[key]
    if actual_probability < likely_probability:
      print(json.dumps({"message":
      "The wiki edit rates of {0} are lower than the expected rate of {1} for {2}"
      .format(actual_probability, likely_probability, key)}))
      sys.stdout.flush()

#Every minute (sleep(60)), we check if any of the thresholds have been breached.
#If they have, we can send out an alert on our medium of choice. For the purpose
#of this exercise, the medium is Slack.
while True:
  alert_on_rate_threshold_breach()
  alert_on_entropy_threshold_breach()
  alert_on_unlikeliness_breach()
  time.sleep(60)

