import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. ДАННЫЕ
# ==========================================
samples = [
    "Бузулук",
    "VIR-2233", "VIR-2699", "VIR-2776", "VIR-3110", "VIR-3384", "VIR-3599", "VIR-3675", "VIR-3714",
    "VNIIMK-1", "VNIIMK-2", "VNIIMK-3", "VNIIMK-4", "VNIIMK-5", "VNIIMK-6", "VNIIMK-7", "VNIIMK-8", "VNIIMK-9",
    "P-SSO",
    "R-C", "R-HL", "R-HO", "R-HPHL", "R-HPHO", "R-HSHO",
    "M-CAS-3", "M-RHA-274",
]

# Значения выбранной кислоты во всех фракциях для этих объектов
sn123 = [
    64,
    40.9, 46.2, 44.2, 1.1, 53.5, 1.8, 51.7, 50.8,
    61.4, 50, 32.7, 32.5, 32.9, 20.6, 18.5, 1.7, 1,
    55.5,
    58.7, 76, 2.1, 46.8, 3.5, 2,
    45, 48.4,
]
sn2   = [
    84.1,
    49.8, 61.1, 55.2, 0.0, 71.5, 0.9, 64.5, 64.6,
    94.4, 82.3, 46.6, 40.8, 52.4, 32.5, 50.8, 3.1, 1.4,
    65.8,
    65.7, 76.9, 1.4, 67.8, 2.8, 0.6,
    65.4, 58,
]
sn13  = [
    53.9,
    36.5, 38.7, 38.6, 1.6, 44.4, 2.3, 45.3, 43.8,
    39, 31.5, 24.7, 27.9, 22.1, 13.9, 2.6, 0.8, 0.8,
    50.3,
    55.2, 75.6, 2.4, 36.3, 3.9, 2.7,
    34.8, 43.6,
]
ef    = [
    43.8,
    40.6, 44.1, 41.6, 0.0, 44.6, 17.1, 41.6, 42.4,
    51.2, 54.9, 47.5, 42.2, 53.4, 52.6, 91.5, 63.1, 47.2,
    39.5,
    37.3, 33.7, 22.2, 48.3, 26.7, 10,
    48.4, 39.9,
]
sf    = [
    39.6,
    34.9, 39.2, 37.4, 0.0, 41.1, 15.9, 37.8, 38.6,
    46.6, 49.7, 43.9, 42, 50.5, 50.8, 92.5, 57.3, 46.1,
    35,
    33.3, 31.3, 21.3, 34.8, 18.9, 8.4,
    30.5, 34.6,
]

fa_name = "Linoleic acid" 

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
# 3. ПОСТРОЕНИЕ ОДНОГО ГРАФИКА
# ==========================================

fig, ax = plt.subplots(figsize=(10, 8))
fig.suptitle(f'Сравнение содержания {fa_name}', fontsize=16)

# Рисуем группы
unique_groups = []
for g in groups:
    if g not in unique_groups: unique_groups.append(g)

for group_name in unique_groups:
    idx = [i for i, g in enumerate(groups) if g == group_name]
    ax.scatter(
        [sn123[i] for i in idx], 
        [sn13[i] for i in idx], 
        c=[colors[i] for i in idx],
        label=group_name,
        s=120, edgecolors='white', linewidth=0.8, alpha=0.85, zorder=3
    )

# Подписи точек
for i, name in enumerate(samples):
    ax.annotate(name, (sn123[i], sn13[i]), xytext=(6, 3), textcoords='offset points', fontsize=9, alpha=0.8)

# Линии
limit = max(max(sn123), max(sn13)) * 1.1
ax.plot([0, limit], [0, limit], color='black', linestyle='--', linewidth=1, alpha=0.3)
x_line = np.array([0, 100])
y_line = 0.9772 * x_line - 7.3848
ax.plot(x_line, y_line, color='red', linestyle='--', linewidth=1, label='y = 0.9772x - 7.3848', zorder=5)

# Оформление
ax.set_title("SN-1,2,3 vs SN-1,3", fontsize=14, fontweight='bold')
ax.set_xlabel("Общее содержание (SN-1,2,3), %", fontsize=11)
ax.set_ylabel("Содержание в SN-1,3, %", fontsize=11)
ax.set_xlim(0, limit)
ax.set_ylim(0, limit)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='lower right', frameon=True, shadow=True)

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.show()