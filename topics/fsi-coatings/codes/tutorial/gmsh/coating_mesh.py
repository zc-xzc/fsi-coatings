#!/usr/bin/env python3
"""
Gmsh涂层-基材网格生成器
"""
import gmsh, sys

gmsh.initialize(sys.argv)
gmsh.model.add("coating_substrate")

# 几何参数
L, H_total, H_coat = 2.0, 1.0, 0.3

# 点
p1 = gmsh.model.geo.addPoint(0,0,0, 0.02)
p2 = gmsh.model.geo.addPoint(L,0,0, 0.02)
p3 = gmsh.model.geo.addPoint(L,H_total-H_coat,0, 0.02)
p4 = gmsh.model.geo.addPoint(0,H_total-H_coat,0, 0.02)
p5 = gmsh.model.geo.addPoint(0,H_total,0, 0.02)
p6 = gmsh.model.geo.addPoint(L,H_total,0, 0.02)

# 线
for p in [p1,p2,p3,p4,p5,p6]:
    print(f'Point {p}')
# 完整版本见 tutorials/gmsh/
# ...

gmsh.finalize()
print("Gmsh网格生成器框架 - 详细脚本见完整版本")
