#!/usr/bin/env bash
sudo rm /tmp/.X0-lock
/wx-entrypoint.sh &
sleep 5
inject-monitor &
sleep 5
DEMO_SERVICE=${DEMO_SERVICE:-yes}
case $DEMO_SERVICE in
  true|yes|y|1)
    demo-service-start &
    ;;
esac
wait
