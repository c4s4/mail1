#!/usr/bin/env python
# encoding: UTF-8
#
# pylint: disable=C0325

import os
import sys
import getopt
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart

ENCODING = 'UTF-8'
SMTP_HOST = None
SMTP_PORT = 25
RECIPIENT = None
SENDER = RECIPIENT


if sys.version_info[0] >= 3:
    def _binary(string):
        if isinstance(string, list):
            return [_binary(e) for e in string]
        return str(string)
else:
    def _binary(string):
        if isinstance(string, unicode):  # pylint: disable=E0602
            return string.encode(ENCODING)
        if isinstance(string, list):
            return [_binary(e) for e in string]
        return str(string)


def _listify(thing):
    if not isinstance(thing, list):
        thing = [thing]
    return _binary(thing)


def send(subject, text, text_html=None, sender=SENDER, recipients=[RECIPIENT], cc=[], bcc=[],
         attachments={}, smtp_host=SMTP_HOST, encoding=ENCODING,
         smtp_port=None, username=None, password=None):
    # manage smtp port
    if not smtp_port:
        if ':' in smtp_host:
            smtp_host, smtp_port = smtp_host.split(':', 2)
            smtp_port = int(smtp_port)
        else:
            smtp_port = SMTP_PORT
    # encode all strings in binary strings
    subject = _binary(subject)
    text = _binary(text)
    sender = _binary(sender)
    recipients = _listify(recipients)
    cc = _listify(cc)
    bcc = _listify(bcc)
    # build the message
    if text_html:
        message = MIMEMultipart('alternative')
    else:
        message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = ', '.join(recipients)
    if cc:
        message['CC'] = ', '.join(cc)
    # attach text part
    message.attach(MIMEText(text, 'plain', _charset=encoding))
    if text_html:
        message.attach(MIMEText(text_html, 'html', _charset=encoding))
    # attach attachments if any
    for name, filename in list(attachments.items()):
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(filename, "rb").read())
        encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % name)
        message.attach(part)
    smtp = smtplib.SMTP(host=smtp_host, port=smtp_port)
    if username and password:
        smtp.connect(smtp_host, smtp_port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(user=username, password=password)
    smtp.sendmail(sender, recipients+cc+bcc, message.as_string())
    smtp.quit()

HELP = '''mail1 [-h] -f from -r recipient -s subject -a file -m smtphost -e encoding message
Send an email with following:
-h            Print this help page
-f from       The mail sender
-r recipient  The mail recipient (repeat for more than one recipient)
-s subject    The mail subject
-a file       A file to attach
-e encoding   The encoding to use
-m smtphost   The SMTP server host
-u username   The username for authentication
-p password   The password for authentication
message       The message'''


def run():
    _sender     = None
    _recipients = []
    _subject    = None
    _attach     = {}
    _encoding   = ENCODING
    _smtp       = SMTP_HOST
    _username   = None
    _password   = None
    _message    = None
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:], "hf:r:s:a:e:m:u:p:", ["help", "from", "recipient", "subject", "attachement", "encoding", "smtp", "username", "password"])
    except getopt.GetoptError as error:
        print("ERROR: %s" % str(error))
        print(HELP)
        sys.exit(1)
    for OPT, ARG in OPTS:
        if OPT in ('-h', '--help'):
            print(HELP)
            sys.exit(0)
        elif OPT in ('-f', '--from'):
            _sender = ARG
        elif OPT in ('-r', '--recipient'):
            _recipients.append(ARG)
        elif OPT in ('-s', '--subject'):
            _subject = ARG
        elif OPT in ('-a', '--attach'):
            _name = os.path.basename(ARG)
            _attach[_name] = ARG
        elif OPT in ('-e', '--encoding'):
            _encoding = ARG
        elif OPT in ('-m', '--smtp'):
            _smtp = ARG
        elif OPT in ('-u', '--username'):
            _username = ARG
        elif OPT in ('-p', '--password'):
            _password = ARG
        else:
            print("Unhandled option: %s" % OPT)
            print(HELP)
            sys.exit(1)
    _message = ' '.join(ARGS)
    if not _recipients:
        print("Missing recipient")
        print(HELP)
        sys.exit(1)
    if not _sender:
        print("Missing sender")
        print(HELP)
        sys.exit(1)
    if not _subject:
        print("Missing subject")
        print(HELP)
        sys.exit(1)
    if not _message:
        print("Missing message")
        print(HELP)
        sys.exit(1)
    send(subject=_subject, text=_message, sender=_sender, recipients=_recipients,
         attachments=_attach, encoding=_encoding,
         smtp_host=_smtp, username=_username,password=_password)


if __name__ == '__main__':
    run()
