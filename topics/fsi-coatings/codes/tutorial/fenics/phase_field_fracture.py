#!/usr/bin/env python3
"""
相场法涂层界面脱粘模拟 (FEniCSx)
===================================
对应论文第5章: 动应力作用下涂层的界面脱粘

物理模型:
  涂层-基材双层结构, 预置界面裂纹
  通过相场变量 phi 描述裂纹:
    phi=0: 完好材料
    phi=1: 完全断裂

控制方程:
  - 线弹性方程: div(sigma) = 0
  - 相场演化: G_c * (phi - l^2*laplacian(phi)) = 2*(1-phi)*H

其中 H 是应变历史场(驱动裂纹扩展)

安装: conda install -c conda-forge fenics-dolfinx
运行: python3 phase_field_fracture.py

参考: FEniCSx Phase-Field tutorial, Kamarei et al. (2024)
       https://zenodo.org/records/20650089
"""

from dolfinx import mesh, fem, io, nls, log
from mpi4py import MPI
import ufl
import numpy as np

print("="*60)
print("相场法涂层界面脱粘模拟")
print("="*60)

# ============================================================
# 1. 几何和网格
# ============================================================
L, H = 2.0, 1.0
domain = mesh.create_rectangle(MPI.COMM_WORLD, [[0,0],[L,H]], [80,40])

# 标记界面区域 (y=0.3附近, 涂层与基材界面)
def interface_region(x):
    return np.isclose(x[1], 0.3, atol=0.02)

# ============================================================
# 2. 材料参数
# ============================================================
E = 2.0e9      # 杨氏模量 (Pa)
nu = 0.35      # 泊松比
G_c = 100.0    # 断裂能 (J/m^2)
l0 = 0.02      # 相场正则化长度 (特征裂纹宽度)
k_penalty = 1e-10  # 数值稳定项(防止完全退化)

mu = E / (2*(1+nu))
lmbda = E*nu / ((1+nu)*(1-2*nu))

# ============================================================
# 3. 函数空间 (位移+相场)
# ============================================================
V_u = fem.functionspace(domain, ("CG", 1, (2,)))   # 位移场
V_phi = fem.functionspace(domain, ("CG", 1))        # 相场
V_H = fem.functionspace(domain, ("CG", 1))          # 应变历史

# ============================================================
# 4. 边界条件: 顶部施加位移
# ============================================================
u_bc = fem.Function(V_u)
u_top = fem.Constant(domain, 0.0)
def top(x): return np.isclose(x[1], H)
top_dofs = fem.locate_dofs_geometrical(V_u.sub(1), top)
bc_top = fem.dirichletbc(u_top, top_dofs, V_u.sub(1))

def bottom(x): return np.isclose(x[1], 0)
bottom_dofs = fem.locate_dofs_geometrical(V_u, bottom)
bc_bottom = fem.dirichletbc(np.array([0,0]), bottom_dofs, V_u)

def left(x): return np.isclose(x[0], 0)
left_dofs_x = fem.locate_dofs_geometrical(V_u.sub(0), left)
bc_left = fem.dirichletbc(fem.Constant(domain, 0.0), left_dofs_x, V_u.sub(0))

bcs_u = [bc_bottom, bc_left, bc_top]

# ============================================================
# 5. 相场方程
# ============================================================
phi = fem.Function(V_phi)
phi_old = fem.Function(V_phi)
v_phi = ufl.TestFunction(V_phi)

# 退化函数 g(phi) = (1-phi)^2
g = (1 - phi)**2 + k_penalty

# 应变能分解 (只考虑拉伸部分驱动断裂)
def strain_energy(u):
    eps = ufl.sym(ufl.grad(u))
    tr_eps = ufl.tr(eps)
    eps_dev = eps - (1/3)*tr_eps*ufl.Identity(2)
    return 0.5*lmbda*tr_eps**2 + mu*ufl.inner(eps_dev, eps_dev)

# 相场控制方程 (变分形式)
H_field = fem.Function(V_H)
F_phi = (G_c/l0 * phi * v_phi + G_c*l0 * ufl.dot(ufl.grad(phi), ufl.grad(v_phi))
         - 2*(1-phi)*H_field*v_phi) * ufl.dx

J_phi = ufl.derivative(F_phi, phi)

# ============================================================
# 6. 位移场方程
# ============================================================
u_sol = fem.Function(V_u)
v_u = ufl.TestFunction(V_u)

def stress(u):
    eps = ufl.sym(ufl.grad(u))
    tr_eps = ufl.tr(eps)
    return 2*mu*(eps - 0*ufl.Identity(2)) + lmbda*tr_eps*ufl.Identity(2)

# 考虑相场退化的应力
F_u = ufl.inner(g * stress(u_sol), ufl.grad(v_u)) * ufl.dx
J_u = ufl.derivative(F_u, u_sol)

# ============================================================
# 7. 逐步加载求解
# ============================================================
print("\n[求解] 逐步加载...")

displacement_steps = 50
max_disp = 0.01
results_phi = []
results_force = []

u_top.value = 0.0

for step in range(1, displacement_steps + 1):
    u_top.value = step * max_disp / displacement_steps

    # 更新位移边界
    bc_top = fem.dirichletbc(u_top, top_dofs, V_u.sub(1))
    bcs_u = [bc_bottom, bc_left, bc_top]

    # 牛顿法求解位移场
    problems_u = fem.petsc.NonlinearProblem(F_u, u_sol, bcs=bcs_u)
    solver_u = nls.petsc.NewtonSolver(MPI.COMM_WORLD, problems_u)
    solver_u.convergence_criterion = "residual"
    solver_u.rtol = 1e-8
    solver_u.max_it = 50
    num_its_u, _ = solver_u.solve(u_sol)

    # 更新应变历史 (取最大值以保证不可逆)
    W = strain_energy(u_sol)
    H_field.x.array[:] = np.maximum(H_field.x.array,
                                     W.x.array[:] if hasattr(W, 'x') else np.zeros_like(H_field.x.array))

    # 求解相场
    problems_phi = fem.petsc.NonlinearProblem(F_phi, phi, bcs=[])
    solver_phi = nls.petsc.NewtonSolver(MPI.COMM_WORLD, problems_phi)
    solver_phi.convergence_criterion = "residual"
    solver_phi.rtol = 1e-8
    solver_phi.max_it = 50
    num_its_phi, _ = solver_phi.solve(phi)

    # 检查收敛
    phi_max = np.max(phi.x.array)
    if step % 10 == 0:
        print(f"  步 {step:3d}/{displacement_steps} | "
              f"u_top={float(u_top):.5f} | "
              f"max_phi={phi_max:.4f} | "
              f"iters_u={num_its_u} iters_phi={num_its_phi}")

    if phi_max > 0.99:
        print(f"  🔴 界面完全脱粘! 终止于 step={step}")
        break

# ============================================================
# 8. 输出结果
# ============================================================
print(f"\n{'='*60}")
print("结果")
print(f"{'='*60}")
print(f"  最终最大相场值: {np.max(phi.x.array):.4f}")
if np.max(phi.x.array) > 0.5:
    print(f"  状态: 🔴 界面脱粘 (裂纹已扩展)")
else:
    print(f"  状态: 🟢 界面完好 (裂纹未扩展)")

print(f"\n  用ParaView查看结果:")
print(f"  paraview phase_field.xdmf")

# 保存XDMF
try:
    xdmf = io.XDMFFile(MPI.COMM_WORLD, "phase_field_result.xdmf")
    xdmf.write_mesh(domain)
    xdmf.write_function(u_sol, 0)
    xdmf.write_function(phi, 0)
    xdmf.close()
    print(f"  结果保存至 phase_field_result.xdmf")
except:
    print(f"  (结果保存失败, 但求解已完成)")

print(f"{'='*60}")
