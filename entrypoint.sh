#!/bin/sh

rm -f /root/coinbase.lock
echo "Starting coinbase-dca Docker..."
if [ -z "$CRON_EXPRESSION" ]; then
  echo "Crontab Not Present running one time now"
  python main.py
else
  echo "$CRON_EXPRESSION /root/run.sh" > /etc/crontabs/root;
  echo "Next run will be scheduled by the following cron $CRON_EXPRESSION"
  crond -f -d 8;
fi