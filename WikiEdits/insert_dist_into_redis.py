import redis

import json
import sys

#Initialises a connection to the non-default Redis database that holds
#the details about the distribution, i.e. a single entry for each wiki
#edit over the span of the last ten minutes.
db2 = redis.Redis(db=1)

#Simply an identifier to not have clashes in the database that we can
#keep incrementing on each new edit.
identifier = 1

while True:
  #Reads the lines that are being piped into this script.
  item = sys.stdin.readline()
  try:
    if item != None:
      #Loads the JSON into a dictionary so that we can pull out the relevant
      #fields.
      data = json.loads(item)
      #Checks if the wiki entry exists in the dictionary, because if it doesn't,
      #we can't really process anything. This should ideally never happen, but
      #we don't live in an ideal world, and sometimes, malformed – or incomplete
      #– JSON is a thing.
      if "wiki" in data:
        wiki = data["wiki"]
        #Increments the identifier so that each entry has a unique ID associated
        #with it.
        identifier = identifier+1

        #Adds the entry into the Redis database. What we are doing here is:
        #setting the hash value as the identifier and then adding the site as
        #a field to the hash. In plainer terms, the entry looks something like
        #this: 14 "site" "en.wikipedia.org"
        #In the above, 14 is the identifier, site is the field name and
        #"en.wikipedia.org" is the field value.
        #The question that arises here is, what purpose does the identifier/hash
        #serve? Well, we want to expire entries every ten minutes, and the way
        #we can do this in a Redis-land is by setting the expiry on the hash (or
        #id). There are other ways to handle this in Redis, but they're less
        #elegant, and more verbose. Setting an expire on the hash/id means that
        #Redis will automatically delete the entry after the 600 seconds are up.
        db2.hset(identifier, "site", wiki)
        db2.expire(identifier, 600)

        #As usual, we need to flush out the information, so that any script
        #that's listening in can pick this edit entry up.
        print(json.dumps({"identifier": identifier, "wiki": wiki}))
        sys.stdout.flush()
  except KeyError:
    continue
  except json.decoder.JSONDecodeError:
    continue
