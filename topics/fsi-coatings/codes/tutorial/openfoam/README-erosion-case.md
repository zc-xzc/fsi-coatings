# OpenFOAM / CFD-DEM 风沙冲蚀案例
# 对应论文第6章
#
# 完整双相耦合需要 OpenFOAM + LIGGGHTS + CFDEMcoupling
# 这里提供框架和设置模板

## 文件结构
```
openfoam/
├── 0/              # 初始条件
│   ├── U           # 速度
│   ├── p           # 压力
│   └── alpha       # 相分数
├── constant/
│   ├── transportProperties   # 流体物性
│   └── turbulenceProperties  # 湍流模型
├── system/
│   ├── controlDict   # 求解控制
│   ├── fvSchemes     # 离散格式
│   └── fvSolution    # 求解器设置
└── Allrun           # 一键运行脚本
```

## 安装要求
```bash
# OpenFOAM v14
curl -s https://dl.openfoam.com/add-debian-repo.sh | sudo bash
sudo apt-get install openfoam2412-dev

# LIGGGHTS (DEM)
git clone https://github.com/CFDEMproject/LIGGGHTS-PUBLIC.git

# CFDEMcoupling
git clone https://github.com/CFDEMproject/CFDEMcoupling-PUBLIC.git
```

## 案例: 气流携沙冲击涂层平板

### 几何: 矩形风洞, 底部为涂层平板
### 边界: 入口风速 10-30 m/s, 出口压力
### 颗粒: 50-500 μm 沙粒, 从入口注入
### 测量: 涂层表面冲蚀磨损率

## 简化单相流设置 (仅CFD)

如果只有OpenFOAM, 可以用拉格朗日粒子追踪:
```bash
cd $FOAM_TUTORIALS/lagrangian/coalChemistryFoam/coalChemistry1
# 修改为沙子颗粒属性
```

## 参考
- CFD-DEM erosion review: Powder Technology, 2025
- CFDEMcoupling docs: https://www.cfdem.com/
