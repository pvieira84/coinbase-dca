#!/bin/sh

rm -f /root/coinbase.lock
echo "Starting coinbase-dca Docker..."
echo "Settings used"
echo "Trading pair: $TRADING_PAIR"
echo "Order size: $ORDER_SIZE"
if [ -z "$CRON_EXPRESSION" ]; then
  echo "Crontab Not Present running one time now"
  python main.py
else
  echo "$CRON_EXPRESSION /root/run.sh" > /etc/crontabs/root;
  echo "Next run will be scheduled by the following cron $CRON_EXPRESSION"
  crond -f -d 8;
fi