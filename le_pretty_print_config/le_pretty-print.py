import requests
import sys
import json


def setup(account_key):
    if account_key is None:
        print "No account key has been submitted. Exiting"
        raise
    else:
        get_config(account_key)
        # pretty_print_config(config)


def get_config(account_key):
    request = requests.get("https://api.logentries.com/%s/hosts/" % account_key)
    if request.status_code == 200:
        data = json.dumps(request.text, separators=(',', ':'), indent=4, sort_keys=True)
        print data

# def pretty_print_config(config):

if __name__ == '__main__':
    account_key = sys.argv[1]
    setup(account_key)
