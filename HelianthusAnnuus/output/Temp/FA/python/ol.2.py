import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
import numpy as np

# --- 1. Данные ---
data = [
    ("2233",    40.9, 44.1, 37.9, 0.66, 40.6, 0.98),
    # ("2699",    46.2, 41.3, 31.2, 0.22, 44.1, 0.54),
    ("2776",    44.2, 42.8, 32.6, 1.25, 41.6, 1.56),
    ("3110",    1.1,  84.6, 38.6, 0.17, 0.0,  0.0),
    ("3384",    53.5, 36.2, 25.3, 1.14, 44.6, 0.64),
    ("3599",    1.8,  88.5, 37.2, 0.17, 17.1, 0.72),
    ("3675",    51.7, 37.1, 30.9, 0.38, 41.6, 0.65),
    # ("3714",    50.8, 37.7, 30.0, 2.40, 42.4, 2.21),
    ("Бузулук", 64.0, 24.1, 19.8, 2.47, 43.8, 1.40)
]

ids = [row[0] for row in data]
L_conc = np.array([row[1] for row in data])
O_conc = np.array([row[2] for row in data])
EF_O_exp = np.array([row[3] for row in data])
EF_O_err = np.array([row[4] for row in data])
EF_L_exp = np.array([row[5] for row in data])
EF_L_err = np.array([row[6] for row in data])

# --- 2. Модель ---
def saturation_model(x, A, B):
    denom = B + x
    with np.errstate(divide='ignore', invalid='ignore'):
        res = (A * x) / denom
        res[denom == 0] = 0
    return res

init_AL, init_BL = 46.0, 3.0
init_AO, init_BO = 60.0, 48.0
x_range = np.linspace(0, 100, 200)

# --- 3. График ---
fig, ax = plt.subplots(figsize=(12, 9))
plt.subplots_adjust(left=0.1, bottom=0.35, right=0.95, top=0.9)

# Экспериментальные точки
ax.errorbar(L_conc, EF_L_exp, yerr=EF_L_err, fmt='o', color='blue', ecolor='black', capsize=3, alpha=0.6, label='Exp Линолевая')
ax.errorbar(O_conc, EF_O_exp, yerr=EF_O_err, fmt='s', color='red', ecolor='black', capsize=3, alpha=0.6, label='Exp Олеиновая')

# Линии моделей
line_L, = ax.plot(x_range, saturation_model(x_range, init_AL, init_BL), color='blue', linewidth=2, label='Model Линолевая')
line_O, = ax.plot(x_range, saturation_model(x_range, init_AO, init_BO), color='red', linewidth=2, linestyle='--', label='Model Олеиновая')

# Текст ошибок
mae_text_L = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='blue', fontsize=11, fontweight='bold')
mae_text_O = ax.text(0.02, 0.90, '', transform=ax.transAxes, color='red', fontsize=11, fontweight='bold')

# --- СОЗДАНИЕ ПОДПИСЕЙ (Изначально скрыты) ---
labels_objects = [] # Список для хранения текстовых объектов

# Подписи для Линолевой (Синие)
for i, txt in enumerate(ids):
    # annotate позволяет задать смещение (xytext) в пунктах, чтобы текст не наезжал на точку
    lbl = ax.annotate(txt, (L_conc[i], EF_L_exp[i]), xytext=(5, 5), textcoords='offset points', 
                      fontsize=8, color='darkblue', visible=False, fontweight='bold')
    labels_objects.append(lbl)

# Подписи для Олеиновой (Красные)
for i, txt in enumerate(ids):
    lbl = ax.annotate(txt, (O_conc[i], EF_O_exp[i]), xytext=(5, -10), textcoords='offset points', 
                      fontsize=8, color='darkred', visible=False, fontweight='bold')
    labels_objects.append(lbl)

def update_mae_text(al, bl, ao, bo):
    calc_L = saturation_model(L_conc, al, bl)
    mae_L = np.mean(np.abs(calc_L - EF_L_exp))
    mae_text_L.set_text(f'MAE Линолевая: {mae_L:.2f}')
    
    calc_O = saturation_model(O_conc, ao, bo)
    mae_O = np.mean(np.abs(calc_O - EF_O_exp))
    mae_text_O.set_text(f'MAE Олеиновая: {mae_O:.2f}')

update_mae_text(init_AL, init_BL, init_AO, init_BO)

ax.set_title('Интерактивный подбор параметров')
ax.set_xlabel('Концентрация кислоты (%)')
ax.set_ylabel('EF')
ax.legend(loc='upper right')
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_ylim(0, 60)

# --- 4. Виджеты ---
axcolor = 'lightgoldenrodyellow'

# Слайдеры
ax_AL = plt.axes([0.15, 0.20, 0.3, 0.03], facecolor=axcolor)
ax_BL = plt.axes([0.15, 0.15, 0.3, 0.03], facecolor=axcolor)
ax_AO = plt.axes([0.60, 0.20, 0.3, 0.03], facecolor=axcolor)
ax_BO = plt.axes([0.60, 0.15, 0.3, 0.03], facecolor=axcolor)

s_AL = Slider(ax_AL, 'Lin A (Max)', 20.0, 80.0, valinit=init_AL, valstep=0.1, color='lightblue')
s_BL = Slider(ax_BL, 'Lin B (Rate)', 0.1, 20.0, valinit=init_BL, valstep=0.1, color='lightblue')
s_AO = Slider(ax_AO, 'Ole A (Max)', 20.0, 100.0, valinit=init_AO, valstep=0.1, color='salmon')
s_BO = Slider(ax_BO, 'Ole B (Rate)', 1.0, 100.0, valinit=init_BO, valstep=0.1, color='salmon')

def update(val):
    al, bl = s_AL.val, s_BL.val
    ao, bo = s_AO.val, s_BO.val
    line_L.set_ydata(saturation_model(x_range, al, bl))
    line_O.set_ydata(saturation_model(x_range, ao, bo))
    update_mae_text(al, bl, ao, bo)
    fig.canvas.draw_idle()

s_AL.on_changed(update)
s_BL.on_changed(update)
s_AO.on_changed(update)
s_BO.on_changed(update)

# --- ЧЕКБОКС ДЛЯ ID ---
ax_check = plt.axes([0.8, 0.025, 0.15, 0.08], frameon=False) # Позиция справа внизу
check = CheckButtons(ax_check, ['Показать ID'], [False])

def toggle_labels(label):
    # Получаем текущее состояние (True/False)
    status = check.get_status()[0]
    # Применяем ко всем текстовым объектам
    for lbl in labels_objects:
        lbl.set_visible(status)
    fig.canvas.draw_idle()

check.on_clicked(toggle_labels)

# Кнопка сброса
resetax = plt.axes([0.45, 0.05, 0.1, 0.04])
button = Button(resetax, 'Сброс', color=axcolor, hovercolor='0.975')
def reset(event):
    s_AL.reset()
    s_BL.reset()
    s_AO.reset()
    s_BO.reset()
button.on_clicked(reset)

plt.show()