from hazelcast import HazelcastClient as hazelcastClient
import random
import time

class HazelcastClient:
  def __init__(self, numOfInstances = 1, resultFilename = 'res-hazelcast-py.txt', totalOperations = 10000, totalProcesses = 1):
    self.numOfInstances = numOfInstances
    self.config = self.generateConfig(self.numOfInstances)
    self.resultFilename = resultFilename
    self.totalOperations = totalOperations
    self.totalProcesses = totalProcesses
    self.keys = []
    self.client = None
    self.map = None

  def generateConfig(self, numOfInstances):
    config = []

    for i in range(numOfInstances):
      config.append(f'127.0.0.1:570{i}')
    
    return config

  def connect(self):
    self.client = hazelcastClient(
      cluster_members = self.config
    )

    self.map = self.client.get_map('benchmark-map')

    # print("Connected to Hazelcast")

  def disconnect(self):
    self.client.shutdown()
    # print("Disconnected from Hazelcast")

  def benchmarkWrite(self, dataSize, show=False):
    data = 'a' * dataSize

    totalTimeTaken = 0
    for i in range(self.totalOperations):
      key = f'key-{dataSize}-{i}'
      self.keys.append(key)

      start = time.time()
      self.map.set(key, data)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations
    if show:
      print(f'Hazelcast WRITE SINGLE {dataSize} {averageTime:.8f}')
    
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Hazelcast WRITE SINGLE {dataSize} {averageTime:.8f}\n')
    resultFile.close()

  def benchmarkWriteMultiprocess(self, dataSize, show=False):
    data = 'a' * dataSize

    totalTimeTaken = 0
    for i in range(self.totalOperations):
      key = f'key-{dataSize}-{i}'
      self.keys.append(key)

      start = time.time()
      self.map.set(key, data)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations
    if show:
      print(f'Hazelcast WRITE MULTI {dataSize} {averageTime:.8f}')
    
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Hazelcast WRITE MULTI {dataSize} {averageTime:.8f}\n')
    resultFile.close()


  def benchmarkWriteMultiprocessOld(self, dataSize, offset, show=False, processNum=1):
    self.connect()
    data = 'a' * dataSize

    totalTimeTaken = 0
    for i in range(offset, offset + self.totalOperations//self.totalProcesses):
      key = f'key-{dataSize}-{i}'
      self.keys.append(key)

      start = time.time()
      self.map.set(key, data)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations
    if show:
      print(f'Hazelcast WRITE MULTI {dataSize} {averageTime:.8f}')
    
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Hazelcast WRITE MULTI {dataSize} {averageTime:.8f}\n')
    resultFile.close()

    self.disconnect()

  def benchmarkRead(self, dataSize, show=False):
    random.shuffle(self.keys)

    totalTimeTaken = 0
    for i in range(self.totalOperations):
      key = self.keys[i]
      start = time.time()
      self.map.get(key)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations
    if show:
      print(f'Hazelcast READ SINGLE {dataSize} {averageTime:.8f}')
      
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Hazelcast READ SINGLE {dataSize} {averageTime:.8f}\n')
    resultFile.close()


  def benchmarkReadMultiprocess(self, dataSize, show=False, processNum=1):
    self.connect()
    random.shuffle(self.keys)

    totalTimeTaken = 0
    for i in range(self.totalOperations):
      key = self.keys[i]
      start = time.time()
      self.map.get(key)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations
    if show:
      print(f'Hazelcast READ MULTI {dataSize} {averageTime:.8f}')
    
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Hazelcast READ MULTI {dataSize} {averageTime:.8f}\n')
    resultFile.close()

    self.disconnect()

  def cleanup(self):
    self.map.clear()
      