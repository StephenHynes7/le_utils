le\_add\_logset\_to\_alert
======================

Script to add a logset to a specific alert in your Logentries Account

Usage
-----

To run the script:

    python le_add_tags_to_all.py ACCOUNT_KEY ALERT_NAME LOG_SET_NAME

* You can find your Logentries Account Key here https://logentries.com/doc/accountkey/.

* Alert name is case insensitive

* Log Set name is case sensitive

A sample command would be:

    python le_add_logset_to_alert.py XXXX MyAlert MyLogSet

