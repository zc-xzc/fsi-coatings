# 论文复现计划

## Phase 1: 热循环应力分布 (对应第2章)
工具: FEniCSx
- 1.1 涂层-基材热传导 → codes/tutorial/fenics/heat_conduction.py
- 1.2 温度场→热应力 → codes/tutorial/fenics/linear_elasticity.py
- 验证: 应力空间特征与论文一致

## Phase 2: 静应力老化 (对应第3-4章)
工具: Python+SciPy
- 时变老化模型参数标定
- 拟合优度 R² > 0.95

## Phase 3: 风沙冲蚀 (对应第6章)
工具: OpenFOAM+LIGGGHTS
- 单颗粒冲击 → 多颗粒CFD-DEM
- 验证: 冲蚀量与实验误差<10%
