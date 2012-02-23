from __future__ import with_statement
import os
import re

def build_config_dict():
  '''Builds a dictionary of (key, value) configs from the .env file'''
  configs = dict()
  with open('.env', 'r') as f:
    for line in f:
      key, value = re.search('(.*)=(.*)', line).groups()
      configs[key] = value
  return configs

def get_config(key):
  '''Return the environment variable (if it exists), else return the value
  from the config file.'''
  try:
    return os.environ[key]
  except KeyError:
    return build_config_dict()[key]
