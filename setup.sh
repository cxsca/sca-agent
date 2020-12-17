#!/bin/sh

echo "Copying .env file..."

if test -f ".env"; then
  mv .env.template .env
fi

echo "Pulling docker images..."

docker --version
docker-compose --version

docker-compose pull

echo "Ensuring logs directory exists..."

mkdir -p "$(grep LOG_LOCATION .env | cut -d'=' -f 2)"

echo "Setup completed. Run 'docker-compose up -d' to start the agent."
