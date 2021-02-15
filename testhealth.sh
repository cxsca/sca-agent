#!/bin/bash

docker-compose -f tests/health/docker-compose.yml up --build --exit-code-from health-test
if [[ $? -eq 0 ]]
then
    echo "Test Passed!"
else
    echo "Error : Test Failed!"
    exit 1
fi