import redis
import sys
import json
import time
import json.decoder

redis = redis.Redis()

while (True):
  fatality = sys.stdin.readline()
  print("In Redis: " + fatality)
  try:
    json.loads(fatality)
  except JSONDecodeError:
    pass
  redis.setex("fatality", fatality, 60)
  time.sleep(120)
