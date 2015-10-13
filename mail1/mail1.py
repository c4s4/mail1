#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
import getopt
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart

ENCODING = u'UTF-8'
SMTP_HOST = None
SMTP_PORT = 25
RECIPIENT = None
SENDER = RECIPIENT


def _binary(string):
    if isinstance(string, unicode):
        return string.encode(ENCODING)
    elif isinstance(string, list):
        return [_binary(e) for e in string]
    else:
        return str(string)


def _listify(thing):
    if not isinstance(thing, list):
        thing = [thing]
    return _binary(thing)


def send(subject, text, text_html=None, sender=SENDER, recipients=[RECIPIENT], cc=[], bcc=[], attachments={}, smtp_host=SMTP_HOST, smtp_port=SMTP_PORT, encoding=ENCODING):
    # encode all strings in binary strings
    subject = _binary(subject)
    text = _binary(text)
    sender = _binary(sender)
    recipients = _listify(recipients)
    cc = _listify(cc)
    bcc = _listify(bcc)
    # build the message
    if text_html:
        message = MIMEMultipart(u'alternative')
    else:
        message = MIMEMultipart()
    message[u'Subject'] = subject
    message[u'From'] = sender
    message[u'To'] = u', '.join(recipients)
    if cc:
        message[u'CC'] = u', '.join(cc)
    # attach text part
    message.attach(MIMEText(text, u'plain', _charset=encoding))
    if text_html:
        message.attach(MIMEText(text_html, u'html', _charset=encoding))
    # attach attachments if any
    for name, filename in attachments.items():
        part = MIMEBase(u'application', u'octet-stream')
        part.set_payload(open(filename, u"rb").read())
        encode_base64(part)
        part.add_header(u'Content-Disposition',
                        u'attachment; filename="%s"' % name)
        message.attach(part)
    smtp = smtplib.SMTP(host=smtp_host, port=smtp_port)
    smtp.sendmail(sender, recipients+cc+bcc, message.as_string())
    smtp.quit()

HELP = u'''mail1 [-h] -f from -r recipient -s subject -a file -m smtphost -e encoding message
Send an email with following:
-h            Print this help page
-f from       The mail sender
-r recipient  The mail recipient(s)
-s subject    The mail subject
-a file       A file to attach
-m smtphost   The SMTP server host
-e encoding   The encoding to use
message       The message'''


def run():
    _sender     = None
    _recipients = []
    _subject    = None
    _attach     = {}
    _smtp       = SMTP_HOST
    _encoding   = ENCODING
    _message    = None
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:], u"hf:r:s:a:m:e:", [u"help", u"from", u"recipient", u"subject", u"attachement", u"smtp", u"encoding"])
    except getopt.GetoptError, error:
        print u"ERROR: %s" % str(error)
        print HELP
        sys.exit(1)
    for OPT, ARG in OPTS:
        if OPT in (u'-h', u'--help'):
            print HELP
            sys.exit(0)
        elif OPT in (u'-f', u'--from'):
            _sender = ARG
        elif OPT in (u'-r', u'--recipient'):
            _recipients.append(ARG)
        elif OPT in (u'-s', u'--subject'):
            _subject = ARG
        elif OPT in (u'-a', u'--attach'):
            _name = os.path.basename(ARG)
            _attach[_name] = ARG
        elif OPT in (u'-m', u'--smtp'):
            _smtp = ARG
        elif OPT in (u'-e', u'--encoding'):
            _encoding = ARG
        else:
            print u"Unhandled option: %s" % OPT
            print HELP
            sys.exit(1)
    _message = u' '.join(ARGS)
    if not _recipients:
        print u"Missing recipient"
        print HELP
        sys.exit(1)
    if not _sender:
        print u"Missing sender"
        print HELP
        sys.exit(1)
    if not _subject:
        print u"Missing subject"
        print HELP
        sys.exit(1)
    if not _message:
        print u"Missing message"
        print HELP
        sys.exit(1)
    send(subject=_subject, text=_message, sender=_sender, recipients=_recipients, attachments=_attach, smtp_host=_smtp, encoding=_encoding)


if __name__ == u'__main__':
    run()
