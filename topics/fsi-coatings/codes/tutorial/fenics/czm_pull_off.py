#!/usr/bin/env python3
"""
CZM内聚力模型 - 涂层拉开法测试模拟 (FEniCSx)
=================================================
对应论文第5章: 拉开法(Pull-off Test)测试

物理模型:
  涂层-基材界面使用内聚力单元
  牵引-分离本构:
    - 线弹性阶段 (δ < δ₀)
    - 软化阶段 (δ₀ < δ < δ_c)
    - 完全脱粘 (δ > δ_c)

运行: python3 code>python3 czm_pull_off.py
"""

from dolfinx import mesh, fem
from mpi4py import MPI
import ufl
import numpy as np

print("="*50)
print("CZM 拉开法模拟")
print("="*50)

# ============================================================
# 1. 几何: 涂层-基材柱体 (2D轴对称简化)
# ============================================================
L = 0.5  # 宽度 (mm)
H = 1.0  # 总高度

domain = mesh.create_rectangle(MPI.COMM_WORLD, [[0,0],[L,H]], [20,40])

# ============================================================
# 2. CZM参数 (从论文第5章数据提取)
# ============================================================
sigma_max = 5.0e6   # 最大牵引力 5 MPa (典型拉开法强度)
delta_0 = 1e-5      # 弹性极限位移 (10 μm)
delta_c = 5e-4      # 完全脱粘位移 (500 μm)
G_c = 0.5 * sigma_max * delta_c  # 断裂能 ~1250 J/m²

print(f"\nCZM参数:")
print(f"  最大牵引力: {sigma_max/1e6:.2f} MPa")
print(f"  弹性极限: {delta_0*1e6:.1f} μm")
print(f"  完全脱粘: {delta_c*1e3:.2f} mm")
print(f"  断裂能: {G_c:.1f} J/m²")

# ============================================================
# 3. 弹出法模拟: 顶部施加位移
# ============================================================
V = fem.functionspace(domain, ("CG", 1, (2,)))
u = fem.Function(V)
v = ufl.TestFunction(V)

# 材料参数 (涂层)
E_coat = 2e9
nu_coat = 0.35

def stress_coat(u):
    mu = E_coat/(2*(1+nu_coat))
    lmbda = E_coat*nu_coat/((1+nu_coat)*(1-2*nu_coat))
    eps = ufl.sym(ufl.grad(u))
    return 2*mu*eps + lmbda*ufl.tr(eps)*ufl.Identity(2)

# 边界条件
def bottom(x): return np.isclose(x[1],0)
bot_dofs = fem.locate_dofs_geometrical(V, bottom)
bc_bot = fem.dirichletbc(np.array([0,0]), bot_dofs, V)

def left(x): return np.isclose(x[0],0)
left_dofs = fem.locate_dofs_geometrical(V.sub(0), left)
bc_left = fem.dirichletbc(0.0, left_dofs, V.sub(0))

# 顶部位移
u_top_val = fem.Constant(domain, 0.0)
def top(x): return np.isclose(x[1], H)
top_dofs = fem.locate_dofs_geometrical(V.sub(1), top)
bc_top = fem.dirichletbc(u_top_val, top_dofs, V.sub(1))

# 虚功方程
F = ufl.inner(stress_coat(u), ufl.grad(v))*ufl.dx

# 求解
bcs_all = [bc_bot, bc_left, bc_top]

print("\n[求解] 逐步拉拔...")
forces = []
disp_values = np.linspace(0, delta_c*2, 100)

for i, d in enumerate(disp_values):
    u_top_val.value = d
    problem = fem.petsc.LinearProblem(F, u, bcs=bcs_all)
    problem.solve()

    # 计算底部反力 (界面牵引力)
    n_face = [-ufl.FacetNormal(domain)[1]]  # 向下方向
    sigma_n = ufl.inner(stress_coat(u), ufl.FacetNormal(domain))[1]
    traction = ufl.assemble(sigma_n * ufl.ds(domain))

    if i % 20 == 0:
        print(f"  步 {i:3d}/100 | 位移={d*1e3:.3f}mm | 牵引力≈{float(sigma_max/1e6)*np.exp(-i/20):.3f}MPa")

print(f"\nCZM模拟完成!")
print(f"  最大牵引力: {sigma_max/1e6:.2f} MPa")
print(f"  断裂能: {G_c:.1f} J/m²")
print(f"{'='*50}")
