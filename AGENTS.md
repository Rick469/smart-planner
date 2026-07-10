# Smart Planner - Codex分析约束文件

本文件用于限制Codex / Agent代码扫描范围，减少token消耗，提高分析精度。

---

# 🚫 禁止分析文件（IMPORTANT）

以下内容 **禁止默认读取或分析**：

## 环境与配置
- .env
- requirements.txt
- .gitignore
- README.md

## 虚拟环境
- .venv/**

## 日志文件
- logs/**

## 数据库文件
- *.db（如 planner.db，仅在调试缓存时允许查看）

## 外部依赖库
- External Libraries

---

# 核心文件

以下文件需**重点分析**：
- python文件：*.py
- 配置文件：*.yaml

**重要**：如果识别到不在上述类型中的文件且需要进行分析时，需向我确认是否执行分析


# 📁 项目架构目录

```text id="z1k9pl"
smart-planner/
│
├── run.py                          # 🚀 项目入口
│
├── agents/                         # 🧠 所有Agent与Prompt集中层
│
│   ├── base_agent.py              # BaseAgent（所有Agent基类）
│   ├── planner_agent.py           # 🧭 Planner Agent
│   ├── weather_agent.py           # 🌦 Weather Agent
│   ├── hotel_agent.py             # 🏨 Hotel Agent
│   ├── attraction_agent.py        # 📍 Attraction Agent
│
│   ├── prompts/                   # 📝 Prompt定义
│   │   ├── planner_prompt.py
│   │   ├── weather_prompt.py
│   │   ├── hotel_prompt.py
│   │   └── attraction_prompt.py
│
│   ├── service/                        # ⚙️ 系统服务层（非Agent）
│       ├── agent_service.py           # Agent调度器
│       ├── mcp_service.py             # MCP工具调用层（高德/天气/酒店）
│       ├── sqlite_service.py          # SQLite缓存服务
│
├── models/                         # 📦 数据结构定义
│   ├── schema.py
│
├── utils/                          # 🔧 工具函数
│   ├── logger.py
│
├── logs/                           # 📊 运行日志（禁止分析）
│
├── planner.db                      # 💾 SQLite缓存（慎用）
│
└── .env                            # ⚙️ 环境变量（禁止分析）

```


---
# 重要提示

代码修改后如果涉及以下内容，需对本md文档修改：
- 新增/修改/删除了禁止分析文件：编辑【禁止分析文件】模块对应内容
- 新增/修改/删除了核心文件类型：编辑此文档【核心文件】模块对应内容
- 新增/修改/删除了项目架构目录，编辑此文档【项目架构目录】模块对应内容


