import sys
import json
import urllib2


def main(account_key, alert_name, log_set_name):
    alert = get_alert(account_key, alert_name)
    log_set = get_log_set_keys(account_key, log_set_name)
    if alert is not None:
        add_logs_to_alerts(alert, log_set)
    else:
        raise ''


def get_log_set_keys(account_key, log_set_name):
    url = 'https://api.logentries.com/%s/hosts/%s' % (account_key, log_set_name)
    log_sets = {}
    keys = []
    try:
        response = urllib2.urlopen(url).read()
        log_sets = json.loads(response)
        if 'logs' in log_sets:
            # log_sets is all logs of a host
            for logkey in log_sets['logs']:
                keys.append(logkey['key'])
        else:
            # log_sets is the specific log of a host
            keys.append(log_sets['key'])
    except Exception, e:
        raise e
    return keys


def get_alert(account_key, alert_name):
    request = {
        'request': 'list',
        'account': account_key,
        'acl': account_key
    }
    req = urllib2.Request('https://api.logentries.com/v2/hooks')
    req.add_header('Content-Type', 'application/json')
    try:
        response = urllib2.urlopen(req, json.dumps(request))
        hooks = json.loads(response.read())
        for item in hooks['hooks']:
            name = item['name'].encode('utf8')
            if name.lower() == alert_name.lower():
                print 'Found match'
                return item

    except Exception, e:
        raise e
    return {}


def add_logs_to_alerts(alert, log_keys):
    keys = alert['sources'] + log_keys
    request = {
        'request': 'update',
        'account': alert['account_id'],
        'acl': alert['account_id'],
        'id': alert['id'],
        'name': alert['name'],
        'triggers': alert['triggers'],
        'sources': keys,
        'groups': alert['groups'],
        'actions': alert['actions']
    }
    req = urllib2.Request('https://api.logentries.com/v2/hooks')
    req.add_header('Content-Type', 'application/json')
    try:
        response = urllib2.urlopen(req, json.dumps(request))
        message = json.loads(response.read())
        status = message['status'].encode('utf8')
        print 'Status is %s' % message['status']
        if status == 'ok':
            print 'Sucessfully updated alert'
    except Exception, e:
        raise e


if __name__ == '__main__':
    account_key = sys.argv[1]
    alert_name = sys.argv[2]
    log_set_name = sys.argv[3]
    main(account_key, alert_name, log_set_name)
