#!/usr/bin/env python3
"""
速度过程理论(RPT)参数拟合 - 对应论文第3-4章
================================================
拟合涂层附着力/厚度的时变曲线, 标定RPT模型参数

模型: P(t) = P0 * exp(-k_eff * t)
      k_eff = A * exp(-U_eff / (R*T))
      U_eff = U0 - gamma*sigma - delta_U_damage

安装: pip install numpy scipy matplotlib
运行: python3 rpt_model_fitting.py
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 50)
print("RPT参数拟合工具 - 论文第3-4章")
print("=" * 50)

# ============================================================
# 1. 模拟实验数据 (论文中提取的典型值)
# ============================================================
# 注: 实际使用时从论文图表中数字化提取真实数据
#     这里是演示用的典型数据

# 时间 (天)
t_data = np.array([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200])

# 附着力数据 (归一化, 论文Fig 3.xx的典型值)
# 不同温度下的附着力衰减
adhesion_25C = np.array([100, 92, 85, 79, 73, 68, 63, 59, 55, 51, 48])  # 25°C
adhesion_50C = np.array([100, 85, 73, 63, 54, 47, 41, 36, 31, 27, 24])  # 50°C
adhesion_70C = np.array([100, 76, 58, 45, 35, 27, 21, 17, 13, 10, 8])   # 70°C

print("\n[数据] 模拟附着力衰减数据:")
print(f"  温度 25°C: 初始 {adhesion_25C[0]:.0f}%, 200天后 {adhesion_25C[-1]:.0f}%")
print(f"  温度 50°C: 初始 {adhesion_50C[0]:.0f}%, 200天后 {adhesion_50C[-1]:.0f}%")
print(f"  温度 70°C: 初始 {adhesion_70C[0]:.0f}%, 200天后 {adhesion_70C[-1]:.0f}%")

# ============================================================
# 2. 拟合时变模型: P(t) = P0 * exp(-k * t)
# ============================================================
print("\n[拟合] 指数衰减模型: P(t) = P0 * exp(-k * t)")

def exp_decay(t, P0, k):
    return P0 * np.exp(-k * t)

rates = []  # 各温度下的反应速率
temperatures = [25, 50, 70]
adhesion_data = [adhesion_25C, adhesion_50C, adhesion_70C]

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
colors = ['#0077BB', '#EE7733', '#009988']

for i, (T, A_data, color) in enumerate(zip(temperatures, adhesion_data, colors)):
    popt, _ = curve_fit(exp_decay, t_data, A_data, p0=[100, 0.005])
    P0_fit, k_fit = popt
    rates.append(k_fit)

    t_fine = np.linspace(0, 210, 100)
    A_fit = exp_decay(t_fine, *popt)

    plt.plot(t_data, A_data, 'o', color=color, markersize=5,
             alpha=0.7, label=f'{T}°C (实验)')
    plt.plot(t_fine, A_fit, '-', color=color, linewidth=2,
             label=f'{T}°C 拟合 k={k_fit:.4f}')

    print(f"  T={T}°C: P0={P0_fit:.2f}, k={k_fit:.4f}, "
          f"半衰期={np.log(2)/k_fit:.1f}天")

plt.xlabel('时间 (天)')
plt.ylabel('附着力 (%)')
plt.title('(a) 附着力时变曲线拟合')
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend()
plt.xlim(0, 210)
plt.ylim(0, 110)

# ============================================================
# 3. Arrhenius 分析: 求活化能 U0
# ============================================================
print("\n[Arrhenius分析]")
print(f"{'='*50}")
print(f"  ln(k) = ln(A) - U0/(R*T)")
print(f"  通过不同温度下的 k 值拟合求 U0")
print(f"{'='*50}")

R = 8.314  # 气体常数 J/(mol·K)
T_K = np.array(temperatures) + 273.15
ln_k = np.log(rates)

# 线性拟合
coeffs = np.polyfit(1.0/T_K, ln_k, 1)
U0_fit = -coeffs[0] * R  # 斜率 = -U0/R
ln_A_fit = coeffs[1]

print(f"  拟合结果:")
print(f"    活化能 U0 = {U0_fit:.2f} J/mol = {U0_fit/1000:.2f} kJ/mol")
print(f"    指前因子 ln(A) = {ln_A_fit:.4f}")
print(f"    相关系数 R² = {np.corrcoef(ln_k, np.polyval(coeffs, 1/T_K))[0,1]**2:.4f}")

# 绘制Arrhenius图
plt.subplot(1, 2, 2)
T_fine = np.linspace(min(T_K)-10, max(T_K)+10, 50)
ln_k_fit = np.polyval(coeffs, 1/T_fine)

plt.plot(1/T_K, ln_k, 'o', color='#CC3311', markersize=8,
         label='实验值')
plt.plot(1/T_fine, ln_k_fit, '-', color='#CC3311', linewidth=2,
         label=f'拟合 U0={U0_fit/1000:.1f} kJ/mol')

plt.xlabel('1/T (1/K)')
plt.ylabel('ln(k)')
plt.title('(b) Arrhenius图 — 活化能标定')
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend()

# 注释
plt.annotate(f'斜率 = -U0/R', xy=(0.0032, -6.0), fontsize=10, color='#333333')
plt.annotate(f'U0 = {U0_fit/1000:.1f} kJ/mol', xy=(0.0032, -6.5), fontsize=10, color='#333333')

plt.tight_layout()
plt.savefig('rpt_fitting_results.png', dpi=150)
print(f"\n✅ 拟合图保存至 rpt_fitting_results.png")

# ============================================================
# 4. CSSS分析: 确定附着力临界值
# ============================================================
print(f"\n{'='*50}")
print("CSSS分析")
print(f"{'='*50}")
print(f"  论文CSSS判据: 拉开法中间漆/底漆附着破坏")
print(f"  对应的附着力: 约初始值的50%")
print(f"")
print(f"  在 25°C: CSSS时间 ≈ {np.log(100/50)/rates[0]:.1f} 天")
print(f"  在 50°C: CSSS时间 ≈ {np.log(100/50)/rates[1]:.1f} 天")
print(f"  在 70°C: CSSS时间 ≈ {np.log(100/50)/rates[2]:.1f} 天")
print(f"{'='*50}")

# ============================================================
# 5. 应力修正因子 gamma 的估算
# ============================================================
print(f"\n[应力效应] 估算应力敏感系数 γ")
print(f"{'='*50}")
print(f"  U_eff = U0 - gamma*sigma")
print(f"  通过不同应力水平的寿命数据拟合")
print(f"{'='*50}")

# 模拟有应力/无应力条件下的寿命比
sigma_levels = [0, 10, 20, 30]  # MPa
life_ratios = [1.0, 0.78, 0.61, 0.47]  # 相对于无应力的剩余寿命

gamma_coeffs = np.polyfit(sigma_levels, np.log(life_ratios), 1)
gamma_fit = -gamma_coeffs[0] * R * 323  # 假设 T=50°C=323K

print(f"  估算 gamma = {gamma_fit:.6f} J/(mol·Pa)")
print(f"  这意味着: 每增加1MPa应力, 活化能降低 {gamma_fit*1e6:.2f} J/mol")
print(f"")
print(f"⚠️ 注意: 以上为演示数据生成的估算值")
print(f"   实际使用时, 需要从论文原始数据中重新提取")

print(f"\n{'='*50}")
print("拟合完成!")
print(f"{'='*50}")
