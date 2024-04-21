#!/bin/bash

# Start Docker Compose services
echo "Starting Redis containers..."
docker-compose -f triple-instance.yml up -d

# Wait for containers to fully start
echo "Waiting for Redis containers to initialize..."
sleep 3

# Fetch IPs of Redis containers dynamically
REDIS_IP1=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f triple-instance.yml ps -q redis0))
REDIS_IP2=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f triple-instance.yml ps -q redis1))
REDIS_IP3=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f triple-instance.yml ps -q redis2))

# Ensure IPs are not empty
if [ -z "$REDIS_IP1" ] || [ -z "$REDIS_IP2" ] || [ -z "$REDIS_IP3" ]; then
  echo "Error fetching Redis IPs. Exiting."
  exit 1
fi

# Create the Redis cluster using the fetched IP addresses
echo "Creating Redis cluster with IPs: $REDIS_IP1, $REDIS_IP2, $REDIS_IP3"
redis-cli --cluster create $REDIS_IP1:6379 $REDIS_IP2:6379 $REDIS_IP3:6379 --cluster-replicas 0 --cluster-yes

echo "Redis cluster setup complete."
