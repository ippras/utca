# Нужны графики ковариации EF от SN123 для эксперимента и для расчета для L и O

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
L_conc = np.array([row[1] for row in data]) # SN123 для Линолевой
O_conc = np.array([row[2] for row in data]) # SN123 для Олеиновой
EF_O_exp = np.array([row[3] for row in data])
EF_L_exp = np.array([row[5] for row in data])

# --- 2. Модель ---
def saturation_model(x, A, B):
    denom = B + x
    with np.errstate(divide='ignore', invalid='ignore'):
        res = (A * x) / denom
        res[denom == 0] = 0
    return res

# Начальные параметры
init_AL, init_BL = 46.0, 3.0
init_AO, init_BO = 60.0, 48.0
x_range = np.linspace(0, 100, 200)

# --- 3. Настройка фигуры ---
fig, (ax_L, ax_O) = plt.subplots(1, 2, figsize=(16, 7))
plt.subplots_adjust(left=0.05, bottom=0.30, right=0.95, top=0.88, wspace=0.2)

# === ГРАФИК 1: ЛИНОЛЕВАЯ (L vs EF_L) ===
# Эксперимент (неподвижные точки)
ax_L.scatter(L_conc, EF_L_exp, color='blue', marker='s', s=60, label='Exp Data', alpha=0.6)
# Модель (подвижные точки - для расчета ковариации именно по точкам)
scat_L_model = ax_L.scatter(L_conc, saturation_model(L_conc, init_AL, init_BL), 
                            color='cyan', marker='o', s=60, label='Model Points', edgecolors='blue')
# Линия тренда модели
line_L, = ax_L.plot(x_range, saturation_model(x_range, init_AL, init_BL), color='blue', alpha=0.4)

ax_L.set_title('Линолевая: EF vs Концентрация (SN123)')
ax_L.set_xlabel('Концентрация L (%)')
ax_L.set_ylabel('EF_L')
ax_L.legend(loc='upper left')
ax_L.grid(True, linestyle=':', alpha=0.6)

# Текст статистики L
stats_text_L = ax_L.text(0.05, 0.05, '', transform=ax_L.transAxes, fontsize=10, 
                         bbox=dict(facecolor='white', alpha=0.9, edgecolor='blue'))

# === ГРАФИК 2: ОЛЕИНОВАЯ (O vs EF_O) ===
# Эксперимент
ax_O.scatter(O_conc, EF_O_exp, color='red', marker='s', s=60, label='Exp Data', alpha=0.6)
# Модель
scat_O_model = ax_O.scatter(O_conc, saturation_model(O_conc, init_AO, init_BO), 
                            color='orange', marker='o', s=60, label='Model Points', edgecolors='red')
# Линия тренда
line_O, = ax_O.plot(x_range, saturation_model(x_range, init_AO, init_BO), color='red', alpha=0.4)

ax_O.set_title('Олеиновая: EF vs Концентрация (SN123)')
ax_O.set_xlabel('Концентрация O (%)')
ax_O.set_ylabel('EF_O')
ax_O.legend(loc='upper right')
ax_O.grid(True, linestyle=':', alpha=0.6)

# Текст статистики O
stats_text_O = ax_O.text(0.05, 0.05, '', transform=ax_O.transAxes, fontsize=10, 
                         bbox=dict(facecolor='white', alpha=0.9, edgecolor='red'))

# --- ПОДПИСИ ID ---
labels = []
# Для L
for i, txt in enumerate(ids):
    l = ax_L.annotate(txt, (L_conc[i], EF_L_exp[i]), xytext=(3, 3), textcoords='offset points', 
                      fontsize=8, color='darkblue', visible=False, fontweight='bold')
    labels.append(l)
# Для O
for i, txt in enumerate(ids):
    l = ax_O.annotate(txt, (O_conc[i], EF_O_exp[i]), xytext=(3, 3), textcoords='offset points', 
                      fontsize=8, color='darkred', visible=False, fontweight='bold')
    labels.append(l)

# --- ФУНКЦИЯ ОБНОВЛЕНИЯ СТАТИСТИКИ ---
def update_stats(cL, cO):
    # --- Линолевая ---
    # Эксперимент
    cov_L_exp = np.cov(L_conc, EF_L_exp)[0, 1]
    corr_L_exp = np.corrcoef(L_conc, EF_L_exp)[0, 1]
    # Модель
    cov_L_mod = np.cov(L_conc, cL)[0, 1]
    corr_L_mod = np.corrcoef(L_conc, cL)[0, 1] if np.std(cL) > 0 else 0
    
    text_L = (f"EXPERIMENT:\n"
              f"  Cov = {cov_L_exp:.1f}\n"
              f"  Corr = {corr_L_exp:.3f}\n\n"
              f"MODEL:\n"
              f"  Cov = {cov_L_mod:.1f}\n"
              f"  Corr = {corr_L_mod:.3f}")
    stats_text_L.set_text(text_L)

    # --- Олеиновая ---
    # Эксперимент
    cov_O_exp = np.cov(O_conc, EF_O_exp)[0, 1]
    corr_O_exp = np.corrcoef(O_conc, EF_O_exp)[0, 1]
    # Модель
    cov_O_mod = np.cov(O_conc, cO)[0, 1]
    corr_O_mod = np.corrcoef(O_conc, cO)[0, 1] if np.std(cO) > 0 else 0
    
    text_O = (f"EXPERIMENT:\n"
              f"  Cov = {cov_O_exp:.1f}\n"
              f"  Corr = {corr_O_exp:.3f}\n\n"
              f"MODEL:\n"
              f"  Cov = {cov_O_mod:.1f}\n"
              f"  Corr = {corr_O_mod:.3f}")
    stats_text_O.set_text(text_O)

# Начальный расчет
calc_L_init = saturation_model(L_conc, init_AL, init_BL)
calc_O_init = saturation_model(O_conc, init_AO, init_BO)
update_stats(calc_L_init, calc_O_init)

# --- СЛАЙДЕРЫ ---
axcolor = 'lightgoldenrodyellow'
ax_AL = plt.axes([0.10, 0.15, 0.35, 0.03], facecolor=axcolor)
ax_BL = plt.axes([0.10, 0.10, 0.35, 0.03], facecolor=axcolor)
ax_AO = plt.axes([0.55, 0.15, 0.35, 0.03], facecolor=axcolor)
ax_BO = plt.axes([0.55, 0.10, 0.35, 0.03], facecolor=axcolor)

s_AL = Slider(ax_AL, 'Lin A', 20.0, 80.0, valinit=init_AL, valstep=0.1, color='lightblue')
s_BL = Slider(ax_BL, 'Lin B', 0.1, 20.0, valinit=init_BL, valstep=0.1, color='lightblue')
s_AO = Slider(ax_AO, 'Ole A', 20.0, 100.0, valinit=init_AO, valstep=0.1, color='salmon')
s_BO = Slider(ax_BO, 'Ole B', 1.0, 100.0, valinit=init_BO, valstep=0.1, color='salmon')

def update(val):
    al, bl = s_AL.val, s_BL.val
    ao, bo = s_AO.val, s_BO.val
    
    # Расчет новых значений в точках
    new_cL = saturation_model(L_conc, al, bl)
    new_cO = saturation_model(O_conc, ao, bo)
    
    # Обновление линий тренда
    line_L.set_ydata(saturation_model(x_range, al, bl))
    line_O.set_ydata(saturation_model(x_range, ao, bo))
    
    # Обновление точек модели
    scat_L_model.set_offsets(np.c_[L_conc, new_cL])
    scat_O_model.set_offsets(np.c_[O_conc, new_cO])
    
    # Обновление статистики
    update_stats(new_cL, new_cO)
    
    fig.canvas.draw_idle()

s_AL.on_changed(update)
s_BL.on_changed(update)
s_AO.on_changed(update)
s_BO.on_changed(update)

# --- ЧЕКБОКС ДЛЯ ID ---
ax_check = plt.axes([0.85, 0.025, 0.1, 0.05], frameon=False)
check = CheckButtons(ax_check, ['IDs'], [False])

def toggle_labels(label):
    status = check.get_status()[0]
    for lbl in labels:
        lbl.set_visible(status)
    fig.canvas.draw_idle()

check.on_clicked(toggle_labels)

# Кнопка сброса
resetax = plt.axes([0.45, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
def reset(event):
    s_AL.reset()
    s_BL.reset()
    s_AO.reset()
    s_BO.reset()
button.on_clicked(reset)

plt.show()