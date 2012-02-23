import unittest

import database

class DatabaseTester(unittest.TestCase):
  def test_message_to_send_parsing(self):
    '''This should only be run if database's job queue is empty.'''
    self.assertFalse(database._get_database().exists('message_to_send'))
    
    created_message = database.MessageToSend('topher200',
                                             'This is a test message, see?')
    database.push_message_to_send(created_message)
    parsed_message = database.pop_message_to_send()
    
    self.assertTrue(created_message.user == parsed_message.user)
    self.assertTrue(created_message.message == parsed_message.message)
    self.assertTrue(created_message.time == parsed_message.time)

if __name__ == "__main__":
  unittest.main()
