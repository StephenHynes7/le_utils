import urllib
import json
import sys
import os
import binascii
import random

ACCOUNT_KEY = ''


def create_host():
    request = urllib.urlencode({
        'request': 'register',
        'user_key': ACCOUNT_KEY,
        'name': 'MyHost',
        'distver': '',
        'system': '',
        'distname': ''
    })

    req = urllib.urlopen("http://api.logentries.com", request)
    response_dict = json.loads(req.read())
    host = response_dict
    print host
    host_key = host['host_key']
    create_log(host_key)


def create_log(host_key):
    request = urllib.urlencode({
        'request': 'new_log',
        'user_key': ACCOUNT_KEY,
        'host_key': host_key,
        'name': 'MyLog'),
        'type': '',
        'filename': '',
        'retention': '-1',
        'source': 'token'
    })

    req = urllib.urlopen("http://api.logentries.com", request)

if __name__ == '__main__':
    ACCOUNT_KEY = sys.argv[1]
    print ACCOUNT_KEY
    r = random.randint(1, 15)
    for x in (1, r):
        create_host()
