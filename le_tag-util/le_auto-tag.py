import sys
import random
import urllib2
import urllib
import json

FILE_NAME=''
ACCOUNT_KEY=''
LOG_KEYS=[]


def get_account_data():
	response = urllib2.urlopen('https://api.logentries.com/'+ACCOUNT_KEY+'/hosts/').read()
	hosts = json.loads(response)
	search_hosts(hosts['list'])
	open_file()

def search_hosts(hosts):
	print "finding hosts"
	for host in hosts:
		print host['name']
		url = 'https://api.logentries.com/'+ACCOUNT_KEY+'/hosts/'+host['name']+'/'
		url = url.replace(' ','%20')
		response = urllib2.urlopen(url).read()
		logs = json.loads(response)
		logs = logs['list']
		set_log_keys(logs)

def set_log_keys(logs):
	for log in logs:
		LOG_KEYS.append(log['key'])

def open_file():
	try:
		regex_file = open(FILE_NAME, 'r')
		for line in regex_file:
			name = line.split('|')[0]
			list_of_regex = []
			for count, regex in enumerate(line.split('|')):
				if count != 0:
					list_of_regex.append(regex)
			create_data(name,list_of_regex)
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

def create_data(name,regex):
	color = generate_color()
	label_id = create_label(name , color)
	tag_id = create_tag(label_id)
	create_hook(name ,regex , tag_id)

def generate_color():
	r = lambda: random.randint(0,255)
	color = ('%02X%02X%02X' % (r(),r(),r()))
	return color

def create_label(name, color):
	request = {
		'name': name,
		'title': name,
		'description': name,
		'appearance': {
			'color': color
		},
		'request': 'create',
		'account': ACCOUNT_KEY,
		'acl': ACCOUNT_KEY
	}

	req = urllib2.Request('https://api.logentries.com/v2/tags')
	req.add_unredirected_header('Content-Type','application/json')
	response = 	urllib2.urlopen(req, json.dumps(request))
	response_dict = json.loads(response.read())
	if response_dict['status'] == 'ok':
		return response_dict['sn']

def create_tag(sn):
	request = {
		'type': 'tagit',
		'rate_count': 0,
		'rate_range': 'day',
		'limit_count': 0,
		'limit_range': 'day',
		'schedule': [],
		'type': 'tagit',
		'args': {
			'sn': sn,
			'tag_sn': sn
		},
		'request': 'create',
		'account': ACCOUNT_KEY,
		'acl': ACCOUNT_KEY
	}
	req = urllib2.Request('https://api.logentries.com/v2/actions')
	req.add_header('Content-Type', 'application/json')
	response = urllib2.urlopen(req, json.dumps(request))
	response_dict = json.loads(response.read())
	if response_dict['status'] == 'ok':
		return response_dict['id']

def create_hook(name, regex ,tag_id):
	request = {
		'name': name,
		'triggers': regex,
		'sources':LOG_KEYS,
		'groups': [],
		'actions': [
			tag_id
		],
		'request': 'create',
		'account': ACCOUNT_KEY,
		'acl': ACCOUNT_KEY
	}
	req = urllib2.Request('https://api.logentries.com/v2/hooks')
	req.add_header('Content-Type', 'application/json')
	response = urllib2.urlopen(req, json.dumps(request))
	response_dict = json.loads(response.read())
	print "hooks"
	print json.dumps(request)
	print response_dict

if __name__ == '__main__':
	ACCOUNT_KEY = sys.argv[1]
	FILE_NAME = sys.argv[2]
	get_account_data()
