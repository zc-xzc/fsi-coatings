#!/usr/bin/env python3
"""
涂层热循环热-力耦合模拟 (FEniCSx)
=================================
复现论文第2章: 热循环作用下涂层老化的空间特征

物理模型:
  ┌──────────────────────┐
  │   涂层 (Coating)      │  ← 上表面: 温度边界/热流
  │  厚度 H_c = 0.3 mm   │
  ├──────────────────────┤
  │   基材 (Steel)        │  ← 下表面: 固定温度
  │  厚度 H_s = 0.7 mm   │
  └──────────────────────┘

分析方法: 热-力顺序耦合
  1. 瞬态热传导 → 温度场 T(x,y,t)
  2. 热弹性本构 → 应力场 σ(x,y,t)
  3. 分析应力的空间分布特征

安装: conda install -c conda-forge fenics-dolfinx
运行: python3 thermal_cycling_coating.py

作者: Research Notebook | 2026
"""

from dolfinx import mesh, fem, io, plot
from mpi4py import MPI
import ufl
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 50)
print("涂层热循环热-力耦合模拟")
print("=" * 50)

# ============================================================
# 1. 几何参数
# ============================================================
L = 2.0           # 长度 (mm)
H_total = 1.0     # 总厚度 (mm)
H_coating = 0.3   # 涂层厚度 (mm) —— 对应论文中~300μm
H_substrate = 0.7 # 基材厚度 (mm)
H_interface = H_substrate  # 界面位置 (y坐标)

# ============================================================
# 2. 网格
# ============================================================
nx, ny = 60, 30
domain = mesh.create_rectangle(
    MPI.COMM_WORLD,
    [[0, 0], [L, H_total]],
    [nx, ny],
    mesh.CellType.triangle
)
print(f"网格: {nx}x{ny} = {domain.topology.index_map(domain.topology.dim).size_local} 单元")

# ============================================================
# 3. 材料参数
# ============================================================
# 涂层 (聚合物) —— 论文中的涂装体系
k_c = fem.Constant(domain, 0.25)       # 导热系数 (W/m·K)
rho_c = fem.Constant(domain, 1200.0)   # 密度 (kg/m^3)
cp_c = fem.Constant(domain, 1500.0)    # 比热容 (J/kg·K)
E_c = fem.Constant(domain, 2.0e9)      # 杨氏模量 (Pa)
nu_c = fem.Constant(domain, 0.35)      # 泊松比
alpha_c = fem.Constant(domain, 5.0e-5) # 热膨胀系数 (1/K)

# 基材 (钢材)
k_s = fem.Constant(domain, 50.0)       # W/m·K
rho_s = fem.Constant(domain, 7850.0)   # kg/m^3
cp_s = fem.Constant(domain, 480.0)     # J/kg·K
E_s = fem.Constant(domain, 210.0e9)    # Pa
nu_s = fem.Constant(domain, 0.30)      # --
alpha_s = fem.Constant(domain, 1.2e-5) # 1/K

def coating_indicator(x):
    """判断是否在涂层区域"""
    return x[1] >= H_interface

# 涂层 vs 基材 属性 (使用条件表达式)
k = ufl.conditional(ufl.ge(domain.geometry.x[:, 1], H_interface), k_c, k_s)
rho_cp = ufl.conditional(ufl.ge(domain.geometry.x[:, 1], H_interface),
                          rho_c * cp_c, rho_s * cp_s)
E = ufl.conditional(ufl.ge(domain.geometry.x[:, 1], H_interface), E_c, E_s)
nu = ufl.conditional(ufl.ge(domain.geometry.x[:, 1], H_interface), nu_c, nu_s)
alpha = ufl.conditional(ufl.ge(domain.geometry.x[:, 1], H_interface), alpha_c, alpha_s)

print("材料参数:")
print(f"  涂层: E={float(E_c.values[0])/1e9:.1f}GPa, α={float(alpha_c.values[0]):.1e}/K")
print(f"  基材: E={float(E_s.values[0])/1e9:.1f}GPa, α={float(alpha_s.values[0]):.1e}/K")

# ============================================================
# 4. 第一阶段: 瞬态热传导
# ============================================================
print("\n[Phase 1] 瞬态热传导求解...")

T_space = fem.functionspace(domain, ("CG", 1))
T = fem.Function(T_space)
T_n = fem.Function(T_space)
v = ufl.TestFunction(T_space)
u = ufl.TrialFunction(T_space)

dt_val = 0.005
dt = fem.Constant(domain, dt_val)
theta = 0.5  # Crank-Nicolson 格式

# 变分形式: rho*cp * (T - T_n)/dt = div(k * grad(T))
F_thermal = rho_cp * (u - T_n) / dt * v * ufl.dx             + k * ufl.dot(ufl.grad(theta * u + (1 - theta) * T_n), ufl.grad(v)) * ufl.dx

a_thermal = ufl.lhs(F_thermal)
L_thermal = ufl.rhs(F_thermal)

# 边界条件: 下表面 T = 0
def bottom_boundary(x):
    return np.isclose(x[1], 0)
bottom_dofs = fem.locate_dofs_geometrical(T_space, bottom_boundary)
bc_bottom = fem.dirichletbc(fem.Constant(domain, 0.0), bottom_dofs, T_space)

problem_thermal = fem.petsc.LinearProblem(a_thermal, L_thermal, bcs=[bc_bottom])

# 初始条件
T_n.x.array[:] = 0.0

# 热循环加载: 方波信号
def thermal_cycle(t, period=1.0, T_max=60.0):
    """
    模拟一个热循环周期
    t: 当前时间 (归一化)
    period: 周期长度
    T_max: 最高温度
    """
    t_mod = t % period
    if t_mod < 0.4:      # 升温
        return T_max * (t_mod / 0.4)
    elif t_mod < 0.6:    # 保温
        return T_max
    elif t_mod < 0.9:    # 降温
        return T_max * (1 - (t_mod - 0.4) / 0.5)
    else:                 # 低温保温
        return 0.0

# 时间步进
T_steps = 200
output_interval = 50

# 准备XDMF输出
xdmf_thermal = io.XDMFFile(MPI.COMM_WORLD, "thermal_field.xdmf")
xdmf_thermal.write_mesh(domain)

T_series = []
t = 0.0

for n in range(T_steps):
    t += dt_val

    # 施加温度边界: 上表面温度 = 热循环值
    T_top = thermal_cycle(t)

    # 上表面温度边界 (Dirichlet)
    def top_boundary(x):
        return np.isclose(x[1], H_total)
    top_dofs = fem.locate_dofs_geometrical(T_space, top_boundary)
    bc_top = fem.dirichletbc(fem.Constant(domain, T_top), top_dofs, T_space)

    problem_thermal = fem.petsc.LinearProblem(a_thermal, L_thermal,
                                               bcs=[bc_bottom, bc_top])

    T = problem_thermal.solve()
    T_n.x.array[:] = T.x.array[:]

    if n % output_interval == 0:
        T_series.append(np.max(T.x.array))
        xdmf_thermal.write_function(T, n)
        print(f"  时间步 {n:4d} | t = {t:6.3f} | T_top = {T_top:6.1f}°C | max T = {np.max(T.x.array):.2f}°C")

xdmf_thermal.close()
print(f"✅ 热传导求解完成! 结果保存至 thermal_field.xdmf")

# ============================================================
# 5. 第二阶段: 热应力计算
# ============================================================
print("\n[Phase 2] 热应力求解...")

# 取最终温度场作为热载荷
T_final = T

# 位移函数空间 (矢量)
V_elu = fem.functionspace(domain, ("CG", 1, (domain.geometry.dim,)))
u_elu = fem.Function(V_elu)
v_elu = ufl.TestFunction(V_elu)

# 热弹性本构
def thermal_elastic_stress(u_elu, E, nu, alpha, T, T_ref=0.0):
    mu = E / (2.0 * (1.0 + nu))
    lmbda = E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
    epsilon = ufl.sym(ufl.grad(u_elu))
    epsilon_thermal = alpha * (T - T_ref) * ufl.Identity(len(u_elu))
    return 2.0 * mu * (epsilon - epsilon_thermal)            + lmbda * ufl.tr(epsilon - epsilon_thermal) * ufl.Identity(len(u_elu))

# 虚功方程
F_stress = ufl.inner(
    thermal_elastic_stress(u_elu, E, nu, alpha, T_final, 0.0),
    ufl.grad(v_elu)
) * ufl.dx

# 边界条件: 底部固定, 左右x方向约束
def bottom_elu(x):
    return np.isclose(x[1], 0)
bottom_elu_dofs = fem.locate_dofs_geometrical(V_elu, bottom_elu)
bc_bottom_elu = fem.dirichletbc(np.array([0, 0], dtype=np.float64),
                                 bottom_elu_dofs, V_elu)

def left_elu(x):
    return np.isclose(x[0], 0)
left_dofs_x = fem.locate_dofs_geometrical(V_elu.sub(0), left_elu)
bc_left_elu = fem.dirichletbc(fem.Constant(domain, 0.0), left_dofs_x, V_elu.sub(0))

# 求解
problem_stress = fem.petsc.LinearProblem(F_stress, u_elu,
                                          bcs=[bc_bottom_elu, bc_left_elu])
problem_stress.solve()

# 计算应力 (von Mises)
stress_sigma = thermal_elastic_stress(u_elu, E, nu, alpha, T_final, 0.0)

# Von Mises 等效应力 (用于可视化)
def von_mises(s):
    s_dev = s - (1/3) * ufl.tr(s) * ufl.Identity(len(u_elu))
    return ufl.sqrt(3/2 * ufl.inner(s_dev, s_dev))

W = fem.functionspace(domain, ("CG", 1))
vm_stress = fem.Function(W)
vm_expr = fem.Expression(von_mises(stress_sigma), W.element.interpolation_points())
vm_stress.interpolate(vm_expr)

# 输出位移和应力到XDMF
xdmf_mech = io.XDMFFile(MPI.COMM_WORLD, "stress_field.xdmf")
xdmf_mech.write_mesh(domain)
xdmf_mech.write_function(u_elu)
xdmf_mech.write_function(vm_stress, 0)
xdmf_mech.close()

# ============================================================
# 6. 结果摘要
# ============================================================
print(f"\n{'='*50}")
print("结果摘要")
print(f"{'='*50}")

# 最大位移
u_mag = np.sqrt(u_elu.x.array[0::2]**2 + u_elu.x.array[1::2]**2)
print(f"位移范围: u_min={np.min(u_mag):.4e}, u_max={np.max(u_mag):.4e}")

# 最大von Mises应力
print(f"von Mises应力: max={np.max(vm_stress.x.array):.2e} Pa")

# 涂层区域与基材区域分别统计
coating_dofs = np.where(domain.geometry.x[:, 1] >= H_interface)[0]
substrate_dofs = np.where(domain.geometry.x[:, 1] < H_interface)[0]
if len(coating_dofs) > 0:
    print(f"涂层区域: avg von Mises = {np.mean(vm_stress.x.array[coating_dofs]):.2e} Pa")
if len(substrate_dofs) > 0:
    print(f"基材区域: avg von Mises = {np.mean(vm_stress.x.array[substrate_dofs]):.2e} Pa")

print(f"\n✅ 热-力耦合模拟全部完成!")
print(f"   温度场: thermal_field.xdmf (可用ParaView查看)")
print(f"   应力场: stress_field.xdmf (可用ParaView查看)")
print(f"\n提示: paraview thermal_field.xdmf")
print(f"      paraview stress_field.xdmf")
print(f"{'='*50}")
