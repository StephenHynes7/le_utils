le_alert-util
=========

Script to configure all alerts to use a user supplied email address for a given host.

Setup
-----

Run the following command,

	python le_alert-util.py ACCOUNT_KEY HOST_NAME EMAIL

You can find your Logentries Account Key here https://logentries.com/doc/accountkey/

A sample command would be,

	python le_alert-util.py 12345 MyHost stephen@logentries.com
