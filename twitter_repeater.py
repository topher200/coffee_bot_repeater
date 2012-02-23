from __future__ import division
from time import sleep, time
import logging

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
    database.push_message_to_send(database.MessageToSend(user, tweet_text))
    
  database.set_last_handled_tweet_id(this_tweet_id)

def do_deferred_job():
  '''Attempts to run a job in the queue. Returns True if a job is found.'''
  message_to_send = database.pop_message_to_send()
  if not message_to_send:
    return False
  
  # If it's been more then 5 minutes, throw away the job
  if time() + (5 * 60) > message_to_send.time:
    logging.error(
      "Timing out DM to %s. dm.time: %s, current time: %s. Message: %s" \
        % (message_to_send.user, message_to_send.time, time(),
           message_to_send.message))
    return True
      
  # Job is still valid. Run it!
  if twitter.send_dm(message_to_send.user, message_to_send.tweet_text):
    logging.info('sent DM to user: %s' % message_to_send.user)
  else:
    logging.warn('DM to user %s failed' % message_to_send.user)
    # We couldn't finish the job - push it back into the queue
    database.push_message_to_send(message_to_send)

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  while True:
    run()
    run_time = time()
    # Process jobs for 30 seconds
    while time() < run_time + 30:
      do_deferred_job()
      sleep(.1)
