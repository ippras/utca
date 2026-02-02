import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
import numpy as np

# --- 1. Данные ---
# Структура: ID, sn-1,2,3 Linoleic, sn-1,2,3 Oleic, sn-2 Linoleic, sn-2 Oleic
data = [
    ("2233",    40.9, 44.1, 49.8, 50.0),
    ("2699",    46.2, 41.3, 61.1, 38.6),
    ("2776",    44.2, 42.8, 55.2, 41.9),
    ("3110",    1.1,  84.6, 0.0,  97.9),
    ("3384",    53.5, 36.2, 71.5, 27.5),
    ("3599",    1.8,  88.5, 0.9,  98.9),
    ("3675",    51.7, 37.1, 64.5, 34.4),
    ("3714",    50.8, 37.7, 64.6, 33.9),
    ("Бузулук", 64.0, 24.1, 84.1, 14.3)
]

# Распаковка данных
sample_ids = [row[0] for row in data]
linoleic_sn123 = np.array([row[1] for row in data])
oleic_sn123    = np.array([row[2] for row in data])
linoleic_sn2   = np.array([row[3] for row in data])
oleic_sn2      = np.array([row[4] for row in data])

# --- 2. Модель (Линейная со смещением) ---
def linear_offset_model(x, slope, offset):
    """
    Формула: y = Slope * (x - Offset)
    Например: 1.5 * (x - 7.3)
    """
    return slope * (x - offset)

# Начальные параметры
# Для Линолевой ставим запрошенные вами 1.5 и 7.3
init_lin_slope, init_lin_offset = 1.5, 7.3 

# Для Олеиновой поставим нейтральные значения для старта (или можно подобрать похожие)
init_ole_slope, init_ole_offset = 1.1, 0.0 

x_range = np.linspace(0, 100, 200)

# --- 3. Настройка Графика ---
fig, ax = plt.subplots(figsize=(12, 9))
plt.subplots_adjust(left=0.1, bottom=0.35, right=0.95, top=0.9)

# Экспериментальные точки
ax.plot(linoleic_sn123, linoleic_sn2, 'o', color='blue', markersize=8, alpha=0.7, label='Exp Линолевая (sn-2)')
ax.plot(oleic_sn123, oleic_sn2, 's', color='red', markersize=8, alpha=0.7, label='Exp Олеиновая (sn-2)')

# Линии моделей
line_linoleic, = ax.plot(x_range, linear_offset_model(x_range, init_lin_slope, init_lin_offset), 
                         color='blue', linewidth=2, label='Model Линолевая')
line_oleic, = ax.plot(x_range, linear_offset_model(x_range, init_ole_slope, init_ole_offset), 
                      color='red', linewidth=2, linestyle='--', label='Model Олеиновая')

# Текстовые поля для ошибок (MAE)
mae_text_lin = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='blue', fontsize=11, fontweight='bold')
mae_text_ole = ax.text(0.02, 0.90, '', transform=ax.transAxes, color='red', fontsize=11, fontweight='bold')

# --- Подписи точек (Labels) ---
labels_objects = []

for i, txt in enumerate(sample_ids):
    # Линолевая
    lbl_l = ax.annotate(txt, (linoleic_sn123[i], linoleic_sn2[i]), xytext=(5, 5), textcoords='offset points', 
                      fontsize=8, color='darkblue', visible=False, fontweight='bold')
    labels_objects.append(lbl_l)
    # Олеиновая
    lbl_o = ax.annotate(txt, (oleic_sn123[i], oleic_sn2[i]), xytext=(5, -10), textcoords='offset points', 
                      fontsize=8, color='darkred', visible=False, fontweight='bold')
    labels_objects.append(lbl_o)

# Функция обновления текста ошибок
def update_mae_text(l_slope, l_offset, o_slope, o_offset):
    calc_lin = linear_offset_model(linoleic_sn123, l_slope, l_offset)
    mae_lin = np.mean(np.abs(calc_lin - linoleic_sn2))
    mae_text_lin.set_text(f'MAE Линолевая: {mae_lin:.2f}')
    
    calc_ole = linear_offset_model(oleic_sn123, o_slope, o_offset)
    mae_ole = np.mean(np.abs(calc_ole - oleic_sn2))
    mae_text_ole.set_text(f'MAE Олеиновая: {mae_ole:.2f}')

# Первичный расчет
update_mae_text(init_lin_slope, init_lin_offset, init_ole_slope, init_ole_offset)

# Оформление осей
ax.set_title('Линейная модель: 1.5 * (sn123 - 7.3)')
ax.set_xlabel('Концентрация sn-1,2,3 (%)')
ax.set_ylabel('Концентрация sn-2 (%)')
ax.legend(loc='upper left')
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_ylim(0, 105)
ax.set_xlim(0, 100)

# --- 4. Виджеты (Слайдеры и Кнопки) ---
axcolor = 'lightgoldenrodyellow'

# Создание осей для слайдеров
ax_slider_lin_slope  = plt.axes([0.15, 0.20, 0.3, 0.03], facecolor=axcolor)
ax_slider_lin_offset = plt.axes([0.15, 0.15, 0.3, 0.03], facecolor=axcolor)
ax_slider_ole_slope  = plt.axes([0.60, 0.20, 0.3, 0.03], facecolor=axcolor)
ax_slider_ole_offset = plt.axes([0.60, 0.15, 0.3, 0.03], facecolor=axcolor)

# Инициализация слайдеров
# Slope (множитель)
slider_lin_slope = Slider(ax_slider_lin_slope, 'Lin Slope', 0.5, 3.0, valinit=init_lin_slope, valstep=0.05, color='lightblue')
# Offset (вычитаемое)
slider_lin_offset = Slider(ax_slider_lin_offset, 'Lin Offset', -10.0, 20.0, valinit=init_lin_offset, valstep=0.1, color='lightblue')

slider_ole_slope = Slider(ax_slider_ole_slope, 'Ole Slope', 0.5, 3.0, valinit=init_ole_slope, valstep=0.05, color='salmon')
slider_ole_offset = Slider(ax_slider_ole_offset, 'Ole Offset', -10.0, 20.0, valinit=init_ole_offset, valstep=0.1, color='salmon')

# Функция обновления графика при движении слайдеров
def update_plot(val):
    # Получаем значения
    l_slope, l_offset = slider_lin_slope.val, slider_lin_offset.val
    o_slope, o_offset = slider_ole_slope.val, slider_ole_offset.val
    
    # Обновляем линии
    line_linoleic.set_ydata(linear_offset_model(x_range, l_slope, l_offset))
    line_oleic.set_ydata(linear_offset_model(x_range, o_slope, o_offset))
    
    # Обновляем текст ошибок
    update_mae_text(l_slope, l_offset, o_slope, o_offset)
    
    # Перерисовываем
    fig.canvas.draw_idle()

# Привязка событий
slider_lin_slope.on_changed(update_plot)
slider_lin_offset.on_changed(update_plot)
slider_ole_slope.on_changed(update_plot)
slider_ole_offset.on_changed(update_plot)

# --- Чекбокс для отображения ID ---
ax_check = plt.axes([0.8, 0.025, 0.15, 0.08], frameon=False)
check_btn = CheckButtons(ax_check, ['Показать ID'], [False])

def toggle_labels(label):
    status = check_btn.get_status()[0]
    for lbl in labels_objects:
        lbl.set_visible(status)
    fig.canvas.draw_idle()

check_btn.on_clicked(toggle_labels)

# --- Кнопка сброса (Reset) ---
ax_reset = plt.axes([0.45, 0.05, 0.1, 0.04])
btn_reset = Button(ax_reset, 'Сброс', color=axcolor, hovercolor='0.975')

def reset_sliders(event):
    slider_lin_slope.reset()
    slider_lin_offset.reset()
    slider_ole_slope.reset()
    slider_ole_offset.reset()

btn_reset.on_clicked(reset_sliders)

plt.show()