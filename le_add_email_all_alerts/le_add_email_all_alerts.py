import urllib2
import json
import sys
import re


def setup(account_key, host_name, email): 
    get_hosts(account_key, host_name, email)


def get_hosts(account_key, host_name, email):
    log_keys = []
    url = 'https://api.logentries.com/' + account_key + '/hosts/' + host_name + '/'
    response = urllib2.urlopen(url).read()
    hosts = json.loads(response)
    for log in hosts['list']:
        log_keys.append(log['key'])
    if log_keys:
        print "getting actions"
        retrieve_actions(log_keys, email, account_key)


def retrieve_actions(log_keys, email, account_key):
    request = {
        'request': 'list',
        'account': account_key,
        'acl': account_key
    }
    req = urllib2.Request('https://api.logentries.com/v2/actions')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(request))
    response_dict = json.loads(response.read())
    for action in response_dict['actions']:
        try:
            if action['args']['direct']:
                print action['args']['direct']
                action['args']['direct'] += ',' + email 
                update_action(action, account_key)
        except KeyError, e:
                print "Could not get email for Alert"


def update_action(action, account_key):
    request = {
        "id": action['id'],
        "type": action['type'],
        "rate_count": action['rate_count'],
        "rate_range": action['rate_range'],
        "limit_count": action['limit_count'],
        "limit_range": action['limit_range'],
        "schedule": action['schedule'],
        "args": action['args'],
        "request": "update",
        "account": account_key,
        "acl": account_key
    }
    req = urllib2.Request('https://api.logentries.com/v2/actions')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(request))
    response_dict = json.loads(response.read())
    print 'Update Alert with email %s', response_dict

if __name__ == '__main__':
    account_key = sys.argv[1]
    host_name = sys.argv[2]
    email = sys.argv[3]
    setup(account_key, host_name, email)

