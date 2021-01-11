#!/bin/sh

echo "Initializing .env file..."

if test ! -f ".env"; then
  cp .env.defaults .env
fi

echo "Resolving SCA Agent version..."

if test ! -f "VERSION"; then
	build_agent_version="0.0.0"
else
	build_agent_version="$(cat VERSION)"
fi

env_agent_version="$(grep AGENT_VERSION .env | cut -d'=' -f 2)"

buildv=`echo $build_agent_version | sed 's/\.//g'`
envv=`echo $env_agent_version | sed 's/\.//g'`

if [ -z "$env_agent_version" ]
  then
		echo "\nAGENT_VERSION=$build_agent_version" >> .env
		echo "Added AGENT_VERSION variable to .env"
elif [ $buildv -gt $envv ];
  then
    sed -i "s/AGENT_VERSION=$env_agent_version/AGENT_VERSION=$build_agent_version/g" .env
		echo "UPGRADED AGENT_VERSION from $env_agent_version to $build_agent_version"
fi

echo "Pulling docker images..."

docker --version
docker-compose --version

docker-compose pull

echo "Ensuring logs directory exists..."

mkdir -p "$(grep LOG_LOCATION .env | cut -d'=' -f 2)"

echo "Setup completed. Run 'docker-compose up -d' to start the agent."
