# 调试指南 - 同步模式调试

现在所有代码已转换为同步模式，可以轻松使用 IDE 的调试器进行单步跟踪。

## 快速开始

### 方案 1: 直接使用 Python 调试器 (pdb)

**在代码中添加断点:**

```python
def diagnose_database(issue_description: str):
    """运行数据库诊断"""
    import pdb; pdb.set_trace()  # 在这里暂停执行
    
    agent = create_rca_agent()
    result = agent.invoke(...)
    return result
```

**运行代码:**
```bash
python main.py
# 会在断点处暂停，可以交互式调试
```

**常用命令:**
- `l` - 列出当前代码
- `n` - 执行下一行
- `s` - 步入函数
- `c` - 继续执行
- `p 变量名` - 打印变量
- `pp locals()` - 打印所有本地变量

### 方案 2: VS Code 调试 (推荐)

**1. 安装 Python 扩展**
- 搜索 "Python" (Microsoft)
- 点击安装

**2. 创建调试配置**

在项目根目录创建 `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "调试: main.py",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "调试: FastAPI 服务器",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": ["app.api:app", "--reload", "--host", "0.0.0.0"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "jinja": true
        },
        {
            "name": "调试: 集成测试",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/test_integration.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

**3. 添加断点并调试**

- 在代码行号左边点击，添加红点断点
- 按 F5 启动调试
- 使用快捷键:
  - F10: 单步跳过 (Step Over)
  - F11: 单步进入 (Step Into)
  - Shift+F11: 单步跳出 (Step Out)
  - F9: 继续执行到下一断点 (Continue)

**4. 查看变量和监视**

- **变量面板**: 显示当前作用域的所有变量
- **监视面板**: 添加表达式进行监视
  - 例如: `result["status"]`
  - 例如: `db_manager.engine.url`

**5. 调试控制台**

可以在调试暂停时，在控制台输入 Python 代码执行:

```python
# 调试时在控制台输入
>> p issue_description
'Database queries are running slowly'

>> p result
{'status': 'success', 'analysis': '...'}

>> p result.keys()
dict_keys(['status', 'analysis', 'issue_description'])
```

## 实际调试场景

### 场景 1: 调试 main.py

**目标:** 追踪诊断流程

```python
# main.py
def main():
    print("Starting MySQL RCA Diagnostic System\n")
    
    print("Testing database connection...")
    if not db_manager.test_connection():  # 可在此设置断点
        print("❌ Failed to connect")
        return
    
    print("✓ Connection successful\n")
    
    for issue in ["Database queries are running slowly"]:
        print(f"Diagnosing: {issue}")
        
        try:
            result = diagnose_database(issue)  # 可在此 F11 进入
            
            if result["status"] == "success":  # 可检查 result
                print(result.get("analysis", ""))
        except Exception as e:  # 异常自动暂停
            print(f"Error: {e}")
```

**调试步骤:**
1. 在 `db_manager.test_connection()` 行设置断点
2. F5 启动调试
3. F10 跳过数据库连接
4. 在 `diagnose_database(issue)` 行设置断点
5. F11 进入 `diagnose_database()` 函数
6. 逐行跟踪诊断过程

### 场景 2: 调试 API 路由

**目标:** 追踪 API 请求处理

```python
# app/router/diagnostic.py
@router.post("/analyze")
def analyze_issue(request: DiagnosticRequest):  # 设置断点这里
    try:
        # 在这里检查 request 对象
        print(f"[DEBUG] 收到请求: {request.issue_description}")  # 可以 F10
        
        result = diagnose_database(request.issue_description or "")  # 可以 F11 进入
        
        if result["status"] == "error":  # 可以检查 result
            raise HTTPException(status_code=500)
        
        return AnalysisResult(...)  # 可以看返回值
    except Exception as e:
        raise HTTPException(status_code=500)
```

**调试步骤:**
1. 启动 FastAPI 调试: F5 选择 "调试: FastAPI 服务器"
2. 在路由处理函数设置断点
3. 使用 curl 或 Postman 发送请求到 `http://localhost:8000/api/v1/diagnostic/analyze`
4. VS Code 会暂停在断点处
5. 使用 F10/F11 逐步跟踪

### 场景 3: 调试 LLM Factory

**目标:** 验证 LLM 提供者选择

```python
# app/core/llm_factory.py
def create_llm(provider: str = None, model: str = None, api_key: str = None, **kwargs):
    provider = provider or settings.llm.provider  # 设断点查看值
    model = model or settings.llm.model
    api_key = api_key or settings.llm.api_key
    
    if ":" in model:  # 设断点跟踪模型解析
        model_provider, model_name = model.split(":", 1)
        print(f"[DEBUG] 解析模型: {model_provider}:{model_name}")
    
    provider = provider.lower()
    
    if provider == "openai":  # 设断点检查provider
        return _create_openai_llm(model, api_key, **kwargs)
    elif provider == "deepseek":
        return _create_deepseek_llm(model, api_key, **kwargs)
```

**调试步骤:**
1. 在 `create_llm()` 入口设置断点
2. 运行测试: `python test_integration.py`
3. 当到达断点时，查看 `provider` 和 `model` 的值
4. F10 跟踪模型解析逻辑
5. F11 进入提供者特定函数

## 常见调试技巧

### 技巧 1: 条件断点

在断点上右键 → 编辑断点，添加条件:

```python
def analyze_database_issues(issues: list):
    for i, issue in enumerate(issues):  # 在此设置条件断点
        if i > 5:  # 只在 i > 5 时暂停
            process_issue(issue)
```

**VS Code 条件:**
- `i > 5` - 当 i 大于 5 时暂停
- `"error" in issue` - 当 issue 包含 "error" 时暂停

### 技巧 2: 日志点 (Log Point)

在断点上右键 → 添加日志点，不暂停但记录日志:

```python
result = diagnose_database(issue)  # 右键 → 添加日志点
# 输入: "诊断结果: {result['status']}"
# 会在控制台打印，但不暂停执行
```

### 技巧 3: 变量监视

**监视特定表达式:**

```
// 添加到监视列表
result["status"]
result.get("analysis", "").length
db_manager.engine.url
len(issue_descriptions)
```

### 技巧 4: 调试控制台交互

在 VS Code 调试控制台，可以执行 Python 代码:

```python
# 检查变量
> result
{'status': 'success', 'analysis': '...'}

# 调用函数
> db_manager.test_connection()
True

# 导入模块
> from app.core.config import settings
> settings.llm.provider
'openai'
```

## 调试常见问题

### 问题 1: 断点不工作

**原因:** 代码没有通过该代码路径

**解决:**
1. 确认入口点正确
2. 添加日志打印验证代码是否执行
3. 检查条件逻辑

### 问题 2: 无法进入第三方库

**原因:** `justMyCode` 设置为 true

**解决:** 改为 false 可调试第三方库:

```json
{
    "justMyCode": false  // 允许调试第三方库
}
```

### 问题 3: 断点位置显示错误

**原因:** Python 文件未保存或有空格问题

**解决:**
1. 保存所有文件 (Ctrl+S)
2. 重新启动调试器
3. 删除 `__pycache__` 目录

### 问题 4: 调试时代码不更新

**原因:** Python 缓存问题

**解决:**
```bash
# 清除 Python 缓存
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete

# 重新启动调试器
```

## PyCharm IDE 调试

### 1. 配置运行

Menu → Run → Edit Configurations

### 2. 添加新配置

- Name: `Debug Main`
- Script path: `main.py`
- Working directory: 项目根目录

### 3. 启动调试

- Shift+F9: 启动调试 (Debug)
- F8: 单步跳过 (Step Over)
- F7: 单步进入 (Step Into)
- Shift+F8: 单步跳出 (Step Out)

### 4. 查看变量

- 右侧 "Debugger" 面板
- 展开 "Variables" 查看所有变量
- 双击变量可修改值 (临时)

## Vim 中的调试

如果使用 Vim，可以使用 `ipdb`:

```python
# 在代码中添加
import ipdb; ipdb.set_trace()  # 和 pdb 类似但功能更强

# 运行
python main.py
```

在 ipdb 中:
- `l` - 列出代码
- `n` - 下一行
- `s` - 步入
- `c` - 继续
- `pp` - 漂亮打印

## 总结

✅ **调试现在很简单:**
1. 添加断点
2. F5 启动调试
3. F10/F11 单步跟踪
4. 在变量面板查看值
5. 在控制台执行代码验证

✅ **同步模式的优势:**
- 代码执行流清晰可见
- 错误堆栈易于理解
- 条件断点有效工作
- IDE 集成完美

**现在可以高效地调试代码！🎉**
