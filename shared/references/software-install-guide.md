# 安装指南

## Python
```bash
conda create -n fsi python=3.11
conda activate fsi
pip install numpy scipy matplotlib jupyter
```

## FEniCSx
```bash
conda create -n fenicsx -c conda-forge fenics-dolfinx
conda activate fenicsx
python -c "from dolfinx import fem; print('OK')"
```

## OpenFOAM v14 (Ubuntu/WSL)
```bash
sudo apt-get install openfoam
# 或 docker pull openfoam/openfoam2412-dev
```

## preCICE
```bash
sudo apt-add-repository ppa:precice/precice
sudo apt-get update
sudo apt-get install precice
```

## Gmsh
```bash
conda install -c conda-forge gmsh
```
