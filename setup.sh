#!/bin/sh

echo "Initializing .env file..."

if test ! -f ".env"; then
  docker run --rm -v "${PWD}":/sca-agent -w /sca-agent python:slim python create-env-file.py
fi

echo "Pulling docker images..."

docker --version
docker-compose --version

docker-compose pull

echo "Ensuring logs directory exists..."

mkdir -p "$(grep LOG_LOCATION .env | cut -d'=' -f 2)"

echo "Setup completed. Run 'docker-compose up -d' to start the agent."
