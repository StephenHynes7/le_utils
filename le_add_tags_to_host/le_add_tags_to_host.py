import urllib2
import json
import sys
import copy

ACCOUNT_KEY = ''
HOST_NAME = ''
TAGS=[]

log_keys=[]

def get_logs():
    url = 'http://api.logentries.com/'+ ACCOUNT_KEY + '/hosts/'
    response = urllib2.urlopen(url).read()
    hosts = json.loads(response)
    for host in hosts['list']:
	print host['name']
	if host['name']==HOST_NAME:
        	url2 = 'http://api.logentries.com/'+ ACCOUNT_KEY + '/hosts/' + host['name'] + '/'
        	response2 = urllib2.urlopen(url2).read()
        	logs = json.loads(response2)
		for log in logs['list']:
            	   log_keys.append(log['key'])
    	print log_keys	
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
	print tag
        update_tag(tag)

def update_tag(tag):
    for source in tag['sources']:
    	log_keys.append(source)
    request = {
        'request': 'update',
        'account': ACCOUNT_KEY,
        'acl': ACCOUNT_KEY,
	'id': tag['id'],
	'name': tag['name'],
	'triggers' : tag['triggers'],
	'sources': log_keys,
	'groups': tag['groups'],
	'actions': tag['actions']
    }

    print json.dumps(request)
    req = urllib2.Request('https://api.logentries.com/v2/hooks')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(request))
    response_dict = json.loads(response.read())
    print response_dict


if __name__ == '__main__':
    ACCOUNT_KEY = sys.argv[1]
    HOST_NAME=sys.argv[2]
    get_logs()
