#!/bin/sh

testName=$1

if [ -z "$TEST_SCA_TENANT" ]; then
    echo "TEST_SCA_TENANT is not set"
    exit 1
elif [ -z "$TEST_SCA_USERNAME" ]; then
    echo "TEST_SCA_USERNAME is not set"
    exit 1
elif [ -z "$TEST_SCA_PASSWORD" ]; then
    echo "TEST_SCA_PASSWORD is not set"
    exit 1
fi

bundle_overrides_dir="tests/$testName/bundle-overrides"

if [ -d "$bundle_overrides_dir" ]; then
    echo "======Copy Bundle Overrides======"
    cp -a "$bundle_overrides_dir/." .
fi

echo "======Setup Agent======"
chmod +x setup.sh
./setup.sh

if test -f ".env.overrides"; then
    echo "======Override Agent Environment Variables======"

    echo "\n" >> .env
    for line in $(cat .env.overrides); do
        echo "$line" >> .env
    done
fi

echo "======Run Agent======"
docker-compose -f docker-compose.yml -p "$testName-agent" up -d

sleep 5s

echo "======Run Test======"
docker-compose -f "tests/$testName/docker-compose.yml" up --build --abort-on-container-exit

echo "======Shutdown Agent======"
docker-compose -f docker-compose.yml -p "$testName-agent" down

echo "======Shutdown Test======"
docker-compose -f "tests/$testName/docker-compose.yml" down