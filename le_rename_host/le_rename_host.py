import json
import urllib2
import urllib
import sys


def main(account_key, logset_name, new_logset):
    logset_key = get_logset(account_key, logset_name)
    rename_logset(account_key, logset_key, new_logset)


def get_logset(account_key, logset_name):
    url = 'https://api.logentries.com/%s/hosts/%s' %(account_key, logset_name)
    logset = {}
    logset_key = ''
    try:
        response = urllib2.urlopen(url).read()
        logset = json.loads(response)
        logset_key = logset['key']
    except Exception, e:
        raise e
    return logset_key


def rename_logset(account_key, logset_key, new_logset):
    request = {
        'request': 'set_host',
        'user_key': account_key,
        'host_key': logset_key,
        'name': new_logset,
        'hostname': new_logset
    }
    req = urllib2.Request('https://api.logentries.com/')
    req.add_header('Content-Type', 'application/json')
    try:
        response = urllib2.urlopen(req, urllib.urlencode(request))
        msg = json.loads(response.read())
        print 'API call was %s' % msg['response']
    except Exception, e:
        raise e

if __name__ == '__main__':
    account_key = sys.argv[1]
    logset_name = sys.argv[2]
    new_logset = sys.argv[3]
    main(account_key, logset_name, new_logset)
