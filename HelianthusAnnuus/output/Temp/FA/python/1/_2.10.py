import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, CheckButtons, RadioButtons, TextBox
from scipy.optimize import curve_fit

# --- 1. Данные ---
samples = ['2233', '2699', '2776', '3110', '3384', '3599', '3675', '3714', 'Buzuluk', 
           'Commodity', 'High linoleic', 'High oleic', 'High palmitic, high linoleic', 
           'High palmitic, high oleic', 'High stearic, high oleic']

L_sn123_all = np.array([40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 64.0, 58.7, 76.0, 2.1, 46.8, 3.5, 2.0])
L_2_all     = np.array([49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 84.1, 65.7, 76.9, 1.4, 67.8, 2.8, 0.6])
O_sn123_all = np.array([44.1, 41.3, 42.8, 84.6, 36.2, 88.5, 37.1, 37.7, 24.1, 27.8, 13.3, 91.5, 17.1, 59.8, 79.1])
O_2_all     = np.array([50.0, 38.6, 41.9, 97.9, 27.5, 98.9, 34.4, 33.9, 14.3, 31.5, 18.9, 96.6, 24.9, 93.4, 95.9])

n_orig = 9
with np.errstate(divide='ignore', invalid='ignore'):
    EF_L_all = L_2_all / L_sn123_all
    EF_O_all = O_2_all / O_sn123_all

# --- 2. Модели ---
def smooth_haldane_ef(x, A, B, C, D):
    """
    A, B, C - стандартные параметры
    D - степень (ранее была фиксирована 1.5)
    """
    x_safe = np.maximum(x, 1e-6)
    # Защита от переполнения степени, если введут огромное число
    try:
        term = x_safe**D
    except:
        term = x_safe
    return (A * x_safe) / (B + x_safe + (term / C))

def michaelis_ef_growing(x, A, B): return (A * x) / (B + x)

# --- 3. Функция подбора ---
def perform_fit(use_all=True):
    idx_L = np.isfinite(EF_L_all)
    idx_O = np.isfinite(EF_O_all)
    if not use_all:
        mask = np.zeros_like(EF_L_all, dtype=bool)
        mask[:n_orig] = True
        idx_L &= mask
        idx_O &= mask
    
    # Haldane Linoleic (4 параметра: A, B, C, D)
    try:
        # bounds=([low], [high]) - границы для автоподбора, но вручную можно вводить что угодно
        pL, _ = curve_fit(smooth_haldane_ef, L_sn123_all[idx_L], EF_L_all[idx_L], 
                          p0=[100, 20, 20, 1.5], 
                          bounds=([0, 0, 0, 0], [1000, 1000, 1000, 1000]))
    except: 
        pL = [100, 20, 20, 1.5]
    
    # MM Growing Linoleic
    try:
        pL_mm, _ = curve_fit(michaelis_ef_growing, L_sn123_all[idx_L], EF_L_all[idx_L], 
                             p0=[2.0, 10.0], bounds=([0, 0], [1000, 1000]))
    except: pL_mm = [2.0, 10.0]
    
    # MM Fading Oleic
    try:
        pO, _ = curve_fit(michaelis_ef_growing, O_sn123_all[idx_O], EF_O_all[idx_O], 
                          p0=[150, 50], bounds=([0, 0], [1000, 1000]))
    except: pO = [150, 50]
    
    return pL, pL_mm, pO

# Первичный расчет
best_h, best_mm, best_o = perform_fit(use_all=True)

# --- 4. Графики ---
x_range = np.linspace(0.1, 100, 400)
fig, axs = plt.subplots(2, 2, figsize=(15, 11))
# Увеличим отступ снизу для размещения текстовых полей
plt.subplots_adjust(bottom=0.40, hspace=0.35, wspace=0.2)
(ax_L_abs, ax_O_abs), (ax_L_ef, ax_O_ef) = axs

def create_labels(ax, x, y, labels):
    return [ax.text(x[i], y[i], labels[i], fontsize=7, visible=False, fontweight='bold') for i in range(len(labels))]

texts_list = [create_labels(ax_L_abs, L_sn123_all, L_2_all, samples),
              create_labels(ax_O_abs, O_sn123_all, O_2_all, samples),
              create_labels(ax_L_ef, L_sn123_all, EF_L_all, samples),
              create_labels(ax_O_ef, O_sn123_all, EF_O_all, samples)]

# Отрисовка линий (инициализация)
ax_L_abs.scatter(L_sn123_all[:n_orig], L_2_all[:n_orig], c='blue', label='My Exp')
ax_L_abs.scatter(L_sn123_all[n_orig:], L_2_all[n_orig:], c='green', marker='s', label='Others')
line_L_abs, = ax_L_abs.plot(x_range, x_range * smooth_haldane_ef(x_range, *best_h), 'r-')
line_L_abs_mm, = ax_L_abs.plot(x_range, x_range * michaelis_ef_growing(x_range, *best_mm), 'g--')
ax_L_abs.legend()

ax_L_ef.scatter(L_sn123_all[:n_orig], EF_L_all[:n_orig], c='blue')
ax_L_ef.scatter(L_sn123_all[n_orig:], EF_L_all[n_orig:], c='green', marker='s')
line_L_ef, = ax_L_ef.plot(x_range, smooth_haldane_ef(x_range, *best_h), 'r-')
line_L_ef_mm, = ax_L_ef.plot(x_range, michaelis_ef_growing(x_range, *best_mm), 'g--')
ax_L_ef.set_ylim(0, 2.5)

ax_O_abs.scatter(O_sn123_all[:n_orig], O_2_all[:n_orig], c='orange')
ax_O_abs.scatter(O_sn123_all[n_orig:], O_2_all[n_orig:], c='green', marker='s')
line_O_abs, = ax_O_abs.plot(x_range, x_range * michaelis_ef_growing(x_range, *best_o), 'purple')

ax_O_ef.scatter(O_sn123_all[:n_orig], EF_O_all[:n_orig], c='orange')
ax_O_ef.scatter(O_sn123_all[n_orig:], EF_O_all[n_orig:], c='green', marker='s')
line_O_ef, = ax_O_ef.plot(x_range, michaelis_ef_growing(x_range, *best_o), 'purple')
ax_O_ef.set_ylim(0, 3.0)

# --- 5. Виджеты (TextBox вместо Slider) ---

# Функция для создания бокса
def make_box(rect, label, val):
    ax = plt.axes(rect)
    # initial принимает строку
    box = TextBox(ax, label, initial=str(round(val, 3)), label_pad=0.05)
    return box

# Координаты: [left, bottom, width, height]
# Левая колонка (Linoleic Haldane)
box_AL = make_box([0.20, 0.32, 0.1, 0.025], 'Lin Hald A: ', best_h[0])
box_BL = make_box([0.20, 0.29, 0.1, 0.025], 'Lin Hald B: ', best_h[1])
box_CL = make_box([0.20, 0.26, 0.1, 0.025], 'Lin Hald C: ', best_h[2])
box_DL = make_box([0.20, 0.23, 0.1, 0.025], 'Lin Hald Exp: ', best_h[3])

# Левая колонка ниже (Linoleic MM)
box_AL_MM = make_box([0.20, 0.18, 0.1, 0.025], 'Lin MM A: ', best_mm[0])
box_BL_MM = make_box([0.20, 0.15, 0.1, 0.025], 'Lin MM B: ', best_mm[1])

# Правая колонка (Oleic MM)
box_AO = make_box([0.65, 0.30, 0.1, 0.025], 'Ole MM A: ', best_o[0])
box_BO = make_box([0.65, 0.27, 0.1, 0.025], 'Ole MM B: ', best_o[1])

# Остальные элементы управления
radio_ax = plt.axes([0.42, 0.08, 0.15, 0.06], facecolor='#f0f0f0')
radio = RadioButtons(radio_ax, ('All Data', 'My Exp (9)'))

rax = plt.axes([0.15, 0.02, 0.7, 0.04], frameon=False)
check = CheckButtons(rax, ('L-Abs ID', 'O-Abs ID', 'L-EF ID', 'O-EF ID'), (False, False, False, False))

btn_res = Button(plt.axes([0.45, 0.01, 0.1, 0.03]), 'AUTO-FIT')

# --- Логика обновления ---

def get_val(box):
    """Безопасное получение числа из текста"""
    try:
        return float(box.text)
    except ValueError:
        return 1.0 # Возврат безопасного значения при ошибке ввода

def update(text):
    # Считываем значения из всех боксов
    h_A = get_val(box_AL)
    h_B = get_val(box_BL)
    h_C = get_val(box_CL)
    h_D = get_val(box_DL) # Степень
    
    mm_L_A = get_val(box_AL_MM)
    mm_L_B = get_val(box_BL_MM)
    
    mm_O_A = get_val(box_AO)
    mm_O_B = get_val(box_BO)

    # Обновляем графики
    # Linoleic Haldane
    y_haldane = smooth_haldane_ef(x_range, h_A, h_B, h_C, h_D)
    line_L_ef.set_ydata(y_haldane)
    line_L_abs.set_ydata(x_range * y_haldane)
    
    # Linoleic MM
    y_mm_l = michaelis_ef_growing(x_range, mm_L_A, mm_L_B)
    line_L_ef_mm.set_ydata(y_mm_l)
    line_L_abs_mm.set_ydata(x_range * y_mm_l)
    
    # Oleic MM
    y_mm_o = michaelis_ef_growing(x_range, mm_O_A, mm_O_B)
    line_O_ef.set_ydata(y_mm_o)
    line_O_abs.set_ydata(x_range * y_mm_o)
    
    fig.canvas.draw_idle()

def apply_fit(event):
    bh, bmm, bo = perform_fit(use_all=(radio.value_selected == 'All Data'))
    
    # Обновляем значения в боксах (событие on_submit не вызывается автоматически при set_val,
    # поэтому вызываем update вручную или полагаемся на то, что пользователь нажмет Enter, 
    # но лучше обновить график сразу)
    
    # Отключаем callback временно, чтобы не перерисовывать 8 раз подряд
    boxes = [box_AL, box_BL, box_CL, box_DL, box_AL_MM, box_BL_MM, box_AO, box_BO]
    vals = [*bh, *bmm, *bo]
    
    for box, val in zip(boxes, vals):
        box.set_val(str(round(val, 4)))
    
    update('') # Принудительное обновление графиков

# Привязываем события
# on_submit срабатывает при нажатии Enter в поле ввода
box_AL.on_submit(update)
box_BL.on_submit(update)
box_CL.on_submit(update)
box_DL.on_submit(update)
box_AL_MM.on_submit(update)
box_BL_MM.on_submit(update)
box_AO.on_submit(update)
box_BO.on_submit(update)

btn_res.on_clicked(apply_fit)
check.on_clicked(lambda lab: [ [t.set_visible(not t.get_visible()) for t in texts_list[i]] 
                               for i, l in enumerate(['L-Abs ID', 'O-Abs ID', 'L-EF ID', 'O-EF ID']) if l==lab ] and fig.canvas.draw_idle())

plt.show()