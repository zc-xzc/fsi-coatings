"""
FEniCSx 热传导教程 - 涂层热模拟基础
问题: 涂层-基材双层，上表面加热，下表面固定温度
"""
from dolfinx import mesh, fem
from mpi4py import MPI
import ufl
import numpy as np

L, H = 2.0, 1.0
H_c, H_s = 0.3, 0.7  # 涂层/基材厚度

domain = mesh.create_rectangle(MPI.COMM_WORLD, [[0,0],[L,H]], [60,30])

# 材料参数
k_c, rho_c, cp_c = 0.25, 1200, 1500   # 涂层(聚合物)
k_s, rho_s, cp_s = 50.0, 7850, 480    # 基材(钢)

V = fem.functionspace(domain, ("CG", 1))
v, u = ufl.TestFunction(V), ufl.TrialFunction(V)

# 按位置分配材料
rho_cp = ufl.conditional(ufl.ge(domain.geometry.x[:,1], H_s), rho_c*cp_c, rho_s*cp_s)
k = ufl.conditional(ufl.ge(domain.geometry.x[:,1], H_s), k_c, k_s)

dt = fem.Constant(domain, 0.01)
theta = 0.5  # Crank-Nicolson
T_prev = fem.Function(V)

F = rho_cp*(u-T_prev)/dt*v*ufl.dx + k*ufl.dot(ufl.grad(theta*u+(1-theta)*T_prev), ufl.grad(v))*ufl.dx

# 边界: 下表面 T=0
bottom_dofs = fem.locate_dofs_geometrical(V, lambda x: np.isclose(x[1],0))
bc = fem.dirichletbc(0.0, bottom_dofs, V)

problems = fem.petsc.LinearProblem(ufl.lhs(F), ufl.rhs(F), bcs=[bc])
T_prev.x.array[:] = 0.0

for n in range(200):
    T = problems.solve()
    T_prev.x.array[:] = T.x.array[:]
    if n % 50 == 0:
        print(f"Step {n}, max T = {np.max(T.x.array):.2f}")

print("热传导模拟完成! 用ParaView可视化结果")
