from __future__ import division
import base64
import json
import logging
import os
import redis
import time
import urllib
import urllib2

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_PASS = os.environ['REDIS_PASS']
SUPERTWEET_USER = os.environ['SUPERTWEET_USER']
SUPERTWEET_PASS = os.environ['SUPERTWEET_PASS']

###### DB functions
def get_database():
  return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                           password=REDIS_PASS)

def get_last_handled_tweet_id():
  return get_database().get('last_tweet_id')

def set_last_handled_tweet_id(id_number):
  get_database().set('last_tweet_id', id_number)

def get_followers():
  return get_database().smembers('followers')
###### DB functions

###### Twitter functions
def get_latest_tweet():
  '''Returns the latest tweet in JSON form.

  In case of urllib2 error, returns None.'''
  r = urllib2.Request(("https://api.twitter.com/1/statuses/user_timeline.json" \
                         "?screen_name=fscoffeebot&count=1"))
  try:
    tweets = json.load(urllib2.urlopen(r))
  except urllib2.URLError, e:
    logging.warn('urllib error: %s', e)
    return None
  return tweets[0]

def send_dm(user, message):
  logging.info('sending tweet to user: %s', user)
  req = urllib2.Request('http://api.supertweet.net/1/direct_messages/new.json')
  req.add_data(urllib.urlencode({'user': user, 'text': message}))
  auth = 'Basic ' + base64.urlsafe_b64encode('%s:%s' % (SUPERTWEET_USER,
                                                        SUPERTWEET_PASS))
  req.add_header('Authorization', auth)
  try:
    response = urllib2.urlopen(req)
  except urllib2.HTTPError, e:
    logging.error('urllib2 error')
    logging.error(e.read())
    return False
  return int(response.getcode()) == 200
###### Twitter functions

def run():
  logging.debug('entering run()')
  # Get the latest tweet from @FSCoffeeBot
  tweet = get_latest_tweet()
  if not tweet:
    logging.warning('no tweet found')
    return False

  last_tweet_id = int(get_last_handled_tweet_id())
  this_tweet_id = int(tweet['id'])
  logging.debug('found tweet. tweet id: %s' % this_tweet_id)
  if not last_tweet_id:
    # We haven't init-ed the DB yet - this must be the first run
    logging.info('No last_tweet_id found. Setting it.')
    set_last_handled_tweet_id(this_tweet_id)
    return False

  if last_tweet_id >= this_tweet_id:
    logging.debug('We already processed this tweet')
    return False
    
  # If we've made it here, it must be a new tweet
  tweet_text = tweet['text']
  logging.info('New tweet found: %s', tweet_text)
  for user in get_followers():
    success = False
    try_number = 0
    while (not success) and try_number < 5:
      res = send_dm(user, tweet_text)
      if res:
        logging.info('Tweet to %s sent successfully' % user)
        success = True
      else:
        logging.warn('Tweet to %s failed. Try #%s' % (user, try_number))
        try_number += 1
        time.sleep(2**try_number/10)
    if not success:
      logging.error('Failed to send tweet to %s. Giving up' % user)
    
  set_last_handled_tweet_id(this_tweet_id)

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  while True:
    run()
    for _ in range(30):
      time.sleep(1)
