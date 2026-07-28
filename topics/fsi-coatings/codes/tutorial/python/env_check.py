#!/usr/bin/env python3
"""
环境检查脚本 - 检测所有工具是否安装
运行: python3 env_check.py
"""

import importlib
import sys
import subprocess

print("=" * 55)
print("  🔍 科研环境检查工具")
print("=" * 55)

checks = [
    ("Python 版本", sys.version.split()[0], sys.version_info >= (3, 9)),
]

# Python 包
packages = [
    ("numpy", "numpy"),
    ("scipy", "scipy"),
    ("matplotlib", "matplotlib"),
    ("jupyter", "jupyter"),
    ("requests", "requests"),
]

for name, pkg in packages:
    try:
        mod = importlib.import_module(pkg)
        ver = getattr(mod, "__version__", "✓")
        checks.append((f"  {name}", ver, True))
    except ImportError:
        checks.append((f"  {name}", "未安装", False))

# FEniCSx
try:
    import importlib
    import dolfinx
    checks.append(("FEniCSx (dolfinx)", dolfinx.__version__, True))
except:
    try:
        from dolfinx import fem
        checks.append(("FEniCSx (dolfinx)", "已安装(版本未知)", True))
    except:
        checks.append(("FEniCSx (dolfinx)", "未安装", False))

# CLI 工具
cli_tools = ["gmsh", "ffmpeg"]
for tool in cli_tools:
    try:
        subprocess.run([tool, "--version"], capture_output=True, timeout=3)
        checks.append((f"  {tool}", "✓", True))
    except:
        checks.append((f"  {tool}", "未找到", False))

# OpenFOAM
try:
    result = subprocess.run(["simpleFoam", "--help"], capture_output=True, text=True, timeout=3)
    checks.append(("OpenFOAM (simpleFoam)", "✓", True))
except:
    checks.append(("OpenFOAM (simpleFoam)", "未设置/未找到", False))

# preCICE
try:
    result = subprocess.run(["precice", "--version"], capture_output=True, text=True, timeout=3)
    ver = result.stdout.strip() or result.stderr.strip() or "✓"
    checks.append(("preCICE", ver[:30], True))
except:
    checks.append(("preCICE", "未安装", False))

# Git
try:
    result = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=3)
    ver = result.stdout.strip() or "✓"
    checks.append(("Git", ver, True))
except:
    checks.append(("Git", "未找到", False))

# 打印结果
print(f"\n{'结果':<40} {'版本':<20} {'状态':>8}")
print("-" * 68)
passed = 0
for name, ver, ok in checks:
    status = "✅" if ok else "❌"
    if ok:
        passed += 1
    print(f"  {name:<38} {str(ver):<20} {status:>8}")

print(f"\n  总计: {passed}/{len(checks)} 通过")
print(f"  {'✅ 环境配置完整!' if passed == len(checks) else '⚠️ 部分工具未安装, 详见安装指南'}")
print("=" * 55)
