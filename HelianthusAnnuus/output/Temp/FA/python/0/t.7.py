# а можно формулы привести не через точку перегиба, а через точку подъема и точку выхода на плато (и также параметры в графике)

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# --- 1. Данные ---
# Объединяем все данные для удобства
L_total = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0, 58.7, 76.0, 2.1, 2.0, 46.8, 3.5])
L_sn2   = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1, 65.7, 76.9, 1.4, 0.6, 67.8, 2.8])

O_total = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1, 27.8, 13.3, 91.5, 79.1, 17.1, 59.8])
O_sn2   = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3, 31.5, 18.9, 96.6, 95.9, 24.9, 93.4])

# Маркеры для легенды
idx_old = slice(0, 9)
idx_new = slice(9, 13)
idx_palm = slice(13, 15)

# --- 2. Модель через Start/End ---

# Начальные параметры (подобраны под оптимум)
# Оптимум был: x0=34.2, k=0.135.
# Width = 6 / 0.135 ≈ 44.4
# Start = 34.2 - 22.2 = 12.0
# End = 34.2 + 22.2 = 56.4
init_start = 12.0
init_end = 56.5
init_l_max = 96.8
init_cap = 99.2
init_sat = 12.5

def sigmoid_range(x, l_max, start, end):
    """
    Сигмоида, определенная через начало и конец подъема.
    """
    # Защита от деления на ноль
    if end == start: end += 0.01
    
    width = end - start
    midpoint = (start + end) / 2
    k = 6.0 / width  # Коэффициент 6 обеспечивает диапазон от ~5% до ~95%
    
    arg = -k * (x - midpoint)
    arg = np.clip(arg, -100, 100)
    return l_max / (1.0 + np.exp(arg))

def model_O_range(x_oleic, l_max, start, end, cap, sat_fat):
    l_equiv = (100 - sat_fat) - x_oleic
    l_occ = sigmoid_range(l_equiv, l_max, start, end)
    return cap - l_occ

# Диапазоны
xr_L = np.linspace(0, 100, 300)
xr_O = np.linspace(0, 100, 300)

# --- 3. Графики ---

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
plt.subplots_adjust(bottom=0.35)

# === График L ===
ax1.scatter(L_total[idx_old], L_sn2[idx_old], c='blue', label='Standard')
ax1.scatter(L_total[idx_new], L_sn2[idx_new], c='navy', marker='s', label='Hi-Oleic/Lin')
ax1.scatter(L_total[idx_palm], L_sn2[idx_palm], c='green', marker='^', label='Hi-Palmitic')

line_L, = ax1.plot(xr_L, sigmoid_range(xr_L, init_l_max, init_start, init_end), 'r-', lw=3)

# Линии визуализации параметров
vline_start = ax1.axvline(init_start, color='green', ls=':', lw=2, label='Start (Rise)')
vline_end = ax1.axvline(init_end, color='green', ls=':', lw=2, label='End (Plateau)')
hline_max = ax1.axhline(init_l_max, color='gray', ls='--', alpha=0.5, label='Max L')

ax1.set_title('L: Активная зона фермента')
ax1.set_xlabel('Total L (%)')
ax1.set_ylabel('SN-2 L (%)')
ax1.set_xlim(0, 100)
ax1.set_ylim(-5, 105)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='lower right')

# === График O ===
ax2.scatter(O_total[idx_old], O_sn2[idx_old], c='orange', label='Standard')
ax2.scatter(O_total[idx_new], O_sn2[idx_new], c='darkred', marker='s', label='Hi-Oleic/Lin')
ax2.scatter(O_total[idx_palm], O_sn2[idx_palm], c='green', marker='^', label='Hi-Palmitic')

line_O, = ax2.plot(xr_O, model_O_range(xr_O, init_l_max, init_start, init_end, init_cap, init_sat), 'purple', lw=3)
hline_cap = ax2.axhline(init_cap, color='purple', ls='--', alpha=0.3, label='Capacity')

ax2.set_title('O: Заполнение остатка')
ax2.set_xlabel('Total O (%)')
ax2.set_ylabel('SN-2 O (%)')
ax2.set_xlim(0, 100)
ax2.set_ylim(-5, 105)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='lower right')

# --- 4. Ползунки ---

ax_start = plt.axes([0.15, 0.20, 0.7, 0.03])
ax_end   = plt.axes([0.15, 0.16, 0.7, 0.03])
ax_lmax  = plt.axes([0.15, 0.12, 0.7, 0.03])
ax_cap   = plt.axes([0.15, 0.08, 0.7, 0.03])
ax_sat   = plt.axes([0.15, 0.04, 0.7, 0.03])

s_start = Slider(ax_start, 'Start Point (Rise)', 0.0, 50.0, valinit=init_start)
s_end   = Slider(ax_end,   'End Point (Plateau)', 40.0, 90.0, valinit=init_end)
s_lmax  = Slider(ax_lmax,  'L Max (Plateau)', 80.0, 100.0, valinit=init_l_max)
s_cap   = Slider(ax_cap,   'SN-2 Capacity', 90.0, 100.0, valinit=init_cap)
s_sat   = Slider(ax_sat,   'Sat Fat Offset', 0.0, 30.0, valinit=init_sat)

def update(val):
    st = s_start.val
    en = s_end.val
    lm = s_lmax.val
    cap = s_cap.val
    sf = s_sat.val
    
    # Обновляем кривые
    line_L.set_ydata(sigmoid_range(xr_L, lm, st, en))
    line_O.set_ydata(model_O_range(xr_O, lm, st, en, cap, sf))
    
    # Обновляем вспомогательные линии
    vline_start.set_xdata([st, st])
    vline_end.set_xdata([en, en])
    hline_max.set_ydata([lm, lm])
    hline_cap.set_ydata([cap, cap])
    
    fig.canvas.draw_idle()

s_start.on_changed(update)
s_end.on_changed(update)
s_lmax.on_changed(update)
s_cap.on_changed(update)
s_sat.on_changed(update)

plt.show()