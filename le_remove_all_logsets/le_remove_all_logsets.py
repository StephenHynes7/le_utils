import json
import sys
import requests


host_keys = []


def get_hosts():
    r = requests.get('http://api.logentries.com/' + ACCOUNT_KEY + '/hosts/')
    hosts = r.json()
    for host in hosts['list']:
        delete_hosts(host['key'])


def delete_hosts(host_key):
    request = {
        "request": "rm_host",
        "user_key": ACCOUNT_KEY,
        "host_key": host_key
    }
    print json.dumps(request)
    req = 'http://api.logentries.com/'
    r = requests.post(req, data=request)
    print r.text


if __name__ == '__main__':
    ACCOUNT_KEY = sys.argv[1]
    get_hosts()
    print "All hosts deleted"
