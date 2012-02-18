from __future__ import division
import os
import redis

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_PASS = os.environ['REDIS_PASS']

def _get_database():
  return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                           password=REDIS_PASS)

def get_last_handled_tweet_id():
  return _get_database().get('last_tweet_id')

def set_last_handled_tweet_id(id_number):
  _get_database().set('last_tweet_id', id_number)

def get_followers():
  return _get_database().smembers('followers')
