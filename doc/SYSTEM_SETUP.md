# MySQL RCA 多智能体系统 - 完整设置说明

## 项目概述

这是一个基于 **deepagents** 框架的多智能体应用系统，用于 MySQL 数据库的故障诊断和根因分析（RCA）。系统通过多个专业的子智能体协同工作，提供全面的数据库诊断和优化建议。

## 系统架构

### 核心结构

```
app/
├── core/                           # 核心模块
│   ├── config.py                  # 配置管理
│   └── database.py                # 数据库连接管理
│
├── agents/                         # 多智能体系统
│   ├── root_cause_analyzer.py     # 主控制智能体（使用deepagents）
│   └── subagents/                 # 4个专业子智能体
│       ├── performance_analyzer.py   # 性能分析
│       ├── log_analyzer.py          # 日志分析
│       ├── query_analyzer.py        # 查询分析
│       └── config_inspector.py      # 配置检查
│
├── router/                         # FastAPI 路由
│   └── diagnostic.py              # 诊断 API 端点
│
└── api.py                         # FastAPI 应用主文件
```

## 已创建的文件清单

### 核心文件

| 文件 | 说明 |
|------|------|
| `app/core/config.py` | 配置管理 - 数据库、LLM、智能体配置 |
| `app/core/database.py` | 数据库连接 - SQLAlchemy 连接池、查询执行 |

### 智能体文件

| 文件 | 说明 |
|------|------|
| `app/agents/root_cause_analyzer.py` | 主控制智能体 - 使用deepagents协调所有子智能体 |
| `app/agents/subagents/performance_analyzer.py` | 性能分析智能体 |
| `app/agents/subagents/log_analyzer.py` | 日志分析智能体 |
| `app/agents/subagents/query_analyzer.py` | 查询分析智能体 |
| `app/agents/subagents/config_inspector.py` | 配置检查智能体 |

### API 文件

| 文件 | 说明 |
|------|------|
| `app/api.py` | FastAPI 主应用 |
| `app/router/diagnostic.py` | 诊断 API 端点定义 |

### 应用文件

| 文件 | 说明 |
|------|------|
| `main.py` | CLI 命令行入口 |
| `test_setup.py` | 系统验证脚本 |

### 文档文件

| 文件 | 说明 |
|------|------|
| `README.md` | 完整用户文档 |
| `ARCHITECTURE.md` | 系统架构详细说明 |
| `PROJECT_STRUCTURE.md` | 项目结构详解 |
| `QUICKSTART.md` | 快速开始指南 |
| `SYSTEM_SETUP.md` | 本文件 |

### 配置文件

| 文件 | 说明 |
|------|------|
| `pyproject.toml` | Python 项目配置（已更新） |
| `.env.example` | 环境变量模板 |

## 多智能体系统设计

### 数据流

```
用户请求
    ↓
RootCauseAnalyzer (主控制智能体)
    ├─→ PerformanceAnalyzer.analyze()
    │   └─→ 获取性能指标
    │
    ├─→ LogAnalyzer.analyze()
    │   └─→ 获取日志和错误模式
    │
    ├─→ QueryAnalyzer.analyze()
    │   └─→ 获取查询优化建议
    │
    └─→ ConfigInspector.analyze()
        └─→ 获取配置问题
    ↓
数据聚合 → LLM 分析 → 推荐生成
    ↓
诊断报告
```

### 子智能体功能

#### 1. 性能分析智能体 (PerformanceAnalyzer)

**分析内容：**
- 慢查询检测和统计
- 连接池利用率
- 缓存命中率
- 磁盘 I/O 分析

**输出示例：**
```
Performance Analysis by Performance Analyzer:
⚠️  Found 5 slow queries
📊 Connection utilization: 45.3%
```

#### 2. 日志分析智能体 (LogAnalyzer)

**分析内容：**
- 错误计数统计
- 常见错误模式识别
- 系统警告提取
- 复制状态检查

**输出示例：**
```
Log Analysis by Log Analyzer:
✓ No significant connection errors
📋 Found 3 distinct error types
⚠️  2 system warnings detected
```

#### 3. 查询分析智能体 (QueryAnalyzer)

**分析内容：**
- 慢查询优化建议
- 表统计和碎片化分析
- 索引使用情况
- 锁冲突检测

**输出示例：**
```
Query Analysis by Query Analyzer:
⚠️  Found 5 slow queries
📊 8 tables are fragmented
🔍 12 unused indexes found
```

#### 4. 配置检查智能体 (ConfigInspector)

**分析内容：**
- 内存配置验证
- 连接设置审查
- 日志配置检查
- InnoDB 参数优化

**输出示例：**
```
Configuration Analysis by Configuration Inspector:
⚠️  Memory issues: innodb_buffer_pool_size is too small
📋 Logging recommendations: 2 issues
🔧 InnoDB optimizations: 1 recommendation
```

## 依赖关系

### 主要依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| `deepagents` | >=0.6.2 | 多智能体框架 |
| `langchain-openai` | >=1.2.1 | LLM 集成 |
| `fastapi` | >=0.136.1 | Web API 框架 |
| `sqlalchemy` | >=2.0.49 | ORM 和数据库抽象 |
| `pymysql` | >=1.1.0 | MySQL 驱动 |

### 安装依赖

```bash
# 使用 uv（推荐）
/Users/jihui/app/uv-aarch64/uv sync

# 或使用 pip
pip install -e .
```

## 配置要求

### 环境变量

**MySQL 配置：**
```bash
export MYSQL_HOST=localhost           # MySQL 主机
export MYSQL_PORT=3306               # MySQL 端口
export MYSQL_USER=root               # 数据库用户
export MYSQL_PASSWORD=               # 数据库密码
export MYSQL_DATABASE=mysql          # 目标数据库
```

**LLM 配置：**
```bash
export OPENAI_API_KEY=sk-...         # 必需！OpenAI API 密钥
export LLM_MODEL=gpt-4               # 使用的模型
export LLM_TEMPERATURE=0.7           # 温度参数
export LLM_MAX_TOKENS=2048           # 最大 token 数
```

**智能体配置：**
```bash
export AGENT_MAX_ITERATIONS=10       # 最大迭代次数
export AGENT_TIMEOUT=300             # 超时时间（秒）
export AGENT_VERBOSE=true            # 详细日志
export AGENT_DEBUG=false             # 调试模式
```

## 使用方式

### 1. CLI 使用

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行诊断
python main.py
```

### 2. API 使用

```bash
# 启动 API 服务
python -m uvicorn app.api:app --reload --host 0.0.0.0 --port 8000

# 健康检查
curl http://localhost:8000/health

# 运行诊断
curl -X POST http://localhost:8000/api/v1/diagnostic/analyze \
  -H "Content-Type: application/json" \
  -d '{"issue_description": "数据库查询变慢"}'

# 获取诊断报告
curl "http://localhost:8000/api/v1/diagnostic/report?issue=数据库查询变慢"
```

### 3. Python 脚本使用

```python
from app.agents.root_cause_analyzer import RootCauseAnalyzer

analyzer = RootCauseAnalyzer()

# 运行诊断
diagnosis = analyzer.diagnose("数据库查询变慢")

# 获取格式化报告
report = analyzer.get_diagnostic_report("数据库查询变慢")
print(report)

# 访问详细结果
print(diagnosis['recommendations'])
```

## 验证系统

```bash
# 运行测试脚本
source .venv/bin/activate
python test_setup.py
```

**预期输出：**
```
✓ Configuration loaded!
✓ Sub-agents loaded!
✓ Orchestrator initialized!

✗ Database connection failed!  (预期 - 需要 MySQL)
```

## 诊断输出示例

```json
{
  "status": "complete",
  "issue_description": "数据库查询变慢",
  "findings_summary": {
    "performance_status": "warning",
    "log_status": "ok",
    "query_status": "warning",
    "config_status": "ok"
  },
  "recommendations": [
    "优化识别的慢查询",
    "对碎片化的表进行碎片整理",
    "移除未使用的索引",
    "启用慢查询日志"
  ],
  "analysis": "[LLM 分析结果]"
}
```

## API 端点清单

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/health` | 系统健康检查 |
| POST | `/api/v1/diagnostic/analyze` | 运行诊断分析 |
| GET | `/api/v1/diagnostic/report` | 获取诊断报告 |
| GET | `/api/v1/diagnostic/metrics` | 获取性能指标 |
| GET | `/api/v1/diagnostic/slow-queries` | 获取慢查询列表 |
| GET | `/api/v1/diagnostic/table-stats` | 获取表统计信息 |
| GET | `/api/v1/diagnostic/lock-info` | 获取锁定信息 |
| GET | `/api/v1/diagnostic/process-list` | 获取进程列表 |

## deepagents 集成

RootCauseAnalyzer 使用 deepagents 框架：

```python
from deepagents import SubAgent

self.subagent = SubAgent(
    name=self.name,
    description=self.description,
    model=settings.llm.model,
    verbose=settings.agent.verbose,
)
```

**特点：**
- 自动化工具使用
- 迭代推理能力
- 可配置的迭代次数
- 错误恢复机制

## 扩展系统

### 添加新的子智能体

1. 创建新文件：`app/agents/subagents/new_analyzer.py`
2. 实现分析类和接口
3. 在 `RootCauseAnalyzer` 中注册

### 自定义 LLM

```python
from langchain_community.llms import MyCustomLLM

self.llm = MyCustomLLM(...)
```

## 故障排查

### MySQL 连接失败

```
Error: Can't connect to MySQL server
```

**解决方案：**
- 确保 MySQL 正在运行
- 检查 `MYSQL_HOST` 和 `MYSQL_PORT`
- 验证用户凭证

### OPENAI_API_KEY 未设置

```
Error: Missing credentials
```

**解决方案：**
- 设置 `OPENAI_API_KEY` 环境变量
- 验证 API 密钥有效性
- 检查 API 配额

### Performance Schema 不可用

```
Error: Failed to fetch slow queries
```

**解决方案：**
- 在 MySQL my.cnf 中启用：`performance_schema=ON`
- 重启 MySQL：`systemctl restart mysql`

## 项目特点

✅ **多智能体协调** - 4 个专业子智能体的有机组合
✅ **LLM 驱动** - 使用 OpenAI GPT 进行智能分析
✅ **全面诊断** - 性能、日志、查询、配置四大维度
✅ **REST API** - 完整的 FastAPI 集成
✅ **可扩展** - 易于添加新的分析器
✅ **详细报告** - 结构化的诊断结果和建议

## 下一步

1. **配置 MySQL** - 启用 performance_schema
2. **获取 API 密钥** - 从 OpenAI 获取
3. **运行诊断** - 执行 `python main.py`
4. **启动 API** - 部署为微服务
5. **集成监控** - 融入现有监控系统

## 相关文档

- [README.md](README.md) - 完整文档
- [ARCHITECTURE.md](ARCHITECTURE.md) - 系统架构
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构

## 许可证

MIT
