from pymemcache.client.base import Client as memcachedClient
from pymemcache.client.hash import HashClient as memcachedCluster
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool
from multiprocessing import Array
from threading import Thread
import threading
import random
import time

class MemcachedClient:
  def __init__(self, numOfInstances = 1, resultFilename = 'res-memcached-py.txt', totalOperations = 10000, totalProcesses = 1):
    self.numOfInstances = numOfInstances
    self.config = self.generateConfig(self.numOfInstances)
    self.resultFilename = resultFilename
    self.totalOperations = totalOperations
    self.totalProcesses = totalProcesses
    self.keys = []
    self.client = None


  def generateConfig(self, numOfInstances):
    config = []

    config.append('192.168.1.7:11210')
    if numOfInstances > 1: config.append('192.168.1.110:11211')
    if numOfInstances > 2: config.append('192.168.1.9:11212')

    print(config)
    
    return config


  def connect(self):
    if len(self.config) == 1:
      self.client = memcachedClient(self.config[0])
    else:
      self.client = memcachedCluster(self.config)

  def disconnect(self):
    self.client.disconnect_all()


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
      
    resultFile = open(self.resultFilename, 'a')
    print(f'Memcached WRITE SINGLE {dataSize} {averageTime:.8f}')
    resultFile.write(f'Memcached WRITE SINGLE {dataSize} {averageTime:.8f}\n')
    resultFile.close()

  def benchmarkClusterWrite(self, processNum, totalProcesses):
    self.connect()
    totalTimeTaken = 0
    data = 'a' * (1024 // totalProcesses)

    for i in range(self.totalOperations):
      key = f'key-{i}-{processNum}'
      start = time.time()
      self.client.set(key, data)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations

    print(f'Memcached WRITE CLUSTER {averageTime:.8f}')
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Memcached WRITE CLUSTER {averageTime:.8f}\n')
    resultFile.close()

    self.disconnect()

  def benchmarkClusterRead(self, processNum, totalProcesses):
    self.connect()
    totalTimeTaken = 0

    for i in range(self.totalOperations):
      key = f'key-{i}-{processNum}'
      start = time.time()
      self.client.get(key)
      end = time.time()

      totalTimeTaken += end - start

    averageTime = totalTimeTaken / self.totalOperations

    print(f'Memcached READ CLUSTER {averageTime:.8f}')
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Memcached READ CLUSTER {averageTime:.8f}\n')
    resultFile.close()

    self.disconnect()


  def benchmarkWriteMultiprocess(self, dataSize, show=False):
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
      print(f'Memcached WRITE MULTI {dataSize} {averageTime:.8f}')
      
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Memcached WRITE MULTI {dataSize} {averageTime:.8f}\n')
    resultFile.close()

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
      print(f'Memcached WRITE MULTI {dataSize} {averageTime:.8f}')
      
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Memcached WRITE MULTI {dataSize} {averageTime:.8f}\n')
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
      print(f'Memcached READ SINGLE {dataSize} {averageTime:.8f}')
      
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Memcached READ SINGLE {dataSize} {averageTime:.8f}\n')
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
      print(f'Memcached READ MULTI {dataSize} {averageTime:.8f}')
      
    resultFile = open(self.resultFilename, 'a')
    resultFile.write(f'Memcached READ MULTI {dataSize} {averageTime:.8f}\n')
    resultFile.close()

    self.disconnect()


  def cleanup(self):
    self.client.flush_all()



