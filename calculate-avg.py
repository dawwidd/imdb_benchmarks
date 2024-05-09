import sys
from multiprocessing import Process
from time import time, sleep

def process_file(filename):
    results = {}
    count = {}
    
    with open(filename, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            parts = line.strip().split()
            key = ' '.join(parts[:-1])  # Concatenate all except the last part
            time = float(parts[-1])
            
            if key in results:
                results[key] += time
                count[key] += 1
            else:
                results[key] = time
                count[key] = 1

    # Calculate averages
    averages = {key: results[key] / count[key] for key in results}

    with open('avg-' + filename, 'w') as file:
        for key, average in averages.items():
            file.write(f"{key} {average:.12f}\n")

def main():
    filenames = [f'result-new-{i}-1000-{j}.txt' for i in [1, 3, 10] for j in [5, 10, 50, 100]]

    processes = [Process(target=process_file, args=[filename]) for filename in filenames]
    start = time()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    end = time()
    print(f"Total time: {end - start}")

if __name__ == "__main__":
    main()