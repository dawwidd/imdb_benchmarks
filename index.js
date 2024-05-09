const MemcachedClient = require("./src/clients/memcached-client");
const HazelcastClient = require("./src/clients/hazelcast-client");
const RedisClient = require("./src/clients/redis-client");
const fs = require('fs');

const args = process.argv.slice(2);
const numOfInstances = args[0] || 1;

async function main() {
  const resultFilename = 'results2.txt';
  const totalOperations = 10000;

  const memcached = new MemcachedClient(numOfInstances, resultFilename, totalOperations);
  const hazelcast = new HazelcastClient(numOfInstances, resultFilename, totalOperations);
  const redis = new RedisClient(numOfInstances, resultFilename, totalOperations);

  await memcached.connect();
  await hazelcast.connect();
  await redis.connect();

  console.log("All clients connected");

  // Clear the results.txt file
  fs.writeFile(resultFilename, '', (err) => {
    if (err) console.error(err);
  });

  // 16B, 128B, 1KiB, 8KiB, 64KiB, 512KiB
  const dataSizes = [
    16,
    32, 
    64,
    128,
    256, 
    512, 
    1024, 
    2048, 
    4096, 
    8192,
    16384,
    32768, 
    65536,
  ];
  try {
    
    // Memcached
    await memcached.benchmarkWrite(16);
    await memcached.benchmarkRead(16);
    await memcached.cleanup();

    for (let dataSize of dataSizes) {
      await memcached.benchmarkWrite(dataSize, true);
      await memcached.benchmarkRead(dataSize, true);
      await memcached.cleanup();
    }

    // Hazelcast
    await hazelcast.benchmarkWrite(16);
    await hazelcast.benchmarkRead(16);
    await hazelcast.cleanup();

    for (let dataSize of dataSizes) {
      await hazelcast.benchmarkWrite(dataSize, true);
      await hazelcast.benchmarkRead(dataSize, true);
      await hazelcast.cleanup();
    }

    // Redis
    await redis.benchmarkWrite(16);
    await redis.benchmarkRead(16);
    await redis.cleanup();

    for (let dataSize of dataSizes) {
      await redis.benchmarkWrite(dataSize, true);
      await redis.benchmarkRead(dataSize, true);
      await redis.cleanup();
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