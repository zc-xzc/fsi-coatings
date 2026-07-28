# 📁 仓库完整结构

> 最后更新: 2026-07-28

## 总览

```
fsi-coatings/                           # 仓库根目录
│
├── README.md                           # 🏠 仓库导航
├── .gitignore                          # 忽略规则
├── LICENSE                             # MIT 许可
├── Dockerfile                          # 🐳 Docker 环境
├── docker-compose.yml                  # 🐳 Docker Compose
├── .github/
│   ├── workflows/ci.yml               # 🤖 自动CI检查
│   ├── ISSUE_TEMPLATE/                 # 标准化Issue
│   │   ├── paper-reading.md
│   │   └── research-idea.md
│   └── PULL_REQUEST_TEMPLATE.md        # PR模板
│
├── shared/                             # 🔄 跨方向共享
│   ├── templates/
│   │   ├── paper-notes.md              # 论文笔记模板
│   │   └── project-proposal.md         # 项目提案模板
│   ├── glossary.md                     # 📖 40+术语
│   ├── research-workflow.md            # 🧭 工作流指南
│   └── references/
│       ├── books.md                    # 📚 20+本教材
│       ├── courses.md                  # 🎓 15+门课程
│       ├── journal-list.md             # 🏅 20+本期刊
│       ├── search-strategy.md          # 🔍 检索策略
│       ├── software-install-guide.md   # ⚙️ 安装指南
│       └── fsi-coatings.bib            # 📄 完整BibTeX
│
├── topics/
│   └── fsi-coatings/                   # 🛡️ 当前研究方向
│       │
│       ├── README.md                   # 方向入口
│       │
│       ├── papers/                     # 📄 论文库
│       │   ├── README.md               # 索引+种子文献
│       │   ├── literature-map.md       # 文献地图
│       │   ├── search-strategy.md      # 检索策略
│       │   └── qi-yanfu-2026-steel-bridge-coating/
│       │       ├── notes.md            # 总笔记
│       │       ├── ch1-notes.md        # 第1章
│       │       ├── ch2-notes.md        # 第2章
│       │       ├── ch3-notes.md        # 第3章 ⭐
│       │       ├── ch4-notes.md        # 第4章
│       │       ├── ch5-notes.md        # 第5章
│       │       ├── ch6-notes.md        # 第6章 ⭐
│       │       └── ch7-notes.md        # 第7章
│       │
│       ├── notes/                      # 🧠 专题知识
│       │   ├── FSI-basics.md           # FSI基础
│       │   ├── coating-theory.md       # 涂层理论
│       │   ├── coating-ch2-thermal-model.md  # 第2章深度
│       │   ├── coating-ch3-RPT-model.md     # 第3章深度 ⭐
│       │   ├── numerical-methods.md    # 数值方法
│       │   ├── software-compare.md     # 工具对比
│       │   └── material-parameters.md  # 材料参数
│       │
│       ├── codes/                      # 💻 可运行代码
│       │   ├── requirements.txt        # 依赖
│       │   ├── tutorial/
│       │   │   ├── README.md           # 运行指南
│       │   │   ├── fenics/
│       │   │   │   ├── heat_conduction.py          # 热传导
│       │   │   │   ├── linear_elasticity.py        # 热应力
│       │   │   │   ├── thermal_cycling_coating.py  # 完整热-力耦合 🔥
│       │   │   │   ├── phase_field_fracture.py     # 相场法断裂 🔥
│       │   │   │   └── czm_pull_off.py             # CZM拉拔 🔥
│       │   │   ├── openfoam/
│       │   │   │   └── README-erosion-case.md      # CFD-DEM冲蚀框架
│       │   │   ├── gmsh/
│       │   │   │   ├── coating_mesh.py             # 网格生成器
│       │   │   │   └── coating_mesh_full.py        # 完整网格生成
│       │   │   └── python/
│       │   │       ├── plot_style.py               # 绘图模板
│       │   │       ├── paper_data_analysis.ipynb   # Jupyter分析
│       │   │       └── digitize_paper_data.py      # 数据提取
│       │   └── reproduction/qi-yanfu/
│       │       ├── reproduction-plan.md            # 复现计划
│       │       ├── rpt_model_fitting.py            # RPT参数拟合
│       │       └── run_all.py                      # 统一运行入口
│       │
│       ├── projects/project-001/       # 📋 项目管理
│       │   ├── proposal.md             # 项目提案
│       │   ├── tasks.md                # 任务清单
│       │   ├── journal.md              # 研究日志
│       │   ├── progress.md             # 进度追踪
│       │   └── roadmap.md              # 全年路线图
│       │
│       ├── presentations/              # 🎤 汇报
│       │   └── 2026-09-coating-report/
│       │       ├── script.md           # 讲稿
│       │       ├── outline.md          # PPT大纲
│       │       └── meeting-notes.md    # 导师交流准备
│       │
│       └── data/                       # 📊 数据
│           └── processed/
│               └── adhesion_thickness_data.csv
│
└── archive/                            # 🗄️ 归档
