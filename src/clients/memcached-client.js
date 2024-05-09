const Memcached = require('memcached');
const fs = require('fs');

class MemcachedClient {
  
  constructor(numOfInstances = 1, resultFilename = 'results-memcached.txt', totalOperations = 10000) {
    this.config = this.generateConfig(numOfInstances);
    this.numOfInstances = numOfInstances;
    this.resultFilename = resultFilename;
    this.totalOperations = totalOperations;
  }
  
  generateConfig(numOfInstances) {
    let config = [];
  
    for (let i = 0; i < numOfInstances; i++) {
      config.push(`127.0.0.1:1121${i}`);
    }
  
    return config;
  }

  async connect() {
    this.client = new Memcached(this.config, {
      poolSize: this.numOfInstances,
    });
    console.log("Connected to Memcached");
    return this.client;
  }

  async disconnect() {
    await this.cleanup();
    this.client.end();
    console.log("Memcached Client Disconnected");
  }

  benchmarkWrite(dataSize, show=false) {
    return new Promise((resolve) => {
      const data = Buffer.alloc(dataSize, 'a');
      let totalTimeTaken = 0;
      this.keys = [];
      const operations = [];
  
      for (let i = 0; i < this.totalOperations; i++) {
        const key = `key-${dataSize}-${i}`;
        this.keys.push(key);
        
        operations.push(new Promise((resolve, reject) => {
            this.client.set(key, data, 10000, (err) => {
                if (err) reject(err);
                else resolve();
            });
        }));
      }
  
      const start = process.hrtime.bigint();
      Promise.all(operations).then(() => {
        const end = process.hrtime.bigint();
    
        totalTimeTaken += Number(end - start) / 1e6; 
    
        const averageTime = totalTimeTaken / this.totalOperations;
        if(show) {
          console.info(`Memcached WRITE ASYNC for size ${dataSize} bytes: ${averageTime.toFixed(6)} ms per operation`);
          fs.appendFile(this.resultFilename, 'Memcached, WRITE ASYNC, ' + this.numOfInstances + ', ' + dataSize + ', ' + averageTime.toFixed(6) + '\n', (err) => {
            if(err) console.error(err);
          });
        }
    
        resolve();
      });
    })
  }

  benchmarkRead(dataSize, show=false) {
    return new Promise((resolve) => {
      let keys = this.keys
                    .map(val => ({ val, sort: Math.random() }))
                    .sort((a, b) => a.sort - b.sort)
                    .map(obj => obj.val);

      // if(dataSize > 16384) {
      //   keys = keys.slice(0, 1000);
      // }
  
      let operations = [];
  
      operations = keys.map(key => {
        return new Promise((resolve, reject) => {
          this.client.get(key, () => {
              resolve();
          });
        })
      })

      const start = process.hrtime.bigint();
      Promise.all(operations).then(() => {
      // operations[0].then(() => {
        const end = process.hrtime.bigint();
    
        const averageTime = (Number(end - start) / 1e6) / this.keys.length;
        if(show) {
          console.info(`Memcached READ ASYNC for size ${dataSize} bytes: ${averageTime.toFixed(6)} ms per operation`);
          fs.appendFile(this.resultFilename, 'Memcached, READ ASYNC, ' + this.numOfInstances + ', ' + dataSize + ', ' + averageTime.toFixed(6) + '\n', (err) => {
            if(err) console.error(err);
          });
        }
  
        resolve();
      });
    })

  }

  cleanup() {
    return new Promise((resolve) => {
      this.client.flush((err) => {
        if (err) {
          console.error(err);
        }
        // console.log("Memcached Client Cleaned Up");
        resolve();
      })
    });
  }

  shuffle(array) {
    let currentIndex = array.length;
  
    while (currentIndex != 0) {
  
      let randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
  

      [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }

    return array;
  }
}

module.exports = MemcachedClient;