# -*- coding: utf-8 -*-
"""
Plot of SN‑2 vs Total L and SN‑2 vs Total O.
Each data set now has its own colour + marker.
All sliders control the “rise” (start) and “plateau” points,
the maximal L, the O‑capacity and the saturated‑fat offset.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# ----------------------------------------------------------------------
# 1. Исходные данные
# ----------------------------------------------------------------------
L_total = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0, 58.7,
                    76.0, 2.1, 2.0, 46.8, 3.5])
L_sn2   = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1, 65.7,
                    76.9, 1.4, 0.6, 67.8, 2.8])

O_total = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1, 27.8,
                    13.3, 91.5, 79.1, 17.1, 59.8])
O_sn2   = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3, 31.5,
                    18.9, 96.6, 95.9, 24.9, 93.4])

# ----------------------------------------------------------------------
# 2. Группы (каждая получает собственный маркер)
# ----------------------------------------------------------------------
idx_std  = slice(0, 9)          # 0‑8 – стандартные сорта (о‑эли)
idx_hiOL = slice(9, 12)         # 9‑11 – “Hi‑Oleic/Lin”
idx_hiP  = slice(12, 15)        # 12‑14 – “Hi‑Palmitic”

# ----------------------------------------------------------------------
# 3. Словарь стилей маркеров
# ----------------------------------------------------------------------
marker_style = {
    "Standard":    {"color": "tab:blue",   "marker": "o",   "label": "Standard"},
    "Hi‑Oleic/Lin":{"color": "tab:red",   "marker": "s",   "label": "Hi‑Oleic/Lin"},
    "Hi‑Palmitic": {"color": "tab:green", "marker": "^",   "label": "Hi‑Palmitic"},
}

# Общие параметры (alpha = отображение, s = size маркеров)
SCATTER_PARAMS = {
    "alpha": 0.8,
    "s": 8,               # площадь маркера в points²
}

# ----------------------------------------------------------------------
# 4. Модель через «начальную» и «конечную» точки
# ----------------------------------------------------------------------
def sigmoid_range(x, l_max, start, end, low=0.05, high=0.95):
    """
    Сигмоида от start (low %) до end (high %).
    low/high – пороги, которые задают коэффициент k.
    """
    if end == start:  # защита от деления на ноль
        end += 0.01

    width = end - start
    midpoint = (start + end) / 2.0
    k = np.log(high / low) / width   # ≈ 6 / width при low=0.05, high=0.95

    arg = -k * (x - midpoint)
    arg = np.clip(arg, -100, 100)      # отрезаем огромные аргументы

    return l_max / (1.0 + np.exp(arg))


def model_O_range(x_O, l_max, start, end,
                  cap, sat_fat, low=0.05, high=0.95):
    """
    Комплемент‑модель для O‑axis.
    L_eq – SN‑2‑эквивалент, полученный через sigmoid_range.
    """
    l_equiv = sigmoid_range((100.0 - sat_fat) - x_O,
                            l_max, start, end,
                            low, high)
    return cap - l_equiv


# ----------------------------------------------------------------------
# 5. Диапазоны осей
# ----------------------------------------------------------------------
xr_L = np.linspace(0, 100, 300)
xr_O = np.linspace(0, 100, 300)

# ----------------------------------------------------------------------
# 6. Отрисовка
# ----------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
plt.subplots_adjust(bottom=0.30, hspace=0.05)

# --------------------------------------------------------------
# 6.1. График L (Total L % → SN‑2 L %)
# --------------------------------------------------------------
# Стандартные (0‑8)
ax1.scatter(L_total[idx_std], L_sn2[idx_std],
            marker=marker_style["Standard"]["marker"],
            color=marker_style["Standard"]["color"],
            label=marker_style["Standard"]["label"],
            s=SCATTER_PARAMS["s"],               # площадь маркера
            alpha=SCATTER_PARAMS["alpha"])

# Hi‑Oleic/Lin (9‑11)
ax1.scatter(L_total[idx_hiOL], L_sn2[idx_hiOL],
            marker=marker_style["Hi‑Oleic/Lin"]["marker"],
            color=marker_style["Hi‑Oleic/Lin"]["color"],
            label=marker_style["Hi‑Oleic/Lin"]["label"],
            s=SCATTER_PARAMS["s"],
            alpha=SCATTER_PARAMS["alpha"])

# Hi‑Palmitic (12‑14)
ax1.scatter(L_total[idx_hiP], L_sn2[idx_hiP],
            marker=marker_style["Hi‑Palmitic"]["marker"],
            color=marker_style["Hi‑Palmitic"]["color"],
            label=marker_style["Hi‑Palmitic"]["label"],
            s=SCATTER_PARAMS["s"],
            alpha=SCATTER_PARAMS["alpha"])

# Общая сигмоида‑модель
l_max = 96.8
l_start = 12.0
l_end   = 56.5

line_L, = ax1.plot(xr_L,
                   sigmoid_range(xr_L, l_max, l_start, l_end),
                   color='tab:orange', lw=2.5,
                   label='Model L (sigmoid)')

# Вспомогательные вертикальные/горизонтальные линии
vline_start = ax1.axvline(l_start, ls=':', color='tab:gray', lw=2,
                         label='Start (rise)')
vline_end   = ax1.axvline(l_end,   ls=':', color='tab:gray', lw=2,
                         label='End (plateau)')
hline_max   = ax1.axhline(l_max,   ls='--', color='tab:gray', lw=1,
                         label='L_max (plateau)')

# Форматирование
ax1.set_title('L % vs SN‑2 %')
ax1.set_xlabel('Total L (%)')
ax1.set_ylabel('SN‑2 L (%)')
ax1.set_xlim(0, 100)
ax1.set_ylim(-5, 105)
ax1.grid(True, alpha=0.3)

ax1.legend(loc='lower right')

# --------------------------------------------------------------
# 6.2. График O (Total O % → SN‑2 O %)
# --------------------------------------------------------------
# Стандартные
ax2.scatter(O_total[idx_std], O_sn2[idx_std],
            marker=marker_style["Standard"]["marker"],
            color=marker_style["Standard"]["color"],
            label=marker_style["Standard"]["label"],
            s=SCATTER_PARAMS["s"],
            alpha=SCATTER_PARAMS["alpha"])

# Hi‑Oleic/Lin
ax2.scatter(O_total[idx_hiOL], O_sn2[idx_hiOL],
            marker=marker_style["Hi‑Oleic/Lin"]["marker"],
            color=marker_style["Hi‑Oleic/Lin"]["color"],
            label=marker_style["Hi‑Oleic/Lin"]["label"],
            s=SCATTER_PARAMS["s"],
            alpha=SCATTER_PARAMS["alpha"])

# Hi‑Palmitic
ax2.scatter(O_total[idx_hiP], O_sn2[idx_hiP],
            marker=marker_style["Hi‑Palmitic"]["marker"],
            color=marker_style["Hi‑Palmitic"]["color"],
            label=marker_style["Hi‑Palmitic"]["label"],
            s=SCATTER_PARAMS["s"],
            alpha=SCATTER_PARAMS["alpha"])

# Общая модель O‑axis
cap_O   = 99.2
sat_fat = 12.5   # % жирных кислот, которые не могут участвовать в SN‑2

line_O, = ax2.plot(xr_O,
                   model_O_range(xr_O, l_max, l_start, l_end,
                                cap=cap_O, sat_fat=sat_fat),
                   color='tab:purple', lw=2.5,
                   label='Model O (complement)')

hline_cap = ax2.axhline(cap_O, ls='--', color='tab:purple',
                       alpha=0.3, label='O_capacity')

# Форматирование
ax2.set_title('O % vs SN‑2 %')
ax2.set_xlabel('Total O (%)')
ax2.set_ylabel('SN‑2 O (%)')
ax2.set_xlim(0, 100)
ax2.set_ylim(-5, 105)
ax2.grid(True, alpha=0.3)

ax2.legend(loc='lower right')

# ----------------------------------------------------------------------
# 7. Ползунки – управление параметрами модели
# ----------------------------------------------------------------------
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

    # Обновляем линии модели
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

# ----------------------------------------------------------------------
# 8. Отображение
# ----------------------------------------------------------------------
plt.show()