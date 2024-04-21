const MemcachedClient = require("./src/clients/memcached-client");
const HazelcastClient = require("./src/clients/hazelcast-client");
const RedisClient = require("./src/clients/redis-client");

const args = process.argv.slice(2);
const numOfInstances = args[0] || 1;

async function main() {
  const memcached = new MemcachedClient(numOfInstances);
  const hazelcast = new HazelcastClient(numOfInstances);
  const redis = new RedisClient(numOfInstances);

  await memcached.connect();
  await hazelcast.connect();
  await redis.connect();

  console.log("All clients connected");

  // 16B, 128B, 1KiB, 8KiB, 64KiB, 512KiB
  const dataSizes = [
    16, 
    128, 
    1024, 
    8192, 
    65536,
    // 131072
    // 524288
  ];
  try {
    for (let dataSize of dataSizes) {
      await memcached.benchmarkWrite(dataSize);
    }
    for (let dataSize of dataSizes) {
      await memcached.benchmarkWrite(dataSize, true);
    }
    for (let dataSize of dataSizes) {
      await hazelcast.benchmarkWrite(dataSize);
    }
    for (let dataSize of dataSizes) {
      await hazelcast.benchmarkWrite(dataSize, true);
    }
    for (let dataSize of dataSizes) {
      await redis.benchmarkWrite(dataSize);
    }
    for (let dataSize of dataSizes) {
      await redis.benchmarkWrite(dataSize, true);
    }
  }
  catch (err) {
    console.error(err);
  }

  await memcached.disconnect();
  await hazelcast.disconnect();
  await redis.disconnect();
}

main();