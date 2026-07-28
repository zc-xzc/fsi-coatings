# Research Notebook

> 多方向科研笔记仓库 | 同一套工作流，跨研究方向复用

## 📂 研究方向

| 方向 | 目录 | 状态 | 简介 |
|------|------|------|------|
| 🛡️ FSI + 涂层 | `topics/fsi-coatings/` | ✅ 活跃 | 流固耦合数值模拟 × 钢结构涂层多场耦合老化 |
| 📝 待添加 | — | ⏳ | |

## 🔧 共享资源

| 资源 | 链接 |
|------|------|
| 📄 论文笔记模板 | [shared/templates/paper-notes.md](shared/templates/paper-notes.md) |
| 📖 术语表 | [shared/glossary.md](shared/glossary.md) |
| 🧭 科研工作流 | [shared/research-workflow.md](shared/research-workflow.md) |
| 📚 教材书单 | [shared/references/books.md](shared/references/books.md) |
| 🎓 课程资源 | [shared/references/courses.md](shared/references/courses.md) |
| 🏅 目标期刊 | [shared/references/journal-list.md](shared/references/journal-list.md) |
| 🔍 检索策略 | [shared/references/search-strategy.md](shared/references/search-strategy.md) |
| ⚙️ 安装指南 | [shared/references/software-install-guide.md](shared/references/software-install-guide.md) |

## 📐 架构说明

```
research-notebook/
├── shared/                  ← 跨方向共享（模板/术语/工作流/参考）
├── topics/                  ← 各研究方向独立目录
│   ├── fsi-coatings/        ← 当前方向：FSI + 涂层
│   │   ├── papers/          ← 本方向论文（命名: 作者-年份-关键词）
│   │   ├── notes/           ← 本方向专题笔记
│   │   ├── codes/           ← 本方向代码
│   │   ├── projects/        ← 本方向项目管理
│   │   └── presentations/   ← 本方向汇报
│   └── (future-topic)/      ← 新方向直接加
└── .github/                 ← Issue 模板
```

**规则：**
- 新增论文 → `topics/{topic}/papers/{作者}-{年份}-{关键词}/`
- 新方向 → `topics/{方向名}/` 自包含
- 跨方向通用资源 → `shared/`

## 🚀 快速开始

```bash
# 克隆
git clone git@github.com:zc-xzc/research-notebook.git
cd research-notebook

# 进入当前方向
cd topics/fsi-coatings

# 按 tasks.md 任务清单推进
```
