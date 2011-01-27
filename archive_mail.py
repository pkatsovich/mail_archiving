#! /bin/python

import mailbox
import sys
import email
import os
import sys
from subprocess import call

username = sys.argv[1]
password = sys.argv[2]
cwd = os.getcwd()


#write fetmailrc file
fetchrc = open("fetchmailrc", "w")
fetchrc.write("poll imap.gmail.com with proto IMAP\n")
fetchrc.write("user '%s@theopenskyproject.com' there with password '%s' is '%s' here options ssl\n" % (username, password, username) )
fetchrc.write("fetchall\n")
fetchrc.write("no rewrite\n")
fetchrc.write('mda "/usr/bin/procmail -m %s/procmail.conf" ' % cwd )

fetchrc.close()


#write procmail.conf 
procmailconf = open("procmail.conf", "w")
procmailconf.write("CORRECTHOME=/tmp/\n")
procmailconf.write("MAILDIR=$CORRECTHOME/\n")
procmailconf.write("MDIR=/tmp/pm\n")
procmailconf.write("LOGFILE=$PMDIR/log\n")
procmailconf.write("VERBOSE=on\n")
procmailconf.write(":0\n")
procmailconf.write("%s/" % username)

if not os.path.exists("/tmp/%s" % username):
  os.makedirs("/tmp/%s" % username)

procmailconf.close()
os.chmod("fetchmailrc", 0700)
call(['fetchmail', '-f', 'fetchmailrc', '-v'])


#
#
# work on this
# open the existing maildir and the target mbox file
maildir = mailbox.Maildir("/tmp/%s" % username, email.message_from_file)
mbox = mailbox.mbox("/tmp/%s.mbox" %username)

# lock the mbox
mbox.lock()

# iterate over messages in the maildir and add to the mbox
for msg in maildir:
    mbox.add(msg)

# close and unlock
mbox.close()
maildir.close()

call(['tar','-cvzf', '%s.mbox.tar.gz' % username, '/tmp/%s.mbox' % username])

