import matplotlib.pyplot as plt

# ==========================================
# 1. ВСТАВЬТЕ ДАННЫЕ ДЛЯ КОНКРЕТНОЙ КИСЛОТЫ (например, Linoleic)
# ==========================================

# Определение групп и цветов
def color(name):
    if name.startswith("VIR-"):
        return "red", "VIR"
    elif name.startswith("VNIIMK-"):
        return "green", "VNIIMK"
    elif name.startswith("RESKE-"):
        return "blue", "RESKE"
    else:
        return "orange", "Бузулук"

# Названия объектов (проб)
samples = [
    "Бузулук",
    "VIR-2233", "VIR-2699", "VIR-2776", "VIR-3110", "VIR-3384", "VIR-3599", "VIR-3675", "VIR-3714",
    "VNIIMK-1", "VNIIMK-2", "VNIIMK-3", "VNIIMK-4", "VNIIMK-5", "VNIIMK-6", "VNIIMK-7", "VNIIMK-8", "VNIIMK-9",
    'RESKE-Commodity', 'RESKE-HL', 'RESKE-HO', 'RESKE-HPHL', 'RESKE-HPHO', 'RESKE-HSHO'
]

# Значения выбранной кислоты во всех фракциях для этих объектов
sn123 = [
    64,
    40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8,
    61.4, 50, 32.7, 32.5, 32.9, 20.6, 18.5, 1.7, 1,
    58.7, 76.0, 2.1, 46.8, 3.5, 2.0
]
sn13  = [
    53.9,
    36.5, 38.7, 38.6, 1.6, 44.4, 2.3, 45.3, 43.8,
    39, 31.5, 24.7, 27.9, 22.1, 13.9, 2.6, 0.8, 0.8,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0
]
sn2   = [
    84.1,
    49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6,
    94.4, 82.3, 46.6, 40.8, 52.4, 32.5, 50.8, 3.1, 1.4,
    65.7, 76.9, 1.4, 67.8, 2.8, 0.6
]
ef    = [
    43.8,
    40.6, 44.1, 41.6, 0.0, 44.6, 17.1, 41.6, 42.4,
    51.2, 54.9, 47.5, 42.2, 53.4, 52.6, 91.5, 63.1, 47.2,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0
]
sf    = [
    39.6,
    34.9, 39.2, 37.4, 0.0, 41.1, 15.9, 37.8, 38.6,
    46.6, 49.7, 43.9, 42, 50.5, 50.8, 92.5, 57.3, 46.1,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0
]

# Название кислоты для заголовка
fa_name = "Linoleic acid" 

# ==========================================
# 2. ПОСТРОЕНИЕ ГРАФИКОВ
# ==========================================

fig, axs = plt.subplots(2, 2, figsize=(15, 13))
fig.suptitle(f'Сравнение содержания {fa_name} в разных объектах', fontsize=18)

plots = [
    (sn13, "SN-1,3", axs[0, 0]),
    (sn2,  "SN-2",   axs[0, 1]),
    (ef,   "EF",     axs[1, 0]),
    (sf,   "SF",     axs[1, 1])
]

for y_data, title, ax in plots:
    # Рисуем точки (одинаковый цвет для всех, так как подписи именованные)
    ax.scatter(sn123, y_data, color='forestgreen', s=80, edgecolors='black', zorder=3)
    
    # Подписываем каждую точку названием объекта
    for i, sample_name in enumerate(samples):
        ax.annotate(sample_name, 
                    (sn123[i], y_data[i]), 
                    xytext=(7, 0), # Смещение текста вправо
                    textcoords='offset points',
                    fontsize=10,
                    verticalalignment='center')
    
    # Линия y=x (эталонное соответствие)
    all_vals = sn123 + y_data
    max_val = max(all_vals) * 1.1
    ax.plot([0, max_val], [0, max_val], color='red', linestyle='--', alpha=0.4, label='y = x')
    
    # Оформление
    ax.set_title(f"SN-1,2,3 vs {title}", fontsize=14, fontweight='bold')
    ax.set_xlabel("Общее содержание (SN-1,2,3), %")
    ax.set_ylabel(f"Содержание в фракции {title}, %")
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Устанавливаем лимиты осей от 0 до максимума
    ax.set_xlim(0, max_val)
    ax.set_ylim(0, max_val)
    ax.legend(loc='upper left')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()