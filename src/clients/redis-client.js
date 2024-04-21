const redis = require("redis");

class RedisClient {
  constructor(numOfInstances = 1) {
    this.numOfInstances = numOfInstances;
    this.config = this.generateConfig();
  }

  generateConfig() {
    let config = {};

    if (this.numOfInstances === 1) {
      config.url = `redis://127.0.0.1:6370`;
      return config;   
    }
    
    config = {
      rootNodes: []
    };
  
    for (let i = 0; i < this.numOfInstances; i++) {
      config.rootNodes.push({
        url: `redis://127.0.0.1:637${i}`,
      });
    }
  
    return config;
  }

  createInstance(config) {
    if(this.numOfInstances === 1) {
      return redis.createClient(config);
    }

    return redis.createCluster(config);
  }

  async benchmarkWrite(dataSize, show=false) {
    const data = Buffer.alloc(dataSize, 'a').toString();
    let totalOperations = 10000;
    let totalTimeTaken = 0;
    let keys = [];

    const operations = [];

    for (let i = 0; i < totalOperations; i++) {
        const key = `key-${dataSize}-${i}`;
        keys.push(key);
        
        operations.push(this.client.set(key, data));
    }

    const start = process.hrtime.bigint();
    await Promise.all(operations);
    const end = process.hrtime.bigint();

    totalTimeTaken += Number(end - start) / 1e6;

    for (let delKey of keys) {
        await this.client.del(delKey);
    }

    const averageTime = totalTimeTaken / totalOperations;
    if(show) console.info(`Redis Write for size ${dataSize} bytes: ${averageTime.toFixed(6)} ms per operation`);
  }

  async connect() {
    this.client = this.createInstance(this.config);
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