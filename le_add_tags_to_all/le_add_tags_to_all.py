import urllib2
import urllib
import json
import sys

ACCOUNT_KEY = ''
TAGS = []
log_keys = []


def get_logs():
    url = 'https://api.logentries.com/' + ACCOUNT_KEY + '/hosts/'
    response = urllib2.urlopen(url).read()
    hosts = json.loads(response)
    print 'Getting log keys'
    for host in hosts['list']:
        host_name = urllib.quote_plus(host['name'])
        url2 = 'https://api.logentries.com/' + ACCOUNT_KEY + '/hosts/' + host_name + '/'
        response2 = urllib2.urlopen(url2).read()
        logs = json.loads(response2)
        for log in logs['list']:
            log_keys.append(log['key'])
    if log_keys:
        print "getting tags"
        get_tags()


def get_tags():
    request = {
        'request': 'list',
        'account': ACCOUNT_KEY,
        'acl': ACCOUNT_KEY
    }
    req = urllib2.Request('https://api.logentries.com/v2/hooks')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(request))
    tags = json.loads(response.read())

    for tag in tags['hooks']:
        print TAGS
        if not TAGS:
            print 'Adding %s to logs', tag
            update_tag(tag)
        elif tag['name'] in TAGS:
            print tag
            update_tag(tag)


def update_tag(tag):
    request = {
        'request': 'update',
        'account': ACCOUNT_KEY,
        'acl': ACCOUNT_KEY,
        'id': tag['id'],
        'name': tag['name'],
        'triggers': tag['triggers'],
        'sources': log_keys,
        'groups': tag['groups'],
        'actions': tag['actions']
    }

    req = urllib2.Request('https://api.logentries.com/v2/hooks')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(request))
    response_dict = json.loads(response.read())
    print response_dict


if __name__ == '__main__':
    ACCOUNT_KEY = sys.argv[1]
    print ACCOUNT_KEY
    try:
        TAGS = sys.argv[2:]
    except NameError:
        TAGS = []
    get_logs()
