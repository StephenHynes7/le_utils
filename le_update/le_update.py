import urllib2
import json
import subprocess
import re
import sys

ACCOUNT_KEY = ''

def setVars():
	output = subprocess.check_output(['le', 'whoami'])
	key = re.search("[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}",output)
	if key is not None:
		get_hosts(key.group())

def get_hosts(key):
	log_keys = []
	url = 'http://api.logentries.com/'+ACCOUNT_KEY+'/hosts/'+key+'/'
	response = urllib2.urlopen(url).read()
	hosts = json.loads(response)
	for log in hosts['list']:
		log_keys.append(log['key'])
	if log_keys:
		print "getting hooks"
		retrieve_hooks(log_keys)

def retrieve_hooks(log_keys):
	request = {
		'request':'list',
		'account': ACCOUNT_KEY,
		'acl': ACCOUNT_KEY
	}
	req = urllib2.Request('https://api.logentries.com/v2/hooks')
	req.add_header('Content-Type', 'application/json')
	response = urllib2.urlopen(req, json.dumps(request))
	response_dict = json.loads(response.read())
	for hook in response_dict['hooks']:
		hook['sources'] = hook['sources'] + log_keys
		print  'Updating Tag&Alert ' + hook['name']
		update_hook(hook)

def update_hook(hook):
	request = {
		'name': hook['name'],
		'id': hook['id'],
		'triggers': hook['triggers'],
		'sources': hook['sources'],
		'groups': [],
		'actions': hook['actions'],
		'request': 'update',
		'account': ACCOUNT_KEY,
		'acl': ACCOUNT_KEY
	}
	print json.dumps(request)
	req = urllib2.Request('https://api.logentries.com/v2/hooks')
	req.add_header('Content-Type', 'application/json')
	response = urllib2.urlopen(req, json.dumps(request))
	response_dict = json.loads(response.read())
	print response_dict

if __name__ == '__main__':
	ACCOUNT_KEY = sys.argv[1]
	setVars()