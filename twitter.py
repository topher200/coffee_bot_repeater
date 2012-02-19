import base64
import json
import logging
import os
import urllib
import urllib2

SUPERTWEET_USER = os.environ['SUPERTWEET_USER']
SUPERTWEET_PASS = os.environ['SUPERTWEET_PASS']

def _try_function_multiple_times(func):
  result = None
  success = False
  try_number = 0
  while (not success) and try_number < 5:
    try:
      result = func()
      success = True
    except (urllib2.URLError, urllib2.HTTPError), e:
      logging.info('Dangerous function try #%s failed. error: %s' %
                   (try_number, e))
      try_number += 1
      time.sleep(2**try_number/10)
  if not success:
    logging.warning('Dangerous function failed permanently')
    return False
  return result
  
  
def get_latest_tweet():
  '''Returns the latest tweet in JSON form.

  In case of a prohibitive number of urllib2 errors, returns False.'''
  def func():
    r = urllib2.Request(("https://api.twitter.com/1/statuses/user_timeline.json" \
                           "?screen_name=fscoffeebot&count=1"))
    tweets = json.load(urllib2.urlopen(r))
    return tweets[0]
  return _try_function_multiple_times(func)

def send_dm(user, message):
  '''Sends the message as a Twitter DM to the given user.

  Returns True if we receive a good response from the server. Returns False if
  the response is bad (not 200), or if we are unable to communicate with the
  server.
  '''
  logging.info('sending DM to user: %s', user)
  def func():
    req = urllib2.Request(
      'http://api.supertweet.net/1/direct_messages/new.json')
    req.add_data(urllib.urlencode({'user': user, 'text': message}))
    auth = 'Basic ' + base64.urlsafe_b64encode('%s:%s' % (SUPERTWEET_USER,
                                                          SUPERTWEET_PASS))
    req.add_header('Authorization', auth)
    response = urllib2.urlopen(req)
    return int(response.getcode()) == 200
  return _try_function_multiple_times(func)
  
  
