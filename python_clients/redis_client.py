from redis import Redis as redisClient
from redis.cluster import RedisCluster as redisCluster
from redis.cluster import ClusterNode
import random
import time

class RedisClient:
  def __init__(self, numOfInstances = 1, resultFilename = 'res-redis-py.txt', totalOperations = 10000, totalProcesses = 1):
    self.numOfInstances = numOfInstances
    self.config = self.generateConfig(self.numOfInstances)
    self.resultFilename = resultFilename
    self.totalOperations = totalOperations
    self.totalProcesses = totalProcesses
    self.keys = []
    self.client = None


  def generateConfig(self, numOfInstances):
    config = []

    # config = [
    #   ClusterNode('172.23.0.7', 6379),
    #   ClusterNode('172.23.0.8', 6379),
    #   ClusterNode('172.23.0.3', 6379),
    #   # ClusterNode('172.22.0.14', 6379),
    #   # ClusterNode('172.22.0.30', 6379),
    #   # ClusterNode('172.22.0.7', 6379),
    #   # ClusterNode('172.22.0.4', 6379),
    #   # ClusterNode('172.22.0.21', 6379),
    #   # ClusterNode('172.22.0.5', 6379),
    #   # ClusterNode('172.22.0.12', 6379),
    # ]
    for i in range(numOfInstances):
      config.append(ClusterNode('localhost', 6370 + i))

    
    return config


  def connect(self):

    if len(self.config) == 1:
      self.client = redisClient(host = 'localhost', port = 6370)
    else:
      self.client = redisCluster(startup_nodes = self.config)

    # print("Connected to Redis")

  def connect(self, instanceNumber):
    self.client = redisClient(host = 'localhost', port = 6370 + instanceNumber)

  def disconnect(self):
    self.client.close()
    # print("Disconnected from Redis")

  def benchmarkWrite(self, dataSize, show=False):
    data = 'a' * dataSize

    totalTimeTaken = 0
    for i in range(self.totalOperations):
      key = f'key-{dataSize}-{i}'
      self.keys.append(key)

      start = time.time()
      self.client.set(key, data)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations
    if show:
      print(f'Redis WRITE SINGLE {dataSize} {averageTime:.8f}')
      
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Redis WRITE SINGLE {dataSize} {averageTime:.8f}\n')
    resultFile.close()

  def benchmarkWriteMultiprocess(self, dataSize, show=False):
    self.connect()
    data = 'a' * dataSize

    totalTimeTaken = 0
    for i in range(self.totalOperations):
      key = f'key-{dataSize}-{i}'
      self.keys.append(key)

      start = time.time()
      self.client.set(key, data)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations
    if show:
      print(f'Redis WRITE MULTI {dataSize} {averageTime:.8f}')
      
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Redis WRITE MULTI {dataSize} {averageTime:.8f}\n')
    resultFile.close()

    self.disconnect()


  def benchmarkWriteMultiprocessOld(self, dataSize, offset, show=False, processNum=1):
    self.connect()
    data = 'a' * dataSize

    totalTimeTaken = 0
    for i in range(offset, offset + self.totalOperations//self.totalProcesses):
      key = f'key-{dataSize}-{i}'
      self.keys.append(key)

      start = time.time()
      self.client.set(key, data)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations
    if show:
      print(f'Redis WRITE MULTI {dataSize} {averageTime:.12f}')
      
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Redis WRITE MULTI {dataSize} {averageTime:.12f}\n')
    resultFile.close()

    self.disconnect()


  def benchmarkRead(self, dataSize, show=False):
    random.shuffle(self.keys)

    totalTimeTaken = 0
    for i in range(self.totalOperations):
      key = self.keys[i]
      start = time.time()
      self.client.get(key)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations
    if show:
      print(f'Redis READ SINGLE {dataSize} {averageTime:.8f}')
      
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Redis READ SINGLE {dataSize} {averageTime:.8f}\n')
    resultFile.close()

  
  def benchmarkReadMultiprocess(self, dataSize, show=False, processNum=1):
    self.connect()
    random.shuffle(self.keys)

    totalTimeTaken = 0
    for i in range(self.totalOperations):
      key = self.keys[i]
      start = time.time()
      self.client.get(key)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations
    if show:
      print(f'Redis READ MULTI {dataSize} {averageTime:.8f}')
      
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Redis READ MULTI {dataSize} {averageTime:.8f}\n')
    resultFile.close()

    self.disconnect()


  def cleanup(self):
    self.client.flushall()