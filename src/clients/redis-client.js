const redis = require("redis");

class RedisClient {
  constructor(numOfInstances = 1) {
    this.config = this.generateConfig(numOfInstances);
  }

  generateConfig(numOfInstances) {
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

  async connect() {
    this.client = redis.createCluster(this.config);
    await this.client.connect();
    console.log("Connected to Redis");
    return this.client;
  }

  async disconnect() {
    await this.client.quit();
    console.log("Redis Client Disconnected");
  }
}

module.exports = RedisClient;