#!/usr/bin/env python3
import imapclient
from imapclient import IMAPClient as IMAPClient
import email
import logging
import time
from datetime import datetime
import configparser
import re

loglevel=logging.INFO
imapclient_loglevel=1
polling_interval_s = 60
fullupdate_interval_s = 3600
restart_interval_s = 6*3600

def apply_rules(msgs, uid):
    def move_by_header_field(header_field, search_regexp, to_folder):
        msg=msgs.get(uid)
        field_value=msg.get(header_field)
        # print(field_value)
        if re.search(search_regexp, field_value, re.IGNORECASE):
            #print("uid: {} from: {} on subject: {} matches criterion".format(uid, msg.get('From'), msg.get('Subject')))
            msgs.copy([uid], to_folder)
            msgs.delete([uid])

    move_by_header_field('From', 'ebay', "Mist")
    move_by_header_field('From', 'cisco', "Mist")
    move_by_header_field('From', 'cybrary', "Mist")
    move_by_header_field('From', 'linuxacademy', "Mist")
    move_by_header_field('Subject', 'Weihnachten', "Mist")

class Messages:
    def __init__(self, imap_client):
        self.imap_client = imap_client
        self._msg_cache = {}

    def clear(self):
        self._msg_cache = {}

    def get_new_uids(self):
        msg_uids = self.imap_client.search()
        new_uids = [uid for uid in msg_uids if uid not in self._msg_cache]
        new_msgs = {key: None for key in new_uids}
        self._msg_cache.update(new_msgs)
        return new_uids

    def get(self, msg_uid):
        if msg_uid not in self._msg_cache:
            raise LookupError("unknown msg_uid={} with keys={}".format(msg_uid, self._msg_cache.keys()))
        if self._msg_cache.get(msg_uid) is None:
            header_raw=self.imap_client.fetch([msg_uid], ['RFC822.HEADER'])
            if header_raw is not None:
                header_raw = header_raw[msg_uid]
            if header_raw is not None:
                header_raw=header_raw[b'RFC822.HEADER']
            if header_raw is None:
                raise LookupError("could not fetch/decode msg_uid={} with keys={}".format(msg_uid, self._msg_cache.keys()))
            header_raw=header_raw.decode('utf-8')
            header=email.message_from_string(header_raw)
            self._msg_cache[msg_uid]=header
            logging.debug('Fetching header for #{} (from "{}" on "{}")'.format(msg_uid, header.get('From'), header.get('Subject')))
        return self._msg_cache.get(msg_uid)

    def copy(self, msg_uids, folder):
        result=self.imap_client.copy(msg_uids, folder)
        print("copy({},{}) -> {}".format(msg_uids, folder, result))
        return  result

    def delete(self, msg_uids):
        result=self.imap_client.delete_messages(msg_uids)
        print("delete({}) -> {}".format(msg_uids, result))
        return  result


def process_msgs(msgs):
    logging.info('*** Processing new msgs')
    new_uids = msgs.get_new_uids()
    for uid in new_uids:
        apply_rules(msgs, uid)

def main(config):
    imap_hostname=config.get('default','imap_hostname')
    imap_username=config.get('default','imap_username')
    imap_password=config.get('default','imap_password')
    imap_mailbox=config.get('default','imap_mailbox')

    print("Login {}@{} for {}".format(imap_username, imap_hostname, imap_mailbox))
    client=imapclient.IMAPClient(imap_hostname, ssl=True, use_uid=True)
    client.debug=imapclient_loglevel
    client.login(imap_username, imap_password)

    # folders=client.list_folders()
    # print(folders)

    select_info=client.select_folder("INBOX")
    print("%d messages in INBOX" % select_info[b'EXISTS'])

    msgs=Messages(client)
    process_msgs(msgs)

config=configparser.ConfigParser()
config.read('imapfilter.conf')
logger=logging.getLogger('imapfilter')
hdlr=logging.FileHandler("/home/cr0c0/.log/imapfilter.log")
formatter=logging.Formatter('%(asciitime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

try:
    logging.info("*** Restarting at {}".format(str(datetime.now())))
    main(config)
except Exception as e:
    logging.error(e)



