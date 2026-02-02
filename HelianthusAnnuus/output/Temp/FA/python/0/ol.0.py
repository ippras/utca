import matplotlib.pyplot as plt
import numpy as np

# --- 1. Входные данные ---
# Формат: [ID, L_conc, O_conc, EF_O_val, EF_O_err, EF_L_val, EF_L_err]
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

# Распаковка данных
ids = [row[0] for row in data]
L_conc = np.array([row[1] for row in data])
O_conc = np.array([row[2] for row in data])

EF_O_exp = np.array([row[3] for row in data])
EF_O_err = np.array([row[4] for row in data])

EF_L_exp = np.array([row[5] for row in data])
EF_L_err = np.array([row[6] for row in data])

# --- 2. Формулы ---
def formula_linoleic(x):
    # EF = 46 * x / (3 + x)
    return (46 * x) / (3 + x)

def formula_oleic(x):
    # EF = 60 * x / (48 + x)
    return (60 * x) / (48 + x)

# --- 3. Подготовка линий тренда ---
x_range = np.linspace(0, 100, 200) # от 0 до 100%
y_linoleic = formula_linoleic(x_range)
y_oleic = formula_oleic(x_range)

# --- 4. Построение графика ---
plt.figure(figsize=(12, 8))

# --- ЛИНОЛЕВАЯ КИСЛОТА (Синий цвет) ---
# Теоретическая кривая
plt.plot(x_range, y_linoleic, color='blue', linestyle='-', linewidth=2, label=r'Линолевая (модель): $\frac{46 \cdot x}{3 + x}$')
# Экспериментальные точки
plt.errorbar(L_conc, EF_L_exp, yerr=EF_L_err, fmt='o', color='blue', ecolor='black', capsize=4, label='Линолевая (эксперимент)')

# --- ОЛЕИНОВАЯ КИСЛОТА (Красный цвет) ---
# Теоретическая кривая
plt.plot(x_range, y_oleic, color='red', linestyle='--', linewidth=2, label=r'Олеиновая (модель): $\frac{60 \cdot x}{48 + x}$')
# Экспериментальные точки
plt.errorbar(O_conc, EF_O_exp, yerr=EF_O_err, fmt='s', color='red', ecolor='black', capsize=4, label='Олеиновая (эксперимент)')

# --- Оформление ---
plt.title('Сравнение моделей EF для Линолевой и Олеиновой кислот', fontsize=14)
plt.xlabel('Концентрация кислоты в образце (%)', fontsize=12)
plt.ylabel('Значение EF', fontsize=12)
plt.grid(True, which='both', linestyle=':', alpha=0.7)
plt.legend(fontsize=11)

# Подписи ID точек (опционально, чтобы видеть где какой образец)
# Для Линолевой
for i, txt in enumerate(ids):
    plt.annotate(txt, (L_conc[i], EF_L_exp[i]), xytext=(3, 3), textcoords='offset points', fontsize=7, color='blue', alpha=0.7)

# Для Олеиновой
for i, txt in enumerate(ids):
    plt.annotate(txt, (O_conc[i], EF_O_exp[i]), xytext=(3, 3), textcoords='offset points', fontsize=7, color='red', alpha=0.7)

plt.tight_layout()
plt.show()

# --- 5. Расчет ошибки (MAE) для консоли ---
calc_L = formula_linoleic(L_conc)
mae_L = np.mean(np.abs(calc_L - EF_L_exp))

calc_O = formula_oleic(O_conc)
mae_O = np.mean(np.abs(calc_O - EF_O_exp))

print(f"Средняя абсолютная ошибка (MAE) для Линолевой: {mae_L:.2f}")
print(f"Средняя абсолютная ошибка (MAE) для Олеиновой: {mae_O:.2f}")