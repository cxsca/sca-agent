#!/bin/bash

docker-compose -f $1 up --build --exit-code-from $2-test
if [[ $? -eq 0 ]]
then
    echo "Test Passed!"
else
    echo "Error : Test Failed!"
    exit 1
fi