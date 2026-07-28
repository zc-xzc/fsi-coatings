# FSI-Coatings 教程代码

## 前提
```bash
conda create -n fenicsx -c conda-forge fenics-dolfinx
conda activate fenicsx
pip install numpy scipy matplotlib
```

## 运行顺序

### 1. 检查环境
```bash
python python/env_check.py
```

### 2. 热循环涂层模拟 (对应论文第2章)
```bash
python fenics/thermal_cycling_coating.py
```
输出: `thermal_field.xdmf`, `stress_field.xdmf` (用ParaView查看)

### 3. 论文复现: RPT参数拟合 (对应论文第3-4章)
```bash
python ../paper-reproduction/qi-yanfu/rpt_model_fitting.py
```
输出: `rpt_fitting_results.png`

## 可视化
```bash
paraview thermal_field.xdmf     # 温度场
paraview stress_field.xdmf      # 应力场
```

## 数据文件说明
| 文件 | 内容 | 输出 |
|------|------|------|
| thermal_cycling_coating.py | 涂层热-力耦合FEM | .xdmf文件 |
| rpt_model_fitting.py | RPT参数拟合 | .png + 控制台数据 |
| env_check.py | 环境检测 | 控制台报告 |
