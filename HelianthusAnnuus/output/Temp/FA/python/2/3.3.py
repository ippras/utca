import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.optimize import curve_fit

# --- 1. Данные ---
x_data = np.array([1.1, 1.8, 40.9, 44.2, 46.2, 50.8, 51.7, 53.5, 64.0,
                   58.7, 76.0, 2.1, 46.8, 3.5, 2.0])
y_data = np.array([38.6, 37.2, 37.9, 32.6, 31.2, 30.0, 30.9, 25.3, 19.8,
                   37.8, 47.4, 35.2, 48.5, 52.1, 40.4])

# 37.8, 47.4, 35.2, 48.5, 52.1, 40.4
# 31.5/27.8*100/3=round(37.769784172661870503*10)=37.8
# 18.9/13.3*100/3=round(47.368421052631578947*10)=47.4
# 96.6/91.5*100/3=round(35.191256830601092897*10)=35.2
# 24.9/17.1*100/3=round(48.53801169590643275*10)=48.5
# 93.4/59.8*100/3=round(52.062430323299888517*10)=52.1
# 95.9/79.1*100/3=round(40.412979351032448377*10)=40.4

# --- 2. Модель (Softplus) ---
def model_func(x, A, B, C, D):
    # A = Уровень плато
    # B = Наклон спада
    # C = Резкость изгиба
    # D = Сдвиг по X
    return A - B * np.log(1 + np.exp(C * (x - D)))

# --- 3. Настройка графика ---
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(left=0.1, bottom=0.35) # Оставляем место внизу для ползунков

# Начальные значения
init_A, init_B, init_C, init_D = 39.0, 1.5, 0.5, 38.0

# Рисуем данные
ax.scatter(x_data, y_data, color='blue', s=60, label='Данные', zorder=5)

# Рисуем начальную линию
x_line = np.linspace(0, 80, 200)
y_line = model_func(x_line, init_A, init_B, init_C, init_D)
line, = ax.plot(x_line, y_line, color='red', lw=2, label='Модель')

ax.set_title(f'Oleic EF Approximation')
ax.set_xlabel('Linoleic SN-1,2,3 (%)')
ax.set_ylabel('Oleic EF')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()
ax.set_ylim(10, 45)

# --- 4. Создание ползунков (Matplotlib Widgets) ---
# Координаты [left, bottom, width, height]
ax_A = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_B = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_C = plt.axes([0.25, 0.10, 0.65, 0.03])
ax_D = plt.axes([0.25, 0.05, 0.65, 0.03])

slider_A = Slider(ax_A, 'A (Плато)', 30.0, 50.0, valinit=init_A)
slider_B = Slider(ax_B, 'B (Наклон)', 0.1, 5.0, valinit=init_B)
slider_C = Slider(ax_C, 'C (Резкость)', 0.01, 2.0, valinit=init_C)
slider_D = Slider(ax_D, 'D (Сдвиг X)', 20.0, 60.0, valinit=init_D)

# --- 5. Функция обновления при движении ползунков ---
def update(val):
    A = slider_A.val
    B = slider_B.val
    C = slider_C.val
    D = slider_D.val
    
    # Пересчитываем Y
    new_y = model_func(x_line, A, B, C, D)
    line.set_ydata(new_y)
    
    # Считаем ошибку (MSE) для заголовка
    y_pred = model_func(x_data, A, B, C, D)
    mse = np.mean((y_data - y_pred)**2)
    ax.set_title(f'MSE Error: {mse:.2f}')
    
    fig.canvas.draw_idle()

# Привязываем функцию к ползункам
slider_A.on_changed(update)
slider_B.on_changed(update)
slider_C.on_changed(update)
slider_D.on_changed(update)

# --- 6. Кнопка "Авто-подбор" ---
ax_button = plt.axes([0.8, 0.25, 0.1, 0.04])
btn = Button(ax_button, 'Auto Fit', color='lightgreen', hovercolor='0.975')

def auto_fit(event):
    # Берем текущие значения как стартовые
    p0 = [slider_A.val, slider_B.val, slider_C.val, slider_D.val]
    try:
        # Подбираем параметры
        popt, _ = curve_fit(model_func, x_data, y_data, p0=p0, maxfev=10000)
        
        # Обновляем ползунки (это автоматически вызовет update)
        slider_A.set_val(popt[0])
        slider_B.set_val(popt[1])
        slider_C.set_val(popt[2])
        slider_D.set_val(popt[3])
        print(f"Найдены параметры: A={popt[0]:.2f}, B={popt[1]:.2f}, C={popt[2]:.2f}, D={popt[3]:.2f}")
    except Exception as e:
        print(f"Ошибка подбора: {e}")

btn.on_clicked(auto_fit)

plt.show()