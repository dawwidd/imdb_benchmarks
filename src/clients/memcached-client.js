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

  async benchmarkWrite(dataSize, show=false) {
    const data = Buffer.alloc(dataSize, 'a');  // Create data of the specified size
    let totalOperations = 10000;               // Total operations for each size
    let totalDataWritten = 0;                  // Track the total data written
    let totalTimeTaken = 0;                    // Track total time taken for writing
    let keys = [];                             // Keep track of keys used for cleanup
    const operations = [];

    for (let i = 0; i < totalOperations; i++) {
        const key = `key-${dataSize}-${i}`;    // Unique key for each operation
        keys.push(key);

        const start = process.hrtime.bigint();
        await this.client.set(key, data);
        const end = process.hrtime.bigint();

        totalTimeTaken += Number(end - start) / 1e6;  // Convert nanoseconds to milliseconds
        totalDataWritten += dataSize;
    }


    // for (let i = 0; i < totalOperations; i++) {
    //   const key = `key-${dataSize}-${i}`;
    //   keys.push(key);
      
    //   // Wrap the set operation in a Promise
    //   operations.push(new Promise((resolve, reject) => {
    //       this.client.set(key, data, 0, (err) => {
    //           if (err) reject(err);
    //           else resolve();
    //       });
    //   }));
    // }

    // const start = process.hrtime.bigint();
    // await Promise.all(operations);
    // const end = process.hrtime.bigint();

    // totalTimeTaken += Number(end - start) / 1e6; 

    // Clean up after all operations
    for (let key of keys) {
        await this.client.del(key);
    }

    const averageTime = totalTimeTaken / totalOperations;
    if(show) console.info(`Memcached write for size ${dataSize} bytes: ${averageTime.toFixed(6)} ms per operation`);
  }
}

module.exports = MemcachedClient;