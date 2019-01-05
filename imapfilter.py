#!/usr/bin/env python3
import imapclient
import logging
import time
from datetime import datetime
import configparser

loglevel=logging.INFO
imapclient_loglevel=1
polling_interval_s = 60
fullupdate_interval_s = 3600
restart_interval_s = 6*3600

def main(config):
    imap_hostname=config.get('default','imap_hostname')
    imap_username=config.get('default','imap_username')
    imap_password=config.get('default','imap_password')
    imap_mailbox=config.get('default','imap_mailbox')

    print("Login {}@{} for {}".format(imap_username, imap_hostname, imap_mailbox))
    client=imapclient.IMAPClient(imap_hostname, ssl=True, use_uid=True)
    client.debug=imapclient_loglevel
    client.login(imap_username, imap_password)
    folders=client.list_folders()

    print(folders)


config=configparser.ConfigParser()
config.read('imapfilter.conf')

try:
    logging.info("*** Restarting at {}".format(str(datetime.now())))
    main(config)
except Exception as e:
    logging.error(e)



