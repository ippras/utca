import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
from scipy.optimize import curve_fit

# --- 1. Данные ---
L_sn123_all = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0, 
                        58.7, 76.0, 2.1, 46.8, 3.5, 2.0])
L_2_all     = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1, 
                        65.7, 76.9, 1.4, 67.8, 2.8, 0.6])

O_sn123_all = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1, 
                        27.8, 13.3, 91.5, 17.1, 59.8, 79.1])
O_2_all     = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3, 
                        31.5, 18.9, 96.6, 24.9, 93.4, 95.9])

# Разделение
n_orig = 9
L_sn123_orig, L_2_orig = L_sn123_all[:n_orig], L_2_all[:n_orig]
L_sn123_resk, L_2_resk = L_sn123_all[n_orig:], L_2_all[n_orig:]
O_sn123_orig, O_2_orig = O_sn123_all[:n_orig], O_2_all[:n_orig]
O_sn123_resk, O_2_resk = O_sn123_all[n_orig:], O_2_all[n_orig:]

# Расчет EF
with np.errstate(divide='ignore', invalid='ignore'):
    EF_L_all = L_2_all / L_sn123_all
    valid_idx_L = np.isfinite(EF_L_all)
    
    EF_O_all = O_2_all / O_sn123_all
    valid_idx_O = np.isfinite(EF_O_all)
    
    EF_L_orig = L_2_orig / L_sn123_orig
    EF_L_resk = L_2_resk / L_sn123_resk
    EF_O_orig = O_2_orig / O_sn123_orig
    EF_O_resk = O_2_resk / O_sn123_resk

# --- 2. Модели ---

def smooth_haldane_ef(x, A, B, C):
    """ EF = (A * x) / (B + x + x^1.5 / C) """
    x_safe = np.maximum(x, 1e-6)
    denom = B + x_safe + (x_safe**1.5 / C)
    return (A * x_safe) / denom

def smooth_haldane_abs(x, A, B, C):
    return x * smooth_haldane_ef(x, A, B, C)

def michaelis_ef(x, A, B):
    return A / (B + x)

def michaelis_abs(x, A, B):
    return (A * x) / (B + x)

# --- 3. Расчет физических параметров (Пик) ---
def get_peak_info(A, B, C):
    """
    Находит точку максимума для функции Smooth Haldane.
    Математически для степени 1.5 пик находится при x = (2*B*C)^(1/1.5)
    """
    try:
        # Производная равна 0 при 2*B*C = x^1.5
        x_peak = (2 * B * C) ** (1 / 1.5)
        y_peak = smooth_haldane_ef(x_peak, A, B, C)
        return x_peak, y_peak
    except:
        return 0, 0

# --- 4. Авто-подбор ---
try:
    popt_L, _ = curve_fit(smooth_haldane_ef, L_sn123_all[valid_idx_L], EF_L_all[valid_idx_L], 
                          p0=[100, 20, 20], bounds=([1, 1, 1], [2000, 500, 500]))
    best_A_L, best_B_L, best_C_L = popt_L
except:
    best_A_L, best_B_L, best_C_L = 100, 20, 20

try:
    popt_O, _ = curve_fit(michaelis_ef, O_sn123_all[valid_idx_O], EF_O_all[valid_idx_O], 
                          p0=[150, 50], bounds=(1, 500))
    best_A_O, best_B_O = popt_O
except:
    best_A_O, best_B_O = 150, 50

# --- 5. Графики ---
x_range = np.linspace(0.1, 100, 400)

fig, axs = plt.subplots(2, 2, figsize=(14, 10))
plt.subplots_adjust(bottom=0.35, hspace=0.4, wspace=0.25)

ax_L_abs, ax_O_abs = axs[0]
ax_L_ef,  ax_O_ef  = axs[1]

# --- ЛИНОЛЕВАЯ ---
# Abs
ax_L_abs.scatter(L_sn123_orig, L_2_orig, c='blue', label='Original')
ax_L_abs.scatter(L_sn123_resk, L_2_resk, c='green', marker='s', label='Reske')
line_L_abs, = ax_L_abs.plot(x_range, smooth_haldane_abs(x_range, best_A_L, best_B_L, best_C_L), c='red', lw=2)
ax_L_abs.set_title('Linoleic: sn-2 (Abs)')
ax_L_abs.set_ylabel('sn-2 (%)')
ax_L_abs.grid(True, alpha=0.3)
ax_L_abs.legend()

# EF
ax_L_ef.scatter(L_sn123_orig, EF_L_orig, c='blue')
ax_L_ef.scatter(L_sn123_resk, EF_L_resk, c='green', marker='s')
line_L_ef, = ax_L_ef.plot(x_range, smooth_haldane_ef(x_range, best_A_L, best_B_L, best_C_L), c='red', lw=2)

# Линии пика (инициализация)
peak_x, peak_y = get_peak_info(best_A_L, best_B_L, best_C_L)
vline_peak = ax_L_ef.axvline(peak_x, color='gray', linestyle='--', alpha=0.6)
hline_peak = ax_L_ef.axhline(peak_y, color='gray', linestyle='--', alpha=0.6)
text_peak = ax_L_ef.text(0.5, 0.9, '', transform=ax_L_ef.transAxes, ha='center', color='darkred', fontweight='bold')

ax_L_ef.set_title('Linoleic: EF (Enrichment Factor)')
ax_L_ef.set_ylabel('EF')
ax_L_ef.set_xlabel('sn-1,2,3 (%)')
ax_L_ef.grid(True, alpha=0.3)
ax_L_ef.set_ylim(0, 2.5)

# --- ОЛЕИНОВАЯ ---
# Abs
ax_O_abs.scatter(O_sn123_orig, O_2_orig, c='orange', label='Original')
ax_O_abs.scatter(O_sn123_resk, O_2_resk, c='green', marker='s', label='Reske')
line_O_abs, = ax_O_abs.plot(x_range, michaelis_abs(x_range, best_A_O, best_B_O), c='purple', lw=2)
ax_O_abs.set_title('Oleic: sn-2 (Abs)')
ax_O_abs.set_ylabel('sn-2 (%)')
ax_O_abs.grid(True, alpha=0.3)

# EF
ax_O_ef.scatter(O_sn123_orig, EF_O_orig, c='orange')
ax_O_ef.scatter(O_sn123_resk, EF_O_resk, c='green', marker='s')
line_O_ef, = ax_O_ef.plot(x_range, michaelis_ef(x_range, best_A_O, best_B_O), c='purple', lw=2, linestyle='--')
ax_O_ef.set_title('Oleic: EF')
ax_O_ef.set_ylabel('EF')
ax_O_ef.set_xlabel('sn-1,2,3 (%)')
ax_O_ef.grid(True, alpha=0.3)
ax_O_ef.set_ylim(0, 3.0)

# --- 6. Виджеты ---
axcolor = 'lightgoldenrodyellow'

# Linoleic Sliders
ax_AL = plt.axes([0.15, 0.22, 0.3, 0.03], facecolor=axcolor)
ax_BL = plt.axes([0.15, 0.18, 0.3, 0.03], facecolor=axcolor)
ax_CL = plt.axes([0.15, 0.14, 0.3, 0.03], facecolor=axcolor)

# Oleic Sliders
ax_AO = plt.axes([0.60, 0.20, 0.3, 0.03], facecolor=axcolor)
ax_BO = plt.axes([0.60, 0.16, 0.3, 0.03], facecolor=axcolor)

s_AL = Slider(ax_AL, 'Lin A (Мощность)', 10.0, 20.0, valinit=best_A_L, color='lightblue')
s_BL = Slider(ax_BL, 'Lin B (Старт)', 1.0, 200.0, valinit=best_B_L, color='lightblue')
s_CL = Slider(ax_CL, 'Lin C (Хвост)', 0.0, 10.0, valinit=best_C_L, color='lightblue')

s_AO = Slider(ax_AO, 'Ole A (Max)', 10.0, 300.0, valinit=best_A_O, color='salmon')
s_BO = Slider(ax_BO, 'Ole B (Km)', 1.0, 200.0, valinit=best_B_O, color='salmon')

# Текст MAE
mae_text = plt.figtext(0.5, 0.05, '', ha='center', fontsize=12, fontweight='bold', 
                       bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# Кнопка сброса
resetax = plt.axes([0.45, 0.01, 0.1, 0.03])
button = Button(resetax, 'Auto-Fit', color=axcolor, hovercolor='0.975')

def update(val):
    al, bl, cl = s_AL.val, s_BL.val, s_CL.val
    ao, bo = s_AO.val, s_BO.val
    
    # 1. Обновляем линии
    line_L_abs.set_ydata(smooth_haldane_abs(x_range, al, bl, cl))
    line_L_ef.set_ydata(smooth_haldane_ef(x_range, al, bl, cl))
    
    line_O_abs.set_ydata(michaelis_abs(x_range, ao, bo))
    line_O_ef.set_ydata(michaelis_ef(x_range, ao, bo))
    
    # 2. Обновляем физические маркеры (Пик)
    px, py = get_peak_info(al, bl, cl)
    vline_peak.set_xdata([px])
    hline_peak.set_ydata([py])
    text_peak.set_text(f"Пик EF: {py:.2f} при {px:.1f}%")
    
    # 3. Считаем ошибку
    pred_EF_L = smooth_haldane_ef(L_sn123_all[valid_idx_L], al, bl, cl)
    mae_EF_L = np.mean(np.abs(EF_L_all[valid_idx_L] - pred_EF_L))
    
    pred_EF_O = michaelis_ef(O_sn123_all[valid_idx_O], ao, bo)
    mae_EF_O = np.mean(np.abs(EF_O_all[valid_idx_O] - pred_EF_O))
    
    mae_text.set_text(f"Ошибка EF (MAE): Lin={mae_EF_L:.3f} | Ole={mae_EF_O:.3f}")
    fig.canvas.draw_idle()

def reset(event):
    s_AL.set_val(best_A_L)
    s_BL.set_val(best_B_L)
    s_CL.set_val(best_C_L)
    s_AO.set_val(best_A_O)
    s_BO.set_val(best_B_O)

s_AL.on_changed(update)
s_BL.on_changed(update)
s_CL.on_changed(update)
s_AO.on_changed(update)
s_BO.on_changed(update)
button.on_clicked(reset)

# Инициализация текста
update(None)

plt.show()