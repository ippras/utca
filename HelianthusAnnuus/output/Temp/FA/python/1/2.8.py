import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.optimize import curve_fit

# --- 1. Данные ---
samples = ['2233', '2699', '2776', '3110', '3384', '3599', '3675', '3714', 'Buzuluk', 
           'Commodity', 'High linoleic', 'High oleic', 'High palmitic, high linoleic', 
           'High palmitic, high oleic', 'High stearic, high oleic']

L_sn123_all = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0, 58.7, 76.0, 2.1, 46.8, 3.5, 2.0])
L_2_all     = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1, 65.7, 76.9, 1.4, 67.8, 2.8, 0.6])
O_sn123_all = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1, 27.8, 13.3, 91.5, 17.1, 59.8, 79.1])
O_2_all     = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3, 31.5, 18.9, 96.6, 24.9, 93.4, 95.9])

n_orig = 9
with np.errstate(divide='ignore', invalid='ignore'):
    EF_L_all = L_2_all / L_sn123_all
    EF_O_all = O_2_all / O_sn123_all
    valid_idx_L = np.isfinite(EF_L_all)
    valid_idx_O = np.isfinite(EF_O_all)

# --- 2. Модели ---
def smooth_haldane_ef(x, A, B, C):
    x_safe = np.maximum(x, 1e-6)
    return (A * x_safe) / (B + x_safe + (x_safe**1.5 / C))

def michaelis_ef_growing(x, A, B): return (A * x) / (B + x)
def michaelis_ef_fading(x, A, B): return A / (B + x)

# --- 3. Авто-подбор ---
try:
    popt_L, _ = curve_fit(smooth_haldane_ef, L_sn123_all[valid_idx_L], EF_L_all[valid_idx_L], p0=[100, 20, 20])
    best_A_L, best_B_L, best_C_L = popt_L
except: best_A_L, best_B_L, best_C_L = 100, 20, 20

try:
    popt_L_mm, _ = curve_fit(michaelis_ef_growing, L_sn123_all[valid_idx_L], EF_L_all[valid_idx_L], p0=[2.0, 10.0])
    best_A_L_mm, best_B_L_mm = popt_L_mm
except: best_A_L_mm, best_B_L_mm = 2.0, 10.0

try:
    popt_O, _ = curve_fit(michaelis_ef_fading, O_sn123_all[valid_idx_O], EF_O_all[valid_idx_O], p0=[150, 50])
    best_A_O, best_B_O = popt_O
except: best_A_O, best_B_O = 150, 50

# --- 4. Графики ---
x_range = np.linspace(0.1, 100, 400)
fig, axs = plt.subplots(2, 2, figsize=(15, 11))
plt.subplots_adjust(bottom=0.38, hspace=0.35, wspace=0.2)
(ax_L_abs, ax_O_abs), (ax_L_ef, ax_O_ef) = axs

def create_labels(ax, x, y, labels):
    return [ax.text(x[i], y[i], labels[i], fontsize=7, alpha=0.8, visible=False, color='black', fontweight='bold') for i in range(len(labels))]

texts_list = [
    create_labels(ax_L_abs, L_sn123_all, L_2_all, samples),
    create_labels(ax_O_abs, O_sn123_all, O_2_all, samples),
    create_labels(ax_L_ef, L_sn123_all, EF_L_all, samples),
    create_labels(ax_O_ef, O_sn123_all, EF_O_all, samples)
]

# LIN
ax_L_abs.scatter(L_sn123_all[:n_orig], L_2_all[:n_orig], c='blue')
ax_L_abs.scatter(L_sn123_all[n_orig:], L_2_all[n_orig:], c='green', marker='s')
line_L_abs, = ax_L_abs.plot(x_range, x_range * smooth_haldane_ef(x_range, best_A_L, best_B_L, best_C_L), 'r-', label='Haldane')
line_L_abs_mm, = ax_L_abs.plot(x_range, x_range * michaelis_ef_growing(x_range, best_A_L_mm, best_B_L_mm), 'g--', alpha=0.6, label='M-M')
ax_L_abs.set_title('Linoleic: sn-2 (Abs)')

ax_L_ef.scatter(L_sn123_all[:n_orig], EF_L_all[:n_orig], c='blue')
ax_L_ef.scatter(L_sn123_all[n_orig:], EF_L_all[n_orig:], c='green', marker='s')
line_L_ef, = ax_L_ef.plot(x_range, smooth_haldane_ef(x_range, best_A_L, best_B_L, best_C_L), 'r-')
line_L_ef_mm, = ax_L_ef.plot(x_range, michaelis_ef_growing(x_range, best_A_L_mm, best_B_L_mm), 'g--', alpha=0.6)
ax_L_ef.set_ylim(0, 2.5)

# OLE
ax_O_abs.scatter(O_sn123_all[:n_orig], O_2_all[:n_orig], c='orange')
ax_O_abs.scatter(O_sn123_all[n_orig:], O_2_all[n_orig:], c='green', marker='s')
line_O_abs, = ax_O_abs.plot(x_range, x_range * michaelis_ef_fading(x_range, best_A_O, best_B_O), 'purple')

ax_O_ef.scatter(O_sn123_all[:n_orig], EF_O_all[:n_orig], c='orange')
ax_O_ef.scatter(O_sn123_all[n_orig:], EF_O_all[n_orig:], c='green', marker='s')
line_O_ef, = ax_O_ef.plot(x_range, michaelis_ef_fading(x_range, best_A_O, best_B_O), 'purple')
ax_O_ef.set_ylim(0, 3.0)

# --- 5. Виджеты ---
axcolor = 'lightgoldenrodyellow'
# Слайдеры
s_AL = Slider(plt.axes([0.15, 0.28, 0.3, 0.02]), 'Lin Hald A', 10, 500, valinit=best_A_L)
s_BL = Slider(plt.axes([0.15, 0.25, 0.3, 0.02]), 'Lin Hald B', 1, 200, valinit=best_B_L)
s_CL = Slider(plt.axes([0.15, 0.22, 0.3, 0.02]), 'Lin Hald C', 0.1, 100, valinit=best_C_L)
s_AL_MM = Slider(plt.axes([0.15, 0.16, 0.3, 0.02]), 'Lin MM A', 0.1, 10, valinit=best_A_L_mm, color='green')
s_BL_MM = Slider(plt.axes([0.15, 0.13, 0.3, 0.02]), 'Lin MM B', 0.1, 200, valinit=best_B_L_mm, color='green')
s_AO = Slider(plt.axes([0.60, 0.25, 0.3, 0.02]), 'Ole MM A', 10, 500, valinit=best_A_O, color='salmon')
s_BO = Slider(plt.axes([0.60, 0.22, 0.3, 0.02]), 'Ole MM B', 1, 300, valinit=best_B_O, color='salmon')

# Чекбоксы (внизу в ряд)
rax = plt.axes([0.15, 0.05, 0.7, 0.04], frameon=False)
check = CheckButtons(rax, ('L-Abs ID', 'O-Abs ID', 'L-EF ID', 'O-EF ID'), (False, False, False, False))

# Кнопка Автофита (в самом низу)
resetax = plt.axes([0.45, 0.01, 0.1, 0.03])
button_res = Button(resetax, 'AUTO-FIT', color=axcolor)

def toggle_labels(label):
    idx = {'L-Abs ID':0, 'O-Abs ID':1, 'L-EF ID':2, 'O-EF ID':3}[label]
    for t in texts_list[idx]:
        t.set_visible(not t.get_visible())
    fig.canvas.draw_idle()

def update(val):
    line_L_ef.set_ydata(smooth_haldane_ef(x_range, s_AL.val, s_BL.val, s_CL.val))
    line_L_abs.set_ydata(x_range * smooth_haldane_ef(x_range, s_AL.val, s_BL.val, s_CL.val))
    line_L_ef_mm.set_ydata(michaelis_ef_growing(x_range, s_AL_MM.val, s_BL_MM.val))
    line_L_abs_mm.set_ydata(x_range * michaelis_ef_growing(x_range, s_AL_MM.val, s_BL_MM.val))
    line_O_ef.set_ydata(michaelis_ef_fading(x_range, s_AO.val, s_BO.val))
    line_O_abs.set_ydata(x_range * michaelis_ef_fading(x_range, s_AO.val, s_BO.val))
    fig.canvas.draw_idle()

def reset(event):
    s_AL.set_val(best_A_L); s_BL.set_val(best_B_L); s_CL.set_val(best_C_L)
    s_AL_MM.set_val(best_A_L_mm); s_BL_MM.set_val(best_B_L_mm)
    s_AO.set_val(best_A_O); s_BO.set_val(best_B_O)

check.on_clicked(toggle_labels)
button_res.on_clicked(reset)
for s in [s_AL, s_BL, s_CL, s_AL_MM, s_BL_MM, s_AO, s_BO]: s.on_changed(update)

plt.show()
