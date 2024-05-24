import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Funkcja do wczytywania wyników z pliku tekstowego
def load_results_from_file(filename):
    with open(filename, 'r') as file:
        results = [float(line.strip()) for line in file]
    return results

# Ścieżka do pliku z wynikami
filename = 'evict_results_actual_final_final/redis_results_random.txt'

# Wczytanie wyników do listy
results = load_results_from_file(filename)

# Podzielenie danych na dwie części
mid_point = len(results) // 2
first_half = results[:mid_point]
second_half = results[mid_point:]

# Sprawdzanie normalności rozkładu
shapiro_first_half = stats.shapiro(first_half)
shapiro_second_half = stats.shapiro(second_half)

print(f"Test Shapiro-Wilka dla pierwszej połowy danych:\nW = {shapiro_first_half[0]:.3f}, p-value = {shapiro_first_half[1]}")
print(f"Test Shapiro-Wilka dla drugiej połowy danych:\nW = {shapiro_second_half[0]:.3f}, p-value = {shapiro_second_half[1]}")


# Test t-Studenta dla prób zależnych
t_stat, t_p_value = stats.ttest_ind(first_half, second_half)
print(f"Test t-Studenta:\nT = {t_stat:.3f}, p-value = {t_p_value}")

# Test Wilcoxona
w_stat, w_p_value = stats.wilcoxon(first_half, second_half)
print(f"Test Wilcoxona:\nW = {w_stat}, p-value = {w_p_value}")
