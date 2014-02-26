le_update
=========

Script to run along side auto scaling to update all Logentries Tags and Alerts to include the new logs being followed by the agent running the given machine.

Setup
-----
**You must have the [Logentries Agent](https://logentries.com/doc/agent/)  registered and following a file for this script to work**

Run the following command,

	sudo python le_update.py ACCOUNT_KEY

You can find your Logentries Account Key here https://logentries.com/doc/accountkey/
