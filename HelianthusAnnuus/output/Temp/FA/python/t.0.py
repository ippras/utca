import matplotlib.pyplot as plt
import numpy as np

# 1. Исходные данные из вашей таблицы
samples = ['2233', '2699', '2776', '3110', '3384', '3599', '3675', '3714', 'Buzuluk']

# Концентрации во всех положениях (Total)
L_total = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0])
O_total = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1])

# Концентрации во 2-м положении (SN-2)
L_2_exp = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1])
O_2_exp = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3])

# 2. Настройка теоретической модели
# Параметры, которые мы вывели:
THRESHOLD = 7.3  # Порог насыщения 1-го положения
K_FACTOR = 1.5   # Коэффициент агрессивности заполнения 2-го положения
MAX_SUM_2 = 99.0 # Примерная сумма L+O во 2-м положении (остальное - насыщенные)

def smooth_model_L(x, k, x0):
    """
    Функция Softplus: k * ln(1 + e^(x - x0))
    Обеспечивает плавный переход к нулю без отрицательных значений.
    """
    # np.logaddexp используется для стабильности при больших числах, 
    # но здесь можно и просто np.log(1 + np.exp(...))
    return k * np.log(1 + np.exp(x - x0))

# Генерируем точки для плавной линии графика (от 0 до 70% концентрации)
x_range = np.linspace(0, 70, 200)

# Расчет теоретических кривых
# Для Линолевой:
y_L_theoretical = smooth_model_L(x_range, K_FACTOR, THRESHOLD)

# Для Олеиновой:
# Мы знаем, что O_total примерно обратно пропорционален L_total.
# Для графика O vs O_2 мы можем использовать зеркальную логику:
# O_2 заполняет всё, что не заняла L_2.
# Предположим для моделирования, что L_total ≈ 90 - O_total (грубая оценка суммы кислот)
x_range_O = np.linspace(20, 95, 200) # Диапазон для Олеиновой
L_equivalent = 90 - x_range_O # Переводим O в L, чтобы посчитать сколько L займет места
L_2_predicted = smooth_model_L(L_equivalent, K_FACTOR, THRESHOLD)
y_O_theoretical = MAX_SUM_2 - L_2_predicted 

# 3. Построение графиков
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# --- График 1: Линолевая кислота (L) ---
ax1.scatter(L_total, L_2_exp, color='blue', s=80, label='Экспериментальные точки', zorder=5)
ax1.plot(x_range, y_L_theoretical, color='red', linewidth=2.5, label=f'Теория: 1.5 * Softplus(L - {THRESHOLD})')

# Визуализация порога
ax1.axvline(x=THRESHOLD, color='green', linestyle='--', alpha=0.5, label=f'Порог насыщения ({THRESHOLD}%)')
ax1.text(THRESHOLD + 1, 5, 'Зона дефицита L', color='green', rotation=90)

ax1.set_title('Зависимость L в SN-2 от Общей L', fontsize=14)
ax1.set_xlabel('Общая концентрация L ({1:L|2:L|3:L}), %', fontsize=12)
ax1.set_ylabel('Концентрация L в SN-2 ({2:L}), %', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.legend()

# --- График 2: Олеиновая кислота (O) ---
ax2.scatter(O_total, O_2_exp, color='orange', s=80, label='Экспериментальные точки', zorder=5)
ax2.plot(x_range_O, y_O_theoretical, color='purple', linewidth=2.5, label='Теория: Вытеснение Линолевой')

ax2.set_title('Зависимость O в SN-2 от Общей O', fontsize=14)
ax2.set_xlabel('Общая концентрация O ({1:O|2:O|3:O}), %', fontsize=12)
ax2.set_ylabel('Концентрация O в SN-2 ({2:O}), %', fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.show()