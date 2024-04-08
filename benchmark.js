const { HazelcastClient } = require("hazelcast-client/lib/HazelcastClient");
const Memcached = require("memcached");
const redis = require("redis");

async function createRedisClient() {
  const client = redis.createClient();

  client.on("error", (err) => console.log("Redis Client Error", err));

  await client.connect();
  console.log("Connected to Redis");

  return client;
}

async function createHazelcastClient() {
  const client = await HazelcastClient.newHazelcastClient();

  console.log("Connected to Hazelcast");

  return client;
}

async function createMemcachedClient() {
  const client = new Memcached([
    "127.0.0.1:11211",
    "127.0.0.1:11212",
    "127.0.0.1:11213",
  ]);

  console.log("Connected to Memcached");

  return client;
}

async function initClients() {
  try {
    const memcachedClient = await createMemcachedClient();
    // const hazelcastClient = await createHazelcastClient();
    // const redisClient = await createRedisClient();
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
      // hazelcastClient.shutdown();
      // redisClient.quit();
      console.log("All clients disconnected");
    }, 5000);
  } catch (err) {
    console.error("Error initializing clients", err);
  }
}

initClients();
