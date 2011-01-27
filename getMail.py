#! /bin/python
import sys, os, string
import getpass, imaplib, email, mailbox
from pprint import pprint

username = sys.argv[1]
mbox = mailbox.mbox("/tmp/%s.mbox" % username)
M = imaplib.IMAP4_SSL("imap.gmail.com")
M.login(username, getpass.getpass())
typ, data = M.list()
for label in data:
   if "All" in  label.split("\"")[-2]:
      M.select(label.split("\"")[-2])
      typ, data = M.search(None, 'ALL')
      for i in data[0].split():
          typ, data = M.fetch(i, '(RFC822)')
#         print typ
          msg = email.message_from_string(data[0][1])
          mbox.add(msg)
#print 'Response code:', typ
#print 'Response:'
#pprint(data)
#M.close()
M.logout()
