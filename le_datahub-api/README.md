DataHub Connection API
========================

A simple example of creating a Connection via the Logentries API.

API Request
----------------

To create a Connection via the API please send a POST request to *https://logentries.com/hoover/api/new-connection/*

The request body should contain the following parameters

```json
        'name': 'Awesome New Connection',
        'pattern': 'mylog',
        'account_key': 'YOUR_ACCOUNT_KEY',
        'token': 'LOG_TOKEN',
        'source_tag': 'log1',
        'source_host': '127.0.0.1',
```


| Parameter     | Description
| ------------- |-------------|
| name          |The connection name that is displayed in the UI  |
| pattern       |A string or regex that will be used to set the Pattern field      |
| account_key   |The Users account_key, used for authentication.     |
| token         |The Log token to associate the connection with.     |
| source_tag    |A string or regex that will be used to set the Tag field    |
| source_host   |A string or regex that will be used to set the Host field.     |
