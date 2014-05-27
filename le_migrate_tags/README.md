le\_migrate\_tags
-------------------
-------------------

Script to migrate all the Tags/Alerts from one account to another

Overview:
-------

This script allows to export all the Tags/Alerts from one account into a file and to import them from a file into a second account.


Usage:
------


To run the script:

Download it from github and save it in a directory. 

From the Terminal move into that directory and run the following: 

	python le_migrate_tags.py ACCOUNT_1_KEY export filename.txt

Where ACCOUNT\_1\_KEY is the Key of the account from where you want to export the Tags/Alerts and filename.txt is the name of the file where you want to export the data

You should now see in your working directory a file with all the data that you want to import.

From the Terminal run the following:

	python le_migrate_tags.py ACCOUNT_2_KEY import filename.txt

Where ACCOUNT\_2_KEY is the Key of the account where you want to import the Tags/Alerts


Help:
-----

If you need help on how to use the script run the following:

	python le_migrate_tags -h

