#!/bin/bash

#This script will execute the command to follow all the log in a directory. To run it you need:
# 1) specify 'path_to_your_logs' with the directory in which the logs that you want to follow are
# 2) run the bash file   

#If you want to follow all the logs in the specific directory AND in the subdirectories you will need to delete the '-maxdepth 1'

Dir_to_follow=("path_to_your_logs")
find $Dir_to_follow -maxdepth 1 -name '*.log' -exec sudo le follow '{}' \; 

echo 'Restarting the Agent'
sudo service logentries restart
echo 'Remember to refresh the Logentries page to see your new logs'



 

