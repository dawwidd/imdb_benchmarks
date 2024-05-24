import sys
from pymemcache.client.base import Client
from python_clients.memcached_client import MemcachedClient
from python_clients.hazelcast_client import HazelcastClient
from python_clients.redis_client import RedisClient
from multiprocessing import Pool, Process, Manager
import time
import matplotlib.pyplot as plt


def runHazelcastBenchmark(process_num, num_of_runs, result_list, total_operations, measure_interval, manager_lock):
    hazelcastClient = HazelcastClient()
    hazelcastClient.connect(process_num)

    for run in range(num_of_runs):
        time_samples = []
        for i in range(total_operations):
            start = time.time()
            hazelcastClient.map.set(f'key-{process_num}-{run}-{i}', 'a' * 512)  # Set value size to 512 bytes
            end = time.time()

            time_samples.append(end - start)

            if (i + 1) % measure_interval == 0:
                with manager_lock:
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
            redisClient.client.set(f'key-{process_num}-{run}-{i}', 'a' * 512)  # Set value size to 512 bytes
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


def save_results(filename, result_list):
    with open(filename, 'w') as f:
        for avg_time in result_list:
            f.write(f'{avg_time}\n')


def load_results(filename):
    with open(filename, 'r') as f:
        return [float(line.strip()) for line in f]


def plot_results(datasets):
    db_methods = {}
    for filename, times in datasets.items():
        db_type, method = filename.split('_')[0], filename.split('_')[1]
        if db_type not in db_methods:
            db_methods[db_type] = {}
        db_methods[db_type][method] = times

    fig, ax = plt.subplots(figsize=(12, 6))

    bar_width = 0.35
    index = range(len(db_methods['hazelcast']))

    for i, (db_type, methods) in enumerate(db_methods.items()):
        avg_times = [sum(times) / len(times) for times in methods.values()]
        ax.bar([p + i * bar_width for p in index], avg_times, bar_width, label=db_type)

    ax.set_xlabel('Persistence Method')
    ax.set_ylabel('Average Write Time (seconds)')
    ax.set_title('Average Write Time for Different Persistence Methods')
    ax.set_xticks([p + bar_width for p in index])
    ax.set_xticklabels(db_methods['hazelcast'].keys())
    ax.legend()

    plt.grid(True)
    plt.savefig('average_write_times_comparison.png')
    plt.show()


def benchmark_persistence(db_type, persistence_method):
    num_processes = 10
    num_of_runs = 1
    total_operations = 1024
    measure_interval = 10

    manager = Manager()
    result_list = manager.list()
    manager_lock = manager.Lock()

    processes = []


    if db_type == "hazelcast":
        for process_num in range(num_processes):
            p = Process(target=runHazelcastBenchmark, args=(process_num, num_of_runs, result_list, total_operations, measure_interval, manager_lock))
            p.start()
            processes.append(p)
    elif db_type == "redis":
        for process_num in range(num_processes):
            p = Process(target=runRedisBenchmark, args=(process_num, num_of_runs, result_list, total_operations, measure_interval, manager_lock))
            p.start()
            processes.append(p)

    for p in processes:
        p.join()

    # Save results to file
    filename = f'persistence_check_results/{db_type}_{persistence_method}_results.txt'
    save_results(filename, result_list)

    print(f'Results saved to {filename}')


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python benchmark_persistence.py <hazelcast|redis|plot> <persistence_method|plot_files>")
        sys.exit(1)

    action = sys.argv[1].lower()
    if action == "plot":
        plot_files = sys.argv[2:]
        datasets = {filename: load_results(filename) for filename in plot_files}
        plot_results(datasets)
    else:
        persistence_method = sys.argv[2].lower()
        benchmark_persistence(action, persistence_method)
