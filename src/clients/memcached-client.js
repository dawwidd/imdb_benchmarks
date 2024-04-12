const Memcached = require('memcached');

class MemcachedClient {
  
  constructor(numOfInstances = 1) {
    this.config = this.generateConfig(numOfInstances);
  }
  
  generateConfig(numOfInstances) {
    let config = [];
  
    for (let i = 0; i < numOfInstances; i++) {
      config.push(`127.0.0.1:1121${i}`);
    }
  
    return config;
  }

  async connect() {
    this.client = new Memcached(this.config);
    console.log("Connected to Memcached");
    return this.client;
  }

  async disconnect() {
    this.client.end();
    console.log("Memcached Client Disconnected");
  }
}

module.exports = MemcachedClient;