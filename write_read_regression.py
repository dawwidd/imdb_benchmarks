import numpy as np
import pandas as pd
import scipy.stats as stats

# Dane wejściowe
data = {
    "data_size": [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072],
    "memcached_write": [110864.75, 83056.48, 100502.51, 84175.08, 91157.70, 138888.89, 87108.01, 136054.42, 108695.65, 59136.61, 46146.75, 43346.34, 19516.00, 13306.72],
    "memcached_read": [11759.17, 9807.77, 7727.38, 8042.46, 15552.10, 9930.49, 9750.39, 14349.26, 7367.57, 12420.82, 10034.92, 9124.09, 6933.85, 6177.80],
    "hazelcast_write": [15398.83, 14526.44, 16217.97, 16212.71, 16801.08, 19080.33, 17488.63, 22737.61, 21217.91, 16315.88, 18556.32, 15482.27, 12526.62, 7959.88],
    "hazelcast_read": [14889.82, 21819.77, 16450.07, 18761.73, 17627.36, 15033.07, 23201.86, 26932.40, 34435.26, 20153.16, 15527.95, 33222.59, 29222.68, 32819.17],
    "redis_write": [10646.23, 11674.06, 10912.27, 11343.01, 10552.98, 9911.79, 11827.32, 11875.07, 10795.64, 6983.24, 8729.05, 6831.53, 3348.96, 4316.30],
    "redis_read": [10625.86, 11933.17, 12509.38, 12103.61, 11277.77, 11524.72, 10198.88, 11951.72, 11619.80, 10746.91, 11164.45, 10220.77, 5358.48, 5025.13]
}

# Konwersja do DataFrame
df = pd.DataFrame(data)
df["log_data_size"] = np.log(df["data_size"])

# Obliczenie korelacji Kendalla
results = {}
columns = ["memcached_write", "memcached_read", "hazelcast_write", "hazelcast_read", "redis_write", "redis_read"]

for col in columns:
    tau, p_value = stats.kendalltau(df["data_size"], df[col])
    results[col] = {"tau": tau, "p_value": p_value}

# Wyświetlenie wyników
for col, result in results.items():
    print(f"{col}: tau = {result['tau']:.3f}, p-value = {result['p_value']:.8f}")