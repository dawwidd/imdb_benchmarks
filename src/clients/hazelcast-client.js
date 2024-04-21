const { HazelcastClient: HClient } = require("hazelcast-client/lib/HazelcastClient");


class HazelcastClient {

  constructor(numOfInstances = 1) {
    this.config = {
      ...this.generateConfig(numOfInstances),
      customLogger: new SilentLogger()
    }
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
    console.log("Connected to Hazelcast");
    return this.client;
  }

  async disconnect() {
    await this.client.shutdown();
    console.log("Hazelcast Client Disconnected");
  }

  async benchmarkWrite(dataSize, show = false) {
    let data = Buffer.alloc(dataSize, 'a').toString(); 
    const map = await this.client.getMap('benchmark-map');  
    let totalOperations = 10000;
    let totalTimeTaken = 0;
    const operations = [];

    for (let i = 0; i < totalOperations; i++) {
      const key = `key-${dataSize}-${i}`;
      
      operations.push(map.set(key, data));  
    }
    const start = process.hrtime.bigint();
    await Promise.all(operations);
    const end = process.hrtime.bigint();

    totalTimeTaken += Number(end - start) / 1e6;

    await map.clear();

    const averageTime = totalTimeTaken / totalOperations;
    if(show) console.info(`Hazelcast Write for size ${dataSize} bytes: ${averageTime.toFixed(6)} ms per operation`);
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