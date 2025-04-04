#!/bin/sh

FILE=/root/coinbase.lock

if [ ! -f "$FILE" ]; then
   touch $FILE
   echo "Starting work"
   cd /usr/app/src || exit
   python main.py
   rm $FILE
   echo "Finished work"
else
   echo "Lock-file present $FILE, try increasing time between runs, next schedule will be $CRON"
fi