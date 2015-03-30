======
MAIL 1
======

Mail1 is an API to send email with a single function call. For instance, we could send an email running::

    import mail1
    
    mail1.send(subject='Test',
               text='This is a test!',    
               recipients='casa@sweetohm.net',
               sender='casa@sweetohm.net',
               smtp_host='smtp.orange.fr')

That's it!

send() method
=============

The signature of the method to send an email is the following::

    send(subject, text, text_html=None, sender=None,
         recipients=[None], cc=[], bcc=[], attachments={},
         smtp_host=SMTP_HOST, smtp_port=SMTP_PORT,
         encoding=ENCODING)

The parameters are the following:

- subject: this is the subject of the email, as a string.
- text: this is the text of the email as a string.
- text_html: text as HTML.
- sender: email address of the sender of the email.
- recipients: the list of recipients, or the recipient as a string if there is a single one.
- cc: the list of carbon copies.
- bcc: the list of blind carbon copies.
- attachments: a dictionnary that gives the file name for a given attachment name.
- smtp_host: the hostname of the email server.
- smtp_port: the port of the email server (defaults to 25).
- encoding: the encoding of the message.

Command line
============

You can also invoke this script on command line to send emails. To get help about command line parameters, type *mail1 -h*, which will display following help page::

  mail1 [-h] -f from -r recipient -s subject -a file 
             -m smtphost -e encoding message
  Send an email with following:
  -h            Print this help page
  -f from       The mail sender
  -r recipient  The mail recipient(s)
  -s subject    The mail subject
  -a file       A file to attach
  -m smtphost   The SMTP server host
  -e encoding   The encoding to use
  message       The message

Enjoy!

