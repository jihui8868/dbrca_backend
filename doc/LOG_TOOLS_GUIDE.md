# 日志分析工具指南

## 概述

日志分析子代理配备了 7 种强大的分析工具，可以从多个角度全面评估数据库的日志和事件。

## 可用工具

### 1. 错误模式分析 (analyze_error_patterns)

**用途**: 识别并分析数据库错误日志中的模式

**功能**:
- 统计错误总数
- 识别最常见的错误类型
- 按频率排序错误
- 提供错误优化建议

**典型输出**:
```
Status: WARNING
Found 23 errors in recent logs
Top Error Patterns:
  • "Access denied": 8 occurrences
  • "Connection reset": 6 occurrences
  • "Timeout expired": 5 occurrences
  • "Out of memory": 4 occurrences

Recommendations:
  • Review authentication and permission settings
  • Check for connection pool exhaustion
  • Monitor memory usage and query optimization
  • Implement circuit breaker for timeout handling
```

**何时使用**:
- 看到数据库错误日志增多
- 应用报告间歇性失败
- 需要根因分析错误原因

### 2. 连接问题分析 (analyze_connection_issues)

**用途**: 识别连接相关的错误和中止连接

**功能**:
- 统计连接中止次数
- 分类连接错误类型
- 识别连接模式问题
- 建议连接优化措施

**典型输出**:
```
Status: CRITICAL
Found 34 connection-related issues
Aborted Connections: 34
Connection Errors:
  • "Too many connections": 15 occurrences
  • "Connection timeout": 12 occurrences
  • "Connection refused": 7 occurrences

Recommendations:
  • Increase max_connections setting
  • Implement application-level connection pooling
  • Review idle connection timeout policies
  • Monitor for connection leaks in application code
```

**何时使用**:
- 应用报告"Too many connections"错误
- 连接突然断开或拒绝
- 看到大量中止连接日志

### 3. 警告事件分析 (analyze_warnings)

**用途**: 提取和分析系统警告事件

**功能**:
- 统计警告事件数量
- 分类警告类型
- 评估警告严重性
- 提供警告处理建议

**典型输出**:
```
Status: WARNING
Found 12 warning events
Warning Distribution:
  • "Slow query": 5 events
  • "Index size": 3 events
  • "Table size": 2 events
  • "Deprecated feature": 2 events

Recommendations:
  • Review slow query optimization opportunities
  • Monitor and optimize large indexes
  • Consider table partitioning for large tables
  • Plan migration away from deprecated features
```

**何时使用**:
- 定期审查数据库健康警告
- 看到大量警告日志
- 需要预防性地解决潜在问题

### 4. 复制状态分析 (analyze_replication)

**用途**: 检查复制状态并识别复制相关问题

**功能**:
- 检测复制错误
- 监控复制延迟问题
- 识别主从不同步
- 建议复制优化

**典型输出**:
```
Status: CRITICAL
Replication Issues: 3
Issues:
  • Replication error in binary log position
  • Slave SQL thread stopped
  • Replication lag detected (5.2 seconds)

Recommendations:
  • Check SHOW SLAVE STATUS for detailed info
  • Review slave error log for root cause
  • Consider manual replication resync if necessary
  • Monitor network latency between primary and replica
```

**何时使用**:
- 看到 slave 线程停止的日志
- 复制延迟超过预期
- 需要验证主从数据一致性

### 5. 日志卷分析 (analyze_log_volume)

**用途**: 分析日志卷和增长模式

**功能**:
- 统计日志条目总数
- 分析日志级别分布
- 评估日志增长率
- 建议日志管理策略

**典型输出**:
```
Status: WARNING
Total Log Entries: 256
Entries by Level:
  • ERROR: 45 entries
  • WARNING: 78 entries
  • INFO: 89 entries
  • DEBUG: 44 entries

Recommendations:
  • Configure log rotation if not already enabled
  • Reduce verbosity of DEBUG logging in production
  • Archive logs older than 30 days
  • Monitor disk space usage for log files
```

**何时使用**:
- 日志文件增长过快
- 磁盘空间因日志占用而不足
- 需要优化日志存储策略

### 6. 事件时间线分析 (analyze_event_timeline)

**用途**: 分析日志中的时间模式和事件分布

**功能**:
- 统计事件总数
- 分类事件类型
- 识别时间聚集模式
- 建议事件关联分析

**典型输出**:
```
Status: OK
Timeline Analysis: 45 events detected
Event Distribution:
  • Error: 15 events
  • Warning: 20 events
  • Event: 10 events
Latest Events:
  • [2024-05-21 14:30:45] Connection timeout on user_db
  • [2024-05-21 14:25:12] Slow query detected (8.2s)
  • [2024-05-21 14:20:33] Index rebuild completed

Recommendations:
  • Track event frequency trends
  • Identify recurring issues at specific times
  • Correlate with application deployment or scheduled jobs
```

**何时使用**:
- 需要了解事件发生的时间模式
- 识别是否存在定期性问题
- 进行事件关联和根因分析

### 7. 综合日志报告 (comprehensive_log_report)

**用途**: 生成完整的日志分析报告

**功能**:
- 整合所有日志指标
- 确定整体健康状态
- 列出优先级排序的建议
- 提供执行摘要

**典型输出**:
```
COMPREHENSIVE LOG ANALYSIS REPORT
==================================
Timestamp: 2024-05-21T14:30:45
Database: MySQL 8.0
Overall Status: WARNING

Critical Issues: connection_issues

Top Recommendations:
• Increase max_connections setting from 100 to 250
• Implement application-level connection pooling
• Review authentication and permission settings
• Monitor memory usage and configure log rotation

Detailed Findings:
- Error Patterns: WARNING (23 errors detected)
- Connection Issues: CRITICAL (34 aborted connections)
- Warning Events: WARNING (12 warning events)
- Replication Status: OK (no issues detected)
- Log Volume: WARNING (256 total entries)
- Event Timeline: OK (normal event distribution)
```

**何时使用**:
- 定期性能检查（每日/周/月）
- 数据库故障的根本原因分析
- 容量规划和升级决策
- 生成日志分析基准报告

## 工具架构

### 核心类: LogAnalyzer

```python
class LogAnalyzer:
    """日志分析工具"""

    @staticmethod
    def analyze_error_patterns(hours: int = 24) -> Dict[str, Any]:
        """分析错误模式"""

    @staticmethod
    def analyze_connection_issues() -> Dict[str, Any]:
        """分析连接问题"""

    @staticmethod
    def analyze_warning_events() -> Dict[str, Any]:
        """分析警告事件"""

    @staticmethod
    def analyze_replication_status() -> Dict[str, Any]:
        """分析复制状态"""

    @staticmethod
    def analyze_log_volume() -> Dict[str, Any]:
        """分析日志卷"""

    @staticmethod
    def analyze_event_timeline() -> Dict[str, Any]:
        """分析事件时间线"""

    @staticmethod
    def generate_log_report() -> Dict[str, Any]:
        """生成日志报告"""
```

### 工具集成

工具通过以下方式集成到日志分析子代理：

```python
log_tools = {
    "error_patterns": {
        "name": "analyze_error_patterns",
        "description": "分析错误模式...",
        "function": get_error_patterns_report,
    },
    # ... 其他工具
}
```

## 使用示例

### 示例 1: 快速日志检查

```python
from app.tools.log_tools import LogAnalyzer

# 快速生成综合报告
report = LogAnalyzer.generate_log_report()
print(report["overall_status"])  # 获取整体状态
print(report["critical_issues"])  # 获取关键问题
```

### 示例 2: 针对性分析

```python
from app.tools.log_tools import LogAnalyzer

# 如果看到连接错误，分析连接问题
connection_analysis = LogAnalyzer.analyze_connection_issues()

if connection_analysis["status"] == "CRITICAL":
    print("连接是性能问题的主要原因")
    print(f"发现 {connection_analysis['aborted_connections']} 个中止连接")
    for rec in connection_analysis["recommendations"]:
        print(f"  - {rec}")
```

### 示例 3: 子代理中使用

```python
from app.agents.subagents.log_analyzer import execute_all_log_analyses

# 日志分析子代理执行所有分析
results = execute_all_log_analyses()

for analysis_type, result in results.items():
    print(f"{analysis_type}: {result}")
```

## 错误阈值和警告

### 错误模式

| 错误数 | 状态 | 含义 |
|--------|------|------|
| 0-5 | ✓ 正常 | 无问题 |
| 5-10 | ⚠ 监控 | 有错误出现 |
| 10-50 | ⚠ 警告 | 错误增多 |
| >50 | 🔴 严重 | 严重问题 |

### 连接问题

| 中止连接数 | 状态 | 含义 |
|-----------|------|------|
| 0-5 | ✓ 正常 | 正常范围 |
| 5-20 | ⚠ 监控 | 需要关注 |
| 20-50 | ⚠ 警告 | 有问题 |
| >50 | 🔴 严重 | 紧急处理 |

### 日志卷

| 日志条数 | 状态 | 操作 |
|---------|------|------|
| 0-50 | ✓ 正常 | 继续监控 |
| 50-100 | ⚠ 监控 | 关注增长 |
| 100-500 | ⚠ 警告 | 配置日志轮转 |
| >500 | 🔴 严重 | 立即处理 |

## 最佳实践

### 1. 定期监控

```python
# 每日运行综合报告
from app.tools.log_tools import get_comprehensive_log_report
report = get_comprehensive_log_report()
```

### 2. 针对性调查

- 如果看到错误增多 → 运行 analyze_error_patterns
- 如果看到连接失败 → 运行 analyze_connection_issues
- 如果看到警告增多 → 运行 analyze_warning_events

### 3. 优先级排序

根据以下顺序解决问题：
1. **CRITICAL** 状态问题（可能导致停机）
2. **WARNING** 状态问题（影响可靠性）
3. **INFO** 状态问题（优化机会）

### 4. 趋势分析

```python
# 跟踪问题改进
before = LogAnalyzer.analyze_error_patterns()
# 应用修复...
after = LogAnalyzer.analyze_error_patterns()
# 对比 before['error_count'] 和 after['error_count']
```

## 与主代理的集成

日志分析子代理在 RCA 流程中的角色：

```
主代理 (RootCauseAnalyzer)
  ↓
调用日志分析子代理
  ↓
日志分析子代理使用工具
  ├─ analyze_error_patterns → 发现错误模式
  ├─ analyze_connection_issues → 发现连接问题
  ├─ analyze_warnings → 发现警告事件
  ├─ analyze_replication → 发现复制问题
  └─ ... 其他工具
  ↓
收集所有日志指标
  ↓
LLM 分析综合结果
  ↓
生成根因分析报告
```

## 扩展工具

### 添加新工具步骤

1. 在 `LogAnalyzer` 中添加新的 `analyze_*` 方法
2. 创建对应的 `get_*_report()` 便利函数
3. 在 `log_tools` 字典中注册
4. 更新子代理的 system_prompt

### 示例：添加审计日志分析

```python
@staticmethod
def analyze_audit_log() -> Dict[str, Any]:
    """分析审计日志和权限变更"""
    # 实现分析逻辑
    return {
        "status": "OK",
        "audit_events": 0,
        "recommendations": [...]
    }

# 在 log_tools 中注册
log_tools["audit"] = {
    "name": "analyze_audit",
    "description": "检查审计日志和权限变更",
    "function": get_audit_report,
}
```

## 故障排除

### 工具返回错误

**问题**: `"message": "Failed to analyze..."`

**原因**:
- 数据库连接断开
- 权限不足无法读取错误日志
- 错误日志表/视图不存在

**解决**:
1. 检查数据库连接
2. 验证用户权限
3. 确保错误日志已启用

### 日志数据不可用

**问题**: `"status": "UNKNOWN"`

**原因**:
- 日志功能未启用
- 日志已被清空
- 数据库类型不支持该日志

**解决**:
1. 检查日志启用状态
2. 验证日志表存在且有数据
3. 检查数据库版本兼容性

## 性能提示

- 工具执行时间通常 < 1 秒
- 综合报告生成时间 < 5 秒
- 日志查询不会锁定表或影响性能

## 总结

这 7 个工具为日志分析子代理提供了全面的诊断能力，可以快速识别和解决日志和事件相关问题。合理使用这些工具，可以显著提升数据库故障排查的效率和准确性。
