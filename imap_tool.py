#!/usr/bin/env python3

from imap_tools import MailBox, AND
from logging.config import fileConfig 
import configparser

config=configparser.ConfigParser()
config.read('./imapfilter.conf')

uids=[]

criteria = [
    ('from', 'ebay', "Mist"),
    ('from', 'cisco', "Mist"),
    ('from', 'cybrary', "Mist"),
    ('from', 'linuxacademy', "Mist"),
    ('from', 'netflix', ",Mist"),
    ('from', 'blackhat', "Mist"),
    ('from', 'feedback@binarysecuritysolutions.com', "Mist"),
    ('from', 'youtube.com', "Mist"),
    ('from', 'vodafone.de', "Mist"),
    ('subject', 'Weihnachten', "Mist")
]

def fetch_mails(hst, usr, pwd):
    
    with MailBox(hst).login(usr, pwd) as mailbox:
        for criterion in criteria:
            if criterion[0] == "from":
                print(criterion[1])
                for msg in mailbox.fetch(AND(from_=criterion[1])):
                    uids.append(msg.uid)
            elif criterion[0] == "subject":
                print(criterion[1])
                for msg in mailbox.fetch(AND(from_=criterion[1])):
                    uids.append(msg.uid)
    return uids

def move_mails(mails, hst, usr, pwd):
    input("Will remove {} mails. Continue? ".format(len(mails)))
    with MailBox(hst).login(usr, pwd) as mailbox:
        for uid in mails:
            mailbox.move(uid, "Mist")


def main(config):
    imap_hostname=config.get('default','imap_hostname')
    imap_username=config.get('default','imap_username')
    imap_password=config.get('default','imap_password')
    imap_mailbox=config.get('default','imap_mailbox')

    mails=fetch_mails(imap_hostname, imap_username, imap_password)

    move_mails(mails, imap_hostname, imap_username, imap_password)
    
if __name__=="__main__":
    main(config)
