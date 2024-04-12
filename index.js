const MemcachedClient = require("./src/clients/memcached-client");
const HazelcastClient = require("./src/clients/hazelcast-client");
const RedisClient = require("./src/clients/redis-client");

const args = process.argv.slice(2);
const numOfInstances = args[0] || 1;

async function initClients() {
  try {
    const memcached = new MemcachedClient(numOfInstances);
    const hazelcast = new HazelcastClient(numOfInstances);
    const redis = new RedisClient(numOfInstances);

    await memcached.connect();
    await hazelcast.connect();
    await redis.connect();

    setTimeout(() => {
      memcached.disconnect();
      hazelcast.disconnect();
      redis.disconnect();
      console.log("All clients disconnected");
    }, 5000);
  } catch (err) {
    console.error("Error initializing clients", err);
  }
}

initClients();