import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# --- 1. Исходные данные (Ваши) ---
samples = ['2233', '2699', '2776', '3110', '3384', '3599', '3675', '3714', 'Buzuluk']
L_sn123 = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0])
O_sn123 = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1])
L_2_exp = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1])
O_2_exp = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3])

# --- 2. Новые данные (Reske 1997) ---
samples_Reske1997 = ['Commodity', 'High linoleic', 'High oleic', 'High palmitic, high linoleic', 'High palmitic, high oleic', 'High stearic, high oleic']
L_sn123_Reske = np.array([58.7, 76.0, 2.1, 46.8, 3.5, 2.0])
O_sn123_Reske = np.array([27.8, 13.3, 91.5, 17.1, 59.8, 79.1])
L_2_Reske     = np.array([65.7, 76.9, 1.4, 67.8, 2.8, 0.6])
O_2_Reske     = np.array([31.5, 18.9, 96.6, 24.9, 93.4, 95.9])

# --- 3. Настройка модели ---
init_threshold = 7.3
init_k_factor = 1.5
init_max_sum = 99.0
approx_sn123_fat = 89.0 

def model_L(x, k, thresh):
    """Softplus модель: k * ln(1 + e^(x - thresh))"""
    return k * np.logaddexp(0, x - thresh)

def model_O(x_oleic, k, thresh, max_s):
    """
    Модель для Олеиновой (через вытеснение).
    Примечание: Для Reske (High Palmitic) сумма L+O < 89, поэтому модель может давать погрешность.
    """
    l_equivalent = approx_sn123_fat - x_oleic
    l_2_pred = model_L(l_equivalent, k, thresh)
    return max_s - l_2_pred

x_range_L = np.linspace(0, 80, 200)
x_range_O = np.linspace(10, 100, 200)

# --- 4. Создание графиков ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
plt.subplots_adjust(bottom=0.30, top=0.90) 

# -- График 1: Линолевая --
# Ваши данные
ax1.scatter(L_sn123, L_2_exp, color='blue', s=60, alpha=0.7, label='Original Data', zorder=5)
# Данные Reske
ax1.scatter(L_sn123_Reske, L_2_Reske, color='green', marker='s', s=60, alpha=0.7, label='Reske 1997', zorder=5)
# Линия модели
line_L, = ax1.plot(x_range_L, model_L(x_range_L, init_k_factor, init_threshold), 
                   color='red', lw=2, label='Model')

# Текст MAE (ошибки)
mae_text_L = ax1.text(0.05, 0.85, '', transform=ax1.transAxes, fontsize=10, 
                      bbox=dict(facecolor='white', alpha=0.8))

ax1.set_title('Линолевая (L): Насыщение SN-2')
ax1.set_xlabel('sn123 L (%)')
ax1.set_ylabel('SN-2 L (%)')
ax1.grid(True, alpha=0.3)
ax1.legend(loc='lower right')

# -- График 2: Олеиновая --
# Ваши данные
ax2.scatter(O_sn123, O_2_exp, color='orange', s=60, alpha=0.7, label='Original Data', zorder=5)
# Данные Reske
ax2.scatter(O_sn123_Reske, O_2_Reske, color='green', marker='s', s=60, alpha=0.7, label='Reske 1997', zorder=5)
# Линия модели
line_O, = ax2.plot(x_range_O, model_O(x_range_O, init_k_factor, init_threshold, init_max_sum), 
                   color='purple', lw=2, label='Model')

# Текст MAE
mae_text_O = ax2.text(0.05, 0.85, '', transform=ax2.transAxes, fontsize=10,
                      bbox=dict(facecolor='white', alpha=0.8))

ax2.set_title('Олеиновая (O): Вытеснение из SN-2')
ax2.set_xlabel('sn123 O (%)')
ax2.set_ylabel('SN-2 O (%)')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='lower left')

# --- 5. Ползунки ---
ax_thresh = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_k      = plt.axes([0.2, 0.10, 0.6, 0.03])
ax_max    = plt.axes([0.2, 0.05, 0.6, 0.03])

s_thresh = Slider(ax_thresh, 'Threshold', -5.0, 20.0, valinit=init_threshold, valstep=0.1)
s_k      = Slider(ax_k, 'K Factor', 0.5, 3.0, valinit=init_k_factor, valstep=0.05)
s_max    = Slider(ax_max, 'Max Sum SN-2', 90.0, 105.0, valinit=init_max_sum, valstep=0.1)

# --- 6. Логика обновления ---
def calculate_mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def update(val):
    th = s_thresh.val
    k = s_k.val
    ms = s_max.val
    
    # 1. Обновляем линии
    line_L.set_ydata(model_L(x_range_L, k, th))
    line_O.set_ydata(model_O(x_range_O, k, th, ms))
    
    # 2. Считаем предсказания для точек
    # Линолевая
    pred_L_orig = model_L(L_sn123, k, th)
    pred_L_reske = model_L(L_sn123_Reske, k, th)
    
    # Олеиновая
    pred_O_orig = model_O(O_sn123, k, th, ms)
    pred_O_reske = model_O(O_sn123_Reske, k, th, ms)
    
    # 3. Считаем ошибки (MAE)
    mae_L_orig = calculate_mae(L_2_exp, pred_L_orig)
    mae_L_reske = calculate_mae(L_2_Reske, pred_L_reske)
    
    mae_O_orig = calculate_mae(O_2_exp, pred_O_orig)
    mae_O_reske = calculate_mae(O_2_Reske, pred_O_reske)
    
    # 4. Обновляем текст
    mae_text_L.set_text(f"MAE Orig: {mae_L_orig:.2f}\nMAE Reske: {mae_L_reske:.2f}")
    mae_text_O.set_text(f"MAE Orig: {mae_O_orig:.2f}\nMAE Reske: {mae_O_reske:.2f}")
    
    fig.canvas.draw_idle()

# Инициализация
s_thresh.on_changed(update)
s_k.on_changed(update)
s_max.on_changed(update)

# Первичный вызов для отображения текста
update(None)

plt.show()