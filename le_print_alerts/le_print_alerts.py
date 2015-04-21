import urllib2
import json
import sys


def main(account_key):
    hooks = get_hooks(account_key)
    print_alerts(account_key, hooks)


def get_hooks(account_key):
    request = {
        'request': 'list',
        'account': account_key,
        'acl': account_key
    }
    req = urllib2.Request('https://api.logentries.com/v2/hooks')
    req.add_header('Content-Type', 'application/json')
    data = {}
    try:
        response = urllib2.urlopen(req, json.dumps(request))
        data = json.loads(response.read())
    except Exception, e:
        raise e
    return data


def print_alerts(account_key, hooks):
    print json.dumps(hooks['hooks'], indent=4, separators={':', ';'})


if __name__ == '__main__':
    account_key = sys.argv[1]
    main(account_key)
