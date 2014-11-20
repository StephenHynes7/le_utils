import requests
import json
#!/usr/bin/env python


def postRequest():
    #Make sure to fill these values
    # name    The connection name that is displayed in the UI
    # pattern     A string or regex that will be used to set the Pattern field.
    # account_key     The Users account_key, used for authentication.
    # token   The Log token to associate the connection with.
    # source_tag   A string or regex that will be used to set the Tag field.
    # source_host     A string or regex that will be used to set the Host field.

    request = {
        'name': '',
        'pattern': '',
        'account_key': '',
        'token': '',
        'source_tag': '',
        'source_host': '',
    }
    r = requests.post("https://logentries.com/hoover/api/new-connection/",
                      data=json.dumps(request), verify=False)
    print r.text

if __name__ == '__main__':

    postRequest()
