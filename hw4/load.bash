#!/bin/bash
$@ &
PID=$!
i=1
sp="/-\|"
echo -n 'process running  '
while [ -d /proc/$PID ]
do
  printf "\b${sp:i++%${#sp}:1}"
  sleep 1
done
printf '\nprocess finished'