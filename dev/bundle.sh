#!/bin/sh

echo ${VERSION-Unknown} > VERSION

sed -i "s/SCA_AGENT_VERSION: \${AGENT_VERSION}/SCA_AGENT_VERSION: ${VERSION-Unknown}/g" docker-compose.yml

docker run --rm -v "${PWD}":/sca-agent -w /sca-agent aweponken/alpine-zip zip -r "${1-sca-agent.local.zip}" \
  README.md \
  setup.sh \
  show-scans-status.sh \
  .env.defaults \
  docker-compose.yml \
  volumes \
  logs \
  VERSION \
  LICENSE
