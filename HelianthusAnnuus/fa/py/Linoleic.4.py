import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text # Рекомендую для идеальной читаемости

# ==========================================
# 1. ДАННЫЕ
# ==========================================
samples = [
    "Бузулук", "VIR-2233", "VIR-2699", "VIR-2776", "VIR-3110", "VIR-3384", "VIR-3599", "VIR-3675", "VIR-3714",
    "VNIIMK-1", "VNIIMK-2", "VNIIMK-3", "VNIIMK-4", "VNIIMK-5", "VNIIMK-6", "VNIIMK-7", "VNIIMK-8", "VNIIMK-9",
    "P-SSO", "R-C", "R-HL", "R-HO", "R-HPHL", "R-HPHO", "R-HSHO", "M-CAS-3", "M-RHA-274",
]
sn123 = [64, 40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8, 61.4, 50, 32.7, 32.5, 32.9, 20.6, 18.5, 1.7, 1, 55.5, 58.7, 76, 2.1, 46.8, 3.5, 2, 45, 48.4]
sn2   = [84.1, 49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6, 94.4, 82.3, 46.6, 40.8, 52.4, 32.5, 50.8, 3.1, 1.4, 65.8, 65.7, 76.9, 1.4, 67.8, 2.8, 0.6, 65.4, 58]

def get_group_info(name):
    if name.startswith("VIR-"): return "red", "VIR"
    elif name.startswith("VNIIMK-"): return "green", "VNIIMK"
    elif name.startswith("P-"): return "cyan", "Pchelkin (2001)"
    elif name.startswith("R-"): return "magenta", "Reske (1997)"
    elif name.startswith("M-"): return "yellow", "Martinez-Force (2004)"
    else: return "blue", "Commodity"

colors = [get_group_info(sample)[0] for sample in samples]
groups = [get_group_info(sample)[1] for sample in samples]

# ==========================================
# 2. ПОСТРОЕНИЕ ГРАФИКА (Full HD оптимизация)
# ==========================================
# Увеличиваем размер фигуры и DPI
fig, ax = plt.subplots(figsize=(16, 10), dpi=120)

# Рисуем точки
unique_groups = sorted(list(set(groups)), key=lambda x: groups.index(x))
for group_name in unique_groups:
    idx = [i for i, g in enumerate(groups) if g == group_name]
    ax.scatter([sn123[i] for i in idx], [sn2[i] for i in idx], 
               c=[colors[i] for i in idx], label=group_name,
               s=180, edgecolors='black', linewidth=1.2, alpha=0.85)

# Автоматическая расстановка подписей (чтобы не перекрывали друг друга)
texts = []
for i, name in enumerate(samples):
    texts.append(ax.text(sn123[i], sn2[i], name, fontsize=12, fontweight='bold'))
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

# Линии
limit = max(max(sn123), max(sn2)) * 1.05
ax.plot([0, limit], [0, limit], 'k--', alpha=0.4, linewidth=1.5, label='y = x')
x_line = np.array([0, 100])
ax.plot(x_line, 1.0252 * x_line + 14.2525, 'g-', linewidth=3, label='y = 1.0252x + 14.2525')

# Оформление осей и заголовка
ax.set_title("Сравнение содержания Linoleic acid: SN-1,2,3 vs SN-2", fontsize=22, fontweight='bold', pad=25)
ax.set_xlabel("Общее содержание (SN-1,2,3), %", fontsize=18, fontweight='medium', labelpad=15)
ax.set_ylabel("Содержание в SN-2, %", fontsize=18, fontweight='medium', labelpad=15)

# Настройка делений осей
ax.tick_params(axis='both', which='major', labelsize=14, length=8, width=1.5)
ax.grid(True, linestyle=':', alpha=0.7, linewidth=1)

# Легенда
ax.legend(fontsize=14, loc='lower right', frameon=True, shadow=True, borderpad=1)

plt.tight_layout()
plt.show()