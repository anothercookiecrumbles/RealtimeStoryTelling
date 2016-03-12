import time
import sys
import json

#Calculates the time deltas between Wiki edits,i.e. the time that has elapased
#between the last message and the new one.

#Need to store the last timestamp we received from upstream as a reference
#point, which we can then use to calculate the deltas.
last_timestamp = -1

while True:
  #Reads any data that's piped into this script, and loads it into a dictionary..
  item = sys.stdin.readline()
  if item == None:
    continue
  item_in_json = json.loads(item)
  #Checks if the timestamp appears in the dictionary. This should ideally never
  #happen, but we need to protect ourselves from badly formed JSON.
  if "timestamp" in item_in_json:
    timestamp = int(item_in_json["timestamp"])
    #If the last_timestamp is -1, i.e. if this is the first message received, we
    #simply set the last_timestamp to the timestamp of the message, and do
    #nothing else.
    if (last_timestamp == -1):
      last_timestamp = timestamp
      continue
    #Gets the time that has elapsed between this timestamp and the last one, i.e.
    #how much time has passed between the two messages.
    delta = timestamp - last_timestamp

    #Prints out the delta and the timestamp, and flush it to ensure that
    #listening processes will actually receive the data.
    print(json.dumps({"delta": delta, "timestamp": timestamp}))
    sys.stdout.flush()

    #Sets the last_timestamp to be the timestamp of this message, as this is now
    #the last_timestamp. So, when the next message comes in, the last_timestamp
    #is correct.
    last_timestamp = timestamp

