import redis
import sys
import time

#Establishes the Redis connection as long as Redis is up and running.
#If Redis isn't this will raise a ConnectionRefusedError.
redis = redis.Redis()

#According to the spreadsheet, since 1st January 2000, there have been 11447
#fatalities. That's just over 750 a year, which is approximately two a day.
#However, in 2015, the total amounts to almost 1300 fatalities at just over
#three a day. The 2013 and 2014 numbers are close to the 2015 numbers (the
#difference is in the tens.
#In 2000 and 2001, the numbers are around the 400 mark, which is at
#just over one a day. In 2002, it crossed 500. While these numbers in isolation 
#don't tell the whole story, it's still interesting to observe.
#So, the threshold has been decided based on the current trends, and an
#alert will flag if the average is less than two a day or more than six.
min_threshold = 1
max_threshold = 1

#The time frame for our moving average, i.e. across how many days do we
#calculate the moving average. The idea is, with each new day, we'll drop
#all fatalities that happened before T-14, and add fatalities that occured
#on T. Here, T is indicative of "today."
time_frame = 14;

#We run this forever, as we calculate the average across the fourteen day period
#each time a fatality comes in.
while(True):
  #Pulls out all fatalities from Redis. In Redis, these are stored as the object
  #keys.
  fatalities = redis.keys()
  #We get the number of fatalities, i.e. the size of the keys.
  number_of_fatalities = len(fatalities)

  #We calculate the average
  average = number_of_fatalities/14

  if average < min_threshold:
    print("Good news! On average, there've been less than two fatal encounters"
        + " a day!")
  if average > max_threshold:
    print("Bad news! There seem to be more fatal encounters than normal over " + 
        "the course of the last fourteen days. There were more than " +
        str(average) + " encounters a day.")
  sys.stdout.flush() 
  time.sleep(120)
