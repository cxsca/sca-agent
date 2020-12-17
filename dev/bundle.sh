#!/bin/sh

echo ${VERSION-Unknown} > VERSION

cp .env .env.template

docker run --rm -v "${PWD}":/sca-agent -w /sca-agent aweponken/alpine-zip zip -r "${1-sca-agent.local.zip}" \
  README.md \
  setup.sh \
  show-scans-status.sh \
  .env.template \
  docker-compose.yml \
  volumes \
  logs \
  VERSION \
  LICENSE
