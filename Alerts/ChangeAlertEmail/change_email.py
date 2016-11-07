import requests
import json
import argparse

def get_alerts(api_key):
    headers = {'x-api-key': api_key}
    url = "https://rest.logentries.com/management/actions"
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        print('Successfully retrieved alerts')
        return req.json()
    else:
        print('Error getting alerts. ErrorMessage: {}'.format(req.text))
        exit(1)


def update_alert(alert, api_key):
    headers = {'Content-type': 'application/json', 'x-api-key': api_key}
    url = "https://rest.logentries.com/management/actions/{}".format(alert['id'])
    act = {"action": alert}
    req = requests.put(url, data=json.dumps(act, separators=(',', ':')), headers=headers)
    if req.status_code == 200:
        print('Successfully updated alert {}'.format(alert['id']))


def update_alerts(alerts, email, append, api_key):
    for action in alerts['actions']:
        for idx,target in enumerate(action['targets']):
            if append:
                target['param_set']['direct'] = target['param_set']['direct'] + ',' + email
            else:
                target['params_set'] = {
                        "users": "",
                        "direct": email,
                        "teams": ""
                    }
            action['targets'][idx] = target
        update_alert(action, api_key)

def main(email, api_key, append=False):
    alerts = get_alerts(api_key)
    update_alerts(alerts, email, append, api_key)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--email', help='The email to be used or appended to all alerts.', required=True)
    ap.add_argument('--api_key', help='Your Logentries API key.', required=True)
    ap.add_argument('--append', help='Append your email to existing emails. By default set to false.', required=False)
    args = ap.parse_args()
    main(args.email, args.api_key, args.append)