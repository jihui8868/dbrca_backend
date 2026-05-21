# 查询分析工具指南

## 概述

查询分析子代理配备了 8 种强大的分析工具，可以从多个角度全面评估 SQL 查询性能和优化机会。

## 可用工具

### 1. 查询复杂度分析 (analyze_query_complexity)

**用途**: 识别并分析复杂查询模式

**功能**:
- 计算查询复杂度评分
- 识别高复杂度查询
- 识别优化机会
- 提供简化建议

**典型输出**:
```
Status: WARNING
Found 4 highly complex queries
Top Complex Queries:
  1. Query with 6 JOINs, 3 SUBQUERYs, WINDOW functions (score: 28)
  2. Query with 5 JOINs, UNION, GROUP BY, HAVING (score: 22)
  3. Query with 4 JOINs, 2 SUBQUERYs (score: 18)
  4. Query with 3 CTEs, multiple JOINs (score: 16)

Recommendations:
  • Break down complex queries into simpler components
  • Consider using CTEs (Common Table Expressions)
  • Evaluate if subqueries can be replaced with JOINs
  • Profile execution plans for complex queries
```

**何时使用**:
- 识别需要简化的复杂查询
- 优化查询性能
- 代码可维护性审查

### 2. 执行计划分析 (analyze_execution_plans)

**用途**: 分析查询执行计划并识别低效模式

**功能**:
- 检测不良执行计划指标
- 识别全表扫描
- 发现缺失索引
- 建议执行优化

**典型输出**:
```
Status: CRITICAL
Found 12 execution plan issues
Issues Detected:
  • SELECT * (unnecessary columns) - 3 queries
  • Leading wildcard LIKE (no index usage) - 2 queries
  • Slow execution (>5s) - 7 queries
  • Full table scans - 5 queries

Recommendations:
  • Use specific column lists instead of SELECT *
  • Avoid leading wildcards in LIKE clauses
  • Add indexes for frequently searched columns
  • Use EXPLAIN PLAN to analyze query execution
  • Consider query restructuring or materialized views
```

**何时使用**:
- 优化查询性能
- 检测全表扫描问题
- 改进执行效率

### 3. JOIN 模式分析 (analyze_join_patterns)

**用途**: 分析 JOIN 模式并识别优化机会

**功能**:
- 检测过多 JOIN
- 识别笛卡尔积风险
- 发现缺失 WHERE 条件
- 建议 JOIN 优化

**典型输出**:
```
Status: WARNING
Found 4 JOIN-related issues
JOIN Issues:
  • Many JOINs (5 joins) - query_abc
  • Expensive JOIN (3.2s, 4 joins) - query_xyz
  • Potential Cartesian product - query_def

Recommendations:
  • Limit number of JOINs per query (target: < 5)
  • Ensure all JOINs have proper ON conditions
  • Add indexes on JOIN columns
  • Consider denormalization for frequently joined tables
  • Use EXPLAIN to verify JOIN order optimization
```

**何时使用**:
- 优化多表查询
- 改进 JOIN 效率
- 检测笛卡尔积问题

### 4. 子查询效率分析 (analyze_subquery_efficiency)

**用途**: 分析子查询使用情况和效率

**功能**:
- 识别多层子查询
- 检测低效的 IN 子查询
- 发现关联子查询
- 建议子查询重写

**典型输出**:
```
Status: WARNING
Found 3 subquery-related issues
Subquery Issues:
  • Multiple subqueries (3) - query_abc
  • IN with subquery (potentially slow) - query_xyz
  • Deeply nested subqueries (3 levels) - query_def

Recommendations:
  • Replace IN subqueries with JOINs where possible
  • Use EXISTS instead of IN for large result sets
  • Consider materializing frequently-used subqueries
  • Move subqueries to WITH clauses (CTEs)
  • Evaluate if subqueries can be indexed or cached
```

**何时使用**:
- 优化复杂查询
- 改进子查询性能
- 代码现代化（迁移到 CTE）

### 5. 索引有效性分析 (analyze_index_effectiveness)

**用途**: 评估索引使用情况和有效性

**功能**:
- 识别未使用的索引
- 检测低效的索引
- 评估索引覆盖率
- 建议索引清理

**典型输出**:
```
Status: WARNING
Unused: 5, Ineffective: 8 indexes
Index Summary:
  • 5 completely unused indexes
  • 8 rarely used indexes (<5 uses)
  • Potential space savings: 250MB

Unused Indexes:
  • idx_old_backup (0 uses)
  • idx_temp_data (0 uses)
  • idx_v1_deprecated (0 uses)

Recommendations:
  • Drop 5 unused indexes to improve write performance
  • Schedule index cleanup after application changes
  • Monitor index usage patterns regularly
  • Review rarely used indexes for relevance
```

**何时使用**:
- 优化磁盘空间
- 改进写入性能
- 定期维护索引

### 6. 查询统计分析 (analyze_query_statistics)

**用途**: 分析查询执行统计和性能模式

**功能**:
- 计算查询性能指标
- 分布执行时间分类
- 识别极慢查询
- 提供性能基准

**典型输出**:
```
Status: WARNING
Query statistics: 30 queries analyzed
Performance Metrics:
  • Average time: 2.5s
  • Max time: 28.3s
  • Min time: 0.08s
  • Very slow (>10s): 7 queries
  • Slow (1-10s): 12 queries
  • Moderate (100ms-1s): 11 queries

Recommendations:
  • Average query time is 2.50s - investigate slow queries
  • Found 7 extremely slow queries (>10s)
  • Prioritize optimization of these queries
  • Check for missing indexes or query plan issues
```

**何时使用**:
- 性能基准测试
- 识别最慢查询
- 趋势分析

### 7. 缺失索引检测 (identify_missing_indexes)

**用途**: 基于查询模式识别缺失的索引

**功能**:
- 分析 WHERE 子句模式
- 识别频繁过滤的列
- 建议复合索引
- 评估索引优先级

**典型输出**:
```
Status: WARNING
Identified 4 index opportunities
Index Suggestions:
  • Add index on ID columns (high frequency)
  • Add index on date/time columns (high frequency)
  • Add index on status columns (medium frequency)
  • Consider composite index on (user_id, created_date)

Recommendations:
  • Evaluate suggested indexes based on query frequency
  • Test index creation impact on write performance
  • Monitor query performance improvement after indexing
  • Consider composite indexes for multiple column matches
```

**何时使用**:
- 优化查询性能
- 规划索引策略
- 容量规划

### 8. 综合查询报告 (comprehensive_query_report)

**用途**: 生成完整的查询分析报告

**功能**:
- 整合所有查询指标
- 确定整体优化优先级
- 列出优先级排序的建议
- 提供执行摘要

**典型输出**:
```
COMPREHENSIVE QUERY ANALYSIS REPORT
====================================
Timestamp: 2024-05-21T14:30:45
Database: MySQL 8.0
Overall Status: CRITICAL

Critical Issues: execution_plans, missing_indexes

Top Recommendations:
• Prioritize optimization of 7 extremely slow queries (>10s)
• Drop 5 unused indexes to improve write performance
• Use specific column lists instead of SELECT *
• Add indexes on frequently filtered columns
• Replace IN subqueries with JOINs where possible
• Break down 4 highly complex queries
• Monitor index usage patterns

Detailed Findings:
- Query Complexity: WARNING (4 complex queries)
- Execution Plans: CRITICAL (12 issues)
- JOIN Patterns: WARNING (4 issues)
- Subquery Efficiency: WARNING (3 issues)
- Index Effectiveness: WARNING (5 unused)
- Query Statistics: WARNING (avg 2.5s)
- Missing Indexes: WARNING (4 suggestions)
```

**何时使用**:
- 定期性能检查（每日/周/月）
- 查询优化项目规划
- 性能基准设定
- 数据库审计

---

## 工具架构

### 核心类: QueryAnalyzer

```python
class QueryAnalyzer:
    """查询分析工具"""

    @staticmethod
    def analyze_query_complexity() -> Dict[str, Any]:
        """分析查询复杂度"""

    @staticmethod
    def analyze_execution_plans() -> Dict[str, Any]:
        """分析执行计划"""

    @staticmethod
    def analyze_join_patterns() -> Dict[str, Any]:
        """分析 JOIN 模式"""

    @staticmethod
    def analyze_subquery_efficiency() -> Dict[str, Any]:
        """分析子查询效率"""

    @staticmethod
    def analyze_index_effectiveness() -> Dict[str, Any]:
        """分析索引有效性"""

    @staticmethod
    def analyze_query_statistics() -> Dict[str, Any]:
        """分析查询统计"""

    @staticmethod
    def identify_missing_indexes() -> Dict[str, Any]:
        """识别缺失索引"""

    @staticmethod
    def generate_query_report() -> Dict[str, Any]:
        """生成查询报告"""
```

### 工具集成

工具通过以下方式集成到查询分析子代理：

```python
query_tools = {
    "query_complexity": {
        "name": "analyze_query_complexity",
        "description": "分析查询复杂度...",
        "function": get_query_complexity_report,
    },
    # ... 其他工具
}
```

---

## 使用示例

### 示例 1: 快速查询检查

```python
from app.tools.query_tools import QueryAnalyzer

# 快速生成综合报告
report = QueryAnalyzer.generate_query_report()
print(report["overall_status"])  # 获取整体状态
print(report["critical_issues"])  # 获取关键问题
```

### 示例 2: 针对性分析

```python
from app.tools.query_tools import QueryAnalyzer

# 如果看到执行计划问题，针对分析
plan_analysis = QueryAnalyzer.analyze_execution_plans()

if plan_analysis["status"] == "CRITICAL":
    print("执行计划是性能问题的主要原因")
    print(f"发现 {plan_analysis['inefficient_plans']} 个效率问题")
    for issue in plan_analysis["issues"]:
        print(f"  • {issue['issue']}")
```

### 示例 3: 子代理中使用

```python
from app.agents.subagents.query_analyzer import execute_all_query_analyses

# 查询分析子代理执行所有分析
results = execute_all_query_analyses()

for analysis_type, result in results.items():
    print(f"{analysis_type}: {result}")
```

---

## 性能阈值和警告

### 查询复杂度

| 复杂查询数 | 状态 | 含义 |
|----------|------|------|
| 0-2 | ✓ 正常 | 可接受 |
| 2-5 | ⚠ 监控 | 需要关注 |
| 5-10 | ⚠ 警告 | 需要优化 |
| >10 | 🔴 严重 | 立即优化 |

### 执行计划问题

| 问题数 | 状态 | 含义 |
|--------|------|------|
| 0-3 | ✓ 正常 | 无问题 |
| 3-8 | ⚠ 监控 | 有问题 |
| 8-15 | ⚠ 警告 | 有问题 |
| >15 | 🔴 严重 | 严重问题 |

### 查询执行时间

| 指标 | 状态 | 含义 |
|------|------|------|
| 平均 < 0.5s | ✓ 优秀 | 很好 |
| 平均 0.5-2s | ✓ 良好 | 可接受 |
| 平均 2-5s | ⚠ 警告 | 需要优化 |
| 平均 > 5s | 🔴 严重 | 需要立即优化 |

---

## 最佳实践

### 1. 定期分析

```python
# 每日运行综合报告
from app.tools.query_tools import get_comprehensive_query_report
report = get_comprehensive_query_report()
```

### 2. 针对性优化

- 如果看到执行计划问题 → 运行 analyze_execution_plans
- 如果看到 JOIN 性能问题 → 运行 analyze_join_patterns
- 如果索引性能下降 → 运行 analyze_index_effectiveness

### 3. 优先级排序

根据以下顺序优化：
1. **CRITICAL** 执行计划问题（可能停机）
2. **WARNING** 缺失索引（影响性能）
3. **INFO** 查询复杂度（可维护性）

### 4. 效果验证

```python
# 修改前后对比
before = QueryAnalyzer.analyze_query_statistics()
# 应用优化...
after = QueryAnalyzer.analyze_query_statistics()
# 对比 before['metrics'] 和 after['metrics']
```

---

## 与主代理的集成

查询分析子代理在 RCA 流程中的角色：

```
主代理 (RootCauseAnalyzer)
  ↓
调用查询分析子代理
  ↓
查询分析子代理使用工具
  ├─ analyze_query_complexity → 发现复杂查询
  ├─ analyze_execution_plans → 发现执行问题
  ├─ analyze_join_patterns → 发现 JOIN 问题
  ├─ analyze_subquery_efficiency → 发现子查询问题
  ├─ analyze_index_effectiveness → 发现索引问题
  ├─ analyze_query_statistics → 发现统计异常
  └─ identify_missing_indexes → 发现缺失索引
  ↓
收集所有查询指标
  ↓
LLM 分析综合结果
  ↓
生成根因分析报告
```

---

## 扩展工具

### 添加新工具步骤

1. 在 `QueryAnalyzer` 中添加新的 `analyze_*` 方法
2. 创建对应的 `get_*_report()` 便利函数
3. 在 `query_tools` 字典中注册
4. 更新子代理的 system_prompt

### 示例：添加查询缓存分析

```python
@staticmethod
def analyze_query_cache() -> Dict[str, Any]:
    """分析查询缓存有效性"""
    # 实现分析逻辑
    return {
        "status": "OK",
        "cache_hits": 0,
        "recommendations": [...]
    }

# 在 query_tools 中注册
query_tools["cache"] = {
    "name": "analyze_query_cache",
    "description": "检查查询缓存有效性",
    "function": get_query_cache_report,
}
```

---

## 故障排除

### 工具返回错误

**问题**: `"message": "Failed to analyze..."`

**原因**:
- 数据库连接断开
- 权限不足无法读取执行计划
- 性能 schema 未启用

**解决**:
1. 检查数据库连接
2. 验证用户权限（需要 PROCESS 权限）
3. 启用性能 schema

### 查询数据不可用

**问题**: `"status": "UNKNOWN"`

**原因**:
- 慢查询日志未启用
- 没有慢查询数据
- 数据库版本不兼容

**解决**:
1. 启用慢查询日志：`SET GLOBAL slow_query_log = 'ON'`
2. 设置合理的 slow_query_threshold
3. 检查数据库版本兼容性

---

## 性能提示

- 工具执行时间通常 < 1 秒
- 综合报告生成时间 < 5 秒
- 分析不会锁定表或导致性能下降
- 适合在高峰期和离峰期运行

---

## 总结

这 8 个工具为查询分析子代理提供了全面的优化能力，可以快速识别和解决查询性能问题。合理使用这些工具，可以显著提升数据库查询性能和代码质量。
