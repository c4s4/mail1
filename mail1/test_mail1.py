#!/usr/bin/env python
# encoding=UTF-8

import os
import unittest
import mail1

class Test(unittest.TestCase):

    def test_send_email(self):
        mail1.send(subject='Test',
                   text='This is a test!',
                   recipients=os.environ['MAIL_RECIPIENT'],
                   sender=os.environ['MAIL_FROM'],
                   smtp_host=os.environ['MAIL_SMTP'],
                   username=os.environ['MAIL_USERNAME'],
                   password=os.environ['MAIL_PASSWORD'])

    def test_send_email_environ(self):
        mail1.send(subject='Test',
                   text='This is a test!',
                   recipients=os.environ['MAIL_RECIPIENT'],
                   sender=os.environ['MAIL_FROM'])


if __name__ == '__main__':
    unittest.main()
