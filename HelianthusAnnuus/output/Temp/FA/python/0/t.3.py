# поправь формулы по новым данным. и кривые не только после 7.3 должны скругляться, но и выходить на плато сверху

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# --- 1. Данные ---

# Группа 1: Исходные (Круги)
L_total_old = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0])
O_total_old = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1])
L_2_old     = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1])
O_2_old     = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3])

# Группа 2: Новые (Квадраты) - Commodity, High Lin, High Oleic, HiStear
# Исключаем пока High Palmitic из основной группы для наглядности, или оставляем все вместе
L_total_new = np.array([58.7, 76.0, 2.1, 2.0])
O_total_new = np.array([27.8, 13.3, 91.5, 79.1])
L_2_new     = np.array([65.7, 76.9, 1.4, 0.6])
O_2_new     = np.array([31.5, 18.9, 96.6, 95.9])

# Группа 3: High Palmitic (Треугольники) - они ведут себя иначе из-за высокого насыщения
L_total_palm = np.array([46.8, 3.5])
O_total_palm = np.array([17.1, 59.8])
L_2_palm     = np.array([67.8, 2.8])
O_2_palm     = np.array([24.9, 93.4])

# --- 2. Модель (Сигмоида) ---

# Начальные параметры (подобраны под ваши данные)
init_L_max = 96.0   # Плато сверху
init_k = 0.12       # Крутизна
init_x0 = 35.0      # Точка перегиба (центр S-кривой)
init_sat_fat = 10.0 # Средний % насыщенных жиров (для расчета O)

def sigmoid(x, L_max, k, x0):
    """Логистическая функция: L_max / (1 + exp(-k*(x-x0)))"""
    # Защита от переполнения экспоненты
    argument = -k * (x - x0)
    argument = np.clip(argument, -100, 100) 
    return L_max / (1.0 + np.exp(argument))

def model_O_from_L(x_oleic, L_max, k, x0, sat_fat_percent):
    """
    Расчет O через L:
    1. Считаем доступную L: L_total ≈ (100 - SatFat) - O_total
    2. Считаем L_2 через сигмоиду
    3. O_2 ≈ (100 - SatFat_in_SN2) - L_2
       Для простоты считаем Max_SN2 ≈ L_max
    """
    # Сколько L "должно быть" при таком O
    l_equivalent = (100 - sat_fat_percent) - x_oleic
    
    # Предсказываем L в SN-2
    l_2_pred = sigmoid(l_equivalent, L_max, k, x0)
    
    # Оставшееся место занимает O
    return L_max - l_2_pred

# Диапазоны
x_range_L = np.linspace(0, 90, 200)
x_range_O = np.linspace(10, 100, 200)

# --- 3. Графики ---

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
plt.subplots_adjust(bottom=0.30) # Место для 4 ползунков

# --- График L ---
ax1.scatter(L_total_old, L_2_old, c='blue', marker='o', s=50, label='Standard', alpha=0.6)
ax1.scatter(L_total_new, L_2_new, c='navy', marker='s', s=60, label='Hi-Oleic/Lin/Stear')
ax1.scatter(L_total_palm, L_2_palm, c='green', marker='^', s=70, label='Hi-Palmitic')

line_L, = ax1.plot(x_range_L, sigmoid(x_range_L, init_L_max, init_k, init_x0), 
                   color='red', lw=2.5, label='Сигмоида')

ax1.set_title('Линолевая (L): S-образное насыщение')
ax1.set_xlabel('Total L (%)')
ax1.set_ylabel('SN-2 L (%)')
ax1.grid(True, alpha=0.3)
ax1.legend()

# --- График O ---
ax2.scatter(O_total_old, O_2_old, c='orange', marker='o', s=50, label='Standard', alpha=0.6)
ax2.scatter(O_total_new, O_2_new, c='darkred', marker='s', s=60, label='Hi-Oleic/Lin/Stear')
ax2.scatter(O_total_palm, O_2_palm, c='green', marker='^', s=70, label='Hi-Palmitic')

line_O, = ax2.plot(x_range_O, model_O_from_L(x_range_O, init_L_max, init_k, init_x0, init_sat_fat), 
                   color='purple', lw=2.5, label='Теория (Вытеснение)')

ax2.set_title('Олеиновая (O): Конкуренция')
ax2.set_xlabel('Total O (%)')
ax2.set_ylabel('SN-2 O (%)')
ax2.grid(True, alpha=0.3)
ax2.legend()

# --- 4. Ползунки ---

ax_max = plt.axes([0.15, 0.15, 0.7, 0.03])
ax_k   = plt.axes([0.15, 0.11, 0.7, 0.03])
ax_x0  = plt.axes([0.15, 0.07, 0.7, 0.03])
ax_sat = plt.axes([0.15, 0.03, 0.7, 0.03])

s_max = Slider(ax_max, 'Max Plateau (L_max)', 80.0, 100.0, valinit=init_L_max)
s_k   = Slider(ax_k, 'Steepness (k)', 0.05, 0.30, valinit=init_k)
s_x0  = Slider(ax_x0, 'Midpoint (x0)', 10.0, 60.0, valinit=init_x0)
s_sat = Slider(ax_sat, 'Saturated Fat % (Offset)', 0.0, 30.0, valinit=init_sat_fat)

def update(val):
    lm = s_max.val
    k = s_k.val
    x0 = s_x0.val
    sf = s_sat.val
    
    # Обновляем L
    line_L.set_ydata(sigmoid(x_range_L, lm, k, x0))
    
    # Обновляем O
    line_O.set_ydata(model_O_from_L(x_range_O, lm, k, x0, sf))
    
    fig.canvas.draw_idle()

s_max.on_changed(update)
s_k.on_changed(update)
s_x0.on_changed(update)
s_sat.on_changed(update)

plt.show()