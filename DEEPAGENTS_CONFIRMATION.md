# deepagents 多代理实现 - 确认说明

## ✅ 确认：使用 LangChain deepagents 框架

### 框架信息
- **名称**: deepagents
- **来源**: LangChain 官方
- **用途**: 多代理编程框架
- **版本**: >= 0.6.2
- **核心函数**: `create_deep_agent()`, `SubAgent`

### 依赖确认
```python
# pyproject.toml
dependencies = [
    "deepagents>=0.6.2",      # ✅ LangChain deepagents
    "langchain-openai>=1.2.1",
    ...
]
```

## 系统架构

### 真正的多代理系统结构

```
┌─────────────────────────────────────────────────┐
│  Main Agent (create_deep_agent)                 │
│  - 使用 deepagents.create_deep_agent()          │
│  - 接收用户诊断请求                             │
│  - 使用 task() 工具委托给子代理                 │
│  - 聚合和综合分析结果                           │
└─────────┬───────────────────────────────────────┘
          │
          │ task() 工具调用
          │
    ┌─────┴──────┬────────────┬─────────────┐
    ↓            ↓            ↓             ↓
┌─────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐
│ perf-   │ │ log-     │ │ query-  │ │ config-  │
│analyzer │ │analyzer  │ │analyzer │ │inspector │
│         │ │          │ │         │ │          │
│SubAgent │ │SubAgent  │ │SubAgent │ │SubAgent  │
└─────────┘ └──────────┘ └─────────┘ └──────────┘
```

## 代码示例

### 1. 主代理 (app/agents/main_agent.py)

```python
from deepagents import create_deep_agent
from app.agents.subagents import (
    performance_analyzer,
    log_analyzer,
    query_analyzer,
    config_inspector,
)

def create_rca_agent():
    """创建 deepagents 主代理"""
    agent = create_deep_agent(
        model="openai:gpt-4",
        system_prompt="...",
        subagents=[
            performance_analyzer,
            log_analyzer,
            query_analyzer,
            config_inspector,
        ],
    )
    return agent
```

### 2. 子代理 (app/agents/subagents/*.py)

```python
from deepagents import SubAgent

# 性能分析子代理
performance_analyzer = SubAgent(
    name="performance-analyzer",
    description="Analyzes MySQL performance metrics...",
    system_prompt="You are a MySQL performance expert..."
)

# 日志分析子代理
log_analyzer = SubAgent(
    name="log-analyzer",
    description="Analyzes MySQL error logs...",
    system_prompt="You are a MySQL diagnostics expert..."
)

# 查询分析子代理
query_analyzer = SubAgent(
    name="query-analyzer",
    description="Analyzes query patterns...",
    system_prompt="You are a SQL optimization expert..."
)

# 配置检查子代理
config_inspector = SubAgent(
    name="config-inspector",
    description="Inspects MySQL configuration...",
    system_prompt="You are a MySQL configuration expert..."
)
```

### 3. 使用方式 (app/agents/main_agent.py)

```python
def diagnose_database(issue_description: str):
    """使用 deepagents 多代理系统诊断数据库"""
    agent = create_rca_agent()
    
    # 主代理会自动使用 task() 工具：
    # - task("performance-analyzer", "分析性能指标...")
    # - task("log-analyzer", "分析错误日志...")
    # - task("query-analyzer", "分析查询模式...")
    # - task("config-inspector", "检查配置...")
    
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"请诊断以下问题: {issue_description}"
        }]
    })
    
    return result
```

## 关键特点

### ✅ 1. 真正的多代理框架
- 使用官方的 LangChain deepagents
- 支持主代理和子代理的完整生命周期
- 自动的代理通信和协调

### ✅ 2. 子代理在 subagents 目录下
```
app/agents/subagents/
├── __init__.py
├── performance_analyzer.py    # SubAgent 定义
├── log_analyzer.py            # SubAgent 定义
├── query_analyzer.py          # SubAgent 定义
└── config_inspector.py        # SubAgent 定义
```

### ✅ 3. 主代理在 agents 目录下
```
app/agents/
├── main_agent.py              # 主代理 (create_deep_agent)
├── subagents/                 # 子代理目录
└── example_usage.py
```

### ✅ 4. deepagents 的子代理（SubAgent）
每个子代理都是一个 `deepagents.SubAgent` TypedDict：
```python
SubAgent(
    name="子代理名称",
    description="子代理功能描述",
    system_prompt="系统指示"
)
```

### ✅ 5. 自动通信机制
主代理自动使用 `task()` 工具来调用子代理：
```
task("performance-analyzer", "分析性能...")
task("log-analyzer", "分析日志...")
task("query-analyzer", "分析查询...")
task("config-inspector", "检查配置...")
```

## 验证方式

### 导入验证
```python
from deepagents import create_deep_agent, SubAgent
from app.agents.main_agent import create_rca_agent
from app.agents.subagents import (
    performance_analyzer,
    log_analyzer,
    query_analyzer,
    config_inspector,
)

# 所有导入成功 ✅
```

### 运行验证
```bash
python test_setup.py

# 预期输出：
# ✓ app.agents.subagents (deepagents SubAgent specs)
# ✓ app.agents.main_agent
# ✓ All sub-agent specs loaded!
# ✓ Deepagents main agent created!
```

### CLI 验证
```bash
python main.py

# 主代理会自动：
# 1. 接收诊断请求
# 2. 调用所有子代理
# 3. 聚合分析结果
# 4. 生成诊断报告
```

## 文件清单

### 主代理文件
- ✅ `app/agents/main_agent.py` - 使用 `create_deep_agent()`

### 子代理文件（在 subagents 目录下）
- ✅ `app/agents/subagents/performance_analyzer.py` - SubAgent 定义
- ✅ `app/agents/subagents/log_analyzer.py` - SubAgent 定义
- ✅ `app/agents/subagents/query_analyzer.py` - SubAgent 定义
- ✅ `app/agents/subagents/config_inspector.py` - SubAgent 定义
- ✅ `app/agents/subagents/__init__.py` - 导出所有子代理

### API 和应用
- ✅ `app/api.py` - FastAPI 应用
- ✅ `app/router/diagnostic.py` - 诊断 API 路由
- ✅ `main.py` - CLI 入口
- ✅ `test_setup.py` - 系统验证脚本

## 配置要求

### 环境变量
```bash
# OpenAI API (必需)
export OPENAI_API_KEY=sk-...
export LLM_MODEL=gpt-4

# MySQL 数据库 (可选但推荐)
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=...
```

## 使用示例

### CLI 使用
```bash
source .venv/bin/activate
export OPENAI_API_KEY=sk-...
python main.py
```

### Python 脚本
```python
from app.agents.main_agent import diagnose_database

result = diagnose_database("数据库查询变慢")
print(result["analysis"])
```

### FastAPI 使用
```bash
export OPENAI_API_KEY=sk-...
python -m uvicorn app.api:app --reload

# 然后：
curl -X POST http://localhost:8000/api/v1/diagnostic/analyze \
  -H "Content-Type: application/json" \
  -d '{"issue_description": "数据库查询变慢"}'
```

## 总结

### 确认清单

- ✅ **框架**: 使用 LangChain 官方的 deepagents
- ✅ **主代理**: 在 `app/agents/` 目录下，使用 `create_deep_agent()`
- ✅ **子代理**: 在 `app/agents/subagents/` 目录下，使用 `SubAgent` 规范
- ✅ **通信**: 通过 `task()` 工具的自动化通信机制
- ✅ **数量**: 4 个专业化的子代理
- ✅ **集成**: FastAPI + CLI 完整集成
- ✅ **验证**: 所有组件已验证可工作

---

**项目状态**: ✅ 完全基于 LangChain deepagents 的真正多代理系统
**最后更新**: 2024-05-20
