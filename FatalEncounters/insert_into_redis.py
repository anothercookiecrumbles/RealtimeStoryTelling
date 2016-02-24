import redis
import sys
import json
import time
import json.decoder
from datetime import datetime
from datetime import timedelta

#Simply opens a connection to the local instance of Redis. Redis must be up and
#running for this to work. If Redis isn't up and running, this will throw a 
#ConnectionRefusedError.
redis = redis.Redis()

#We want this to be running _forever_, so just run inside a while loop.
while (True):
  #Reads in the fatality sent down from the fatal_encounters_updates_only
  #script.
  fatality = sys.stdin.readline()
  print("In Redis: " + fatality)
  try:
    #Loads data into a JSON format. If we wanted to do some quick analytics here
    #or build hsets, here would be a good place to do it.
    data = json.loads(fatality)

    #if datetime.now().strftime("%B") in data["date"]:
    #  if redis.get(data['date']) != None:
    #      redis.incr(data['date'])
    #  else:
    #    redis.set(data['date'], 1)
    #  redis.expire(data['date'], 7*24*60*60)


    #Setting the key to be the data instead of something more creative.
    #There could be some really interesting data crunching that we could
    #do here, but for now, let's try capturing the rate of fatal encounters
    #across the last seven days.
    #Sets the data in Redis as the key, so that this can disappear within seven
    #days.

    #Converts date that was previously in a string format to a Python date
    #object so that we can easily manipulate it to extract only the month
    #and year.
    real_date = datetime.strptime(data["date"], '%B %d, %Y')

    #Gets the date that was seven days ago as we're calculating the average
    #across fourteen days. So, there's no point even adding datapoints that are
    #older for this specific exercise. This is more of a precautionary measure
    #as the initial run gets all the data, which spans 15 years. This simply 
    #filters it down to data relevant in the last week or so.
    date_seven_days_ago = datetime.now() - timedelta(days=14)

    #Only add fatalities that occurred within the last week.
    if real_date >= date_seven_days_ago:
      print(data)
      redis.set(data, 1)
      #Delete keys that are older than fourteen days in the Redis-verse.
      #We have to specify the key in seconds; hence, the multiplication.
      redis.expire(data, 14*24*60*60)
  except JSONDecodeError:
    pass
  time.sleep(120)
