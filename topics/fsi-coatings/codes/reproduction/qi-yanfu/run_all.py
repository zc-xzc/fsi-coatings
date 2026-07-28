#!/usr/bin/env python3
"""
论文复现统一运行脚本
按顺序运行所有复现代码
"""
import subprocess, sys, os

SCRIPTS = [
    ("Phase 1: 热-力耦合FEM (对应第2章)",
     "python ../codes/tutorial/fenics/thermal_cycling_coating.py"),
    ("Phase 2: RPT参数拟合 (对应第3-4章)",
     "python rpt_model_fitting.py"),
    ("Phase 3: 相场法断裂 (对应第5章)",
     "python ../codes/tutorial/fenics/phase_field_fracture.py"),
]

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 55)
print("  🏗️  论文复现 Pipeline")
print("=" * 55)

for i, (name, cmd) in enumerate(SCRIPTS, 1):
    print(f"\n[{i}/{len(SCRIPTS)}] {name}")
    print(f"  命令: {cmd}")
    print("  " + "-" * 40)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ✅ 成功!")
    else:
        print(f"  ⚠️  跳过 (可能需要FEniCSx环境): {result.stderr[:100]}")
    if result.stdout:
        for line in result.stdout.split('\n')[-5:]:
            if line.strip():
                print(f"  {line.strip()}")

print(f"\n{'='*55}")
print("  复现完成!")
print(f"{'='*55}")
