le\_follow\_all
======================

Script to follow all the logs in a directory

Usage
-----

To run the script:

Download the script from github and save it in a directory 

Open the file and change the variable *path\_to\_your\_logs* with the directory where your logs are 

From the terminal run the following:
	
	./le_follow_all.sh
	
    	   
Further Details:
----

The script will follow all of the \*.log files in the local directory. If you want to follow all of the \*.log files in the subdirectories you can do it by deleting    the option `-maxdepth 1` in the **find** command in the script.
