import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np

# --- 1. Данные ---
data = [
    ("2233",    40.9, 44.1, 40.6, 0.98),
    ("2699",    46.2, 41.3, 44.1, 0.54),
    ("2776",    44.2, 42.8, 41.6, 1.56),
    ("3110",    1.1,  84.6, 0.0,  0.0),
    ("3384",    53.5, 36.2, 44.6, 0.64),
    ("3599",    1.8,  88.5, 17.1, 0.72),
    ("3675",    51.7, 37.1, 41.6, 0.65),
    ("3714",    50.8, 37.7, 42.4, 2.21),
    ("Бузулук", 64.0, 24.1, 43.8, 1.4)
]

ids = [row[0] for row in data]
L_vals = np.array([row[1] for row in data])
O_vals = np.array([row[2] for row in data])
Exp_vals = np.array([row[3] for row in data])
Exp_errs = np.array([row[4] for row in data])

# Средняя сумма L+O для построения линии тренда
avg_sum = np.mean(L_vals + O_vals)
L_line = np.linspace(0, 70, 100)
O_line = np.maximum(0, avg_sum - L_line)

# --- 2. Функция формулы ---
def calculate_ef(l, o, A, B, C):
    # Защита от деления на ноль, если знаменатель вдруг станет 0
    denom = (B + l + C * o)
    with np.errstate(divide='ignore', invalid='ignore'):
        res = (A * l) / denom
        res[denom == 0] = 0
    return res

# Начальные параметры
init_A = 48.3
init_B = 3.0
init_C = 0.1

# --- 3. Настройка графика ---
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.35) # Оставляем место снизу для слайдеров

# Построение статики (Эксперимент)
ax.errorbar(L_vals, Exp_vals, yerr=Exp_errs, fmt='o', color='red', ecolor='black', capsize=5, label='Эксперимент', alpha=0.6)

# Построение динамики (Расчетные точки)
# Считаем начальные значения
calc_vals = calculate_ef(L_vals, O_vals, init_A, init_B, init_C)
calc_line = calculate_ef(L_line, O_line, init_A, init_B, init_C)

# Рисуем линию тренда
line_plot, = ax.plot(L_line, calc_line, color='gray', linestyle='--', alpha=0.5, label='Тренд (L+O≈88)')

# Рисуем расчетные точки (используем scatter, чтобы обновлять их положение)
scat_plot = ax.scatter(L_vals, calc_vals, color='blue', marker='x', s=80, zorder=5, label='Формула')

# Текст для отображения ошибки
mae = np.mean(np.abs(calc_vals - Exp_vals))
text_mae = ax.text(0.02, 0.95, f'Средняя ошибка (MAE): {mae:.2f}', transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

ax.set_title(r'Подбор параметров: $EF_L = \frac{A \cdot L}{B + L + C \cdot O}$')
ax.set_xlabel('L (Линолевая к-та)')
ax.set_ylabel('EF_L')
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)

# --- 4. Создание слайдеров ---
# Цвет слайдеров
axcolor = 'lightgoldenrodyellow'

# Оси для слайдеров [left, bottom, width, height]
ax_A = plt.axes([0.2, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_B = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_C = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)

# Сами слайдеры
s_A = Slider(ax_A, 'Коэф. насыщ. (A)', 10.0, 100.0, valinit=init_A, valstep=0.1)
s_B = Slider(ax_B, 'Константа (B)', 0.0, 20.0, valinit=init_B, valstep=0.1)
s_C = Slider(ax_C, 'Помеха O (C)', -0.5, 1.0, valinit=init_C, valstep=0.01)

# --- 5. Функция обновления ---
def update(val):
    # Считываем значения
    A = s_A.val
    B = s_B.val
    C = s_C.val
    
    # Пересчитываем точки
    new_calc_vals = calculate_ef(L_vals, O_vals, A, B, C)
    # Пересчитываем линию
    new_line_vals = calculate_ef(L_line, O_line, A, B, C)
    
    # Обновляем графики
    # Для scatter plot нужно обновить offsets (массив пар x,y)
    scat_plot.set_offsets(np.c_[L_vals, new_calc_vals])
    
    # Для линии обновляем Y данные
    line_plot.set_ydata(new_line_vals)
    
    # Обновляем текст ошибки
    new_mae = np.mean(np.abs(new_calc_vals - Exp_vals))
    text_mae.set_text(f'Средняя ошибка (MAE): {new_mae:.2f}')
    
    # Перерисовываем
    fig.canvas.draw_idle()

# Привязываем функцию обновления к событию изменения слайдера
s_A.on_changed(update)
s_B.on_changed(update)
s_C.on_changed(update)

# Кнопка сброса (Reset)
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Сброс', color=axcolor, hovercolor='0.975')

def reset(event):
    s_A.reset()
    s_B.reset()
    s_C.reset()
button.on_clicked(reset)

plt.show()