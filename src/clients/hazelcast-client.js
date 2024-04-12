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