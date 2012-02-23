from __future__ import division
from time import time
import re
import redis

import environment

REDIS_HOST = environment.get_config('REDIS_HOST')
REDIS_PORT = int(environment.get_config('REDIS_PORT'))
REDIS_PASS = environment.get_config('REDIS_PASS')

class MessageToSend():
  def __init__(self, user, message, time=time()):
    self.user = user
    self.message = message
    self.time = time

  @classmethod
  def parse_from_string(cls, string):
    # TODO: This may fail if the tweet ends in a comma followed by digits
    user, message, time = re.search('(.*),(.*),(\d*\.\d*)', string).groups()
    return cls(user, message, float(time))

  def to_string(self):
    return '%s,%s,%s' % (self.user, self.message, self.time)
    
def _get_database():
  return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                           password=REDIS_PASS)

def get_last_handled_tweet_id():
  return _get_database().get('last_tweet_id')

def set_last_handled_tweet_id(id_number):
  _get_database().set('last_tweet_id', id_number)

def get_followers():
  return _get_database().smembers('followers')

def pop_message_to_send():
  return MessageToSend.parse_from_string(_get_database().lpop())

def push_message_to_send(message_to_send):
  _get_database().rpush(message_to_send.to_string())
  
  
