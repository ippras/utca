import matplotlib.pyplot as plt
import numpy as np

# --- 1. Исходные данные (из таблицы) ---
# Linoleic SN-1,2,3 (%)
x_data = np.array([1.1, 1.8, 40.9, 44.2, 46.2, 50.8, 51.7, 53.5, 64.0])
# Oleic EF (фактические значения)
y_data = np.array([38.6, 37.2, 37.9, 32.6, 31.2, 30.0, 30.9, 25.3, 19.8])
labels = ['3110', '3599', '2233', '2776', '2699', '3714', '3675', '3384', 'Бузулук']

# --- 2. Новая единая формула (Softplus) ---
def model_smooth(x):
    # EF = 39 - 1.5 * ln(1 + e^(0.5 * (x - 38)))
    return 39 - 1.5 * np.log(1 + np.exp(0.5 * (x - 38)))

# Создаем плавную линию для графика (от 0 до 70%)
x_line = np.linspace(0, 70, 200)
y_line = model_smooth(x_line)

# --- 3. Построение графика ---
plt.figure(figsize=(10, 6))

# Рисуем линию аппроксимации
plt.plot(x_line, y_line, color='crimson', linewidth=2.5, label='Аппроксимация (Единая формула)')

# Рисуем реальные точки
plt.scatter(x_data, y_data, color='navy', s=80, zorder=5, label='Экспериментальные данные')

# Подписи точек (опционально, чтобы видеть где какой образец)
for i, txt in enumerate(labels):
    # Сдвигаем подписи немного, чтобы не перекрывали точки
    plt.annotate(txt, (x_data[i], y_data[i]), xytext=(5, 5), textcoords='offset points', fontsize=8)

# --- 4. Оформление ---
plt.title('Аппроксимация Oleic EF единой формулой', fontsize=14)
plt.xlabel('Linoleic SN-1,2,3 (%)', fontsize=12)
plt.ylabel('Oleic EF', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Добавляем пояснение формулы на график
formula_text = r"$EF \approx 39 - 1.5 \cdot \ln(1 + e^{0.5 \cdot (x - 38)})$"
plt.text(5, 25, formula_text, fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='crimson'))

plt.legend()
plt.tight_layout()

# Показать график
plt.show()