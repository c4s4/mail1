#!/usr/bin/env python
# encoding=UTF-8

# pylint: disable=W0403
from . import mail1
import unittest
import yaml


class Test(unittest.TestCase):

    SMTP_HOST = 'smtp.orange.fr'

    def test_send_email(self):
        mail1.send(subject='Test', text='This is a test!',
                   recipients='casa@sweetohm.net',
                   sender='casa@sweetohm.net',
                   smtp_host=self.SMTP_HOST)

    def test_send_email_login(self):
        with open('/home/casa/.credentials/email-orange.yml') as stream:
            credentials = yaml.load(stream)
        mail1.send(subject='Test', text='This is a test!',
                   recipients='casa@sweetohm.net',
                   sender='casa@sweetohm.net',
                   smtp_host=self.SMTP_HOST,
                   username=credentials['username'],
                   password=credentials['password'])


if __name__ == '__main__':
    unittest.main()
