import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
from scipy.optimize import curve_fit

# --- 1. Данные ---
samples = ['2233', '2699', '2776', '3110', '3384', '3599', '3675', '3714', 'Buzuluk', 'Commodity', 'High linoleic', 'High oleic', 'High palmitic, high linoleic', 'High palmitic, high oleic', 'High stearic, high oleic']
L_sn123_all = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0, 58.7, 76.0, 2.1, 46.8, 3.5, 2.0])
L_2_all     = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1, 65.7, 76.9, 1.4, 67.8, 2.8, 0.6])
O_sn123_all = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1, 27.8, 13.3, 91.5, 17.1, 59.8, 79.1])
O_2_all     = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3, 31.5, 18.9, 96.6, 24.9, 93.4, 95.9])

n_orig = 9
L_sn123_orig, L_2_orig = L_sn123_all[:n_orig], L_2_all[:n_orig]
L_sn123_resk, L_2_resk = L_sn123_all[n_orig:], L_2_all[n_orig:]

with np.errstate(divide='ignore', invalid='ignore'):
    EF_L_all = L_2_all / L_sn123_all
    valid_idx_L = np.isfinite(EF_L_all)
    EF_O_all = O_2_all / O_sn123_all
    valid_idx_O = np.isfinite(EF_O_all)

# --- 2. Модели ---
def smooth_haldane_ef(x, A, B, C):
    x_safe = np.maximum(x, 1e-6)
    return (A * x_safe) / (B + x_safe + (x_safe**1.5 / C))

def michaelis_ef_growing(x, A, B):
    return (A * x) / (B + x)

def michaelis_ef_fading(x, A, B):
    return A / (B + x)

# --- 3. ПОЛНЫЙ АВТО-ПОДБОР ---
# 3.1 Haldane для Linoleic
try:
    popt_L, _ = curve_fit(smooth_haldane_ef, L_sn123_all[valid_idx_L], EF_L_all[valid_idx_L], 
                          p0=[100, 20, 20], bounds=([1, 1, 1], [2000, 500, 500]))
    best_A_L, best_B_L, best_C_L = popt_L
except: best_A_L, best_B_L, best_C_L = 100, 20, 20

# 3.2 Michaelis-Menten Growing для Linoleic
try:
    popt_L_mm, _ = curve_fit(michaelis_ef_growing, L_sn123_all[valid_idx_L], EF_L_all[valid_idx_L], 
                             p0=[2.0, 10.0], bounds=([0.1, 0.1], [10.0, 300.0]))
    best_A_L_mm, best_B_L_mm = popt_L_mm
except: best_A_L_mm, best_B_L_mm = 2.0, 10.0

# 3.3 Michaelis-Menten Fading для Oleic
try:
    popt_O, _ = curve_fit(michaelis_ef_fading, O_sn123_all[valid_idx_O], EF_O_all[valid_idx_O], 
                          p0=[150, 50], bounds=([1, 1], [1000, 500]))
    best_A_O, best_B_O = popt_O
except: best_A_O, best_B_O = 150, 50

# --- 4. Графики ---
x_range = np.linspace(0.1, 100, 400)
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
plt.subplots_adjust(bottom=0.35, hspace=0.4, wspace=0.25)
(ax_L_abs, ax_O_abs), (ax_L_ef, ax_O_ef) = axs

# LIN (Левая колонка)
ax_L_abs.scatter(L_sn123_orig, L_2_orig, c='blue', label='Original')
ax_L_abs.scatter(L_sn123_resk, L_2_resk, c='green', marker='s', label='Reske')
line_L_abs, = ax_L_abs.plot(x_range, x_range * smooth_haldane_ef(x_range, best_A_L, best_B_L, best_C_L), 'r-', label='Haldane')
line_L_abs_mm, = ax_L_abs.plot(x_range, x_range * michaelis_ef_growing(x_range, best_A_L_mm, best_B_L_mm), 'g--', alpha=0.7, label='M-M')
ax_L_abs.set_title('Linoleic: sn-2 (Abs)')
ax_L_abs.legend()

ax_L_ef.scatter(L_sn123_orig, EF_L_all[:n_orig], c='blue')
ax_L_ef.scatter(L_sn123_resk, EF_L_all[n_orig:], c='green', marker='s')
line_L_ef, = ax_L_ef.plot(x_range, smooth_haldane_ef(x_range, best_A_L, best_B_L, best_C_L), 'r-')
line_L_ef_mm, = ax_L_ef.plot(x_range, michaelis_ef_growing(x_range, best_A_L_mm, best_B_L_mm), 'g--', alpha=0.7)
ax_L_ef.set_ylim(0, 2.5)
ax_L_ef.set_title('Linoleic: EF')

# OLE (Правая колонка)
ax_O_abs.scatter(O_sn123_all[:n_orig], O_2_all[:n_orig], c='orange')
ax_O_abs.scatter(O_sn123_all[n_orig:], O_2_all[n_orig:], c='green', marker='s')
line_O_abs, = ax_O_abs.plot(x_range, x_range * michaelis_ef_fading(x_range, best_A_O, best_B_O), 'purple')
ax_O_abs.set_title('Oleic: sn-2 (Abs)')

ax_O_ef.scatter(O_sn123_all[:n_orig], EF_O_all[:n_orig], c='orange')
ax_O_ef.scatter(O_sn123_all[n_orig:], EF_O_all[n_orig:], c='green', marker='s')
line_O_ef, = ax_O_ef.plot(x_range, michaelis_ef_fading(x_range, best_A_O, best_B_O), 'purple')
ax_O_ef.set_ylim(0, 3.0)
ax_O_ef.set_title('Oleic: EF')

# --- 5. Виджеты ---
axcolor = 'lightgoldenrodyellow'
s_AL = Slider(plt.axes([0.15, 0.22, 0.3, 0.025]), 'Lin Hald A', 10.0, 500.0, valinit=best_A_L)
s_BL = Slider(plt.axes([0.15, 0.18, 0.3, 0.025]), 'Lin Hald B', 1.0, 200.0, valinit=best_B_L)
s_CL = Slider(plt.axes([0.15, 0.14, 0.3, 0.025]), 'Lin Hald C', 0.1, 100.0, valinit=best_C_L)

s_AL_MM = Slider(plt.axes([0.15, 0.08, 0.3, 0.025]), 'Lin MM A', 0.1, 10.0, valinit=best_A_L_mm, color='green')
s_BL_MM = Slider(plt.axes([0.15, 0.04, 0.3, 0.025]), 'Lin MM B', 0.1, 200.0, valinit=best_B_L_mm, color='green')

s_AO = Slider(plt.axes([0.60, 0.18, 0.3, 0.025]), 'Ole MM A', 10.0, 500.0, valinit=best_A_O, color='salmon')
s_BO = Slider(plt.axes([0.60, 0.14, 0.3, 0.025]), 'Ole MM B', 1.0, 300.0, valinit=best_B_O, color='salmon')

def update(val):
    line_L_ef.set_ydata(smooth_haldane_ef(x_range, s_AL.val, s_BL.val, s_CL.val))
    line_L_abs.set_ydata(x_range * smooth_haldane_ef(x_range, s_AL.val, s_BL.val, s_CL.val))
    line_L_ef_mm.set_ydata(michaelis_ef_growing(x_range, s_AL_MM.val, s_BL_MM.val))
    line_L_abs_mm.set_ydata(x_range * michaelis_ef_growing(x_range, s_AL_MM.val, s_BL_MM.val))
    line_O_ef.set_ydata(michaelis_ef_fading(x_range, s_AO.val, s_BO.val))
    line_O_abs.set_ydata(x_range * michaelis_ef_fading(x_range, s_AO.val, s_BO.val))
    fig.canvas.draw_idle()

for s in [s_AL, s_BL, s_CL, s_AL_MM, s_BL_MM, s_AO, s_BO]: s.on_changed(update)

# Кнопка сброса к результатам Авто-подбора
resetax = plt.axes([0.45, 0.01, 0.1, 0.03])
button = Button(resetax, 'Auto-Fit Reset', color=axcolor)

def reset(event):
    s_AL.set_val(best_A_L); s_BL.set_val(best_B_L); s_CL.set_val(best_C_L)
    s_AL_MM.set_val(best_A_L_mm); s_BL_MM.set_val(best_B_L_mm)
    s_AO.set_val(best_A_O); s_BO.set_val(best_B_O)
button.on_clicked(reset)

plt.show()
