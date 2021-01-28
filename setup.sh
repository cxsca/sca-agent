#!/bin/sh

echo "Initializing .env file..."

if test ! -f ".env"; then
  cp .env.defaults .env

  placeHolder="{GenKey()}"
  for str in $(grep ${placeHolder} .env); do sed -i "s/${placeHolder}/$(openssl rand -hex 12)/" .env; done
fi

echo "Pulling docker images..."

docker --version
docker-compose --version

docker-compose pull

echo "Ensuring logs directory exists..."

mkdir -p "$(grep LOG_LOCATION .env | cut -d'=' -f 2)"

echo "Setup completed. Run 'docker-compose up -d' to start the agent."
