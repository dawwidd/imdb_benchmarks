const { HazelcastClient: HClient } = require("hazelcast-client/lib/HazelcastClient");
const fs = require('fs');


class HazelcastClient {

  constructor(numOfInstances = 1, resultFilename = 'results-hazelcast.txt', totalOperations = 10000) {
    this.config = {
      ...this.generateConfig(numOfInstances),
      customLogger: new SilentLogger()
    }
    this.numOfInstances = numOfInstances;
    this.resultFilename = resultFilename;
    this.totalOperations = totalOperations;
  }

  generateConfig(numOfInstances) {
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

  async connect() {
    this.client = await HClient.newHazelcastClient(this.config);
    this.map = await this.client.getMap('benchmark-map');
    console.log("Connected to Hazelcast");
    return this.client;
  }

  async disconnect() {
    await this.client.shutdown();
    console.log("Hazelcast Client Disconnected");
  }

  async cleanup() {
    for (let key of this.keys) {
      await this.map.delete(key);
    }
  }

  benchmarkWrite(dataSize, show = false) {
    return new Promise((resolve) => {
      let data = Buffer.alloc(dataSize, 'a').toString(); 
      let totalOperations = 10000;
      let totalTimeTaken = 0;
      this.keys = [];
      const operations = [];
  
      for (let i = 0; i < totalOperations; i++) {
        const key = `key-${dataSize}-${i}`;
        this.keys.push(key);
        
        operations.push(this.map.set(key, data));  
      }
      const start = process.hrtime.bigint();
      Promise.all(operations).then(() => {
        const end = process.hrtime.bigint();
    
        totalTimeTaken += Number(end - start) / 1e6;

        const averageTime = totalTimeTaken / totalOperations;
        if(show) {
          console.info(`Hazelcast write for size ${dataSize} bytes: ${averageTime.toFixed(6)} ms per operation`);
          fs.appendFile(this.resultFilename, 'Hazelcast, WRITE, ' + this.numOfInstances + ', ' + dataSize + ', ' + averageTime.toFixed(6) + '\n', (err) => {
            if(err) console.error(err);
          });
        }

        resolve();
      });
    })
  }

  benchmarkRead(dataSize, show = false) {
    return new Promise((resolve) => {
      const keys = this.keys
                    .map(val => ({ val, sort: Math.random() }))
                    .sort((a, b) => a.sort - b.sort)
                    .map(obj => obj.val);

      let operations = keys.map(key => this.map.get(key));
      
      const start = process.hrtime.bigint();
      Promise.all(operations).then(() => {
        const end = process.hrtime.bigint();
    
        const averageTime = (Number(end - start) / 1e6) / this.keys.length;
        if(show) {
          console.info(`Hazelcast read for size ${dataSize} bytes: ${averageTime.toFixed(6)} ms per operation`);
          fs.appendFile(this.resultFilename, 'Hazelcast, READ, ' + this.numOfInstances + ', ' + dataSize + ', ' + averageTime.toFixed(6) + '\n', (err) => {
            if(err) console.error(err);
          });
        }
  
        resolve()
      })
    })
  }
}

class SilentLogger {
  trace() {}
  debug() {}
  info() {}
  warn() {}
  error() {}
  log() {}
}

module.exports = HazelcastClient;