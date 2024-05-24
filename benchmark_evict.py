import sys
from pymemcache.client.base import Client
from python_clients.memcached_client import MemcachedClient
from python_clients.hazelcast_client import HazelcastClient
from python_clients.redis_client import RedisClient
from multiprocessing import Pool, Process, Manager
import time
import matplotlib.pyplot as plt

def runMemcachedBenchmark(process_num, num_of_runs, result_list, total_operations, measure_interval, manager_lock):
    memcachedClient = MemcachedClient()
    memcachedClient.connect(process_num)  

    for run in range(num_of_runs):
        time_samples = []
        for i in range(total_operations):
            start = time.time()
            memcachedClient.client.set(f'key-{process_num}-{run}-{i}', 'a' * 1024)  
            end = time.time()

            time_samples.append(end - start)

            if (i + 1) % measure_interval == 0:
                with manager_lock:  
                    avg_time = sum(time_samples) / len(time_samples)
                    result_list.append(avg_time)
                time_samples = []  

            memcachedClient.cleanup()

    memcachedClient.disconnect()

def runHazelcastBenchmark(process_num, num_of_runs, result_list, total_operations, measure_interval, manager_lock):
    hazelcastClient = HazelcastClient()
    hazelcastClient.connect(process_num)  

    for run in range(num_of_runs):
        time_samples = []
        for i in range(total_operations):
            start = time.time()
            hazelcastClient.map.set(f'key-{process_num}-{run}-{i}', 'a' * 1024)  
            end = time.time()

            time_samples.append(end - start)

            if (i + 1) % measure_interval == 0:
                with manager_lock:  
                    print(f'Hazelcast WRITE MULTI {i} {sum(time_samples) / len(time_samples)}')
                    avg_time = sum(time_samples) / len(time_samples)
                    result_list.append(avg_time)
                time_samples = []  

        hazelcastClient.cleanup()

    hazelcastClient.disconnect()


def runRedisBenchmark(process_num, num_of_runs, result_list, total_operations, measure_interval, manager_lock):
    redisClient = RedisClient()
    redisClient.connect(process_num)  

    for run in range(num_of_runs):
        time_samples = []
        for i in range(total_operations):
            start = time.time()
            redisClient.client.set(f'key-{process_num}-{run}-{i}', 'a' * 1024)  
            end = time.time()

            time_samples.append(end - start)

            if (i + 1) % measure_interval == 0:
                with manager_lock:
                    print(f'Redis WRITE MULTI {i} {sum(time_samples) / len(time_samples)}')
                    avg_time = sum(time_samples) / len(time_samples)
                    result_list.append(avg_time)
                time_samples = []  

        redisClient.cleanup()

    redisClient.disconnect()

def benchmark_evict():
    num_processes = 10
    num_of_runs = 1
    total_operations = 1048576
    measure_interval = 100000

    # Memcached
    # manager = Manager()
    # result_list = manager.list()  
    # manager_lock = manager.Lock()  

    # processes = []

    # for process_num in range(num_processes):
    #     p = Process(target=runMemcachedBenchmark, args=(process_num, num_of_runs, result_list, total_operations, measure_interval, manager_lock))
    #     p.start()
    #     processes.append(p)

    # for p in processes:
    #     p.join()

    
    # final_average = sum(result_list) / len(result_list)

    
    # plt.figure(figsize=(12, 6))
    # plt.plot(range(measure_interval, measure_interval * len(result_list) + 1, measure_interval), result_list, marker='o', linestyle='-')
    # plt.title('Liczba operacji na sekundę w zależności od ilości zapisanych danych')
    # plt.xlabel('Liczba zapisanych KB danych')
    # plt.ylabel('Operacje na sekundę')
    # plt.grid(True)
    # plt.savefig('final_memcached_evict_lru.png')
    # plt.show()


    # Hazelcast
    manager = Manager()
    result_list = manager.list()  
    manager_lock = manager.Lock()  

    processes = []

    for process_num in range(num_processes):
        p = Process(target=runHazelcastBenchmark, args=(process_num, num_of_runs, result_list, total_operations, measure_interval, manager_lock))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    
    final_average = sum(result_list) / len(result_list)

    
    plt.figure(figsize=(12, 6))
    plt.plot(range(measure_interval, measure_interval * len(result_list) + 1, measure_interval), result_list, marker='o', linestyle='-')
    plt.title('Liczba operacji na sekundę w zależności od ilości zapisanych danych')
    plt.xlabel('Liczba zapisanych KB danych')
    plt.ylabel('Operacje na sekundę')
    plt.grid(True)
    plt.savefig('hazelcast_average_write_times_lru_test5.png')
    plt.show()


    # Redis
    # manager = Manager()
    # result_list = manager.list()  
    # manager_lock = manager.Lock()  

    # processes = []

    # for process_num in range(num_processes):
    #     p = Process(target=runRedisBenchmark, args=(process_num, num_of_runs, result_list, total_operations, measure_interval, manager_lock))
    #     p.start()
    #     processes.append(p)

    # for p in processes:
    #     p.join()

    
    # final_average = sum(result_list) / len(result_list)

    
    # plt.figure(figsize=(12, 6))
    # plt.plot(range(measure_interval, measure_interval * len(result_list) + 1, measure_interval), result_list, marker='o', linestyle='-')
    # plt.title('Liczba operacji na sekundę w zależności od ilości zapisanych danych')
    # plt.xlabel('Liczba zapisanych KB danych')
    # plt.ylabel('Operacje na sekundę')
    # plt.grid(True)
    # plt.savefig('redis_average_write_times_evict_noeviction.png')
    # plt.show()