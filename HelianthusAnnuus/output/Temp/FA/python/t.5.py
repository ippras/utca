# 

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# --- 1. Данные ---
# Группа 1: Исходные
L_total_old = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0])
O_total_old = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1])
L_2_old     = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1])
O_2_old     = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3])

# Группа 2: Новые (Commodity, High Lin, High Oleic, HiStear)
L_total_new = np.array([58.7, 76.0, 2.1, 2.0])
O_total_new = np.array([27.8, 13.3, 91.5, 79.1])
L_2_new     = np.array([65.7, 76.9, 1.4, 0.6])
O_2_new     = np.array([31.5, 18.9, 96.6, 95.9])

# Группа 3: High Palmitic
L_total_palm = np.array([46.8, 3.5])
O_total_palm = np.array([17.1, 59.8])
L_2_palm     = np.array([67.8, 2.8])
O_2_palm     = np.array([24.9, 93.4])

# --- 2. Модель ---

# Параметры по умолчанию
init_L_plateau = 80.0  # Предел насыщения для L
init_sn2_cap   = 99.12  # Физическая вместимость SN-2 (потолок для O)
init_k         = 0.1451
init_x0        = 38.32
init_sat_fat   = 13.74

def sigmoid(x, plateau, k, x0):
    """Считает L с учетом её собственного плато"""
    argument = -k * (x - x0)
    argument = np.clip(argument, -100, 100)
    return plateau / (1.0 + np.exp(argument))

def model_O(x_oleic, l_plateau, sn2_cap, k, x0, sat_fat):
    """
    Считает O как (Вместимость - L).
    O может расти до sn2_cap, даже если l_plateau низкое.
    """
    # 1. Переводим O в доступную L
    l_equivalent = (100 - sat_fat) - x_oleic
    
    # 2. Считаем, сколько места заняла L (ограничена своим плато)
    l_occupied = sigmoid(l_equivalent, l_plateau, k, x0)
    
    # 3. O занимает всё остальное место в пределах физической вместимости
    return sn2_cap - l_occupied

# Диапазоны
x_range_L = np.linspace(0, 90, 200)
x_range_O = np.linspace(10, 100, 200)

# --- 3. Графики ---

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
plt.subplots_adjust(bottom=0.35) # Больше места для 5 ползунков

# === График L ===
ax1.scatter(L_total_old, L_2_old, c='blue', label='Standard', alpha=0.6)
ax1.scatter(L_total_new, L_2_new, c='navy', marker='s', label='Hi-Oleic/Lin')
ax1.scatter(L_total_palm, L_2_palm, c='green', marker='^', label='Hi-Palmitic')

line_L, = ax1.plot(x_range_L, sigmoid(x_range_L, init_L_plateau, init_k, init_x0), 
                   color='red', lw=3, label='Модель L')
# Линия плато L
line_limit_L = ax1.axhline(y=init_L_plateau, color='red', linestyle='--', alpha=0.3, label='L Plateau')

ax1.set_title('Линолевая (L): Ограничена ферментом')
ax1.set_xlabel('Total L (%)')
ax1.set_ylabel('SN-2 L (%)')
ax1.set_ylim(-5, 105)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper left')

# === График O ===
ax2.scatter(O_total_old, O_2_old, c='orange', label='Standard', alpha=0.6)
ax2.scatter(O_total_new, O_2_new, c='darkred', marker='s', label='Hi-Oleic/Lin')
ax2.scatter(O_total_palm, O_2_palm, c='green', marker='^', label='Hi-Palmitic')

line_O, = ax2.plot(x_range_O, model_O(x_range_O, init_L_plateau, init_sn2_cap, init_k, init_x0, init_sat_fat), 
                   color='purple', lw=3, label='Модель O')
# Линия вместимости SN-2
line_limit_O = ax2.axhline(y=init_sn2_cap, color='purple', linestyle='--', alpha=0.3, label='SN-2 Capacity')

ax2.set_title('Олеиновая (O): Заполняет объём')
ax2.set_xlabel('Total O (%)')
ax2.set_ylabel('SN-2 O (%)')
ax2.set_ylim(-5, 105)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right')

# --- 4. Ползунки ---

ax_l_plat = plt.axes([0.15, 0.20, 0.7, 0.03])
ax_sn2    = plt.axes([0.15, 0.16, 0.7, 0.03])
ax_k      = plt.axes([0.15, 0.12, 0.7, 0.03])
ax_x0     = plt.axes([0.15, 0.08, 0.7, 0.03])
ax_sat    = plt.axes([0.15, 0.04, 0.7, 0.03])

s_l_plat = Slider(ax_l_plat, 'Max L', 70.0, 100.0, valinit=init_L_plateau)
s_sn2    = Slider(ax_sn2,    'Max O', 90.0, 100.0, valinit=init_sn2_cap)
s_k      = Slider(ax_k,      'Steepness (k)', 0.05, 0.30, valinit=init_k)
s_x0     = Slider(ax_x0,     'Midpoint (x0)', 10.0, 60.0, valinit=init_x0)
s_sat    = Slider(ax_sat,    'Sat Fat % (Offset)', 0.0, 30.0, valinit=init_sat_fat)

def update(val):
    lp = s_l_plat.val
    cap = s_sn2.val
    k = s_k.val
    x0 = s_x0.val
    sf = s_sat.val
    
    # Обновляем кривые
    line_L.set_ydata(sigmoid(x_range_L, lp, k, x0))
    line_O.set_ydata(model_O(x_range_O, lp, cap, k, x0, sf))
    
    # Обновляем пунктирные линии границ
    line_limit_L.set_ydata([lp, lp])
    line_limit_O.set_ydata([cap, cap])
    
    fig.canvas.draw_idle()

s_l_plat.on_changed(update)
s_sn2.on_changed(update)
s_k.on_changed(update)
s_x0.on_changed(update)
s_sat.on_changed(update)

plt.show()
