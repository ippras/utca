# подбери наилучшие параметры, когда ошибки до всех экспериментальных точек минимальны

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

# --- 1. Сбор всех данных в одну кучу ---

# L_total (X), L_sn2 (Y)
L_X = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0, # Old
                58.7, 76.0, 2.1, 2.0,                               # New
                46.8, 3.5])                                         # Hi-Palm
L_Y = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1,
                65.7, 76.9, 1.4, 0.6,
                67.8, 2.8])

# O_total (X), O_sn2 (Y)
O_X = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1, # Old
                27.8, 13.3, 91.5, 79.1,                               # New
                17.1, 59.8])                                          # Hi-Palm
O_Y = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3,
                31.5, 18.9, 96.6, 95.9,
                24.9, 93.4])

# --- 2. Функции модели ---

def sigmoid(x, plateau, k, x0):
    # L_model
    arg = -k * (x - x0)
    # Защита от переполнения
    arg = np.clip(arg, -100, 100)
    return plateau / (1.0 + np.exp(arg))

def model_O(x_oleic, plateau, sn2_cap, k, x0, sat_fat):
    # O_model
    l_equiv = (100 - sat_fat) - x_oleic
    l_occ = sigmoid(l_equiv, plateau, k, x0)
    return sn2_cap - l_occ

# --- 3. Функция ошибки (Loss Function) ---

def objective_function(params):
    """
    Считает сумму квадратов ошибок для L и O одновременно.
    params: [plateau, sn2_cap, k, x0, sat_fat]
    """
    p, cap, k, x0, sf = params
    
    # Ошибка по L
    L_pred = sigmoid(L_X, p, k, x0)
    err_L = np.sum((L_Y - L_pred)**2)
    
    # Ошибка по O
    O_pred = model_O(O_X, p, cap, k, x0, sf)
    err_O = np.sum((O_Y - O_pred)**2)
    
    return err_L + err_O

# --- 4. Оптимизация ---

# Начальные догадки (откуда начинать искать)
initial_guess = [96.0, 99.0, 0.12, 35.0, 10.0]

# Границы параметров (чтобы не ушло в минус или бесконечность)
bounds = [
    (80.0, 100.0), # Plateau L
    (90.0, 100.0), # SN2 Cap
    (0.05, 0.5),   # k
    (10.0, 60.0),  # x0
    (0.0, 30.0)    # Sat Fat
]

result = minimize(objective_function, initial_guess, bounds=bounds, method='L-BFGS-B')

# Получаем лучшие параметры
best_p, best_cap, best_k, best_x0, best_sf = result.x

print("=== НАИЛУЧШИЕ ПАРАМЕТРЫ ===")
print(f"L Plateau (Max L): {best_p:.2f} %")
print(f"SN-2 Capacity:     {best_cap:.2f} %")
print(f"Steepness (k):     {best_k:.4f}")
print(f"Midpoint (x0):     {best_x0:.2f}")
print(f"Sat Fat Offset:    {best_sf:.2f} %")
print(f"Общая ошибка (MSE): {result.fun:.2f}")

# --- 5. Построение графика с лучшими параметрами ---

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Диапазоны
xr_L = np.linspace(0, 90, 200)
xr_O = np.linspace(10, 100, 200)

# График L
ax1.scatter(L_X, L_Y, c='blue', s=60, label='Все точки', zorder=3)
ax1.plot(xr_L, sigmoid(xr_L, best_p, best_k, best_x0), 'r-', lw=3, label='Оптимальная модель')
ax1.axhline(best_p, color='gray', ls='--', alpha=0.5, label=f'Plateau {best_p:.1f}%')
ax1.set_title(f'L Optimization (k={best_k:.3f}, x0={best_x0:.1f})')
ax1.set_xlabel('Total L')
ax1.set_ylabel('SN-2 L')
ax1.grid(True, alpha=0.3)
ax1.legend()

# График O
ax2.scatter(O_X, O_Y, c='orange', s=60, label='Все точки', zorder=3)
ax2.plot(xr_O, model_O(xr_O, best_p, best_cap, best_k, best_x0, best_sf), 'purple', lw=3, label='Оптимальная модель')
ax2.axhline(best_cap, color='gray', ls='--', alpha=0.5, label=f'Capacity {best_cap:.1f}%')
ax2.set_title(f'O Optimization (SatFat avg={best_sf:.1f}%)')
ax2.set_xlabel('Total O')
ax2.set_ylabel('SN-2 O')
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.show()