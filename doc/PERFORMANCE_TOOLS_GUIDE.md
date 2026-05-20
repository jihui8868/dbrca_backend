# 性能分析工具指南

## 概述

性能分析子代理配备了 8 种强大的分析工具，可以从多个角度全面评估数据库性能。

## 可用工具

### 1. 慢查询分析 (analyze_slow_queries)

**用途**: 识别并分析执行缓慢的SQL查询

**功能**:
- 列出最慢的 N 个查询
- 识别查询模式
- 计算执行统计

**典型输出**:
```
Status: WARNING
Found 15 slow queries in recent history
Top 3 issues:
  • SELECT * FROM large_table JOIN another_table - 12.5s avg
  • Full table scan on users table - 8.3s avg
  • Missing index on order_date column - 7.1s avg

Recommendations:
  • Add composite index on (user_id, created_date)
  • Optimize JOIN condition in query
  • Add LIMIT clause to prevent full scans
```

**何时使用**:
- 应用响应变慢
- 看到数据库CPU使用率高
- 用户报告特定操作缓慢

### 2. 缓存效率分析 (analyze_cache)

**用途**: 评估缓冲池和缓存的有效性

**功能**:
- 计算缓存命中率
- 分析缓冲池使用情况
- 识别缓存配置问题

**典型输出**:
```
Status: WARNING
Cache hit ratio: 75%
Buffer pool usage: 85%

Recommendations:
  • Cache hit ratio below 90%, increase innodb_buffer_pool_size
  • Consider upgrading to SSD for better I/O
  • Monitor memory pressure
```

**何时使用**:
- 数据库内存持续占用高
- 磁盘I/O突然增加
- 查询响应时间波动

### 3. 连接池分析 (analyze_connections)

**用途**: 监控数据库连接使用情况

**功能**:
- 统计活跃连接数
- 计算连接池利用率
- 识别连接泄漏

**典型输出**:
```
Status: OK
Active connections: 45/100 (45%)
Connection types:
  • Active queries: 23
  • Idle connections: 22
  • Sleeping: 8

Recommendations:
  • Close idle connections periodically
  • Use connection pooling in application
  • Review max_connections setting
```

**何时使用**:
- 应用报告"too many connections"错误
- 连接数持续增长
- 连接响应变慢

### 4. 表统计分析 (analyze_tables)

**用途**: 了解数据库中的表结构和大小

**功能**:
- 列出所有表及其大小
- 识别特别大的表
- 提供表增长信息

**典型输出**:
```
Status: OK
Total tables: 42
Database size: 125.5 GB

Largest tables:
  1. events - 45.2 GB (2.1B rows)
  2. logs - 35.8 GB (1.8B rows)
  3. transactions - 28.3 GB (950M rows)

Recommendations:
  • Implement partitioning for large tables
  • Archive old data to reduce size
  • Consider table compression
```

**何时使用**:
- 磁盘空间不足
- 需要规划容量
- 优化表结构

### 5. 锁分析 (analyze_locks)

**用途**: 检测并分析数据库锁和死锁

**功能**:
- 识别当前锁
- 检测死锁
- 分析长时间锁持有

**典型输出**:
```
Status: WARNING
Active locks: 12
Waiting locks: 3

Details:
  • Transaction ID 123 holding lock on table_a for 45 seconds
  • Transaction ID 456 waiting for lock on table_a
  • Potential deadlock detected

Recommendations:
  • Review long-running transaction logic
  • Optimize transaction boundaries
  • Consider row-level locking
```

**何时使用**:
- 应用报告超时错误
- 看到"Deadlock found"日志
- 某些操作间歇性失败

### 6. 磁盘I/O分析 (analyze_disk_io)

**用途**: 评估磁盘I/O性能和模式

**功能**:
- 分析数据库大小
- 评估I/O模式
- 识别I/O热点

**典型输出**:
```
Status: OK
Database size: 125.5 GB
I/O operations: 15,000 reads/sec, 3,200 writes/sec

Recommendations:
  • Monitor disk throughput utilization
  • Consider SSD for better random access
  • Implement read replicas for load distribution
  • Archive historical data to reduce volume
```

**何时使用**:
- 磁盘利用率高
- I/O等待时间长
- 性能在高峰期下降

### 7. 索引分析 (analyze_indexes)

**用途**: 评估索引的有效性和使用情况

**功能**:
- 列出所有索引及使用统计
- 识别未使用的索引
- 发现缺失的索引

**典型输出**:
```
Status: WARNING
Total indexes: 156
Unused indexes: 23

Unused indexes:
  • idx_users_email_old (0 uses)
  • idx_orders_status_temp (0 uses)
  • idx_products_category_v1 (0 uses)

Recommendations:
  • Drop 23 unused indexes to save space/improve writes
  • Add index on frequently filtered columns
  • Review index fragmentation
```

**何时使用**:
- 写入操作变慢
- 需要优化查询性能
- 磁盘空间优化

### 8. 综合性能报告 (comprehensive_report)

**用途**: 生成完整的性能分析报告

**功能**:
- 整合所有性能指标
- 确定整体健康状态
- 列出优先级排序的建议

**典型输出**:
```
COMPREHENSIVE PERFORMANCE ANALYSIS REPORT
==========================================
Database: MySQL 8.0
Overall Status: WARNING
Analysis Time: 2024-05-20T14:30:45

Critical Issues: 2
  • Cache efficiency below threshold
  • 23 unused indexes consuming space

Top 5 Recommendations:
1. Increase buffer pool size from 4GB to 8GB (impact: high)
2. Add composite index on users(id, created_date) (impact: high)
3. Implement connection pooling (impact: medium)
4. Archive logs older than 90 days (impact: medium)
5. Review long-running transaction at line 234 (impact: medium)

Summary by Category:
- Slow Queries: WARNING (15 queries > 1s)
- Cache: WARNING (75% hit ratio)
- Connections: OK (45% utilization)
- Tables: OK (42 tables, 125GB)
- Locks: OK (no deadlocks)
- Disk I/O: OK (normal patterns)
- Indexes: WARNING (23 unused)
```

**何时使用**:
- 定期性能检查（每日/周/月）
- 性能问题根本原因分析
- 容量规划和升级决策
- 性能基准设定

## 工具架构

### 核心类: PerformanceMetrics

```python
class PerformanceMetrics:
    """性能指标分析器"""

    @staticmethod
    def analyze_slow_queries(limit: int = 10) -> Dict[str, Any]:
        """分析慢查询"""

    @staticmethod
    def analyze_cache_efficiency() -> Dict[str, Any]:
        """分析缓存效率"""

    @staticmethod
    def analyze_connections() -> Dict[str, Any]:
        """分析连接"""

    @staticmethod
    def analyze_table_statistics() -> Dict[str, Any]:
        """分析表统计"""

    @staticmethod
    def analyze_locks() -> Dict[str, Any]:
        """分析锁"""

    @staticmethod
    def analyze_disk_io() -> Dict[str, Any]:
        """分析磁盘I/O"""

    @staticmethod
    def analyze_indexes() -> Dict[str, Any]:
        """分析索引"""

    @staticmethod
    def generate_performance_report() -> Dict[str, Any]:
        """生成性能报告"""
```

### 工具集成

工具通过以下方式集成到性能分析子代理：

```python
performance_tools = {
    "slow_queries": {
        "name": "analyze_slow_queries",
        "description": "分析缓慢查询...",
        "function": get_slow_queries_report,
    },
    # ... 其他工具
}
```

## 使用示例

### 示例 1: 快速性能检查

```python
from app.tools.performance_tools import PerformanceMetrics

# 快速生成综合报告
report = PerformanceMetrics.generate_performance_report()
print(report["overall_status"])  # 获取整体状态
print(report["critical_issues"])  # 获取关键问题
```

### 示例 2: 针对性分析

```python
from app.tools.performance_tools import PerformanceMetrics

# 如果应用报告响应慢，分析慢查询
slow_query_analysis = PerformanceMetrics.analyze_slow_queries(limit=20)

if slow_query_analysis["status"] == "CRITICAL":
    print("慢查询是性能问题的主要原因")
    print(f"发现 {slow_query_analysis['count']} 个慢查询")
    for rec in slow_query_analysis["recommendations"]:
        print(f"  - {rec}")
```

### 示例 3: 子代理中使用

```python
from app.agents.subagents.performance_analyzer import execute_all_analyses

# 性能分析子代理执行所有分析
results = execute_all_analyses()

for analysis_type, result in results.items():
    print(f"{analysis_type}: {result}")
```

## 性能阈值和警告

### 缓存效率

| 指标 | 最优 | 良好 | 警告 | 严重 |
|------|------|------|------|------|
| 命中率 | >95% | 90-95% | 80-90% | <80% |
| 缓冲池使用 | 60-80% | 80-90% | 90-95% | >95% |

### 连接

| 指标 | 状态 | 说明 |
|------|------|------|
| 利用率 | 0-50% | 正常 |
| 利用率 | 50-75% | 监控 |
| 利用率 | 75-90% | 警告 |
| 利用率 | >90% | 严重 |

### 查询性能

| 指标 | 状态 | 说明 |
|------|------|------|
| 慢查询数 | 0-5 | 正常 |
| 慢查询数 | 5-20 | 监控 |
| 慢查询数 | 20-50 | 警告 |
| 慢查询数 | >50 | 严重 |

## 最佳实践

### 1. 定期监控

```python
# 每日运行综合报告
from app.tools.performance_tools import get_comprehensive_performance_report
report = get_comprehensive_performance_report()
```

### 2. 针对性调查

- 如果看到高CPU → 运行 analyze_slow_queries
- 如果看到高内存 → 运行 analyze_cache
- 如果连接数高 → 运行 analyze_connections

### 3. 优先级排序

根据以下顺序解决问题：
1. **CRITICAL** 状态问题（可能导致停机）
2. **WARNING** 状态问题（影响性能）
3. **INFO** 状态问题（优化机会）

### 4. 跟踪改进

```python
# 修改后再次运行相同分析，对比结果
before = PerformanceMetrics.analyze_slow_queries()
# 应用修复...
after = PerformanceMetrics.analyze_slow_queries()
# 对比 before['count'] 和 after['count']
```

## 与主代理的集成

性能分析子代理在 RCA 流程中的角色：

```
主代理 (RootCauseAnalyzer)
  ↓
调用性能分析子代理
  ↓
性能分析子代理使用工具
  ├─ analyze_slow_queries → 发现慢查询
  ├─ analyze_cache → 发现缓存问题
  ├─ analyze_connections → 发现连接问题
  └─ ... 其他工具
  ↓
收集所有指标
  ↓
LLM 分析综合结果
  ↓
生成根因分析报告
```

## 扩展工具

### 添加新工具步骤

1. 在 `PerformanceMetrics` 中添加新的 `analyze_*` 方法
2. 创建对应的 `get_*_report()` 便利函数
3. 在 `performance_tools` 字典中注册
4. 更新子代理的 system_prompt

### 示例：添加复制延迟分析

```python
@staticmethod
def analyze_replication_lag() -> Dict[str, Any]:
    """分析主从复制延迟"""
    # 实现分析逻辑
    return {
        "status": "OK",
        "lag_seconds": 0.5,
        "recommendations": [...]
    }

# 在 performance_tools 中注册
performance_tools["replication"] = {
    "name": "analyze_replication",
    "description": "检查主从复制延迟",
    "function": get_replication_report,
}
```

## 故障排除

### 工具返回错误

**问题**: `"message": "Failed to analyze..."`

**原因**:
- 数据库连接断开
- 权限不足
- 相关表/视图不存在

**解决**:
1. 检查数据库连接
2. 验证用户权限（需要 PROCESS, SUPER 权限）
3. 确保 performance_schema 已启用

### 性能数据不可用

**问题**: `"status": "UNKNOWN"`

**原因**:
- 数据库类型不支持该指标
- 功能尚未启用

**解决**:
1. 检查数据库版本
2. 启用必要的功能（如 performance_schema）
3. 检查兼容性

## 性能提示

- 工具执行时间通常 < 1 秒
- 综合报告生成时间 < 5 秒
- 分析不会锁定表或导致性能下降

## 总结

这 8 个工具为性能分析子代理提供了全面的诊断能力，可以快速识别和解决性能问题。合理使用这些工具，可以显著提升数据库诊断的效率和准确性。
