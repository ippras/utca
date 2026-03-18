import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# ==========================================
# 1. ДАННЫЕ
# ==========================================
sn123 = np.array([64, 40.9, 46.2, 44.2, 53.5, 51.7, 50.8, 61.4, 50, 32.7, 32.5, 32.9, 20.6, 58.7, 76.0, 46.8])
sn13  = np.array([53.9, 36.5, 38.7, 38.6, 44.4, 45.3, 43.8, 39, 31.5, 24.7, 27.9, 22.1, 13.9, 55.2, 75.55, 36.3])
sn2   = np.array([84.1, 49.8, 61.1, 55.2, 71.5, 64.5, 64.6, 94.4, 82.3, 46.6, 40.8, 52.4, 32.5, 65.7, 76.9, 67.8])

# ==========================================
# 2. РАСЧЕТ УРАВНЕНИЙ
# ==========================================

def get_regression(x, y):
    # Находим коэффициенты a (наклон) и b (смещение) для y = ax + b
    a, b = np.polyfit(x, y, 1)
    # Считаем R^2
    y_pred = a * x + b
    r2 = r2_score(y, y_pred)
    return a, b, r2

# Расчет для двух случаев
a1, b1, r2_1 = get_regression(sn123, sn13)
a2, b2, r2_2 = get_regression(sn123, sn2)

print(f"Уравнение для SN-1,3: y = {a1:.4f}x + ({b1:.4f}), R² = {r2_1:.4f}")
print(f"Уравнение для SN-2:   y = {a2:.4f}x + ({b2:.4f}), R² = {r2_2:.4f}")

# ==========================================
# 3. ВИЗУАЛИЗАЦИЯ
# ==========================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# График 1: SN-1,2,3 vs SN-1,3
ax1.scatter(sn123, sn13, color='blue', label='Экспериментальные данные')
x_range = np.linspace(min(sn123), max(sn123), 100)
ax1.plot(x_range, a1 * x_range + b1, color='red', label=f'Регрессия: y={a1:.2f}x+{b1:.2f}')
ax1.set_title("SN-1,2,3 vs SN-1,3")
ax1.set_xlabel("SN-1,2,3 (%)")
ax1.set_ylabel("SN-1,3 (%)")
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.7)

# График 2: SN-1,2,3 vs SN-2
ax2.scatter(sn123, sn2, color='green', label='Экспериментальные данные')
ax2.plot(x_range, a2 * x_range + b2, color='red', label=f'Регрессия: y={a2:.2f}x+{b2:.2f}')
ax2.set_title("SN-1,2,3 vs SN-2")
ax2.set_xlabel("SN-1,2,3 (%)")
ax2.set_ylabel("SN-2 (%)")
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()