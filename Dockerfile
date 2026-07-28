FROM dolfinx/dolfinx:stable

LABEL description="FSI-Coatings Research Environment"

# 安装Python依赖
RUN pip install --no-cache-dir \
    numpy scipy matplotlib jupyter pandas \
    sympy tqdm requests

# 安装Gmsh
RUN apt-get update && apt-get install -y --no-install-recommends \
    gmsh && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root"]
