import base64
import json
import logging
import os
import urllib
import urllib2

SUPERTWEET_USER = os.environ['SUPERTWEET_USER']
SUPERTWEET_PASS = os.environ['SUPERTWEET_PASS']

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
  logging.info('sending DM to user: %s', user)
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
