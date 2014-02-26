le_auto-tag
===========

This python script allows Logentries users to automatically create a tag based on data contained in a text file.

The text file format is seen below, a line must start with a Tag Name and must be then seperated by a pipe |. After the name you can addd as many patterns as you wish as long as they are seperated by a pipe.

	TAG_NAME | /regex pattern/ | string search pattern

Attached in this project is a sample text file with Heroku taggings that you can run to get Heroku Taggings for your log.

Setup
-----

To run this script simply download the file and run the following command,

	python le_auto-tag.py ACCOUNT_KEY FILE_LOCATION

You can find your Logentries Account Key here https://logentries.com/doc/accountkey/

The script will automatically go through the file and create a new Tag based on each line entry.
