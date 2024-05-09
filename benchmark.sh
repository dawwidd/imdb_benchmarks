#!/bin/bash

# Start dockers for singular instances
docker-compose -f single-instance.yml up -d  > /dev/null

# Run the benchmark for single instance
node index.js

# Stop the containers
docker-compose -f single-instance.yml down  > /dev/null


# Start dockers for triple instances
./setup-triple.sh  > /dev/null

# Run the benchmark for triple instance
node index.js 3 

# Stop the containers
docker-compose -f triple-instance.yml down  > /dev/null


# Start dockers for ten instances
./setup-ten.sh > /dev/null

# Run the benchmark for ten instance
node index.js 10

# Stop the containers
docker-compose -f ten-instance.yml down > /dev/null

