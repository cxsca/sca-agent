#!/bin/sh

export EXTERNAL_HOSTNAME=reverse-proxy
(while [ ! -f ./logs/*.log ]; do sleep 1; done; tail -f ./logs/*) &

docker-compose up -d

docker-compose -f dev/docker-compose-e2e.yml up --abort-on-container-exit
exit_code=$?

docker-compose down
docker-compose -f dev/docker-compose-e2e.yml down

jobs
kill %1
exit $exit_code