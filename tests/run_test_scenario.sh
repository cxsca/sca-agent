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
      placeholder=$(echo "$line" | grep -o "%.\+")
      
      if [ ! -z ${placeholder} ] ; then
        var=$(echo "$placeholder" | sed "s|%||g")
        varvalue=$(eval echo \$${var})
        if [ -z ${varvalue} ] ; then
               echo "Missing environment variable ${placeholder}"
               exit 1
        else
              output=$(echo "$line" | sed "s/${placeholder}/${varvalue}/g")
              echo "$output" >> .env
        fi
      else
        echo "$line" >> .env
      fi
    done
fi

echo "======Run Agent======"
docker-compose -f docker-compose.yml -p "$testName-agent" up -d

sleep 5s

echo "======Run Test======"
docker-compose -f "tests/$testName/docker-compose.yml" up --build --exit-code-from "$testName-test"
test_exit_code=$?

echo "======Shutdown Agent======"
docker-compose -f docker-compose.yml -p "$testName-agent" down

echo "======Shutdown Test======"
docker-compose -f "tests/$testName/docker-compose.yml" down

exit $test_exit_code
