# ковариация и корреляция нужны не эксперимент от расчета, а линолевая от олеиновой

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
import numpy as np

# --- 1. Данные ---
data = [
    ("2233",    40.9, 44.1, 37.9, 0.66, 40.6, 0.98),
    ("2699",    46.2, 41.3, 31.2, 0.22, 44.1, 0.54),
    ("2776",    44.2, 42.8, 32.6, 1.25, 41.6, 1.56),
    ("3110",    1.1,  84.6, 38.6, 0.17, 0.0,  0.0),
    ("3384",    53.5, 36.2, 25.3, 1.14, 44.6, 0.64),
    ("3599",    1.8,  88.5, 37.2, 0.17, 17.1, 0.72),
    ("3675",    51.7, 37.1, 30.9, 0.38, 41.6, 0.65),
    ("3714",    50.8, 37.7, 30.0, 2.40, 42.4, 2.21),
    ("Бузулук", 64.0, 24.1, 19.8, 2.47, 43.8, 1.40)
]

ids = [row[0] for row in data]
L_conc = np.array([row[1] for row in data])
O_conc = np.array([row[2] for row in data])
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
fig, (ax_fit, ax_cov) = plt.subplots(1, 2, figsize=(16, 7))
plt.subplots_adjust(left=0.05, bottom=0.30, right=0.95, top=0.90, wspace=0.2)

# === ГРАФИК 1: Подгонка (Слева) ===
ax_fit.errorbar(L_conc, EF_L_exp, yerr=[row[6] for row in data], fmt='o', color='blue', alpha=0.4, label='Exp Lin')
ax_fit.errorbar(O_conc, EF_O_exp, yerr=[row[4] for row in data], fmt='s', color='red', alpha=0.4, label='Exp Ole')

line_L, = ax_fit.plot(x_range, saturation_model(x_range, init_AL, init_BL), color='blue', linewidth=2, label='Model Lin')
line_O, = ax_fit.plot(x_range, saturation_model(x_range, init_AO, init_BO), color='red', linewidth=2, linestyle='--', label='Model Ole')

ax_fit.set_title('Модель насыщения (EF vs Концентрация)')
ax_fit.set_xlabel('Концентрация (%)')
ax_fit.set_ylabel('EF')
ax_fit.legend(loc='upper left')
ax_fit.grid(True, linestyle=':', alpha=0.6)
ax_fit.set_ylim(0, 65)

# === ГРАФИК 2: Ковариация L vs O (Справа) ===
# Расчет начальных точек модели
calc_L = saturation_model(L_conc, init_AL, init_BL)
calc_O = saturation_model(O_conc, init_AO, init_BO)

# Экспериментальные точки (неподвижные)
ax_cov.scatter(EF_O_exp, EF_L_exp, color='black', marker='s', s=50, label='Эксперимент', zorder=5)

# Расчетные точки (подвижные)
scat_model = ax_cov.scatter(calc_O, calc_L, color='limegreen', marker='o', s=60, label='Модель', zorder=6)

# Линии, соединяющие эксперимент и модель (ошибки)
lines_connect = []
for i in range(len(ids)):
    l, = ax_cov.plot([EF_O_exp[i], calc_O[i]], [EF_L_exp[i], calc_L[i]], color='gray', alpha=0.5, linewidth=1)
    lines_connect.append(l)

ax_cov.set_title('Взаимосвязь: Линолевая vs Олеиновая')
ax_cov.set_xlabel('EF Олеиновая (O)')
ax_cov.set_ylabel('EF Линолевая (L)')
ax_cov.legend()
ax_cov.grid(True, linestyle=':', alpha=0.6)
ax_cov.set_xlim(0, 60)
ax_cov.set_ylim(0, 60)

# Текст статистики
stats_text = ax_cov.text(0.02, 0.02, '', transform=ax_cov.transAxes, fontsize=10, 
                         bbox=dict(facecolor='white', alpha=0.9))

# --- ПОДПИСИ ID ---
labels_fit = []
labels_cov = []

for i, txt in enumerate(ids):
    # Слева
    l1 = ax_fit.annotate(txt, (L_conc[i], EF_L_exp[i]), xytext=(3, 3), textcoords='offset points', fontsize=8, color='blue', visible=False)
    l2 = ax_fit.annotate(txt, (O_conc[i], EF_O_exp[i]), xytext=(3, 3), textcoords='offset points', fontsize=8, color='red', visible=False)
    labels_fit.extend([l1, l2])
    
    # Справа (крепим к экспериментальным точкам, так как они стабильны)
    l3 = ax_cov.annotate(txt, (EF_O_exp[i], EF_L_exp[i]), xytext=(5, 5), textcoords='offset points', fontsize=9, color='black', visible=False, fontweight='bold')
    labels_cov.append(l3)

# --- ФУНКЦИЯ ОБНОВЛЕНИЯ ---
def update_stats(cL, cO):
    # Статистика Эксперимента (const)
    cov_exp = np.cov(EF_L_exp, EF_O_exp)[0, 1]
    corr_exp = np.corrcoef(EF_L_exp, EF_O_exp)[0, 1]
    
    # Статистика Модели (dynamic)
    # Если дисперсия 0, корреляция nan, обрабатываем это
    if np.std(cL) == 0 or np.std(cO) == 0:
        corr_mod = 0
    else:
        corr_mod = np.corrcoef(cL, cO)[0, 1]
    cov_mod = np.cov(cL, cO)[0, 1]
    
    text = (f"EXPERIMENT (Black):\n"
            f"  Cov(L, O) = {cov_exp:.1f}\n"
            f"  Corr(r)   = {corr_exp:.3f}\n\n"
            f"MODEL (Green):\n"
            f"  Cov(L, O) = {cov_mod:.1f}\n"
            f"  Corr(r)   = {corr_mod:.3f}")
    stats_text.set_text(text)

update_stats(calc_L, calc_O)

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
    
    # 1. Обновляем линии слева
    line_L.set_ydata(saturation_model(x_range, al, bl))
    line_O.set_ydata(saturation_model(x_range, ao, bo))
    
    # 2. Пересчитываем точки
    new_cL = saturation_model(L_conc, al, bl)
    new_cO = saturation_model(O_conc, ao, bo)
    
    # 3. Обновляем точки справа
    scat_model.set_offsets(np.c_[new_cO, new_cL])
    
    # 4. Обновляем соединительные линии
    for i, line in enumerate(lines_connect):
        line.set_data([EF_O_exp[i], new_cO[i]], [EF_L_exp[i], new_cL[i]])
            
    # 5. Обновляем статистику
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
    for lbl in labels_fit + labels_cov:
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
