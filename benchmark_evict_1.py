import sys
from pymemcache.client.base import Client
from python_clients.memcached_client import MemcachedClient
from python_clients.hazelcast_client import HazelcastClient
from python_clients.redis_client import RedisClient
import time
import matplotlib.pyplot as plt

def runMemcachedBenchmark(num_of_runs, total_operations, measure_interval, filename):
    memcachedClient = MemcachedClient()
    memcachedClient.connect(0)  

    interval_count = total_operations // measure_interval
    aggregated_results = [[] for _ in range(interval_count)]

    with open(filename, 'w') as file:
        for run in range(num_of_runs):
            time_samples = []
            for i in range(total_operations):
                start = time.time()
                memcachedClient.client.set(f'key-{run}-{i}', 'a' * 1024)  
                end = time.time()

                time_samples.append(end - start)

                if (i + 1) % measure_interval == 0:
                    interval_index = (i + 1) // measure_interval - 1
                    avg_time = sum(time_samples) / len(time_samples)
                    aggregated_results[interval_index].append(1/avg_time)
                    print(f'Run {run} Memcached WRITE MULTI {i} {sum(time_samples) / len(time_samples)}')
                    time_samples = []  

            memcachedClient.cleanup()

    memcachedClient.disconnect()

    final_averages = [sum(interval) / len(interval) for interval in aggregated_results if interval]
    
    with open(filename, 'a') as file:
        for avg in final_averages:
            file.write(f'{avg}\n')
    
    return final_averages

def runHazelcastBenchmark(num_of_runs, total_operations, measure_interval, filename):
    hazelcastClient = HazelcastClient()
    hazelcastClient.connect(0)  

    interval_count = total_operations // measure_interval
    aggregated_results = [[] for _ in range(interval_count)]

    with open(filename, 'w') as file:
        for run in range(num_of_runs):
            time_samples = []
            for i in range(total_operations):
                start = time.time()
                hazelcastClient.map.set(f'key-{run}-{i}', 'a' * 1024)  
                end = time.time()

                time_samples.append(end - start)

                if (i + 1) % measure_interval == 0:
                    interval_index = (i + 1) // measure_interval - 1
                    avg_time = sum(time_samples) / len(time_samples)
                    aggregated_results[interval_index].append(1/avg_time)
                    print(f'Run {run} Hazelcast WRITE MULTI {i} {sum(time_samples) / len(time_samples)}')
                    time_samples = []  

            hazelcastClient.cleanup()

    hazelcastClient.disconnect()

    final_averages = [sum(interval) / len(interval) for interval in aggregated_results if interval]

    with open(filename, 'a') as file:
        for avg in final_averages:
            file.write(f'{avg}\n')
    
    return final_averages

def runRedisBenchmark(num_of_runs, total_operations, measure_interval, filename):
    redisClient = RedisClient()
    redisClient.connect(0)  

    interval_count = total_operations // measure_interval
    aggregated_results = [[] for _ in range(interval_count)]

    with open(filename, 'w') as file:
        for run in range(num_of_runs):
            time_samples = []
            for i in range(total_operations):
                start = time.time()
                redisClient.client.set(f'key-{run}-{i}', 'a' * 1024)  
                end = time.time()

                time_samples.append(end - start)

                if (i + 1) % measure_interval == 0:
                    interval_index = (i + 1) // measure_interval - 1
                    avg_time = sum(time_samples) / len(time_samples)
                    aggregated_results[interval_index].append(1/avg_time)
                    print(f'Run {run} Redis WRITE MULTI {i} {sum(time_samples) / len(time_samples)}')
                    time_samples = []  

            redisClient.cleanup()

    redisClient.disconnect()

    final_averages = [sum(interval) / len(interval) for interval in aggregated_results if interval]

    with open(filename, 'a') as file:
        for avg in final_averages:
            file.write(f'{avg}\n')
    
    return final_averages

def benchmark_evict():
    args = sys.argv

    db = args[1]
    method = args[2]

    print(f'BENCHMARK {db} {method}')

    num_of_runs = 1
    total_operations = 1048576
    measure_interval = 32768 // 2 // 2

    # Memcached
    if db == 'memcached':
        memcached_filename = f'evict_results_actual_final_final/memcached_results_{method}.txt'
        memcached_results = runMemcachedBenchmark(num_of_runs, total_operations, measure_interval, memcached_filename)
        final_average = sum(memcached_results) / len(memcached_results)

        plt.figure(figsize=(12, 6))
        plt.plot(range(measure_interval, measure_interval * len(memcached_results) + 1, measure_interval), memcached_results, marker='o', linestyle='-')
        plt.title(f'Liczba operacji na sekundę w zależności od ilości zapisanych danych (Memcached {method})')
        plt.xlabel('Liczba zapisanych KB danych')
        plt.ylabel('Operacje na sekundę')
        plt.grid(True)
        plt.savefig(f'evict_results_actual_final_final/memcached_results_{method}.png')
        plt.show()
    # Hazelcast
    elif db == 'hazelcast':
        hazelcast_filename = f'evict_results_actual_final_final/hazelcast_results_{method}.txt'
        hazelcast_results = runHazelcastBenchmark(num_of_runs, total_operations, measure_interval, hazelcast_filename)
        final_average = sum(hazelcast_results) / len(hazelcast_results)

        plt.figure(figsize=(12, 6))
        plt.plot(range(measure_interval, measure_interval * len(hazelcast_results) + 1, measure_interval), hazelcast_results, marker='o', linestyle='-')
        plt.title(f'Liczba operacji na sekundę w zależności od ilości zapisanych danych (Hazelcast {method})')
        plt.xlabel('Liczba zapisanych KB danych')
        plt.ylabel('Operacje na sekundę')
        plt.grid(True)
        plt.savefig(f'evict_results_actual_final_final/hazelcast_results_{method}.png')
        plt.show()
    # Redis
    elif db == 'redis':
        redis_filename = f'evict_results_actual_final_final/redis_results_{method}.txt'
        redis_results = runRedisBenchmark(num_of_runs, total_operations, measure_interval, redis_filename)
        final_average = sum(redis_results) / len(redis_results)

        plt.figure(figsize=(12, 6))
        plt.plot(range(measure_interval, measure_interval * len(redis_results) + 1, measure_interval), redis_results, marker='o', linestyle='-')
        plt.title(f'Liczba operacji na sekundę w zależności od ilości zapisanych danych (Redis {method})')
        plt.xlabel('Liczba zapisanych KB danych')
        plt.ylabel('Operacje na sekundę')
        plt.grid(True)
        plt.savefig(f'evict_results_actual_final_final/redis_results_{method}.png')
        plt.show()




if __name__ == "__main__":
    benchmark_evict()