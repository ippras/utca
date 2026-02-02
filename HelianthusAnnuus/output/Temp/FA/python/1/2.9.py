import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, CheckButtons, RadioButtons
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

# --- 2. Модели ---
def smooth_haldane_ef(x, A, B, C):
    x_safe = np.maximum(x, 1e-6)
    return (A * x_safe) / (B + x_safe + (x_safe**1.5 / C))

def michaelis_ef_growing(x, A, B): return (A * x) / (B + x)

# --- 3. Исправленная функция подбора ---
def perform_fit(use_all=True):
    idx_L = np.isfinite(EF_L_all)
    idx_O = np.isfinite(EF_O_all)
    if not use_all:
        mask = np.zeros_like(EF_L_all, dtype=bool)
        mask[:n_orig] = True
        idx_L &= mask
        idx_O &= mask
    
    # Haldane Linoleic
    try:
        pL, _ = curve_fit(smooth_haldane_ef, L_sn123_all[idx_L], EF_L_all[idx_L], 
                          p0=[100, 20, 20], bounds=([1, 0.1, 0.1], [500, 200, 200]))
    except: pL = [100, 20, 20]
    
    # MM Growing Linoleic
    try:
        pL_mm, _ = curve_fit(michaelis_ef_growing, L_sn123_all[idx_L], EF_L_all[idx_L], 
                             p0=[2.0, 10.0], bounds=([0.1, 0.1], [10, 300]))
    except: pL_mm = [2.0, 10.0]
    
    # MM Fading Oleic
    try:
        pO, _ = curve_fit(michaelis_ef_growing, O_sn123_all[idx_O], EF_O_all[idx_O], 
                          p0=[150, 50], bounds=([1, 1], [500, 300]))
    except: pO = [150, 50]
    
    return pL, pL_mm, pO

# Первичный расчет
best_h, best_mm, best_o = perform_fit(use_all=True)

# --- 4. Графики ---
x_range = np.linspace(0.1, 100, 400)
fig, axs = plt.subplots(2, 2, figsize=(15, 11))
plt.subplots_adjust(bottom=0.38, hspace=0.35, wspace=0.2)
(ax_L_abs, ax_O_abs), (ax_L_ef, ax_O_ef) = axs

def create_labels(ax, x, y, labels):
    return [ax.text(x[i], y[i], labels[i], fontsize=7, visible=False, fontweight='bold') for i in range(len(labels))]

texts_list = [create_labels(ax_L_abs, L_sn123_all, L_2_all, samples),
              create_labels(ax_O_abs, O_sn123_all, O_2_all, samples),
              create_labels(ax_L_ef, L_sn123_all, EF_L_all, samples),
              create_labels(ax_O_ef, O_sn123_all, EF_O_all, samples)]

# Отрисовка
ax_L_abs.scatter(L_sn123_all[:n_orig], L_2_all[:n_orig], c='blue', label='My Exp')
ax_L_abs.scatter(L_sn123_all[n_orig:], L_2_all[n_orig:], c='green', marker='s', label='Others')
line_L_abs, = ax_L_abs.plot(x_range, x_range * smooth_haldane_ef(x_range, *best_h), 'r-')
line_L_abs_mm, = ax_L_abs.plot(x_range, x_range * michaelis_ef_growing(x_range, *best_mm), 'g--')
ax_L_abs.legend()

ax_L_ef.scatter(L_sn123_all[:n_orig], EF_L_all[:n_orig], c='blue')
ax_L_ef.scatter(L_sn123_all[n_orig:], EF_L_all[n_orig:], c='green', marker='s')
line_L_ef, = ax_L_ef.plot(x_range, smooth_haldane_ef(x_range, *best_h), 'r-')
line_L_ef_mm, = ax_L_ef.plot(x_range, michaelis_ef_growing(x_range, *best_mm), 'g--')
ax_L_ef.set_ylim(0, 2.5)

ax_O_abs.scatter(O_sn123_all[:n_orig], O_2_all[:n_orig], c='orange')
ax_O_abs.scatter(O_sn123_all[n_orig:], O_2_all[n_orig:], c='green', marker='s')
line_O_abs, = ax_O_abs.plot(x_range, x_range * michaelis_ef_growing(x_range, *best_o), 'purple')

ax_O_ef.scatter(O_sn123_all[:n_orig], EF_O_all[:n_orig], c='orange')
ax_O_ef.scatter(O_sn123_all[n_orig:], EF_O_all[n_orig:], c='green', marker='s')
line_O_ef, = ax_O_ef.plot(x_range, michaelis_ef_growing(x_range, *best_o), 'purple')
ax_O_ef.set_ylim(0, 3.0)

# --- 5. Виджеты ---
s_AL = Slider(plt.axes([0.15, 0.30, 0.3, 0.015]), 'Lin Hald A', 0, 500, valinit=best_h[0])
s_BL = Slider(plt.axes([0.15, 0.28, 0.3, 0.015]), 'Lin Hald B', 1, 200, valinit=best_h[1])
s_CL = Slider(plt.axes([0.15, 0.26, 0.3, 0.015]), 'Lin Hald C', 0.1, 500, valinit=best_h[2])
s_AL_MM = Slider(plt.axes([0.15, 0.22, 0.3, 0.015]), 'Lin MM A', 0.1, 10, valinit=best_mm[0], color='green')
s_BL_MM = Slider(plt.axes([0.15, 0.20, 0.3, 0.015]), 'Lin MM B', 0.1, 200, valinit=best_mm[1], color='green')
s_AO = Slider(plt.axes([0.60, 0.28, 0.3, 0.015]), 'Ole MM A', 10, 500, valinit=best_o[0], color='salmon')
s_BO = Slider(plt.axes([0.60, 0.26, 0.3, 0.015]), 'Ole MM B', 1, 300, valinit=best_o[1], color='salmon')

radio_ax = plt.axes([0.42, 0.12, 0.15, 0.06], facecolor='#f0f0f0')
radio = RadioButtons(radio_ax, ('All Data', 'My Exp (9)'))

rax = plt.axes([0.15, 0.05, 0.7, 0.04], frameon=False)
check = CheckButtons(rax, ('L-Abs ID', 'O-Abs ID', 'L-EF ID', 'O-EF ID'), (False, False, False, False))

btn_res = Button(plt.axes([0.45, 0.01, 0.1, 0.03]), 'AUTO-FIT')

def update(val):
    line_L_ef.set_ydata(smooth_haldane_ef(x_range, s_AL.val, s_BL.val, s_CL.val))
    line_L_abs.set_ydata(x_range * smooth_haldane_ef(x_range, s_AL.val, s_BL.val, s_CL.val))
    line_L_ef_mm.set_ydata(michaelis_ef_growing(x_range, s_AL_MM.val, s_BL_MM.val))
    line_L_abs_mm.set_ydata(x_range * michaelis_ef_growing(x_range, s_AL_MM.val, s_BL_MM.val))
    line_O_ef.set_ydata(michaelis_ef_growing(x_range, s_AO.val, s_BO.val))
    line_O_abs.set_ydata(x_range * michaelis_ef_growing(x_range, s_AO.val, s_BO.val))
    fig.canvas.draw_idle()

def apply_fit(event):
    bh, bmm, bo = perform_fit(use_all=(radio.value_selected == 'All Data'))
    s_AL.set_val(bh[0]); s_BL.set_val(bh[1]); s_CL.set_val(bh[2])
    s_AL_MM.set_val(bmm[0]); s_BL_MM.set_val(bmm[1])
    s_AO.set_val(bo[0]); s_BO.set_val(bo[1])

btn_res.on_clicked(apply_fit)
check.on_clicked(lambda lab: [ [t.set_visible(not t.get_visible()) for t in texts_list[i]] 
                               for i, l in enumerate(['L-Abs ID', 'O-Abs ID', 'L-EF ID', 'O-EF ID']) if l==lab ] and fig.canvas.draw_idle())
for s in [s_AL, s_BL, s_CL, s_AL_MM, s_BL_MM, s_AO, s_BO]: s.on_changed(update)

plt.show()
