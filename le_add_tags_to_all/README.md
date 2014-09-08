le\_add\_tags\_to\_all
======================

Script to add specified tags to all of the logs in an account.

Usage
-----

To run the script:

    python le_add_tags_to_all.py ACCOUNT_KEY TAG1 [TAG2...] 

You can find your Logentries Account Key here https://logentries.com/doc/accountkey/
 

A sample command would be:

    python le_add_tags_to_all.py 1234 Error Exception

If no tag is specified all tags will be added to all logs in your Account.
