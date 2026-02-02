# Сделай изменяемыми ползунками

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# --- 1. Исходные данные ---
samples = ['2233', '2699', '2776', '3110', '3384', '3599', '3675', '3714', 'Buzuluk']

# Концентрации Total (SN-1,2,3)
L_total = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0])
O_total = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1])

# Концентрации SN-2
L_2_exp = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1])
O_2_exp = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3])

# --- 2. Настройка модели ---

# Начальные значения параметров
init_threshold = 7.3
init_k_factor = 1.5
init_max_sum = 99.0
approx_total_fat = 89.0 # Средняя сумма L+O для пересчета графиков (константа)

def model_L(x, k, thresh):
    """Softplus модель: k * ln(1 + e^(x - thresh))"""
    # np.logaddexp(0, v) эквивалентно log(1 + exp(v)), но стабильнее
    return k * np.logaddexp(0, x - thresh)

def model_O(x_oleic, k, thresh, max_s):
    """
    Модель для Олеиновой:
    Считаем, сколько места заняла бы L при таком уровне O,
    и вычитаем это из максимума.
    Предполагаем: L_total ≈ approx_total_fat - O_total
    """
    l_equivalent = approx_total_fat - x_oleic
    l_2_pred = model_L(l_equivalent, k, thresh)
    return max_s - l_2_pred

# Диапазоны для линий графиков
x_range_L = np.linspace(0, 75, 200)
x_range_O = np.linspace(15, 95, 200)

# --- 3. Создание графиков ---

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
plt.subplots_adjust(bottom=0.25) # Оставляем место внизу для ползунков

# График 1: Линолевая (L)
ax1.scatter(L_total, L_2_exp, color='blue', s=70, label='Эксперимент', zorder=5)
line_L, = ax1.plot(x_range_L, model_L(x_range_L, init_k_factor, init_threshold), 
                   color='red', lw=2, label='Теория (Softplus)')
ax1.set_title('Линолевая (L): Насыщение SN-2')
ax1.set_xlabel('Total L (%)')
ax1.set_ylabel('SN-2 L (%)')
ax1.grid(True, alpha=0.3)
ax1.legend()

# График 2: Олеиновая (O)
ax2.scatter(O_total, O_2_exp, color='orange', s=70, label='Эксперимент', zorder=5)
line_O, = ax2.plot(x_range_O, model_O(x_range_O, init_k_factor, init_threshold, init_max_sum), 
                   color='purple', lw=2, label='Теория (Вытеснение)')
ax2.set_title('Олеиновая (O): Вытеснение из SN-2')
ax2.set_xlabel('Total O (%)')
ax2.set_ylabel('SN-2 O (%)')
ax2.grid(True, alpha=0.3)
ax2.legend()

# --- 4. Создание ползунков ---

# Координаты для ползунков [left, bottom, width, height]
ax_thresh = plt.axes([0.2, 0.1, 0.6, 0.03])
ax_k      = plt.axes([0.2, 0.06, 0.6, 0.03])
ax_max    = plt.axes([0.2, 0.02, 0.6, 0.03])

s_thresh = Slider(ax_thresh, 'Threshold (Порог)', 0.0, 20.0, valinit=init_threshold, valstep=0.1)
s_k      = Slider(ax_k, 'K Factor (Крутизна)', 0.5, 3.0, valinit=init_k_factor, valstep=0.1)
s_max    = Slider(ax_max, 'Max Sum SN-2', 90.0, 100.0, valinit=init_max_sum, valstep=0.1)

# --- 5. Функция обновления ---

def update(val):
    # Считываем значения с ползунков
    th = s_thresh.val
    k = s_k.val
    ms = s_max.val
    
    # Пересчитываем Y для линий
    y_new_L = model_L(x_range_L, k, th)
    y_new_O = model_O(x_range_O, k, th, ms)
    
    # Обновляем данные на графике
    line_L.set_ydata(y_new_L)
    line_O.set_ydata(y_new_O)
    
    # Перерисовываем
    fig.canvas.draw_idle()

# Привязываем функцию обновления к событию изменения ползунка
s_thresh.on_changed(update)
s_k.on_changed(update)
s_max.on_changed(update)

plt.show()