#!/usr/bin/env python
# encoding=UTF-8

# pylint: disable=W0403
from . import mail1
import unittest


class Test(unittest.TestCase):

    SMTP_HOST = 'smtp.orange.fr'

    def test_send_email(self):
        mail1.send(subject='Test', text='This is a test!',
                   recipients='casa@sweetohm.net',
                   sender='casa@sweetohm.net',
                   smtp_host=self.SMTP_HOST)
        mail1.send(subject='Test', text='This is a test!',
                   recipients=['casa@sweetohm.net'],
                   sender='casa@sweetohm.net',
                   smtp_host=self.SMTP_HOST)


if __name__ == '__main__':
    unittest.main()
