# FSI + Coating Durability

> 流固耦合数值模拟 × 钢结构涂层多场耦合老化

**研究者:** zc-xzc | **导师方向:** 流固耦合数值模拟 | **专业:** 固体力学

## 目录导航

| 目录 | 内容 |
|------|------|
| [papers/](papers/) | 论文库 + 文献地图 |
| [notes/](notes/) | 方向专题笔记 |
| [codes/](codes/) | 数值模拟代码 |
| [projects/](projects/) | 项目管理 |
| [presentations/](presentations/) | 汇报文件 |
| [data/](data/) | 数据文件 |

## 当前主线

**论文解读：** 戚彦福. 钢桥涂层的老化机理与耐久性研究[D]. 兰州交通大学, 2026. (223页)

- [ ] 第1章 引言 (1-29页)
- [ ] 第2章 热循环空间特征 (30-51页)
- [ ] 第3章 静应力+环境耦合 (52-98页) ⬅ 核心
- [ ] 第4章 耐久性量化 (99-130页)
- [ ] 第5章 动应力劣化 (131-164页)
- [ ] 第6章 风沙冲蚀 (165-198页)
- [ ] 第7章 结论 (199-223页)

**开学汇报：** 2026年9月 | **[讲稿](presentations/2026-09-coating-report/script.md)**

## 研究方向衔接

论文中的物理问题 → 对应数值模拟方法：
- 风沙冲蚀 → CFD-DEM（FSI）
- 热循环 → 热-力耦合（多物理场）
- 界面脱粘 → 相场法 / CZM（断裂力学）
- 动应力 → 疲劳寿命（固体力学）

## 工具链

| 工具 | 用途 | 安装 |
|------|------|------|
| FEniCSx | 有限元 | `conda install -c conda-forge fenics-dolfinx` |
| OpenFOAM | CFD | `sudo apt-get install openfoam` |
| preCICE | 耦合库 | `sudo apt-get install precice` |
| Gmsh | 网格 | `conda install -c conda-forge gmsh` |
