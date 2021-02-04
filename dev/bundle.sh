#!/bin/sh

echo ${VERSION-Unknown} > VERSION

sed -i "s/\${AGENT_VERSION}/${VERSION-Unknown}/g" docker-compose.yml

docker run --rm -v "${PWD}":/sca-agent -w /sca-agent aweponken/alpine-zip zip -r "${1-sca-agent.local.zip}" \
  logs \
  tools \
  volumes \
  .env.defaults \
  docker-compose.yml \
  LICENSE \
  README.md \
  setup.sh \
  VERSION
