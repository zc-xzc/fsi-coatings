# ⚙️ 软件安装指南

> 所有工具均为免费/开源 | 适用于 Windows+WSL2 / Ubuntu 22.04 / macOS

## 1. Python 环境

```bash
# Miniconda 推荐
# 下载: https://docs.conda.io/en/latest/miniconda.html

# 创建主环境
conda create -n fsi python=3.11
conda activate fsi

# 基础科学计算
pip install numpy scipy matplotlib pandas jupyter sympy tqdm
```

## 2. FEniCSx (有限元)

### 方法1: conda (最简单)
```bash
conda create -n fenicsx -c conda-forge fenics-dolfinx
conda activate fenicsx

# 验证
python -c "from dolfinx import fem; print('FEniCSx OK ✅')"
```

### 方法2: Docker (最稳定, 跨平台)
```bash
docker pull dolfinx/dolfinx:stable
docker run -ti -v $(pwd):/workspace dolfinx/dolfinx:stable
```

### 方法3: WSL2 + Ubuntu
```bash
# 参考: https://fenicsproject.org/download/
```

## 3. OpenFOAM v14 (CFD)

### Ubuntu / WSL2
```bash
# 推荐: 官方 apt 源
curl -s https://dl.openfoam.com/add-debian-repo.sh | sudo bash
sudo apt-get install openfoam2412-dev

# 或者 docker
docker pull openfoam/openfoam2412-dev
```

### 验证
```bash
source /usr/lib/openfoam/openfoam2412/etc/bashrc
cd $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily
./Allrun
# 可视化: paraFoam
```

## 4. preCICE 耦合库

```bash
# Ubuntu 22.04
sudo apt-add-repository ppa:precice/precice
sudo apt-get update
sudo apt-get install precice

# 验证
precice --version
```

### OpenFOAM adapter
```bash
# 参考: https://precice.org/adapter-openfoam.html
```

### FEniCS adapter
```bash
pip install fenics-adapter
# 参考: https://precice.org/adapter-fenics.html
```

## 5. 网格生成

```bash
conda install -c conda-forge gmsh
python -c "import gmsh; print('Gmsh OK')"
```

## 6. 可视化

```bash
# ParaView (OpenFOAM + FEniCS 结果可视化)
conda install -c conda-forge paraview
# 或官网下载: https://www.paraview.org/download/
```

## 7. Zotero (文献管理)

```bash
# 下载: https://www.zotero.org/download/
# 插件: Better BibTeX for Zotero
# 教程: https://retorque.re/zotero-better-bibtex/
```

## 8. LaTeX (论文写作)

```bash
sudo apt-get install texlive-latex-base texlive-latex-recommended texlive-latex-extra
# 或在线上: https://www.overleaf.com/
```

## 环境验证清单

| 工具 | 验证命令 | 状态 |
|------|---------|------|
| Python | `python --version` | |
| FEniCSx | `python -c "from dolfinx import fem"` | |
| OpenFOAM | `simpleFoam --help` | |
| preCICE | `precice --version` | |
| Gmsh | `gmsh --version` | |
| ParaView | `paraview --version` | |
