const redis = require("redis");
const fs = require('fs');

class RedisClient {
  constructor(numOfInstances = 1, resultFilename = 'results-redis.txt', totalOperations = 10000) {
    this.numOfInstances = numOfInstances;
    this.config = this.generateConfig();
    this.resultFilename = resultFilename;
    this.totalOperations = totalOperations;
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

  benchmarkWrite(dataSize, show=false) {
    return new Promise((resolve) => {
      const data = Buffer.alloc(dataSize, 'a').toString();
      let totalTimeTaken = 0;
      this.keys = [];
      const operations = [];

      for (let i = 0; i < this.totalOperations; i++) {
        const key = `key-${dataSize}-${i}`;
        this.keys.push(key);
        
        operations.push(this.client.set(key, data));
      }

      const start = process.hrtime.bigint();
      Promise.all(operations).then(() => {
        const end = process.hrtime.bigint();
        totalTimeTaken += Number(end - start) / 1e6;
        const averageTime = totalTimeTaken / this.totalOperations;
        if(show) {
          console.info(`Redis WRITE ASYNC for size ${dataSize} bytes: ${averageTime.toFixed(6)} ms per operation`);
          fs.appendFile(this.resultFilename, 'Redis, WRITE ASYNC,' + this.numOfInstances + ', ' + dataSize + ', ' + averageTime.toFixed(6) + '\n', (err) => {
            if(err) console.error(err);
          });
        }
        resolve();
      })
    })
  }

  benchmarkRead(dataSize, show=false) {
    return new Promise((resolve) => {
      const keys = this.keys
                    .map(val => ({ val, sort: Math.random() }))
                    .sort((a, b) => a.sort - b.sort)
                    .map(obj => obj.val);

      let operations = [];

      operations = keys.map(key => {
        return this.client.get(key)
      });

      const start = process.hrtime.bigint();
      Promise.all(operations).then(() => {
        const end = process.hrtime.bigint();

        const averageTime = (Number(end - start) / 1e6) / this.keys.length;
        if(show) {
          console.info(`Redis READ ASYNC for size ${dataSize} bytes: ${averageTime.toFixed(6)} ms per operation`);
          fs.appendFile(this.resultFilename, 'Redis, READ ASYNC,' + this.numOfInstances + ', ' + dataSize + ', ' + averageTime.toFixed(6) + '\n', (err) => {
            if(err) console.error(err);
          });
        }
        resolve();
      })
    })
  }

  async connect() {
    this.client = this.createInstance(this.config);
    await this.client.connect();
    console.log("Connected to Redis");
    return this.client;
  }

  async disconnect() {
    await this.cleanup();
    await this.client.quit();
    console.log("Redis Client Disconnected");
  }

  async cleanup() {
    for (let key of this.keys) {
      await this.client.del(key);
    }
  }
}

module.exports = RedisClient;