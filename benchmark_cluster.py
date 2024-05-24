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
  totalOperations = 1024*1024

  print(f'Processes: {totalProcesses}, Servers: {numOfInstances}')
  
  resultFilename = f'cluster_results/test_servers-{numOfInstances}-processes-{totalProcesses}.txt'

  resultFile = open(resultFilename, 'w')
  resultFile.write('')
  resultFile.close()

  memcachedClient = MemcachedClient(numOfInstances, resultFilename, totalOperations, totalProcesses)
  hazelcastClient = HazelcastClient(numOfInstances, resultFilename, totalOperations, totalProcesses)
  if numOfInstances != 2:
    redisClient = RedisClient(numOfInstances, resultFilename, totalOperations, totalProcesses)



  # MEMCACHED
  # memcachedClient.connect()

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

  # memcachedClient.cleanup()
  # memcachedClient.disconnect()

    

  # HAZELCAST
  hazelcastClient.connect()

  processes = [Process(target=hazelcastClient.benchmarkClusterWrite, args=(i, totalProcesses)) for i in range(totalProcesses)]
  for p in processes:
    p.start()
  
  for p in processes:
    p.join()

  processes = [Process(target=hazelcastClient.benchmarkClusterRead, args=(i, totalProcesses)) for i in range(totalProcesses)]
  for p in processes:
    p.start()
  
  for p in processes:
    p.join()

  hazelcastClient.cleanup()
  hazelcastClient.disconnect()


  # REDIS
  if numOfInstances != 2:
    redisClient.connect()

    processes = [Process(target=redisClient.benchmarkClusterWrite, args=(i, totalProcesses)) for i in range(totalProcesses)]
    for p in processes:
      p.start()
    
    for p in processes:
      p.join()

    processes = [Process(target=redisClient.benchmarkClusterRead, args=(i, totalProcesses)) for i in range(totalProcesses)]
    for p in processes:
      p.start()
    
    for p in processes:
      p.join()

    redisClient.cleanup()
    redisClient.disconnect()


if __name__ == '__main__':
  benchmark_write_read()