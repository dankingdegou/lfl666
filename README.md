# 订单异常识别检测 Agent

## 项目简介

这是一个电商零售方向的数据分析 Agent 课程项目。最终目标包括订单明细分析、异常大额订单识别、高退单率地区分析、异常样本筛选和异常结果汇总。

**当前进度：Day 1**

目前仅完成项目初始化和基础数据探查模块，尚未实现异常识别或 Agent 业务逻辑。

## 当前目录结构

```text
agent-analyzer/
├── frontend/
│   └── .gitkeep
├── backend/
│   └── data_explorer.py
├── mcp_server/
│   └── .gitkeep
├── data/
│   └── .gitkeep
├── output/
│   └── .gitkeep
├── ai_dev_log/
│   └── day01.md
├── docs/
│   └── .gitkeep
├── requirements.txt
├── README.md
└── .gitignore
```

## 环境要求

- Python >= 3.10
- pandas >= 2.0

## 安装依赖

建议在项目根目录创建并启用虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 数据文件

课程提供的原始数据文件应放置在：

```text
data/sales_orders.csv
```

仓库不会生成或伪造课程数据。如果该文件不存在，数据探查脚本会提示补充文件后重新运行。

## 运行 D1 数据探查

在项目根目录、已启用虚拟环境的情况下运行：

```bash
python backend/data_explorer.py
```

脚本只读取原始 CSV，输出数据规模、列信息、缺失值、重复行、数值列统计和分类列分布，不会清洗或覆盖原始数据。

## Day 1 完成内容

- 建立课程要求的项目目录
- 编写函数化数据探查脚本
- 配置 D1 所需的 pandas 依赖
- 建立 AI 开发日志和基础 README
- 使用 `day01` 分支记录 D1 开发过程

## 尚未实现

- FastAPI
- FastMCP
- LLM Agent
- 前端可视化
- 异常订单检测
- 退单率分析

以上功能将在后续课程阶段逐步完成。
