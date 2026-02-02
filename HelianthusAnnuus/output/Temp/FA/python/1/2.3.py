import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# --- 1. Исходные данные ---
samples = ['2233', '2699', '2776', '3110', '3384', '3599', '3675', '3714', 'Buzuluk']

# Данные (Original)
L_sn123 = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0])
O_sn123 = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1])
L_2_exp = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1])
O_2_exp = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3])

# Данные (Reske 1997)
L_sn123_Reske = np.array([58.7, 76.0, 2.1, 46.8, 3.5, 2.0])
O_sn123_Reske = np.array([27.8, 13.3, 91.5, 17.1, 59.8, 79.1])
L_2_Reske     = np.array([65.7, 76.9, 1.4, 67.8, 2.8, 0.6])
O_2_Reske     = np.array([31.5, 18.9, 96.6, 24.9, 93.4, 95.9])

# --- 2. Расчет EF (Enrichment Factor) ---
# EF = sn-2 / sn-1,2,3
# Используем np.divide с where, чтобы избежать деления на ноль, если вдруг встретится 0
EF_L_exp = np.divide(L_2_exp, L_sn123, out=np.zeros_like(L_2_exp), where=L_sn123!=0)
EF_O_exp = np.divide(O_2_exp, O_sn123, out=np.zeros_like(O_2_exp), where=O_sn123!=0)

EF_L_Reske = np.divide(L_2_Reske, L_sn123_Reske, out=np.zeros_like(L_2_Reske), where=L_sn123_Reske!=0)
EF_O_Reske = np.divide(O_2_Reske, O_sn123_Reske, out=np.zeros_like(O_2_Reske), where=O_sn123_Reske!=0)

# --- 3. Модель ---
init_threshold = 7.3
init_k_factor = 1.5
init_max_sum = 99.0
approx_sn123_fat = 89.0 

def model_L(x, k, thresh):
    """Softplus: k * ln(1 + e^(x - thresh))"""
    return k * np.logaddexp(0, x - thresh)

def model_O(x_oleic, k, thresh, max_s):
    """Вытеснение: Max - model_L(approx_total - x_oleic)"""
    l_equivalent = approx_sn123_fat - x_oleic
    l_2_pred = model_L(l_equivalent, k, thresh)
    return max_s - l_2_pred

# Диапазоны (начинаем чуть больше 0, чтобы EF не улетал в бесконечность на графике)
x_range_L = np.linspace(0.5, 80, 200)
x_range_O = np.linspace(10, 100, 200)

# --- 4. Создание графиков (2x2) ---
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
plt.subplots_adjust(bottom=0.25, hspace=0.3, wspace=0.25)

# Распаковка осей
ax_L_abs, ax_O_abs = axs[0] # Верхний ряд (Абсолютные)
ax_L_ef,  ax_O_ef  = axs[1] # Нижний ряд (EF)

# --- ГРАФИК 1: Линолевая (Абсолют) ---
ax_L_abs.scatter(L_sn123, L_2_exp, c='blue', label='Original')
ax_L_abs.scatter(L_sn123_Reske, L_2_Reske, c='green', marker='s', label='Reske')
line_L_abs, = ax_L_abs.plot(x_range_L, model_L(x_range_L, init_k_factor, init_threshold), c='red', lw=2)
ax_L_abs.set_title('Linoleic: sn-2 vs sn-1,2,3')
ax_L_abs.set_ylabel('sn-2 (%)')
ax_L_abs.grid(True, alpha=0.3)
ax_L_abs.legend(loc='upper left', fontsize='small')

# --- ГРАФИК 2: Олеиновая (Абсолют) ---
ax_O_abs.scatter(O_sn123, O_2_exp, c='orange', label='Original')
ax_O_abs.scatter(O_sn123_Reske, O_2_Reske, c='green', marker='s', label='Reske')
line_O_abs, = ax_O_abs.plot(x_range_O, model_O(x_range_O, init_k_factor, init_threshold, init_max_sum), c='purple', lw=2)
ax_O_abs.set_title('Oleic: sn-2 vs sn-1,2,3')
ax_O_abs.set_ylabel('sn-2 (%)')
ax_O_abs.grid(True, alpha=0.3)

# --- ГРАФИК 3: Линолевая (EF) ---
ax_L_ef.scatter(L_sn123, EF_L_exp, c='blue')
ax_L_ef.scatter(L_sn123_Reske, EF_L_Reske, c='green', marker='s')
# Модель EF = Model_Abs / x
y_ef_L_init = model_L(x_range_L, init_k_factor, init_threshold) / x_range_L
line_L_ef, = ax_L_ef.plot(x_range_L, y_ef_L_init, c='red', lw=2, linestyle='--')
ax_L_ef.set_title('Linoleic: EF (Enrichment Factor)')
ax_L_ef.set_xlabel('sn-1,2,3 (%)')
ax_L_ef.set_ylabel('EF (sn-2 / sn-1,2,3)')
ax_L_ef.grid(True, alpha=0.3)
ax_L_ef.set_ylim(0, 2.5) # Ограничим Y, чтобы не масштабировалось из-за выбросов

# --- ГРАФИК 4: Олеиновая (EF) ---
ax_O_ef.scatter(O_sn123, EF_O_exp, c='orange')
ax_O_ef.scatter(O_sn123_Reske, EF_O_Reske, c='green', marker='s')
# Модель EF
y_ef_O_init = model_O(x_range_O, init_k_factor, init_threshold, init_max_sum) / x_range_O
line_O_ef, = ax_O_ef.plot(x_range_O, y_ef_O_init, c='purple', lw=2, linestyle='--')
ax_O_ef.set_title('Oleic: EF (Enrichment Factor)')
ax_O_ef.set_xlabel('sn-1,2,3 (%)')
ax_O_ef.set_ylabel('EF')
ax_O_ef.grid(True, alpha=0.3)
ax_O_ef.set_ylim(0, 2.0)

# --- 5. Ползунки ---
ax_thresh = plt.axes([0.2, 0.12, 0.6, 0.03])
ax_k      = plt.axes([0.2, 0.07, 0.6, 0.03])
ax_max    = plt.axes([0.2, 0.02, 0.6, 0.03])

s_thresh = Slider(ax_thresh, 'Threshold', -5.0, 20.0, valinit=init_threshold, valstep=0.1)
s_k      = Slider(ax_k, 'K Factor', 0.5, 3.0, valinit=init_k_factor, valstep=0.05)
s_max    = Slider(ax_max, 'Max Sum', 90.0, 105.0, valinit=init_max_sum, valstep=0.1)

# --- 6. Обновление ---
def update(val):
    th = s_thresh.val
    k = s_k.val
    ms = s_max.val
    
    # 1. Расчет новых линий (Абсолют)
    y_L_abs = model_L(x_range_L, k, th)
    y_O_abs = model_O(x_range_O, k, th, ms)
    
    # 2. Расчет новых линий (EF)
    y_L_ef = y_L_abs / x_range_L
    y_O_ef = y_O_abs / x_range_O
    
    # 3. Обновление графиков
    line_L_abs.set_ydata(y_L_abs)
    line_O_abs.set_ydata(y_O_abs)
    line_L_ef.set_ydata(y_L_ef)
    line_O_ef.set_ydata(y_O_ef)
    
    fig.canvas.draw_idle()

s_thresh.on_changed(update)
s_k.on_changed(update)
s_max.on_changed(update)

plt.show()