import matplotlib.pyplot as plt
import numpy as np

# 1. Входные данные из таблицы
# Формат: [ID, L, O, Exp_Value, Exp_Error]
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

# Распаковка данных в списки для удобства
ids = [row[0] for row in data]
L_vals = np.array([row[1] for row in data])
O_vals = np.array([row[2] for row in data])
Exp_vals = np.array([row[3] for row in data])
Exp_errs = np.array([row[4] for row in data])

# 2. Функция расчета по формуле
def calculate_ef_l(l, o):
    # EF_L = (48.3 * L) / (3 + L + 0.1 * O)
    return (48.3 * l) / (3 + l + 0.1 * o)

# Расчет теоретических значений для каждой точки
Calc_vals = calculate_ef_l(L_vals, O_vals)

# 3. Подготовка теоретической кривой (для фона)
# Поскольку формула зависит от двух переменных (L и O), 
# для построения гладкой линии предположим, что L + O ≈ const.
# Средняя сумма L+O в ваших данных около 88.
avg_sum = np.mean(L_vals + O_vals) 
L_line = np.linspace(0, 70, 100)
O_line = avg_sum - L_line # Примерная зависимость O от L
O_line[O_line < 0] = 0    # O не может быть отрицательным
EF_line = calculate_ef_l(L_line, O_line)

# 4. Построение графика
plt.figure(figsize=(12, 7))

# Рисуем теоретическую кривую (тренд)
plt.plot(L_line, EF_line, color='gray', linestyle='--', alpha=0.5, label=f'Теоретический тренд (при L+O≈{avg_sum:.0f})')

# Рисуем расчетные точки (по формуле)
plt.scatter(L_vals, Calc_vals, color='blue', marker='x', s=80, zorder=5, label='Расчет по формуле')

# Рисуем экспериментальные точки с погрешностями
plt.errorbar(L_vals, Exp_vals, yerr=Exp_errs, fmt='o', color='red', ecolor='black', capsize=5, zorder=10, label='Эксперимент ± ошибка')

# Подписи точек (ID)
for i, txt in enumerate(ids):
    # Сдвигаем текст немного, чтобы не перекрывал точки
    plt.annotate(txt, (L_vals[i], Exp_vals[i]), xytext=(5, 5), textcoords='offset points', fontsize=8)

# Настройки осей и легенды
plt.title(r'Сравнение формулы $EF_L = \frac{48.3 \cdot L}{3 + L + 0.1 \cdot O}$ с экспериментом', fontsize=14)
plt.xlabel('Содержание Линолевой кислоты (L)', fontsize=12)
plt.ylabel('EF_L', fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Отображение
plt.tight_layout()
plt.show()