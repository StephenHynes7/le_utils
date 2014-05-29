import urllib2
import json
import sys
import argparse
import requests


class LeClient(object):

    def __init__(self, account_key):
        self.account_key = account_key

    def get_hook(self):
        request = {
            'request': 'list',
            'account': self.account_key,
            'acl': self.account_key
        }
        req = urllib2.Request('https://api.logentries.com/v2/hooks')
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(request))
        hooks = json.loads(response.read())
        return hooks['hooks']

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
        return tags['tags']

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
        return actions['actions']

    def create_json_object(self):
        json_object = {}
        print 'Starting to Export Hook Objects'
        json_object["Hooks"] = self.get_hook()
        for hook in json_object["Hooks"]:
        	hook['account_id']=''
        print 'Finished Exporting Hook Objects'
        print 'Starting to Export Tag Objects'
        json_object["Tags"] = self.get_tags()
        for tag in json_object["Tags"]:
        	tag['account_id']=''
        print 'Finished Exporting Tag Objects'
        print 'Starting to Export Action Objects'
        json_object["Actions"] = self.get_actions()
        for act in json_object["Actions"]:
        	act['account_id']=''
        print 'Finished Exporting Tag Objects'
        return json.dumps(json_object)

    def upload_hook(self, hook, actions, tags):
        print 'Creating %s Tag/Alert' % hook['name']
        request = {
            "name": hook['name'],
            "triggers": hook['triggers'],
            "sources": hook['sources'],
            "groups": [],
            "actions": [],
            "request": "create",
            "account": self.account_key,
            "acl": self.account_key
        }
        req = 'https://api.logentries.com/v2/hooks'
        headers = {'Content-Type': 'application/json'}
        for Id in hook['actions']:
            for act in actions:
                if act['id'] == Id:
                    request['actions'].append(self.upload_actions(act, tags))
        requests.post(req, data=json.dumps(request), headers=headers)

    def upload_actions(self, actions, tags):
        request = {
            "rate_count": actions['rate_count'],
            "rate_range": actions['rate_range'],
            "limit_count": actions['limit_count'],
            "limit_range": actions['limit_range'],
            "schedule": [],
            "type": actions['type'],
            "args": actions['args'],
            "request": "create",
            "account": self.account_key,
            "acl": self.account_key
        }
        req = 'https://api.logentries.com/v2/actions'
        headers = {'Content-Type': 'application/json'}
        if actions['type'] == 'tagit':
            for tag in tags:
                if tag['sn'] == int(actions['args']['sn']):
                    actions['args']['sn'] = self.upload_tags(tag)

        r = requests.post(req, data=json.dumps(request), headers=headers)
        actions = json.loads(r.text)
        return actions['id']

    def upload_tags(self, tags):
        request = {
            "name": tags['name'],
            "title": tags['title'],
            "description": tags['description'],
            "appearance": tags['appearance'],
            "request": "create",
            "account": self.account_key,
            "acl": self.account_key
        }
        req = 'https://api.logentries.com/v2/tags'
        headers = {'Content-Type': 'application/json'}
        r = requests.post(req, data=json.dumps(request), headers=headers)
        response = json.loads(r.text)
        return response['sn']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        'account_key', help='If you want to export tags put the account key of the account you want to take tags from \n\n If you want to import tags on your account put your account key')
    ap.add_argument('action', choices=['import', 'export'],
                    help='Choose export if you want to export the tags from an account\n\n Choose import if you want to import someone else tags into your account')
    ap.add_argument(
        'filename', help='Choose the file name where you want to export/import the tags')
    args = ap.parse_args(sys.argv[1:])
    le = LeClient(args.account_key)
    if args.action == 'export':
        print 'Starting Exporting Tags and Alerts to File.'
        file = open(args.filename, 'w+')
        file.write(le.create_json_object())
        print 'Finished Exporting Tags and Alerts to File.'
    else:
        print 'Starting Importing Tags and Alerts to File.'
        file = open(args.filename, 'r')
        print 'Starting to read Export file.'
        object_all = json.loads(file.read())
        print 'Finished reading Export file.'
        Hooks = object_all['Hooks']
        Actions = object_all['Actions']
        Tags = object_all['Tags']
        print 'Starting to create Tags/Alerts.'
        for hook in Hooks:
            le.upload_hook(hook, Actions, Tags)
        print 'Finished creating Tags/Alerts.'


if __name__ == '__main__':
    main()
