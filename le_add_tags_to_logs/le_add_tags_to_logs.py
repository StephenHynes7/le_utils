import argparse
import urllib2
import urllib
import json

def aggregate_logs(logs):
    hosts={}
    for i in range(len(logs))[::2]:
        if (logs[i] in hosts):
            hosts[logs[i]].append(logs[i + 1])
        else:
            hosts[logs[i]] = [logs[i + 1]]
    return hosts;

def get_logs(account_key, hosts):
    log_keys = []
    for h in hosts:
        url = 'https://api.logentries.com/' + account_key + '/hosts/' + urllib.quote_plus(h) + '/'
        response = urllib2.urlopen(url).read()
        logs = json.loads(response)
        for log in logs['list']:
            if (log['name'] in hosts[h] or log['filename'] in hosts[h]):
                log_keys.append(log['key'])

    return log_keys

def get_tags(account_key, userTags):
    request = {
        'request': 'list',
        'account': account_key,
        'acl': account_key
    }
    req = urllib2.Request('https://api.logentries.com/v2/hooks')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(request))
    allTags = json.loads(response.read())

    tags = []
    for tag in allTags['hooks']:
        if tag['name'] in userTags:
            tags.append(tag)

    return tags

def add_tags_to_logs(account_key, log_keys, tags):
    for tag in tags:
        new_source = False;
        for log_key in log_keys:
            if not (log_key in tag['sources']):
                tag['sources'].append(log_key)
                new_source = True;

        if new_source == True:
            request = {
                'request': 'update',
                'account': account_key,
                'acl': account_key,
                'id': tag['id'],
                'name': tag['name'],
                'triggers': tag['triggers'],
                'sources': tag['sources'],
                'groups': tag['groups'],
                'actions': tag['actions']
            }

            req = urllib2.Request('https://api.logentries.com/v2/hooks')
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(request))
            json.loads(response.read())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Add specified tags to all of specified logs in an account',
        usage='%(prog)s \n --logs HostName1 LogName1 [HostName2 LogName2 ...]\n --tags Tag1 [Tag2 Tag3 ...]\n --account-keys ACCOUNT_KEY')
    parser.add_argument('-l','--logs', nargs='+', required=True, metavar="HostName LogName");
    parser.add_argument('-t', '--tags', nargs='+', required=True, metavar="Tag");
    parser.add_argument('-k', '--account-key', nargs=1, required=True);
    args = parser.parse_args()

    if (len(args.logs) % 2 == 1):
        print("--logs must take a even number of argument. Pairs of HostName LogName.")
        exit(-1)

    hosts = aggregate_logs(args.logs);
    logs = get_logs(args.account_key[0], hosts)
    tags = get_tags(args.account_key[0], args.tags)

    add_tags_to_logs(args.account_key[0], logs, tags)
    exit(0)
