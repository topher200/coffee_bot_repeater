import random
import twitter
import string
import unittest

class TwitterTester(unittest.TestCase):
  def test_get_latest_tweet(self):
    self.assertTrue(twitter.get_latest_tweet())

  def test_send_dm(self):
    user = 'topher200'
    message = 'unittest message. '
    # Adding some random characters to twitter doesn't complain about
    # duplicate messages
    for _ in range(5):
      message += random.choice(string.ascii_lowercase + string.digits)
    self.assertTrue(twitter.send_dm(user, message))

if __name__ == "__main__":
  unittest.main()
