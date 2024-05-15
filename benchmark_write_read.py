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
  totalOperations = 1000
  totalProcesses = int(args[2]) if argc > 2 else 1

  print(f'Processes: {totalProcesses}, Servers: {numOfInstances}')
  
  resultFilename = f'result-new-redis-{numOfInstances}-{totalOperations}-{totalProcesses}.txt'

  resultFile = open(resultFilename, 'w')
  resultFile.write('')
  resultFile.close()

  # memcachedClient = MemcachedClient(numOfInstances, resultFilename, totalOperations, totalProcesses)
  # hazelcastClient = HazelcastClient(numOfInstances, resultFilename, totalOperations, totalProcesses)
  redisClient = RedisClient(numOfInstances, resultFilename, totalOperations, totalProcesses)

  dataSizes = [
    # 16,
    # 32, 
    # 64,
    # 128,
    # 256, 
    # 512, 
    # 1024, 
    # 2048, 
    # 4096, 
    # 8192, 
    # 16384, 
    32768, 
    65536,
    131072
  ]


  # for dataSize in dataSizes:
  #   memcachedClient.connect()
    
  #   processes = [Process(target=memcachedClient.benchmarkWriteMultiprocess, args=(dataSize, False)) for i in range(totalProcesses)]
  #   for p in processes:
  #     p.start()
    
  #   for p in processes:
  #     p.join()

  #   memcachedClient.cleanup()
  #   memcachedClient.keys = []

  #   memcachedClient.benchmarkWrite(dataSize, False)
  #   # memcachedClient.benchmarkRead(dataSize, False)
    
  #   processes = [Process(target=memcachedClient.benchmarkReadMultiprocess, args=(dataSize, False, i)) for i in range(totalProcesses)]
  #   for p in processes:
  #     p.start()
    
  #   for p in processes:
  #     p.join()

  #   memcachedClient.cleanup()
  #   memcachedClient.keys = []
  #   memcachedClient.disconnect()


  # for dataSize in dataSizes:
  #   hazelcastClient.connect()

  #   processes = [Process(target=hazelcastClient.benchmarkWriteMultiprocess, args=(dataSize, False)) for i in range(totalProcesses)]
  #   for p in processes:
  #     p.start()
    
  #   for p in processes:
  #     p.join()

  #   hazelcastClient.cleanup()
  #   hazelcastClient.keys = []

  #   hazelcastClient.benchmarkWrite(dataSize, False)
  #   # hazelcastClient.benchmarkRead(dataSize, False)

  #   processes = [Process(target=hazelcastClient.benchmarkReadMultiprocess, args=(dataSize, False, i)) for i in range(totalProcesses)]
  #   for p in processes:
  #     p.start()
    
  #   for p in processes:
  #     p.join()

  #   hazelcastClient.cleanup()
  #   hazelcastClient.keys = []
  #   hazelcastClient.disconnect()



  sleep(10)
  redisClient.connect()
  for dataSize in dataSizes:

    # processes = [Process(target=redisClient.benchmarkWriteMultiprocess, args=(dataSize, False)) for i in range(totalProcesses)]
    processes = [Process(target=redisClient.benchmarkWriteMultiprocessOld, args=(dataSize, i*(totalOperations//totalProcesses), False)) for i in range(totalProcesses)]
    for p in processes:
      p.start()
    
    for p in processes:
      p.join()

    redisClient.cleanup()
    redisClient.keys = []

    redisClient.benchmarkWrite(dataSize, False)
    redisClient.benchmarkRead(dataSize, False)

    processes = [Process(target=redisClient.benchmarkReadMultiprocess, args=(dataSize, False, i)) for i in range(totalProcesses)]
    for p in processes:
      p.start()
    
    for p in processes:
      p.join()

    redisClient.cleanup()
    redisClient.keys = []

  redisClient.disconnect()