#!/usr/bin/env python3
"""
论文图表数据提取工具
=====================
从论文PDF截图或扫描中手动提取数据点

用法:
  1. 打开论文图表截图
  2. 记录数据点坐标 (x, y)
  3. 用此脚本转换为数值

或者: 直接用 WebPlotDigitizer 工具
  下载: https://automeris.io/WebPlotDigitizer/
"""

import numpy as np
import matplotlib.pyplot as plt

def extract_data_manually():
    """
    手动输入从论文图表中读取的数据点。
    先读图, 记录坐标, 再输入。
    """
    print("数据提取工具")
    print("="*50)
    print("推荐使用 WebPlotDigitizer (免费在线工具)")
    print("https://automeris.io/WebPlotDigitizer/")
    print()
    print("或者手动输入数据点...")

def save_data_to_csv(filename, x, y, xlabel="x", ylabel="y"):
    """保存数据到CSV"""
    import pandas as pd
    df = pd.DataFrame({xlabel: x, ylabel: y})
    df.to_csv(filename, index=False)
    print(f"数据保存至 {filename}")

def plot_data(x, y, xlabel="时间 (天)", ylabel="附着力 (%)", title=None):
    """快速绘图"""
    plt.figure(figsize=(8, 4))
    plt.plot(x, y, 'o-', markersize=6)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title or "从论文提取的数据")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    return plt.gcf()

# ============================================================
# 示例: 从论文第3章提取的附着力数据
# ============================================================
def load_example_data():
    """论文中的典型附着力数据 (25°C)"""
    t = np.array([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200])
    A = np.array([100, 92, 85, 79, 73, 68, 63, 59, 55, 51, 48])
    save_data_to_csv("adhesion_25C.csv", t, A, "time_days", "adhesion_pct")
    print("示例数据已保存")
    fig = plot_data(t, A)
    fig.savefig("adhesion_25C.png", dpi=150)

if __name__ == "__main__":
    load_example_data()
    print("\n完成后运行: python3 paper_data_analysis.ipynb")
