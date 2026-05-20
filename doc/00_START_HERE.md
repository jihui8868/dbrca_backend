# 📖 从这里开始 - Start Here

欢迎使用多数据库 RCA 系统！

## 🚀 5 分钟快速开始

### 步骤 1: 选择你的 LLM 提供者

选择其中一个（建议先用 Ollama 本地测试，无需 API 密钥）：

```bash
# 选项 A: OpenAI (推荐用于生产)
export LLM_PROVIDER=openai
export LLM_MODEL=openai:gpt-4
export OPENAI_API_KEY=sk-xxx...

# 选项 B: Deepseek (推荐用于成本控制)
export LLM_PROVIDER=deepseek
export LLM_MODEL=deepseek:deepseek-chat
export DEEPSEEK_API_KEY=sk-xxx...

# 选项 C: Ollama (推荐用于本地开发，无需密钥)
# 先启动: ollama serve
export LLM_PROVIDER=ollama
export LLM_MODEL=ollama:llama2

# 选项 D: Anthropic Claude
export LLM_PROVIDER=anthropic
export LLM_MODEL=anthropic:claude-opus-4
export ANTHROPIC_API_KEY=sk-ant-xxx...
```

### 步骤 2: 配置数据库

```bash
# 选择一个数据库
export DATABASE_TYPE=mysql              # 或 postgresql, informix 等

# MySQL 配置
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=testdb
```

### 步骤 3: 运行应用

```bash
# 直接运行 (同步模式，易于调试)
python main.py

# 或启动 API 服务器
uvicorn app.api:app --reload
```

## 📚 选择你的学习路径

### 路径 1: 开发者 (推荐)
你想了解代码如何工作，并在开发中进行调试。

1. 📖 阅读: [同步模式改造完成报告.md](./同步模式改造完成报告.md) (10 分钟)
2. 🔧 学习: [DEBUG_GUIDE.md](./DEBUG_GUIDE.md) (30 分钟)
3. 💻 动手: 在 VS Code 中按 F5 启动调试
4. 🚀 进阶: [ARCHITECTURE.md](./ARCHITECTURE.md) (了解设计)

### 路径 2: 运维人员
你需要快速部署和配置系统。

1. 📖 阅读: [QUICKSTART.md](./QUICKSTART.md) (10 分钟)
2. 🔧 配置: [SYSTEM_SETUP.md](./SYSTEM_SETUP.md) (15 分钟)
3. 📊 选择数据库: [MULTI_DATABASE_SUPPORT.md](./MULTI_DATABASE_SUPPORT.md) (10 分钟)
4. 🚀 部署: 按照说明启动服务

### 路径 3: 数据库管理员
你需要诊断数据库问题。

1. 📖 阅读: [QUICK_START_LLM.md](./QUICK_START_LLM.md) (10 分钟)
2. 🔍 运行: `python main.py` 进行诊断
3. 📊 查看: 生成的诊断报告
4. 📚 深入: [USAGE_EXAMPLES.md](./USAGE_EXAMPLES.md) (学习更多用法)

### 路径 4: 架构师/PM
你需要理解系统设计和能力。

1. 📖 阅读: [ARCHITECTURE.md](./ARCHITECTURE.md) (20 分钟)
2. 📊 了解: [ARCHITECTURE_REVIEW.md](./ARCHITECTURE_REVIEW.md) (15 分钟)
3. 🔄 多功能: 
   - 数据库: [MULTI_DATABASE_SUPPORT.md](./MULTI_DATABASE_SUPPORT.md)
   - LLM: [LLM_INTEGRATION_SUMMARY.md](./LLM_INTEGRATION_SUMMARY.md)
   - 框架: [DEEPAGENTS_IMPLEMENTATION.md](./DEEPAGENTS_IMPLEMENTATION.md)

## 🔍 按功能查找文档

### 我想要...

| 需求 | 文档 | 时间 |
|------|------|------|
| 快速开始 | [同步模式改造完成报告.md](./同步模式改造完成报告.md) | 10 min |
| 学习调试 | [DEBUG_GUIDE.md](./DEBUG_GUIDE.md) | 30 min |
| 切换 LLM | [QUICK_START_LLM.md](./QUICK_START_LLM.md) | 10 min |
| 支持新数据库 | [MULTI_DATABASE_SUPPORT.md](./MULTI_DATABASE_SUPPORT.md) | 20 min |
| 理解架构 | [ARCHITECTURE.md](./ARCHITECTURE.md) | 20 min |
| 查看代码例子 | [USAGE_EXAMPLES.md](./USAGE_EXAMPLES.md) | 30 min |
| 部署到生产 | [SYSTEM_SETUP.md](./SYSTEM_SETUP.md) | 30 min |

## 💡 IDE 调试 (1 分钟设置)

### VS Code
1. F5 启动调试
2. 在代码行号左边点击添加断点
3. F10 = 单步跳过，F11 = 单步进入

→ 详细: [DEBUG_GUIDE.md](./DEBUG_GUIDE.md#vs-code-调试-推荐)

### PyCharm
1. Menu → Run → Edit Configurations
2. 添加 Python 配置
3. Shift+F9 启动调试

→ 详细: [DEBUG_GUIDE.md](./DEBUG_GUIDE.md#pycharm-调试)

## 🎯 常见任务

### 任务 1: 诊断数据库问题

```bash
# 方式 1: 命令行
python main.py

# 方式 2: API
curl -X POST http://localhost:8000/api/v1/diagnostic/analyze \
  -H "Content-Type: application/json" \
  -d '{"issue_description": "Database is slow"}'
```

### 任务 2: 切换 LLM 提供者

不需要改代码！只需改环境变量：

```bash
# 从 OpenAI 切换到 Deepseek
export LLM_PROVIDER=deepseek
export DEEPSEEK_API_KEY=sk-xxx...
python main.py
```

### 任务 3: 支持新数据库

只需一个环境变量：

```bash
# 从 MySQL 切换到 PostgreSQL
export DATABASE_TYPE=postgresql
export DB_HOST=pg.example.com
export DB_PORT=5432
python main.py
```

### 任务 4: 调试代码

```python
# 在 main.py 中添加
import pdb; pdb.set_trace()  # 暂停在这里

# 然后运行
python main.py

# 在 pdb 中:
n    - 下一行
s    - 步入
c    - 继续
p x  - 打印变量 x
```

## 📊 项目特点

```
多数据库支持
├── MySQL ✓
├── PostgreSQL ✓
├── Informix ✓
└── Oracle, SQL Server (支持中)

多 LLM 提供者
├── OpenAI ✓
├── Deepseek ✓
├── Anthropic Claude ✓
└── Ollama (本地) ✓

同步模式
├── 易于调试 ✓
├── 清晰错误栈 ✓
├── 性能无变化 ✓
└── FastAPI 支持 ✓

deepagents 框架
├── 多代理协调 ✓
├── 性能分析 ✓
├── 日志分析 ✓
└── 查询优化 ✓
```

## 🆘 需要帮助？

### 问题 1: 不知道从哪开始
→ 看看上面的"选择你的学习路径"，选择最适合你的

### 问题 2: 想要快速上手
→ 阅读 [同步模式改造完成报告.md](./同步模式改造完成报告.md)，5 分钟了解全貌

### 问题 3: 想要学习调试
→ 阅读 [DEBUG_GUIDE.md](./DEBUG_GUIDE.md)，包含所有 IDE 的设置

### 问题 4: 想要配置不同的数据库
→ 查看 [MULTI_DATABASE_SUPPORT.md](./MULTI_DATABASE_SUPPORT.md)

### 问题 5: 想要了解架构设计
→ 阅读 [ARCHITECTURE.md](./ARCHITECTURE.md)

## 📖 完整文档列表

所有文档都在这个目录中。快速导航：

- **快速开始类** (3 个)
  - [同步模式改造完成报告.md](./同步模式改造完成报告.md) - 中文快速开始
  - [QUICK_START_LLM.md](./QUICK_START_LLM.md) - LLM 配置
  - [QUICKSTART.md](./QUICKSTART.md) - 项目快速开始

- **调试相关** (3 个)
  - [DEBUG_GUIDE.md](./DEBUG_GUIDE.md) - 完整调试指南
  - [SYNC_MODE_MIGRATION.md](./SYNC_MODE_MIGRATION.md) - 同步模式说明
  - [SYNC_MODE_VERIFICATION.md](./SYNC_MODE_VERIFICATION.md) - 验证报告

- **核心功能** (8 个)
  - 数据库: [MULTI_DATABASE_SUPPORT.md](./MULTI_DATABASE_SUPPORT.md)
  - LLM: [LLM_INTEGRATION_SUMMARY.md](./LLM_INTEGRATION_SUMMARY.md)
  - 框架: [DEEPAGENTS_IMPLEMENTATION.md](./DEEPAGENTS_IMPLEMENTATION.md)
  - 示例: [USAGE_EXAMPLES.md](./USAGE_EXAMPLES.md)
  - 架构: [ARCHITECTURE.md](./ARCHITECTURE.md)
  - 设置: [SYSTEM_SETUP.md](./SYSTEM_SETUP.md)
  - 其他: [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) 等

→ **完整索引**: [INDEX.md](./INDEX.md) (21 个文档)

## ✨ 下一步

1. **立即开始**: 按照上面的"5 分钟快速开始"
2. **选择路径**: 选择最适合你的学习路径
3. **深入学习**: 根据需要阅读相关文档
4. **动手实践**: 在代码中试验和调试

## 🎉 祝你使用愉快！

如有问题，查看对应的文档，或直接阅读源代码。

**现在开始吧！** 🚀

---

**提示**: 按 `Ctrl+F` (或 `Cmd+F`) 在此文件中搜索关键词，快速找到你需要的信息。
