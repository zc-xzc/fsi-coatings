# 流固耦合 (FSI) 基础知识

> 持续更新 | 关联论文: 第6章风沙冲蚀 | 对应项目: CFD-DEM冲蚀模拟

## 什么是流固耦合？

流固耦合 (Fluid-Structure Interaction, FSI) 研究**可变形固体与流体之间的相互作用**。

**核心循环:**
```
流体压力/剪切力 → 固体变形 → 改变流场边界 → 改变流体载荷 → ...
```

## FSI的分类

### 按耦合方向
| 类型 | 方向 | 典型问题 | 数值方法 |
|------|------|---------|---------|
| **单向** (One-way) | 流体→固体 | 风荷载建筑 | 先CFD后FEM |
| **双向** (Two-way) | 流体⇄固体 | 机翼颤振 | 迭代耦合 |
| **强耦合** (Strong) | 双向+大变形 | 柔性膜 | 整体求解 |

### 按求解策略
| 方法 | 优点 | 缺点 | 代表工具 |
|------|------|------|---------|
| **分区耦合** | 复用现有求解器 | 可能不稳定(added-mass) | preCICE |
| **整体耦合** | 稳定, 精度高 | 开发难度大 | MOOSE |

### 按网格处理
| 方法 | 适用 | 代表 |
|------|------|------|
| **ALE** (动网格) | 中等变形 | OpenFOAM + solids4Foam |
| **浸入边界法 (IBM)** | 大变形/生物 | 代码实现 |
| **耦合欧拉-拉格朗日 (CEL)** | 冲击问题 | Abaqus |

## 控制方程

### 流体域: Navier-Stokes
```
质量守恒: ∇·v_f = 0
动量守恒: ρ_f(∂v_f/∂t + v_f·∇v_f) = ∇·σ_f + f_f
```

### 固体域: 动量守恒
```
ρ_s · ∂²u_s/∂t² = ∇·σ_s + f_s
```

### 界面条件 (耦合核心)
```
运动学连续: v_f = ∂u_s/∂t (速度匹配)
动力学平衡: σ_f·n = σ_s·n (力平衡)
几何一致: 界面位置由固体变形决定
```

## FSI Benchmark问题

| Benchmark | 描述 | 用途 |
|-----------|------|------|
| **Turek & Hron** | 弹性挡板绕流 | 验证FSI求解器 |
| **perpendicular-flap** | preCICE教程案例 | 学习preCICE入门 |
| **弹性圆柱涡激振动** | 经典VIV | 验证双向耦合 |
| **柔性薄膜** | 大变形FSI | 验证ALE方法 |

## FSI稳定性问题: Added-Mass Effect

分区耦合中, 流体对固体产生"附加质量"效应:
```
当 ρ_f/ρ_s 较大时 (如水/柔性结构)
→ 耦合迭代可能发散
→ 需要: 隐式耦合 + 松弛因子 + 界面质量预处理
```
**解决办法:** 使用 implicit coupling (固定点迭代或Newton迭代)

## 涂层问题中的FSI

### 现有论文中的FSI关联
| 论文章节 | 物理过程 | FSI方法 | 可用的数值工具 |
|---------|---------|---------|-------------|
| 第2章 | 热循环(温度→应力) | 热-力顺序耦合 | FEniCSx |
| 第5章 | 动应力(循环荷载) | 结构动力学+疲劳 | FEniCSx |
| **第6章** | **风沙冲蚀(气流+颗粒→涂层)** | **CFD-DEM** | **OpenFOAM+LIGGGHTS** |
| 第6章扩展 | 冲蚀坑→应力集中 | 流固耦合损伤 | preCICE |

### 扩展的FSI研究问题
```
1. 风沙冲蚀的CFD-DEM模拟 (直接)
2. 涂层脱粘后流体侵入的FSI (界面)
3. 交通荷载下涂层-气流耦合 (疲劳FSI)
4. 热循环+冲蚀的联合数值模拟 (多物理场)
```

## 推荐资源
- **综述**: [FEM discretization of FSI problems (arXiv 2025)](https://arxiv.org/html/2505.02594v3)
- **综述**: [IBM for Complex FSI (Fluids 2025)](https://researcher.manipal.edu/en/publications/recent-developments-in-the-immersed-boundary-method-for-complex-f/)
- **preCICE教程**: [Official Tutorials](https://precice.org/tutorials.html)
- **FSI Benchmark**: [Turek & Hron (2006)](https://link.springer.com/article/10.1007/s00466-006-0063-4)
