#!/usr/bin/env python3
"""
Gmsh 涂层-基材双层结构网格生成器 (完整版)
=============================================
生成: 涂层-基材矩形, 界面加密, 可导入FEniCSx

用法:
  python3 coating_mesh_full.py           # 生成并保存
  python3 coating_mesh_full.py --viz     # 生成并可视化

输出: coating_mesh.msh (FEniCSx可读)
安装: conda install -c conda-forge gmsh
"""

import gmsh, sys, os

# ============================================================
# 1. 初始化
# ============================================================
gmsh.initialize()
gmsh.model.add("coating_substrate")

# ============================================================
# 2. 几何参数
# ============================================================
L = 2.0          # 长度 (mm)
H_sub = 0.7      # 基材厚度 (mm)
H_coat = 0.3     # 涂层厚度 (mm)
H_total = H_sub + H_coat

# 网格尺寸
lc_coarse = 0.05  # 基材网格
lc_fine = 0.02    # 涂层网格
lc_interface = 0.01  # 界面加密

# ============================================================
# 3. 创建几何
# ============================================================
# 点: 左下角起逆时针
corners = [
    (0, 0), (L, 0), (L, H_sub), (0, H_sub),  # 基材
    (0, H_total), (L, H_total)                 # 涂层
]

# 基材区域: 点 1-4
p1 = gmsh.model.geo.addPoint(0, 0, 0, lc_coarse)
p2 = gmsh.model.geo.addPoint(L, 0, 0, lc_coarse)
p3 = gmsh.model.geo.addPoint(L, H_sub, 0, lc_interface)
p4 = gmsh.model.geo.addPoint(0, H_sub, 0, lc_interface)

# 涂层区域: 点 4-6 + 点3? 用点5,6做涂层顶
p5 = gmsh.model.geo.addPoint(0, H_total, 0, lc_fine)
p6 = gmsh.model.geo.addPoint(L, H_total, 0, lc_fine)

# 线
l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p3)
l3 = gmsh.model.geo.addLine(p3, p4)
l4 = gmsh.model.geo.addLine(p4, p1)

l5 = gmsh.model.geo.addLine(p4, p5)
l6 = gmsh.model.geo.addLine(p5, p6)
l7 = gmsh.model.geo.addLine(p6, p3)

# 环和面
s1 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
s2 = gmsh.model.geo.addCurveLoop([l5, l6, l7, -l3])
substrate = gmsh.model.geo.addPlaneSurface([s1])
coating = gmsh.model.geo.addPlaneSurface([s2])

# ============================================================
# 4. 物理分组 (用于FEniCSx标记)
# ============================================================
gmsh.model.geo.synchronize()

gmsh.model.addPhysicalGroup(2, [substrate], 1)
gmsh.model.setPhysicalName(2, 1, "substrate")

gmsh.model.addPhysicalGroup(2, [coating], 2)
gmsh.model.setPhysicalName(2, 2, "coating")

# 边界分组
# 底部
gmsh.model.addPhysicalGroup(1, [l1], 10)
gmsh.model.setPhysicalName(1, 10, "bottom")

# 涂层顶部
gmsh.model.addPhysicalGroup(1, [l6], 11)
gmsh.model.setPhysicalName(1, 11, "top")

# 界面
gmsh.model.addPhysicalGroup(1, [l3], 12)
gmsh.model.setPhysicalName(1, 12, "interface")

# 左右
gmsh.model.addPhysicalGroup(1, [l4, l5], 13)
gmsh.model.setPhysicalName(1, 13, "left")
gmsh.model.addPhysicalGroup(1, [l2, l7], 14)
gmsh.model.setPhysicalName(1, 14, "right")

# ============================================================
# 5. 生成网格并保存
# ============================================================
gmsh.model.mesh.generate(2)

output = "coating_mesh.msh"
gmsh.write(output)

# 统计
node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
elem_types, elem_tags, elem_node_tags = gmsh.model.mesh.getElements()
num_elements = sum(len(t) for t in elem_tags)
num_nodes = len(node_tags)

print(f"✅ 网格生成完成!")
print(f"   文件: {os.path.abspath(output)}")
print(f"   节点数: {num_nodes}")
print(f"   单元数: {num_elements}")
print(f"   物理分组: substrate(1), coating(2), bottom(10), top(11), interface(12)")

gmsh.finalize()
