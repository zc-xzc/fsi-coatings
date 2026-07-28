# Research Notebook 🧪

> **多方向科研笔记仓库** | 流固耦合 × 涂层耐久性 × 数值模拟
>
> 同一套工作流，跨研究方向复用。

<p align="center">
  <img src="https://img.shields.io/badge/status-active-brightgreen" />
  <img src="https://img.shields.io/badge/方向-FSI%20%2B%20Coating-blue" />
  <img src="https://img.shields.io/badge/license-MIT-orange" />
</p>

---

## 📂 研究方向

| 方向 | 目录 | 状态 | 简介 |
|------|------|------|------|
| 🛡️ **FSI + 涂层** | [`topics/fsi-coatings/`](topics/fsi-coatings/) | ✅ 活跃 | 流固耦合数值模拟 × 钢结构涂层多场耦合老化 |
| 📝 待添加 | — | ⏳ | |

## 📐 仓库架构

```
research-notebook/
├── .github/ISSUE_TEMPLATE/      ← 标准化Issue模板
├── shared/                       ← 跨方向共享资源
│   ├── templates/                ← 笔记模板
│   ├── references/               ← 教材/期刊/课程/安装指南
│   ├── glossary.md               ← 术语表(跨方向积累)
│   └── research-workflow.md      ← 科研工作流
├── topics/                       ← 各研究方向独立
│   ├── fsi-coatings/             ← 当前: FSI+涂层
│   │   ├── papers/               ← 论文笔记
│   │   ├── notes/                ← 专题知识
│   │   ├── codes/                ← 数值代码
│   │   ├── projects/             ← 项目管理
│   │   └── presentations/        ← 汇报文件
│   └── (new-topic)/              ← 新方向直接加
└── README.md
```

**核心规则：**
- 每种 **方向** → `topics/{topic}/` 自包含，互不干扰
- 每篇 **论文** → `topics/{topic}/papers/{作者}-{年份}-{关键词}/`
- 每段 **代码** → `topics/{topic}/codes/`

## 🚀 快速开始

```bash
# 1. 克隆
git clone https://github.com/zc-xzc/fsi-coatings.git
cd fsi-coatings

# 2. 进入研究方向
cd topics/fsi-coatings

# 3. 查看任务清单
cat projects/project-001/tasks.md

# 4. 安装FEniCS环境
conda create -n fenicsx -c conda-forge fenics-dolfinx
conda activate fenicsx

# 5. 跑第一个教程代码
python codes/tutorial/fenics/heat_conduction.py
```

## 🔧 共享资源速查

| 资源 | 说明 | 链接 |
|------|------|------|
| 📄 **论文笔记模板** | 标准化记录格式 | [`shared/templates/paper-notes.md`](shared/templates/paper-notes.md) |
| 📖 **术语表** | 跨方向术语积累 | [`shared/glossary.md`](shared/glossary.md) |
| 🧭 **科研工作流** | Zotero→笔记→代码→论文全流程 | [`shared/research-workflow.md`](shared/research-workflow.md) |
| 📚 **教材书单** | 15+本推荐教材 | [`shared/references/books.md`](shared/references/books.md) |
| 🎓 **课程资源** | 20+门在线课程 | [`shared/references/courses.md`](shared/references/courses.md) |
| 🏅 **目标期刊** | 各方向投稿参考 | [`shared/references/journal-list.md`](shared/references/journal-list.md) |
| 🔍 **检索策略** | 中英文检索关键词 | [`shared/references/search-strategy.md`](shared/references/search-strategy.md) |
| ⚙️ **安装指南** | 全工具环境配置 | [`shared/references/software-install-guide.md`](shared/references/software-install-guide.md) |

## 📖 学习路线图

```
第一层: 基础 (开学前)
├── Python科学计算 + Linux + Git + Markdown

第二层: 核心 (研一上)
├── 连续介质力学 + FEM基础 + CFD基础
├── FEniCSx + OpenFOAM

第三层: 专题 (研一下)
├── FSI理论(ALE/浸入边界) + preCICE
├── 相场法 + CFD-DEM

第四层: 深入 (研二)
├── 高精度数值方法 + 并行计算
├── ML辅助仿真 + 实验验证
```

## 📝 如何贡献

本项目为个人科研笔记仓库，欢迎参考使用。

- 发现错误 → 提 [Issue](https://github.com/zc-xzc/fsi-coatings/issues)
- 有建议 → 提 [Discussion](https://github.com/zc-xzc/fsi-coatings/discussions)

## 📄 License

MIT License — 自由使用、修改、分享。
