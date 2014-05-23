import urllib2
import json
import sys
import copy
import argparse
import requests


class LeClient(object):

    def __init__(self,account_key):
        self.account_key=account_key

    def get_hook(self):
        request = {
            'request': 'list',
            'account': self.account_key,
            'acl': self.account_key
        }
        req = urllib2.Request('https://api.logentries.com/v2/hooks')
        req.add_header('Content-Type', 'application/json') #This is what I expect to receive (Json)
        response = urllib2.urlopen(req, json.dumps(request)) #Ask Peter/Stephen to explain
        hook = json.loads(response.read())
       # print '\n\nHOOKS\n',hook['hooks']
        return hook
       

    def get_tags(self):
        request = {
            'request': 'list',
            'account': self.account_key,
            'acl': self.account_key
        }
        req = urllib2.Request('https://api.logentries.com/v2/tags')
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(request))
        tags = json.loads(response.read())
        # print '\n\nTAGS\n',tags
        return tags

    def get_actions(self):
        request = {
            'request': 'list',
            'account': self.account_key,
            'acl': self.account_key
        }
        req = urllib2.Request('https://api.logentries.com/v2/actions')
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(request))
        actions = json.loads(response.read())
    #    print '\n\nACTIONS\n',actions
        return actions

    def create_json_object(self):
        json_object_app={}
        json_object_app["Hooks"]=self.get_hook()
        json_object_app["Tags"]=self.get_tags()
        json_object_app["Actions"]=self.get_actions()
        return json.dumps(json_object_app)



        
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('account_key',help='If you want to export tags put the account key of the account you want to take tags from \n\n If you want to import tags on your account put your account key')
    ap.add_argument('action',choices=['import','export'],help='Choose export if you want to export the tags from an account\n\n Choose import if you want to import someone else tags into your account')
    ap.add_argument('filename',help='Choose the file name where you want to export/import the tags')
    args=ap.parse_args(sys.argv[1:])
    print args
    le=LeClient(args.account_key)
    if args.action=='export':
        file = open(args.filename,'w+')
        file.write(le.create_json_object())
    else:
        request = {
            'request': 'list',
            'account': args.account_key,
            'acl': args.account_key
        }
        json_data=open(args.filename)
        json_big_object=json.load(json_data)
        Hooks=json.dumps(json_big_object['Hooks'])
        Tags=json.dumps(json_big_object['Tags'])
        Actions=json.dumps(json_big_object['Actions'])
        req1='https://api.logentries.com/v2/hooks'
        headers={'Content-Type': 'application/json'}
        r1 = requests.post(req1,Hooks)
        print r1.status_code
        print r1.content
        req2='https://api.logentries.com/v2/tags'
        r2 = requests.post(req2,Tags)
        print r2
        print r2.status_code
        print r2.content
        req3='https://api.logentries.com/v2/actions'
        r3 = requests.post(req3,Actions)

       

if __name__ == '__main__':
    main()

    