#!/usr/bin/env bash
sudo rm /tmp/.X0-lock
/wx-entrypoint.sh &
sleep 5
inject-monitor &
wait
