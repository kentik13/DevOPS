#!/bin/bash
if [[ $(crontab -l | grep ntpdate | wc -l) == 1 ]]
  then echo "Found a ntpdate in cron,nothing to do...exit"
else
  echo "backup cron jobs..."
  sudo crontab -l > mycron
  echo "add ntpdate to cron file..."
  echo "0 0 * * * ntpdate -u 0.ca.pool.ntp.org" >> mycron
  echo "update cron jobs"
  sudo crontab mycron
  echo "remove old cron file"
  rm mycron
  echo "done...exit"
fi
