#!/bin/bash

# Start Docker Compose services
echo "Starting Redis containers..."
docker-compose -f ten-instance.yml up -d

# Wait for containers to fully start
echo "Waiting for Redis containers to initialize..."
sleep 3

# Fetch IPs of Redis containers dynamically
REDIS_IP1=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f triple-instance.yml ps -q redis0))
REDIS_IP2=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f triple-instance.yml ps -q redis1))
REDIS_IP3=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f triple-instance.yml ps -q redis2))
REDIS_IP4=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f ten-instance.yml ps -q redis3))
REDIS_IP5=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f ten-instance.yml ps -q redis4))
REDIS_IP6=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f ten-instance.yml ps -q redis5))
REDIS_IP7=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f ten-instance.yml ps -q redis6))
REDIS_IP8=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f ten-instance.yml ps -q redis7))
REDIS_IP9=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f ten-instance.yml ps -q redis8))
REDIS_IP10=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker-compose -f ten-instance.yml ps -q redis9))

# Ensure IPs are not empty
if [ -z "$REDIS_IP1" ] || [ -z "$REDIS_IP2" ] || [ -z "$REDIS_IP3" ] || [ -z "$REDIS_IP4" ] || [ -z "$REDIS_IP5" ] || [ -z "$REDIS_IP6" ] || [ -z "$REDIS_IP7" ] || [ -z "$REDIS_IP8" ] || [ -z "$REDIS_IP9" ] || [ -z "$REDIS_IP10" ]; then
  echo "Error fetching Redis IPs. Exiting."
  exit 1
fi

# Create the Redis cluster using the fetched IP addresses
echo "Creating Redis cluster with IPs: $REDIS_IP1, $REDIS_IP2, $REDIS_IP3"
redis-cli --cluster create $REDIS_IP1:6379 $REDIS_IP2:6379 $REDIS_IP3:6379 $REDIS_IP4:6379 $REDIS_IP5:6379 $REDIS_IP6:6379 $REDIS_IP7:6379 $REDIS_IP8:6379 $REDIS_IP9:6379 $REDIS_IP10:6379  --cluster-replicas 0 --cluster-yes

echo "Redis cluster setup complete."
