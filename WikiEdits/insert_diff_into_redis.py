import redis

import sys
import json

#Using multiple databases to store different types of data in the same Redis
#instance. Instructions on how this works can be found here:
#http://www.rediscookbook.org/multiple_databases.html.
#db1 simply stores the timestamps of each edit, and then calculates the moving
#average in 5-minute windows. This enables us to alert when the moving average
#rate breaches the thresholds.
db1 = redis.Redis(db=0)

while True:
  #Reads in the line that's piped into this script.
  item = sys.stdin.readline()
  if item == None:
    continue
  try:
    #Loads the data piped in to a dictionary for easy/clean
    #processing.
    data = json.loads(item)
    if data != None:
      #Pulls out the delta and the timestamp, which are the two fields we want
      #to store in Redis, which will enable us to calculate the moving average.
      delta = data["delta"]
      time = data["timestamp"]

      #Sets the time and delta in Redis along with an expiry of 600 seconds or
      #10 minutes. This means that, in Redis, there will always only be data
      #from the 10 minutes just elapsed.
      db1.setex(time, delta, 600)

      #Prints out the data and flushes it in case there are any "listening
      #processes, i.e. processes that this script is piping data to.
      print(json.dumps({"time": time, "delta": delta}))
      sys.stdout.flush()
  except json.decoder.JSONDecodeError:
    pass
