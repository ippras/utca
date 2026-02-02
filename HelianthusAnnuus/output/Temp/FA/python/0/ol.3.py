# добавь графики ковариации и корреляции

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

# Начальные параметры
init_AL, init_BL = 46.0, 3.0
init_AO, init_BO = 60.0, 48.0
x_range = np.linspace(0, 100, 200)

# --- 3. Настройка фигуры (2 графика) ---
fig, (ax_main, ax_corr) = plt.subplots(1, 2, figsize=(15, 7))
plt.subplots_adjust(left=0.05, bottom=0.30, right=0.95, top=0.90, wspace=0.2)

# === ГРАФИК 1: Основной (Концентрация vs EF) ===
# Эксперимент
ax_main.errorbar(L_conc, EF_L_exp, yerr=EF_L_err, fmt='o', color='blue', ecolor='black', capsize=3, alpha=0.5, label='Exp Lin')
ax_main.errorbar(O_conc, EF_O_exp, yerr=EF_O_err, fmt='s', color='red', ecolor='black', capsize=3, alpha=0.5, label='Exp Ole')

# Линии моделей
line_L, = ax_main.plot(x_range, saturation_model(x_range, init_AL, init_BL), color='blue', linewidth=2, label='Model Lin')
line_O, = ax_main.plot(x_range, saturation_model(x_range, init_AO, init_BO), color='red', linewidth=2, linestyle='--', label='Model Ole')

ax_main.set_title('Модель насыщения')
ax_main.set_xlabel('Концентрация (%)')
ax_main.set_ylabel('EF')
ax_main.legend(loc='upper left', fontsize=9)
ax_main.grid(True, linestyle=':', alpha=0.6)
ax_main.set_ylim(0, 65)

# === ГРАФИК 2: Корреляция (Exp vs Calc) ===
# Диагональ (идеал)
ax_corr.plot([0, 60], [0, 60], color='gray', linestyle='-', alpha=0.3, label='Идеал (y=x)')

# Расчет начальных точек
calc_L = saturation_model(L_conc, init_AL, init_BL)
calc_O = saturation_model(O_conc, init_AO, init_BO)

# Точки корреляции (scatter)
scat_corr_L = ax_corr.scatter(EF_L_exp, calc_L, color='blue', marker='o', alpha=0.7, label='Linoleic')
scat_corr_O = ax_corr.scatter(EF_O_exp, calc_O, color='red', marker='s', alpha=0.7, label='Oleic')

ax_corr.set_title('Корреляция: Эксперимент vs Расчет')
ax_corr.set_xlabel('Экспериментальное EF')
ax_corr.set_ylabel('Расчетное EF')
ax_corr.legend(loc='upper left', fontsize=9)
ax_corr.grid(True, linestyle=':', alpha=0.6)
ax_corr.set_xlim(0, 60)
ax_corr.set_ylim(0, 60)

# Текст статистики (Correlation & Covariance)
stats_text = ax_corr.text(0.05, 0.05, '', transform=ax_corr.transAxes, fontsize=10, 
                          bbox=dict(facecolor='white', alpha=0.8))

# --- ПОДПИСИ ID (для обоих графиков) ---
labels_main = []
labels_corr = []

for i, txt in enumerate(ids):
    # На основном графике
    l1 = ax_main.annotate(txt, (L_conc[i], EF_L_exp[i]), xytext=(3, 3), textcoords='offset points', fontsize=8, color='blue', visible=False)
    l2 = ax_main.annotate(txt, (O_conc[i], EF_O_exp[i]), xytext=(3, 3), textcoords='offset points', fontsize=8, color='red', visible=False)
    labels_main.extend([l1, l2])
    
    # На графике корреляции
    l3 = ax_corr.annotate(txt, (EF_L_exp[i], calc_L[i]), xytext=(3, 3), textcoords='offset points', fontsize=8, color='blue', visible=False)
    l4 = ax_corr.annotate(txt, (EF_O_exp[i], calc_O[i]), xytext=(3, 3), textcoords='offset points', fontsize=8, color='red', visible=False)
    labels_corr.extend([l3, l4])

# --- ФУНКЦИЯ ОБНОВЛЕНИЯ ---
def update_stats(cL, cO):
    # Корреляция Пирсона (r)
    r_L = np.corrcoef(EF_L_exp, cL)[0, 1] if np.std(cL) > 0 else 0
    r_O = np.corrcoef(EF_O_exp, cO)[0, 1] if np.std(cO) > 0 else 0
    
    # Ковариация (Cov)
    cov_L = np.cov(EF_L_exp, cL)[0, 1]
    cov_O = np.cov(EF_O_exp, cO)[0, 1]
    
    # MAE
    mae_L = np.mean(np.abs(cL - EF_L_exp))
    mae_O = np.mean(np.abs(cO - EF_O_exp))
    
    text = (f"Linoleic:\n  r = {r_L:.3f}\n  Cov = {cov_L:.1f}\n  MAE = {mae_L:.2f}\n\n"
            f"Oleic:\n  r = {r_O:.3f}\n  Cov = {cov_O:.1f}\n  MAE = {mae_O:.2f}")
    stats_text.set_text(text)

update_stats(calc_L, calc_O)

# --- СЛАЙДЕРЫ ---
axcolor = 'lightgoldenrodyellow'
# Linoleic
ax_AL = plt.axes([0.10, 0.15, 0.35, 0.03], facecolor=axcolor)
ax_BL = plt.axes([0.10, 0.10, 0.35, 0.03], facecolor=axcolor)
# Oleic
ax_AO = plt.axes([0.55, 0.15, 0.35, 0.03], facecolor=axcolor)
ax_BO = plt.axes([0.55, 0.10, 0.35, 0.03], facecolor=axcolor)

s_AL = Slider(ax_AL, 'Lin A', 20.0, 80.0, valinit=init_AL, valstep=0.1, color='lightblue')
s_BL = Slider(ax_BL, 'Lin B', 0.1, 20.0, valinit=init_BL, valstep=0.1, color='lightblue')
s_AO = Slider(ax_AO, 'Ole A', 20.0, 100.0, valinit=init_AO, valstep=0.1, color='salmon')
s_BO = Slider(ax_BO, 'Ole B', 1.0, 100.0, valinit=init_BO, valstep=0.1, color='salmon')

def update(val):
    al, bl = s_AL.val, s_BL.val
    ao, bo = s_AO.val, s_BO.val
    
    # 1. Обновляем линии на главном графике
    line_L.set_ydata(saturation_model(x_range, al, bl))
    line_O.set_ydata(saturation_model(x_range, ao, bo))
    
    # 2. Пересчитываем точки для корреляции
    new_cL = saturation_model(L_conc, al, bl)
    new_cO = saturation_model(O_conc, ao, bo)
    
    # 3. Обновляем scatter plot (нужно менять offsets)
    scat_corr_L.set_offsets(np.c_[EF_L_exp, new_cL])
    scat_corr_O.set_offsets(np.c_[EF_O_exp, new_cO])
    
    # 4. Обновляем позиции подписей на графике корреляции
    for i, lbl in enumerate(labels_corr):
        # Первые 9 - Linoleic, следующие 9 - Oleic
        if i < len(ids):
            lbl.xy = (EF_L_exp[i], new_cL[i])
        else:
            idx = i - len(ids)
            lbl.xy = (EF_O_exp[idx], new_cO[idx])
            
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
    for lbl in labels_main + labels_corr:
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