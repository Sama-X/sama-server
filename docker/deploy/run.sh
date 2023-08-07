#!/bin/sh
# wait for mysql to start
Path="/app/data/sama/logs"

if [ ! -d ${Path} ]; then
  mkdir ${Path}
fi
supervisord -n -c docker/supervisord.conf
