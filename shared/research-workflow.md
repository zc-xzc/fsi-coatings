# 🧭 科研工作流完整指南

> 从文献管理到论文产出的全流程标准化

## 总览

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  读论文   │ → │  做笔记   │ → │  复现代码  │ → │ 形成想法  │ → │  写论文   │
│  Zotero  │   │  GitHub  │   │ FEniCS/  │   │ proposal │   │  LaTeX   │
│  管理文献  │   │ Markdown │   │ OpenFOAM │   │ project  │   │ Overleaf │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

## 一、文献管理流程

### 1.1 Zotero 配置
```bash
1. 下载安装: https://www.zotero.org/download/
2. 安装 Better BibTeX 插件:
   工具 → 插件 → 搜索 Better BibTeX → 安装
3. 配置 Citation Key:
   编辑 → 首选项 → Better BibTeX
   格式: [auth:lower]_[year]
4. 安装浏览器插件 (Zotero Connector):
   一键保存网页上的论文信息
```

### 1.2 文件夹体系
```
Zotero 文件夹:
FSI-Coating (主文件夹)
├── 涂层基础理论 (RPT/应力/冲蚀/老化)
├── 涂层数值模拟 (多场耦合/相场/CZM)
├── FSI方法 (ALE/IBM/CFD-DEM/耦合库)
├── 力学基础 (连续介质/断裂/疲劳)
└── 工具教程 (FEniCS/OpenFOAM/preCICE)
```

### 1.3 阅读-笔记流程
```
发现论文 → Zotero 抓取元数据 → citation key
  → 方向目录新建文件夹: papers/{作者-年份-关键词}/
  → 写 notes.md (使用模板)
  → 提取关键图表到 figures/
  → 补充到专题笔记 (notes/xxx.md)
  → 更新论文索引 (papers/README.md)
```

## 二、每日科研工作流

### 推荐的作息
```
上午 (09:00-12:00) — 最清醒, 适合深度阅读
  读论文 15面 → 写章节笔记 → 记录待解决问题

下午 (14:00-17:00) — 动手实践
  学工具 (FEniCS/OpenFOAM) → 跑代码 → 记录日志

晚上 (20:00-22:00) — 轻松输入
  看综述/教程视频 → 整理参考文献 → 计划明天
```

### 每日输出
```
每天至少产出:
  1 份阅读笔记  →  topics/{topic}/papers/{paper}/notes.md
  1 行日志      →  topics/{topic}/projects/{project}/journal.md
  1 条术语      →  shared/glossary.md （可选）
```

## 三、Git 工作流

### 基本原则
- **所有变更走 PR** — 不直接推 main
- **每步一个分支** — 完成→合并→删除
- **提交信息清晰** — 前缀表明类型

### 提交信息规范
```
[Step N] 简短描述

具体说明:
- 改了什么
- 为什么改
```

### 每周维护
```bash
# 每周末打 tag
git tag v2026-08-01-week1
git push --tags
```

## 四、论文产出流程

```
形成研究想法
  → 写 research proposal (使用模板)
  → 跟导师讨论
  → 做数值算例, 收集结果
  → 验证 (与实验数据或文献对比)
  → 写论文初稿
  → 修改, 组内预讲
  → 投稿
```

## 五、工具链关系

```
研究问题定义 (涂层多场耦合 + FSI)
      │
   ┌──┼──┐
   ▼  ▼  ▼
理论  数值  实验
分析  模拟  验证
      │
      ▼
结果分析 & 可视化 (Python/Matplotlib)
      │
      ▼
论文写作 & 汇报 (LaTeX/PowerPoint)
```
