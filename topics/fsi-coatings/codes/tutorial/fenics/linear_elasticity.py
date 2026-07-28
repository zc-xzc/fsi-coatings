"""
FEniCSx 线弹性教程 - 涂层热应力
"""
from dolfinx import mesh, fem
from mpi4py import MPI
import ufl
import numpy as np

L, H = 2.0, 1.0
domain = mesh.create_rectangle(MPI.COMM_WORLD, [[0,0],[L,H]], [40,20])
V = fem.functionspace(domain, ("Lagrange", 1, (2,)))

# 材料(基材钢)
E, nu, alpha = fem.Constant(domain, 210e9), fem.Constant(domain, 0.3), fem.Constant(domain, 1.2e-5)
T = fem.Function(fem.functionspace(domain, ("CG", 1)))
T.x.array[:] = 50.0

def sigma(v):
    mu, lmbda = E/(2*(1+nu)), E*nu/((1+nu)*(1-2*nu))
    eps = ufl.sym(ufl.grad(v))
    eps_th = alpha*(T-0.0)*ufl.Identity(2)
    return 2*mu*(eps-eps_th) + lmbda*ufl.tr(eps-eps_th)*ufl.Identity(2)

u, v_ = fem.Function(V), ufl.TestFunction(V)
F = ufl.inner(sigma(u), ufl.grad(v_))*ufl.dx

# 底部固定
bottom_dofs = fem.locate_dofs_geometrical(V, lambda x: np.isclose(x[1],0))
bc1 = fem.dirichletbc(np.array([0,0]), bottom_dofs, V)
left_dofs = fem.locate_dofs_geometrical(V.sub(0), lambda x: np.isclose(x[0],0))
bc2 = fem.dirichletbc(0.0, left_dofs, V.sub(0))

fem.petsc.LinearProblem(F, u, bcs=[bc1, bc2]).solve()
print(f"热应力模拟完成 u_x:[{np.min(u.x.array[0::2]):.2e},{np.max(u.x.array[0::2]):.2e}]")
