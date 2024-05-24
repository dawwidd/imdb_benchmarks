import sys
from pymemcache.client.base import Client
from python_clients.memcached_client import MemcachedClient
from python_clients.hazelcast_client import HazelcastClient
from python_clients.redis_client import RedisClient
from multiprocessing import Pool, Process
from time import sleep


def benchmark_write_read():
  args = sys.argv
  argc = len(args)

  numOfInstances = int(args[1]) if argc > 1 else 1
  totalProcesses = int(args[2]) if argc > 2 else 1
  totalOperations = 1024

  print(f'Processes: {totalProcesses}, Servers: {numOfInstances}')
  
  resultFilename = f'test_multi_comp_result-{numOfInstances}-{totalOperations}-{totalProcesses}.txt'

  resultFile = open(resultFilename, 'w')
  resultFile.write('')
  resultFile.close()

  memcachedClient = MemcachedClient(numOfInstances, resultFilename, totalOperations, totalProcesses)
  hazelcastClient = HazelcastClient(numOfInstances, resultFilename, totalOperations, totalProcesses)
  redisClient = RedisClient(numOfInstances, resultFilename, totalOperations, totalProcesses)
  
  dataSizes = [
    16,
    32, 
    64,
    128,
    256, 
    512, 
    1024, 
    2048, 
    4096, 
    8192, 
    16384, 
    32768, 
    65536,
    131072
  ]

  # for dataSize in dataSizes:
  memcachedClient.connect()

  # memcachedClient.benchmarkWrite(dataSize, True)

  processes = [Process(target=memcachedClient.benchmarkClusterWrite, args=(i, totalProcesses)) for i in range(totalProcesses)]
  for p in processes:
    p.start()
  
  for p in processes:
    p.join()
  
  processes = [Process(target=memcachedClient.benchmarkClusterRead, args=(i, totalProcesses)) for i in range(totalProcesses)]
  for p in processes:
    p.start()
  
  for p in processes:
    p.join()

  memcachedClient.cleanup()
  memcachedClient.keys = []
  memcachedClient.disconnect()

    



  # hazelcastClient.connect()
  # for dataSize in dataSizes:

  #   # processes = [Process(target=hazelcastClient.benchmarkWriteMultiprocess, args=(dataSize, False)) for i in range(totalProcesses)]
  #   # for p in processes:
  #   #   p.start()
    
  #   # for p in processes:
  #   #   p.join()

  #   # hazelcastClient.cleanup()
  #   # hazelcastClient.keys = []

  #   hazelcastClient.benchmarkWrite(dataSize, True)
  #   # hazelcastClient.benchmarkRead(dataSize, False)

  #   # processes = [Process(target=hazelcastClient.benchmarkReadMultiprocess, args=(dataSize, False, i)) for i in range(totalProcesses)]
  #   # for p in processes:
  #   #   p.start()
    
  #   # for p in processes:
  #   #   p.join()

  #   hazelcastClient.cleanup()
  #   hazelcastClient.keys = []

  # hazelcastClient.disconnect()


  # # sleep(10)
  # redisClient.connect()
  # for dataSize in dataSizes:

  #   # processes = [Process(target=redisClient.benchmarkWriteMultiprocess, args=(dataSize, False)) for i in range(totalProcesses)]
  #   # processes = [Process(target=redisClient.benchmarkWriteMultiprocessOld, args=(dataSize, i*(totalOperations//totalProcesses), False)) for i in range(totalProcesses)]
  #   # for p in processes:
  #   #   p.start()
    
  #   # for p in processes:
  #   #   p.join()

  #   # redisClient.cleanup()
  #   # redisClient.keys = []

  #   redisClient.benchmarkWrite(dataSize, False)
  #   # redisClient.benchmarkRead(dataSize, False)

  #   # processes = [Process(target=redisClient.benchmarkReadMultiprocess, args=(dataSize, False, i)) for i in range(totalProcesses)]
  #   # for p in processes:
  #   #   p.start()
    
  #   # for p in processes:
  #   #   p.join()

  #   redisClient.cleanup()
  #   redisClient.keys = []

  # redisClient.disconnect()