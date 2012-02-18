from __future__ import division
import logging
import time

import database
import twitter
  
def run():
  logging.debug('entering run()')
  # Get the latest tweet from @FSCoffeeBot
  tweet = twitter.get_latest_tweet()
  if not tweet:
    logging.warning('no tweet found')
    return False

  last_tweet_id = int(database.get_last_handled_tweet_id())
  this_tweet_id = int(tweet['id'])
  logging.debug('found tweet. tweet id: %s' % this_tweet_id)
  if not last_tweet_id:
    # We haven't init-ed the database yet - this must be the first run
    logging.info('No last_tweet_id found. Setting it.')
    database.set_last_handled_tweet_id(this_tweet_id)
    return False

  if last_tweet_id >= this_tweet_id:
    logging.debug('We already processed this tweet')
    return False
    
  # If we've made it here, it must be a new tweet
  tweet_text = tweet['text']
  logging.info('New tweet found: %s', tweet_text)
  for user in database.get_followers():
    success = False
    try_number = 0
    while (not success) and try_number < 5:
      res = twitter.send_dm(user, tweet_text)
      if res:
        logging.info('Tweet to %s sent successfully' % user)
        success = True
      else:
        logging.warn('Tweet to %s failed. Try #%s' % (user, try_number))
        try_number += 1
        time.sleep(2**try_number/10)
    if not success:
      logging.error('Failed to send tweet to %s. Giving up' % user)
    
  database.set_last_handled_tweet_id(this_tweet_id)

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  while True:
    run()
    for _ in range(30):
      time.sleep(1)
