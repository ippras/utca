# -*- coding: utf-8 -*-
"""
SN‑2 vs Total L и SN‑2 vs Total O.
Каждая точка помечена своим ID (2233, 2699, …).
Групповые маркеры (цвет + символ) сохраняются.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# --------------------------------------------------------------
# 1️⃣ Данные
# --------------------------------------------------------------
L_total = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8,
                    64.0, 58.7, 76.0, 2.1, 2.0, 46.8, 3.5])
L_sn2   = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6,
                    84.1, 65.7, 76.9, 1.4, 0.6, 67.8, 2.8])

O_total = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7,
                    24.1, 27.8, 13.3, 91.5, 79.1, 17.1, 59.8])
O_sn2   = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9,
                    14.3, 31.5, 18.9, 96.6, 95.9, 24.9, 93.4])

# --------------------------------------------------------------
# 2️⃣ ID‑таблица (можно добавить любые имена, которые вам нужны)
# --------------------------------------------------------------
id_L = np.array([
    '2233','2699','2776','3110','3384','3599','3675','3714',
    'Buzlu','Palm1','Palm2','Palm3'
])
id_O = np.array([
    '2233','2699','2776','3110','3384','3599','3675','3714',
    'Buzlu','Palm1','Palm2','Palm3'
])

# --------------------------------------------------------------
# 3️⃣ Группы – обычные массивы индексов (не slice!)
# --------------------------------------------------------------
idx_std  = np.arange(0, 9)          # 0‑8 → Standard (о‑эли)
idx_hiOL = np.arange(9, 12)         # 9‑11 → Hi‑Oleic/Lin
idx_hiP  = np.arange(12, 15)        # 12‑14 → Hi‑Palmitic

# --------------------------------------------------------------
# 4️⃣ Стили маркеров
# --------------------------------------------------------------
marker_style = {
    "Standard":     {"color": "tab:blue",   "marker": "o"},
    "Hi‑Oleic/Lin": {"color": "tab:red",   "marker": "s"},
    "Hi‑Palmitic":  {"color": "tab:green", "marker": "^"},
}
SCATTER_PARAMS = {"s": 8, "alpha": 0.85}   # площадь маркера (points²)

# --------------------------------------------------------------
# 5️⃣ Модель (сигмоида через start‑point и end‑point)
# --------------------------------------------------------------
def sigmoid_range(x, l_max, start, end, low=0.05, high=0.95):
    """Сигмоида, достигающая low‑% в start и high‑% в end."""
    if end == start:
        end += 0.01
    width  = end - start
    midpoint = (start + end) / 2.0
    k = np.log(high / low) / width          # ≈ 6 / width при low=5 %, high=95 %
    arg = -k * (x - midpoint)
    arg = np.clip(arg, -100, 100)
    return l_max / (1.0 + np.exp(arg))


def model_O_range(x_O, l_max, start, end,
                  cap, sat_fat, low=0.05, high=0.95):
    """Комплемент‑модель для O‑axis."""
    l_equiv = sigmoid_range((100.0 - sat_fat) - x_O,
                            l_max, start, end,
                            low, high)
    return cap - l_equiv

# --------------------------------------------------------------
# 6️⃣ Диапазоны осей
# --------------------------------------------------------------
xr_L = np.linspace(0, 100, 300)
xr_O = np.linspace(0, 100, 300)

# --------------------------------------------------------------
# 7️⃣ Главные графики
# --------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
plt.subplots_adjust(bottom=0.30, hspace=0.05)

# ───── 7.1 L – SN‑2 % vs Total L % ─────
ax1.scatter(L_total[idx_std], L_sn2[idx_std],
            marker=marker_style["Standard"]["marker"],
            color=marker_style["Standard"]["color"],
            s=SCATTER_PARAMS["s"], alpha=SCATTER_PARAMS["alpha"],
            label="Standard")

ax1.scatter(L_total[idx_hiOL], L_sn2[idx_hiOL],
            marker=marker_style["Hi‑Oleic/Lin"]["marker"],
            color=marker_style["Hi‑Oleic/Lin"]["color"],
            s=SCATTER_PARAMS["s"], alpha=SCATTER_PARAMS["alpha"],
            label="Hi‑Oleic/Lin")

ax1.scatter(L_total[idx_hiP], L_sn2[idx_hiP],
            marker=marker_style["Hi‑Palmitic"]["marker"],
            color=marker_style["Hi‑Palmitic"]["color"],
            s=SCATTER_PARAMS["s"], alpha=SCATTER_PARAMS["alpha"],
            label="Hi‑Palmitic")

# Подписи ID (annotate без стрелки)
for i in idx_std:
    ax1.annotate(id_L[i],
                 xy=(L_total[i], L_sn2[i]),          # координаты маркера
                 xytext=(0.5, 0.2),                  # смещение 0.5 % по X, 0.2 % по Y
                 textcoords='offset points',
                 ha='left', va='bottom',
                 color='k', fontsize=7,
                 alpha=0.7,
                 # Чтобы не рисовать стрелку, просто не задаём arrowprops
                 )

for i in idx_hiOL:
    ax1.annotate(id_L[i],
                 xy=(L_total[i], L_sn2[i]),
                 xytext=(0.5, 0.2),
                 textcoords='offset points',
                 ha='left', va='bottom',
                 color='k', fontsize=7,
                 alpha=0.7)

for i in idx_hiP:
    ax1.annotate(id_L[i],
                 xy=(L_total[i], L_sn2[i]),
                 xytext=(0.5, 0.2),
                 textcoords='offset points',
                 ha='left', va='bottom',
                 color='k', fontsize=7,
                 alpha=0.7)

# Общая модель (сигмоида)
l_max, l_start, l_end = 96.8, 12.0, 56.5
line_L, = ax1.plot(xr_L,
                   sigmoid_range(xr_L, l_max, l_start, l_end),
                   color='tab:orange', lw=2.5,
                   label='Model L (sigmoid)')

# Вспомогательные линии для параметров
vline_start = ax1.axvline(l_start, ls=':', color='tab:gray', lw=2,
                         label='Start (rise)')
vline_end   = ax1.axvline(l_end,   ls=':', color='tab:gray', lw=2,
                         label='End (plateau)')
hline_max   = ax1.axhline(l_max,   ls='--', color='tab:gray', lw=1,
                         label='L_max (plateau)')

ax1.set_title('L % vs SN‑2 %')
ax1.set_xlabel('Total L (%)')
ax1.set_ylabel('SN‑2 L (%)')
ax1.set_xlim(0, 100)
ax1.set_ylim(-5, 105)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='lower right')

# ───── 7.2 O – SN‑2 % vs Total O % ─────
ax2.scatter(O_total[idx_std], O_sn2[idx_std],
            marker=marker_style["Standard"]["marker"],
            color=marker_style["Standard"]["color"],
            s=SCATTER_PARAMS["s"], alpha=SCATTER_PARAMS["alpha"],
            label="Standard")

ax2.scatter(O_total[idx_hiOL], O_sn2[idx_hiOL],
            marker=marker_style["Hi‑Oleic/Lin"]["marker"],
            color=marker_style["Hi‑Oleic/Lin"]["color"],
            s=SCATTER_PARAMS["s"], alpha=SCATTER_PARAMS["alpha"],
            label="Hi‑Oleic/Lin")

ax2.scatter(O_total[idx_hiP], O_sn2[idx_hiP],
            marker=marker_style["Hi‑Palmitic"]["marker"],
            color=marker_style["Hi‑Palmitic"]["color"],
            s=SCATTER_PARAMS["s"], alpha=SCATTER_PARAMS["alpha"],
            label="Hi‑Palmitic")

# Подписи ID на O‑графике
for i in idx_std:
    ax2.annotate(id_O[i],
                 xy=(O_total[i], O_sn2[i]),
                 xytext=(0.5, 0.2),
                 textcoords='offset points',
                 ha='left', va='bottom',
                 color='k', fontsize=7,
                 alpha=0.7)

for i in idx_hiOL:
    ax2.annotate(id_O[i],
                 xy=(O_total[i], O_sn2[i]),
                 xytext=(0.5, 0.2),
                 textcoords='offset points',
                 ha='left', va='bottom',
                 color='k', fontsize=7,
                 alpha=0.7)

for i in idx_hiP:
    ax2.annotate(id_O[i],
                 xy=(O_total[i], O_sn2[i]),
                 xytext=(0.5, 0.2),
                 textcoords='offset points',
                 ha='left', va='bottom',
                 color='k', fontsize=7,
                 alpha=0.7)

# Общая модель O‑axis (комплемент)
cap_O   = 99.2
sat_fat = 12.5   # % жирных кислот, которые «зарезервированы» под saturated‑fat

line_O, = ax2.plot(xr_O,
                   model_O_range(xr_O, l_max, l_start, l_end,
                                cap=cap_O, sat_fat=sat_fat),
                   color='tab:purple', lw=2.5,
                   label='Model O (complement)')

hline_cap = ax2.axhline(cap_O, ls='--', color='tab:purple',
                       alpha=0.3, label='O_capacity')

ax2.set_title('O % vs SN‑2 %')
ax2.set_xlabel('Total O (%)')
ax2.set_ylabel('SN‑2 O (%)')
ax2.set_xlim(0, 100)
ax2.set_ylim(-5, 105)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='lower right')

# --------------------------------------------------------------
# 8️⃣ Ползунки – управление параметрами модели
# --------------------------------------------------------------
ax_start = plt.axes([0.15, 0.20, 0.70, 0.03])   # left, bottom, width, height
ax_end   = plt.axes([0.15, 0.16, 0.70, 0.03])
ax_lmax  = plt.axes([0.15, 0.12, 0.70, 0.03])
ax_cap   = plt.axes([0.15, 0.08, 0.70, 0.03])
ax_sat   = plt.axes([0.15, 0.04, 0.70, 0.03])

s_start = Slider(ax_start, 'Start (Rise)', 0, 50, valinit=l_start, valstep=0.1)
s_end   = Slider(ax_end,   'End   (Plateau)', 40, 90, valinit=l_end,   valstep=0.1)
s_lmax  = Slider(ax_lmax,  'L_max (Plateau)', 80, 100, valinit=l_max,  valstep=0.5)
s_cap   = Slider(ax_cap,   'O_capacity', 90, 100, valinit=cap_O, valstep=0.5)
s_sat   = Slider(ax_sat,   'Sat_Fat offset', 0, 30, valinit=sat_fat, valstep=0.1)

def update(val):
    st = s_start.val
    en = s_end.val
    lm = s_lmax.val
    cap = s_cap.val
    sf = s_sat.val

    # Обновляем кривые модели
    line_L.set_ydata(sigmoid_range(xr_L, lm, st, en))
    line_O.set_ydata(model_O_range(xr_O, lm, st, en, cap, sf))

    # Обновляем вспомогательные вертикальные/горизонтальные линии
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

# --------------------------------------------------------------
# 9️⃣ Вывод
# --------------------------------------------------------------
plt.show()