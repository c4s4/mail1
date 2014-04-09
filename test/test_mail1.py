#!/usr/bin/env python
# encoding=UTF-8

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import mail1
import unittest

class Test(unittest.TestCase):

    def test_send_email(self):
        mail1.send(subject='Test', text='This is a test!', recipients='casa@sweetohm.net', sender='casa@sweetohm.net', smtp_host='smtp.orange.fr')


if __name__ == '__main__':
    unittest.main()

