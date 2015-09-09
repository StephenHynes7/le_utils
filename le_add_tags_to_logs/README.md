le\_add\_tags\_to\_logs
======================

Script to add specified tags to specified logs in an account.

Usage
-----
```
python le_add_tags_to_logs.py -h

usage: le_add_tags_to_logs.py
 --logs HostName1 LogName1 [HostName2 LogName2 ...]
 --tags Tag1 [Tag2 Tag3 ...]
 --account-keys ACCOUNT_KEY

Add specified tags to all of specified logs in an account

optional arguments:
  -h, --help            show this help message and exit
  -l HostName LogName [HostName LogName ...], --logs HostName LogName [HostName LogName ...]
  -t Tag [Tag ...], --tags Tag [Tag ...]
  -k ACCOUNT_KEY, --account-key ACCOUNT_KEY
```
