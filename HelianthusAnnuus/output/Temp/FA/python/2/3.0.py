import matplotlib.pyplot as plt
import numpy as np

# --- Данные из таблицы ---
# Названия образцов (для подписей, опционально)
labels = ['3110', '3599', '2233', '2776', '2699', '3714', '3675', '3384', 'Бузулук']

# Linoleic SN-1,2,3 (Общее содержание)
lin_total = np.array([1.1, 1.8, 40.9, 44.2, 46.2, 50.8, 51.7, 53.5, 64.0])

# Linoleic SN-2 (Содержание во 2-м положении)
lin_sn2 = np.array([0, 0.9, 49.8, 55.2, 61.1, 64.6, 64.5, 71.5, 84.1])

# Oleic EF (Целевое значение)
oleic_ef = np.array([38.6, 37.2, 37.9, 32.6, 31.2, 30.0, 30.9, 25.3, 19.8])

# --- Настройка графика ---
plt.figure(figsize=(10, 6))

# 1. Точки данных
plt.scatter(lin_total, oleic_ef, color='blue', s=80, label='Данные: Linoleic (SN-1,2,3)', zorder=3)
plt.scatter(lin_sn2, oleic_ef, color='red', marker='s', s=80, label='Данные: Linoleic (SN-2)', zorder=3)

# --- Аппроксимация (Формулы) ---
x_range = np.linspace(0, 90, 100)

# Формула 1: EF = MIN(38.5, 70 - 0.8 * Total)
y_approx_total = np.minimum(38.5, 70 - 0.8 * x_range)

# Формула 2: EF = MIN(38.5, 65 - 0.53 * SN2)
y_approx_sn2 = np.minimum(38.5, 65 - 0.53 * x_range)

# Рисуем линии аппроксимации
plt.plot(x_range, y_approx_total, color='blue', linestyle='--', alpha=0.6, label='Аппроксимация (по Total)')
plt.plot(x_range, y_approx_sn2, color='red', linestyle='--', alpha=0.6, label='Аппроксимация (по SN-2)')

# --- Оформление ---
plt.title('Зависимость Oleic EF от содержания Linoleic', fontsize=14)
plt.xlabel('Содержание Linoleic (%)', fontsize=12)
plt.ylabel('Oleic EF', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

# Добавим зоны
plt.axvspan(0, 40, color='green', alpha=0.1, label='Зона плато')
plt.text(20, 25, 'Высокоолеиновые\n(EF стабилен)', color='green', ha='center', fontsize=10)

plt.axvspan(40, 90, color='orange', alpha=0.1, label='Зона снижения')
plt.text(65, 35, 'Линолевые\n(EF падает)', color='darkorange', ha='center', fontsize=10)

plt.tight_layout()
plt.show()