import urllib2
import json
import sys
import re

ACCOUNT_KEY = ''
HOST_NAME = ''
EMAIL = ''


def setup():
    # TODO: Probably use something better then regex to validate email
    if all(re.search(".+@.+\..+", email) is not None for email in EMAIL_LIST): 
        get_hosts()
    else:
        print "Not a valid email address."


def get_hosts():
    log_keys = []
    url = 'https://api.logentries.com/' + ACCOUNT_KEY + '/hosts/' + HOST_NAME + '/'
    response = urllib2.urlopen(url).read()
    hosts = json.loads(response)
    for log in hosts['list']:
        log_keys.append(log['key'])
    if log_keys:
        print "getting actions"
        retrieve_actions(log_keys)


def retrieve_actions(log_keys):
    request = {
        'request': 'list',
        'account': ACCOUNT_KEY,
        'acl': ACCOUNT_KEY
    }
    req = urllib2.Request('https://api.logentries.com/v2/actions')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(request))
    response_dict = json.loads(response.read())
    for action in response_dict['actions']:
        try:
            if action['args']['direct']:
                print action['args']['direct']
                action['args']['direct'] = ','.join(EMAIL_LIST)
                update_action(action)
        except KeyError, e:
                print ""


def update_action(action):
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
        "account": ACCOUNT_KEY,
        "acl": ACCOUNT_KEY
    }
    print json.dumps(request)
    req = urllib2.Request('https://api.logentries.com/v2/actions')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(request))
    response_dict = json.loads(response.read())
    print response_dict

if __name__ == '__main__':
    ACCOUNT_KEY = sys.argv[1]
    HOST_NAME = sys.argv[2]
    EMAIL_LIST = sys.argv[3:]
    setup()
