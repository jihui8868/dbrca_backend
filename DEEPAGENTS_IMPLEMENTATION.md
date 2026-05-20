# MySQL RCA - deepagents 多代理实现

## 确认：使用 LangChain deepagents 框架

✅ **确认使用**: `langchain` 的官方 `deepagents` 框架
✅ **版本**: deepagents >= 0.6.2
✅ **框架**: LangChain 官方多代理编程框架

## 架构设计

### 主代理 (Main Agent)

**文件**: `app/agents/main_agent.py`

使用 `deepagents.create_deep_agent()` 创建主代理：

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model=settings.llm.model,
    system_prompt=system_prompt,
    subagents=[
        performance_analyzer,
        log_analyzer,
        query_analyzer,
        config_inspector,
    ],
)
```

**主代理职责**:
- 接收诊断请求
- 使用 `task()` 工具委托给子代理
- 聚合所有子代理的分析结果
- 执行综合的根因分析
- 生成结构化的诊断报告

**系统提示特点**:
- 定义了 4 个子代理的使用场景
- 说明了工作流程（委托 → 综合 → 呈现）
- 指导报告格式化方式

### 子代理 (Sub-Agents)

**目录**: `app/agents/subagents/`

每个子代理都是一个 `deepagents.SubAgent` 的 TypedDict 定义：

#### 1. Performance Analyzer
**文件**: `performance_analyzer.py`

```python
from deepagents import SubAgent

performance_analyzer = SubAgent(
    name="performance-analyzer",
    description="分析 MySQL 性能指标...",
    system_prompt="你是 MySQL 性能专家..."
)
```

**专业领域**:
- 慢查询分析
- 连接池利用率
- 缓存命中率
- 磁盘 I/O 模式

#### 2. Log Analyzer
**文件**: `log_analyzer.py`

```python
log_analyzer = SubAgent(
    name="log-analyzer",
    description="分析 MySQL 错误日志和诊断事件...",
    system_prompt="你是 MySQL 诊断专家..."
)
```

**专业领域**:
- 错误计数和模式
- 常见错误识别
- 系统警告提取
- 复制状态检查

#### 3. Query Analyzer
**文件**: `query_analyzer.py`

```python
query_analyzer = SubAgent(
    name="query-analyzer",
    description="分析查询执行模式和优化机会...",
    system_prompt="你是 SQL 优化专家..."
)
```

**专业领域**:
- 查询优化建议
- 表统计分析
- 索引使用分析
- 锁冲突检测

#### 4. Configuration Inspector
**文件**: `config_inspector.py`

```python
config_inspector = SubAgent(
    name="config-inspector",
    description="检查 MySQL 配置和系统变量...",
    system_prompt="你是 MySQL 配置专家..."
)
```

**专业领域**:
- 内存配置验证
- 连接设置检查
- 日志配置分析
- InnoDB 参数优化

## 通信机制

### 主代理 → 子代理

主代理使用 `task()` 工具调用子代理：

```
task("performance-analyzer", "Analyze the slow queries in this database...")
task("log-analyzer", "Check for error patterns and warnings...")
task("query-analyzer", "Identify optimization opportunities...")
task("config-inspector", "Review MySQL configuration settings...")
```

### 数据流

```
用户请求 (issue_description)
    ↓
主代理 (RCA Agent - create_deep_agent)
    ├─→ task() → performance-analyzer
    │   └─→ SubAgent 执行分析
    │       └─→ 返回性能诊断
    │
    ├─→ task() → log-analyzer
    │   └─→ SubAgent 执行分析
    │       └─→ 返回错误模式
    │
    ├─→ task() → query-analyzer
    │   └─→ SubAgent 执行分析
    │       └─→ 返回优化建议
    │
    └─→ task() → config-inspector
        └─→ SubAgent 执行分析
            └─→ 返回配置建议
    │
    ↓
聚合结果 (主代理综合所有输出)
    ↓
生成诊断报告 (结构化的 RCA 输出)
```

## 子代理定义结构

每个子代理遵循 `SubAgent` TypedDict 结构：

```python
SubAgent(
    name: str,                    # 唯一标识符 (必需)
    description: str,             # 功能描述 (必需)
    system_prompt: str,          # 系统指示 (必需)
    tools: Optional[List] = None, # 可用工具 (可选)
    model: Optional[str] = None,  # 模型覆盖 (可选)
)
```

### 系统提示设计

每个子代理的 `system_prompt` 包含：

1. **角色定义**: "你是 MySQL XXX 专家"
2. **职责列表**: 具体需要做什么
3. **输入数据说明**: 会接收什么数据
4. **输出格式要求**: 如何组织响应
5. **结构化指导**: 包含状态、指标、发现、建议

示例格式：
```
你是 MySQL 性能专家。

你的职责：
1. 分析慢查询...
2. 检查连接池...
3. 评估缓存效率...
4. 识别 I/O 瓶颈...

数据包括：
- 慢查询统计...
- 当前连接数...
- 缓存指标...

始终提供：
- 当前性能状态 (OK/WARNING/CRITICAL)
- 关键性能指标
- 识别的问题
- 具体的建议
```

## API 集成

### 诊断函数

**文件**: `app/agents/main_agent.py`

```python
def diagnose_database(issue_description: str):
    """
    运行综合性的数据库诊断
    
    Args:
        issue_description: 数据库问题描述
    
    Returns:
        主代理的诊断分析结果
    """
```

### FastAPI 路由

**文件**: `app/router/diagnostic.py`

```python
@router.post("/api/v1/diagnostic/analyze")
async def analyze_issue(request: DiagnosticRequest):
    """使用 deepagents 多代理系统分析问题"""
    result = diagnose_database(request.issue_description)
    return result
```

## 命令行使用

**文件**: `main.py`

```bash
source .venv/bin/activate
python main.py
```

输出示例：
```
Starting MySQL RCA Diagnostic System (deepagents Multi-Agent)

Testing database connection...
✓ Database connection successful

Diagnosing: Database queries are running slowly
============================================================

[主代理将调用所有子代理进行分析，生成综合诊断报告]
```

## 依赖配置

### pyproject.toml

```toml
dependencies = [
    "deepagents>=0.6.2",           # 多代理框架
    "langchain-openai>=1.2.1",     # OpenAI LLM 集成
    "fastapi>=0.136.1",            # Web API
    "sqlalchemy>=2.0.49",          # ORM
    "pymysql>=1.1.0",              # MySQL 驱动
]
```

## 系统验证

运行测试脚本确认 deepagents 正确集成：

```bash
source .venv/bin/activate
python test_setup.py
```

**验证项**:
- ✅ 所有模块导入成功
- ✅ 4 个子代理 spec 加载成功
- ✅ 主代理初始化成功
- ✅ deepagents 框架集成

## 诊断流程

1. **问题输入**
   ```
   issue_description = "数据库查询变慢"
   ```

2. **主代理初始化**
   ```
   agent = create_rca_agent()
   ```

3. **委托子代理**
   ```
   主代理使用 task() 工具:
   - 呼叫 performance-analyzer
   - 呼叫 log-analyzer
   - 呼叫 query-analyzer
   - 呼叫 config-inspector
   ```

4. **结果聚合**
   ```
   主代理综合所有子代理的输出:
   - 交叉验证发现
   - 识别模式和关联
   - 加权重要性
   ```

5. **报告生成**
   ```
   ## Root Cause Analysis Report
   
   ### 问题总结
   [问题描述]
   
   ### 严重性: CRITICAL/HIGH/MEDIUM/LOW
   
   ### 按领域的发现
   #### 性能分析
   [性能发现]
   
   #### 日志和事件分析
   [错误模式]
   
   #### 查询分析
   [查询优化]
   
   #### 配置分析
   [配置问题]
   
   ### 根本原因
   [识别的主要和次要原因]
   
   ### 立即行动
   1. [行动1] - [时间影响估计]
   2. [行动2] - [时间影响估计]
   
   ### 长期建议
   1. [优化1] - [预期效益]
   2. [优化2] - [预期效益]
   ```

## 扩展指南

### 添加新的子代理

1. 创建新文件: `app/agents/subagents/new_analyzer.py`

2. 定义子代理:
   ```python
   from deepagents import SubAgent
   
   new_analyzer = SubAgent(
       name="new-analyzer",
       description="...",
       system_prompt="..."
   )
   ```

3. 在 `__init__.py` 中导出:
   ```python
   from .new_analyzer import new_analyzer
   __all__ = [..., "new_analyzer"]
   ```

4. 在 `main_agent.py` 中注册:
   ```python
   subagents=[
       performance_analyzer,
       log_analyzer,
       query_analyzer,
       config_inspector,
       new_analyzer,  # 添加新的
   ]
   ```

### 自定义 LLM 模型

在 `config.py` 中修改：
```python
export LLM_MODEL=openai:gpt-4-turbo
# 或
export LLM_MODEL=anthropic:claude-opus-4
```

## 关键特点

✅ **真正的多代理**: 使用 deepagents 官方框架
✅ **清晰的分工**: 4 个专业化的子代理
✅ **智能委托**: 主代理自动使用 task() 工具调用子代理
✅ **结构化通信**: 每个子代理有明确的系统提示和期望输出
✅ **可扩展设计**: 易于添加新的子代理
✅ **生产级 API**: 完整的 FastAPI 和 CLI 集成

## 文件清单

```
app/agents/
├── main_agent.py                  # 主代理 (create_deep_agent)
├── subagents/
│   ├── __init__.py               # 导出所有子代理
│   ├── performance_analyzer.py   # SubAgent 定义
│   ├── log_analyzer.py           # SubAgent 定义
│   ├── query_analyzer.py         # SubAgent 定义
│   └── config_inspector.py       # SubAgent 定义
└── example_usage.py              # 使用示例

main.py                            # CLI 入口
app/router/diagnostic.py          # API 路由
app/api.py                        # FastAPI 应用
```

## 验证结果

```
✓ app.core.config
✓ app.core.database
✓ app.agents.subagents (deepagents SubAgent specs)
✓ app.agents.main_agent

✓ All sub-agent specs loaded!
✓ Deepagents main agent created!
```

---

**实现确认**: ✅ 使用 LangChain deepagents 框架的真正多代理系统
