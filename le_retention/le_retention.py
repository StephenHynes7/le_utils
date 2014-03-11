import urllib2
import json
import sys

ACCOUNT_KEY = ''
LOG_KEY = ''
LOG_NAME = ''
MONTH = 2678400000
WEEK = 604800000


def set_retention_of_log():
    request = 'request=set_log&user_key='+ACCOUNT_KEY+'&log_key='+LOG_KEY+'&name='LOG_NAME'&retention='+MONTH
    req = urllib2.Request('https://api.logentries.com/')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, request)
    response_dict = json.loads(response.read())
    print response_dict


if __name__ == '__main__':
    ACCOUNT_KEY = sys.argv[1]
    LOG_KEY = sys.argv[2]
    LOG_NAME = sys.argv[3]
    set_retention_of_log()

