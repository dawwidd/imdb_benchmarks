const { LogLevel } = require("hazelcast-client");
const { HazelcastClient } = require("hazelcast-client/lib/HazelcastClient");
const Memcached = require("memcached");
const redis = require("redis");

const args = process.argv.slice(2);

class SilentLogger {
  trace() {}
  debug() {}
  info() {}
  warn() {}
  error() {}
  log() {}
}

async function createMemcachedClient(numOfInstances = 1) {
  const config = generateMemcachedConfig(numOfInstances);

  const client = new Memcached(config);

  console.log("Connected to Memcached");

  return client;
}

function generateMemcachedConfig(numOfInstances) {
  let config = [];

  for (let i = 0; i < numOfInstances; i++) {
    config.push(`127.0.0.1:1121${i}`);
  }

  return config;
}

async function createHazelcastClient(numOfInstances = 1) {
  const config = generateHazelcastConfig(numOfInstances);

  config.customLogger = new SilentLogger();

  const client = await HazelcastClient.newHazelcastClient(config);

  console.log("Connected to Hazelcast");

  return client;
}

function generateHazelcastConfig(numOfInstances) {
  const config = {
    network: {
      clusterMembers: []
    }
  }

  for (let i = 0; i < numOfInstances; i++) {
    config.network.clusterMembers.push(`127.0.0.1:570${i}`);
  }

  return config;
}

async function createRedisClient(numOfInstances = 1) {
  const config = generateRedisConfig(numOfInstances);

  const client = redis.createCluster(config);

  client.on("error", (err) => console.log("Redis Client Error", err));

  await client.connect();
  console.log("Connected to Redis");

  return client;
}

function generateRedisConfig(numOfInstances) {
  let config = {
    rootNodes: []
  };

  for (let i = 0; i < numOfInstances; i++) {
    config.rootNodes.push({
      url: `redis://127.0.0.1:637${i}`
    });
  }

  return config;
}


async function initClients() {
  const numOfInstances = args[0] || 1;

  try {
    const memcachedClient = await createMemcachedClient(numOfInstances);
    const hazelcastClient = await createHazelcastClient(numOfInstances);
    const redisClient = await createRedisClient(numOfInstances);
    memcachedClient.set("key", "value", 50, (err) => {
      if (err) throw err;

      console.log("Value set");

      memcachedClient.get("key", (err, value) => {
        if (err) throw err;

        console.log(`Value retrieved: ${value}`);
      });
    });

    setTimeout(() => {
      memcachedClient.end();
      hazelcastClient.shutdown();
      redisClient.quit();
      console.log("All clients disconnected");
    }, 5000);
  } catch (err) {
    console.error("Error initializing clients", err);
  }
}

initClients();
