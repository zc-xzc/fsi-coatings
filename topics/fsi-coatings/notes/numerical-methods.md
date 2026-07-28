# 数值方法笔记

> 持续更新 | 与论文第2-6章数值复现对应

## 一、FEM: 有限元法

### 适用场景
- 固体力学(应力/变形) ✓
- 热传导 ✓
- 多物理场(热-力耦合) ✓

### 核心步骤
```
1. 几何离散 (网格Gmsh)
2. 单元分析 (形函数/刚度矩阵)
3. 组装全局方程
4. 施加边界条件
5. 求解 ([K]{u} = {F})
6. 后处理 (应力/应变/位移)
```

### FEniCSx 特点
- 语法接近数学公式 (weak form 直接写)
- 自动有限元离散 (UFL语言)
- Python接口, 快速原型
- 支持: MPI并行, 混合单元, 任意维度

### 与论文的关联
| 论文第几章 | 物理问题 | FEniCS实现 | 已写代码 |
|-----------|---------|-----------|---------|
| 第2章 | 热传导+热应力 | heat_conduction.py + linear_elasticity.py | ✅ |
| 第5章 | 界面脱粘/CZM | CZM模型 (待实现) | 📝 |
| 第6章 | 单颗粒冲击 | 接触力学 (待实现) | 📝 |

## 二、CFD: 计算流体力学

### 适用场景
- 流体流动
- 传热
- 多相流 ✓ (冲蚀相关)

### 控制方程 (RANS)
```
∂(ρ·u_i)/∂t + ∂(ρ·u_i·u_j)/∂x_j = -∂p/∂x_i + ∂/∂x_j[μ(∂u_i/∂x_j + ∂u_j/∂x_i)] + f_i
```

### 与论文的关联
风沙冲蚀(第6章): 气固两相流
- **气相**: 连续相 (OpenFOAM 求解 RANS)
- **颗粒相**: 离散相 (LIGGGHTS 求解 DEM)
- **耦合**: CFD-DEM (CFDEMcoupling)

## 三、DEM: 离散单元法

### 原理
```
每个颗粒满足牛顿第二定律:
mi·dvi/dt = ΣF_contact + F_body + F_fluid

接触力: Hertz-Mindlin (法向/切向)
流体-颗粒相互作用: 曳力 + 浮力 + 压力梯度
```

### 与论文的关联
- 冲蚀角度的影响 → 颗粒入射角→碰撞力→磨损
- 颗粒速度的影响 → 冲蚀磨损量 ∝ v^n
- 颗粒大小/形状 → 不同涂层材料的磨损特性

## 四、CFD-DEM 流程

```
1. OpenFOAM求解流场(速度/压力/湍流)
2. 将流场信息传递给LIGGGHTS
3. LIGGGHTS计算颗粒运动(受力/碰撞)
4. 将颗粒作用力反馈给OpenFOAM
5. 更新流场 → 循环

工具链: OpenFOAM + LIGGGHTS + CFDEMcoupling
```

## 五、相场法 (Phase-field)

### 原理
```
用连续场变量 φ ∈ [0,1]:
φ = 0 → 完好材料
φ = 1 → 完全断裂

总能量 E = E_elastic + E_fracture + E_thermal
断裂驱动力: δE/δφ

优点: 自动处理裂纹分叉/合并, 不需要重网格
```

### 与论文的关联
- 第5章的动应力界面脱粘 → 相场法可模拟裂纹扩展
- 第2章热应力 → 热-力相场耦合

### 开源代码
- [FEniCSx Phase-Field Fracture教程](https://zenodo.org/records/20650089)
- [GitHub: phase_field_cohesive_fracture](https://github.com/jonas-heinzmann/phase_field_cohesive_fracture)

## 六、CZM: 内聚力模型

### 原理
```
在界面上定义牵引-分离本构:
σ(δ) =
  { σ_max · δ/δ₀,        δ ≤ δ₀  (线弹性)
  { σ_max · (δ_c-δ)/(δ_c-δ₀), δ₀ < δ < δ_c (软化)
  { 0,                    δ ≥ δ_c (完全脱粘)

断裂能 G_c = ∫₀^δ_c σ(δ) dδ
```

### CZM参数与实验对应
| CZM参数 | 对应的实验测量 | 论文中数据 |
|---------|-------------|-----------|
| σ_max | 拉开法附着强度 | 第5章 |
| δ₀ | 弹性极限变形 | 第5章应变数据 |
| G_c | 能量耗散 | 第5章能量模型 |
| δ_c | 临界分离位移 | 拉开法破坏位移 |

## 七、preCICE 耦合库

### 功能
```
1. 通信: 不同求解器数据交换 (TCP/IP)
2. 映射: 非匹配网格间数据插值
3. 加速: 固定点/Newton迭代收敛加速
4. 时间步: 子循环/同步各求解器
```

### 典型FSI耦合
```
OpenFOAM (流体域)  ⇄  preCICE  ⇄  FEniCS/CalculiX (固体域)
```

### 学习路径
```
1. 官方教程: perpendicular-flap (入门)
2. 官方文档: precice.org
3. Community Training: GitHub precice/community-training
