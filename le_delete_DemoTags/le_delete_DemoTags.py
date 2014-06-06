import json
import sys
import argparse
import requests

class DeleteDemo(object):

	def __init__(self,account_key):
		self.account_key=account_key

	def get_hook_id(self):
		request={
		"request":"list",
		"account":self.account_key,
		"acl":self.account_key
		}
		req='https://api.logentries.com/v2/hooks'
		r=requests.post(req, data=json.dumps(request))
		HOOK=json.loads(r.text)
		for hook in HOOK['hooks']:
			if 'DemoTag' in hook['name']:
				self.delete_hook(hook['id'])

	
	def delete_hook(self,hook_id):
		request={
		"id":hook_id,
		"request":"delete",
		"account":self.account_key,
		"acl":self.account_key
		}
		req='https://api.logentries.com/v2/hooks'
		r=requests.post(req, data=json.dumps(request))
		print r.text


	def get_tag_id(self):
		request={
		"request":"list",
		"account":self.account_key,
		"acl":self.account_key
		}
		req='https://api.logentries.com/v2/tags'
		r=requests.post(req, data=json.dumps(request))			
		TAG=json.loads(r.text)
		for tag in TAG['tags']:
			if 'DemoTag' in tag['name']:
				self.delete_tag(tag['id'])

	def delete_tag(self,tag_id):
		request={
		"id":tag_id,
		"request":"delete",
		"account":self.account_key,
		"acl":self.account_key
		}
		req='https://api.logentries.com/v2/tags'
		r=requests.post(req, data=json.dumps(request))
		print r.text


				


def main():

	ap = argparse.ArgumentParser()
	ap.add_argument('account_key', help='ACCOUNT_KEY')
	args=ap.parse_args(sys.argv[1:])
	le=DeleteDemo(args.account_key)
	print 'deleating hook\n'
	le.get_hook_id()
	print 'deleating tags\n'
	le.get_tag_id()


if __name__ == '__main__':
    main()
