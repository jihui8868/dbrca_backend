# 多数据库支持架构

## 概述

系统已重构为支持多种数据库系统，使用**策略模式（Strategy Pattern）**和**方言系统（Dialect System）**来处理不同数据库的差异。

## 支持的数据库

| 数据库 | 驱动程序 | 状态 | 说明 |
|--------|---------|------|------|
| MySQL | pymysql | ✅ 已实现 | 完整支持性能监控 |
| PostgreSQL | psycopg2 | ✅ 已实现 | 完整支持性能监控 |
| Informix | pyodbc | ✅ 已实现 | 基础支持 |
| MariaDB | pymysql | ✅ 可用 | MySQL 兼容 |
| Oracle | cx_oracle | ⚠️ 框架就绪 | 需要驱动 |
| SQL Server | pymssql | ⚠️ 框架就绪 | 需要驱动 |

## 架构设计

### 1. 方言系统 (`database_types.py`)

每个数据库都有一个对应的方言类，继承自 `DatabaseDialect` 基类：

```
DatabaseDialect (基类)
├── MySQLDialect
├── PostgreSQLDialect
├── InformixDialect
├── OracleDialect (可扩展)
└── SQLServerDialect (可扩展)
```

### 2. 方言类的职责

每个方言类负责为其数据库类型提供：

```python
class DatabaseDialect:
    # SQL 查询生成
    def get_database_size_query(self) -> str
    def get_slow_queries_query(self, limit: int) -> str
    def get_table_statistics_query(self) -> str
    def get_process_list_query(self) -> str
    def get_lock_info_query(self) -> str
    def get_error_log_query(self) -> str
    def get_cache_efficiency_query(self) -> str
    def get_index_usage_query(self) -> str
    def get_configuration_query(self, param_name: str) -> str

    # 连接配置
    def get_connection_args(self) -> Dict
```

### 3. 通用数据库管理器 (`database.py`)

```
UniversalDatabaseManager
├── 检测数据库类型
├── 加载对应方言
├── 提供统一接口
└── 委托给方言类执行 SQL
```

## 使用方式

### 配置数据库连接

#### 方法 1：环境变量

```bash
# MySQL（默认）
export DATABASE_TYPE=mysql
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=password
export DB_NAME=testdb

# PostgreSQL
export DATABASE_TYPE=postgresql
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=postgres
export DB_PASSWORD=password
export DB_NAME=testdb

# Informix
export DATABASE_TYPE=informix
export DB_HOST=localhost
export DB_PORT=9088
export DB_USER=informix
export DB_PASSWORD=password
export DB_NAME=testdb
```

#### 方法 2：完整 DSN（推荐用于 CI/CD）

```bash
# MySQL
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/testdb

# PostgreSQL
export DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/testdb

# Informix
export DATABASE_URL=informix+pyodbc://informix:password@localhost:9088/testdb
```

#### 方法 3：`.env` 文件

```ini
# 使用数据库类型
DATABASE_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=mypassword
DB_NAME=mydb

# 或使用完整 DSN
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/mydb
```

### Python 代码

```python
from app.core.database import UniversalDatabaseManager

# 自动检测配置的数据库类型
db_manager = UniversalDatabaseManager()

# 测试连接
if db_manager.test_connection():
    print(f"Connected to {db_manager.db_type.value}")

# 执行数据库操作（自动使用正确的 SQL 方言）
size_info = db_manager.get_database_size()
slow_queries = db_manager.get_slow_queries()
table_stats = db_manager.get_table_statistics()
processes = db_manager.get_process_list()
locks = db_manager.get_lock_info()
```

### 获取数据库信息

```python
# 获取当前连接的数据库信息
info = db_manager.get_database_info()
# 输出: {
#   "type": "postgresql",
#   "host": "localhost",
#   "port": 5432,
#   "database": "mydb",
#   "user": "postgres"
# }
```

## 实现细节

### 数据库类型检测

```python
from app.core.database_types import detect_database_type, DatabaseType

# 从 DSN 自动检测数据库类型
db_type = detect_database_type("postgresql+psycopg2://...")
# 返回: DatabaseType.POSTGRESQL
```

### 获取对应方言

```python
from app.core.database_types import get_dialect, DatabaseType

# 获取 PostgreSQL 方言
dialect = get_dialect(DatabaseType.POSTGRESQL)

# 使用方言的查询
query = dialect.get_slow_queries_query(limit=10)
```

## 添加新数据库支持

### 步骤 1：创建方言类

在 `app/core/database_types.py` 中添加：

```python
class MyNewDatabaseDialect(DatabaseDialect):
    """NewDatabase-specific SQL dialect"""

    def __init__(self):
        super().__init__()
        self.db_type = DatabaseType.MYNEWDB

    def get_database_size_query(self) -> str:
        # NewDatabase 特定的 SQL
        return "SELECT ..."

    def get_slow_queries_query(self, limit: int = 10) -> str:
        return "SELECT ..."

    # ... 实现其他方法

    def get_connection_args(self) -> Dict:
        return {
            # NewDatabase 特定的连接参数
        }
```

### 步骤 2：添加数据库类型枚举

```python
class DatabaseType(Enum):
    MYNEWDB = "mynewdb"
```

### 步骤 3：注册方言

```python
DIALECT_REGISTRY: Dict[DatabaseType, DatabaseDialect] = {
    # ... 现有的
    DatabaseType.MYNEWDB: MyNewDatabaseDialect(),
}
```

### 步骤 4：更新配置

在 `app/core/config.py` 的 `dsn` 属性中添加 DSN 生成逻辑：

```python
elif db_type == "mynewdb":
    driver = "mynewdb_driver"
    return (
        f"mynewdb+{driver}://{self.user}:{self.password}@"
        f"{self.host}:{self.port}/{self.database}"
    )
```

## 查询兼容性

### MySQL 特定查询

```sql
-- 使用 information_schema 和 performance_schema
SELECT * FROM information_schema.tables
SELECT * FROM performance_schema.events_statements_summary_by_digest
```

### PostgreSQL 特定查询

```sql
-- 使用 pg_stat_* 视图
SELECT * FROM pg_stat_statements
SELECT * FROM pg_stat_user_tables
```

### Informix 特定查询

```sql
-- 使用 systables 和 sysadmin 函数
SELECT * FROM systables
SELECT * FROM sysadmin:onstat_m
```

## 子代理的多数据库支持

在子代理中自动使用正确的方言：

```python
# performance_analyzer 子代理
performance_analyzer = SubAgent(
    name="performance-analyzer",
    description="Analyzes database performance for MySQL, PostgreSQL, Informix...",
    system_prompt="""
    You are a database performance expert.
    You will receive analysis data for the connected database type.
    Provide insights specific to that database's optimization opportunities.
    """
)
```

## 测试多数据库配置

```bash
# 测试 MySQL
export DATABASE_TYPE=mysql
python test_setup.py

# 测试 PostgreSQL
export DATABASE_TYPE=postgresql
python test_setup.py

# 测试 Informix
export DATABASE_TYPE=informix
python test_setup.py
```

## 配置示例

### MySQL 配置文件

```ini
# .env
DATABASE_TYPE=mysql
DB_HOST=mysql.example.com
DB_PORT=3306
DB_USER=root
DB_PASSWORD=secure_password
DB_NAME=production_db
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

### PostgreSQL 配置文件

```ini
# .env
DATABASE_TYPE=postgresql
DB_HOST=postgres.example.com
DB_PORT=5432
DB_USER=postgres_user
DB_PASSWORD=secure_password
DB_NAME=analytics_db
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

### 使用 Docker Compose

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: testdb
    ports:
      - "3306:3306"

  postgres:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: postgres_password
      POSTGRES_DB: testdb
    ports:
      - "5432:5432"

  rca-app:
    build: .
    environment:
      DATABASE_TYPE: ${DATABASE_TYPE:-mysql}
      DB_HOST: ${DB_HOST:-mysql}
      DB_PORT: ${DB_PORT:-3306}
      DB_USER: ${DB_USER:-root}
      DB_PASSWORD: ${DB_PASSWORD:-root_password}
      DB_NAME: ${DB_NAME:-testdb}
    depends_on:
      - mysql
      - postgres
```

## 性能考虑

### 连接池管理

```python
# 不同数据库的连接池参数
pool_kwargs = {
    "pool_size": settings.database.pool_size,      # 最小连接数
    "max_overflow": settings.database.max_overflow, # 最大额外连接
}

# PostgreSQL 可能需要特殊配置
if self.db_type == DatabaseType.POSTGRESQL:
    # PostgreSQL 特定的池配置
    pass
```

### 查询超时

不同数据库的超时配置方式不同：

- **MySQL**: `connect_timeout` 在连接参数中
- **PostgreSQL**: `connect_timeout` 和 `options="-c statement_timeout=30000"`
- **Informix**: 使用 ODBC 超时参数

## 故障排除

### 错误：数据库类型无法检测

```
ValueError: Could not detect database type from DSN: ...
```

**解决方案**：确保 DSN 包含有效的驱动程序标识符：
- MySQL: `mysql+pymysql://`
- PostgreSQL: `postgresql+psycopg2://`
- Informix: `informix+pyodbc://`

### 错误：缺少数据库驱动程序

```
ModuleNotFoundError: No module named 'pymysql'
```

**解决方案**：安装所需的驱动程序：
```bash
# MySQL
pip install pymysql

# PostgreSQL
pip install psycopg2-binary

# Informix
pip install pyodbc

# Oracle
pip install cx_oracle

# SQL Server
pip install pymssql
```

### 性能查询不可用

如果某些性能查询返回空结果，可能原因：

1. **performance_schema 未启用**（MySQL）
   ```sql
   SET GLOBAL performance_schema = ON;
   ```

2. **pg_stat_statements 扩展未安装**（PostgreSQL）
   ```sql
   CREATE EXTENSION pg_stat_statements;
   ```

3. **权限不足**
   - 确保数据库用户有必要的查看权限

## 最佳实践

### 1. 使用完整 DSN

推荐在生产环境中使用完整 DSN：

```bash
export DATABASE_URL="postgresql+psycopg2://user:pass@host:5432/db"
```

### 2. 数据库特定优化

为每个数据库类型进行特定优化：

```python
if db_manager.db_type == DatabaseType.MYSQL:
    # MySQL 特定的优化
    db_manager.execute_command("SET SESSION sql_mode='STRICT_TRANS_TABLES'")
elif db_manager.db_type == DatabaseType.POSTGRESQL:
    # PostgreSQL 特定的优化
    db_manager.execute_command("SET work_mem TO '256MB'")
```

### 3. 测试连接

总是测试连接：

```python
if not db_manager.test_connection():
    sys.exit("Cannot connect to database")
```

### 4. 监控数据库类型

```python
info = db_manager.get_database_info()
logger.info(f"Connected to {info['type']} at {info['host']}:{info['port']}")
```

## 文件结构

```
app/core/
├── config.py              ✅ 多数据库配置
├── database.py            ✅ UniversalDatabaseManager
├── database_types.py      ✅ 数据库方言系统
└── __init__.py

支持文件：
├── MULTI_DATABASE_SUPPORT.md  # 本文档
└── 环境变量示例文件
```

## 总结

✅ **多数据库架构就绪**
- 支持 MySQL、PostgreSQL、Informix 等多个数据库
- 易于扩展以支持新数据库
- 使用标准化接口

✅ **灵活的配置**
- 支持环境变量配置
- 支持 DSN 配置
- 支持 .env 文件

✅ **自动化检测**
- 从 DSN 自动检测数据库类型
- 自动加载对应方言
- 统一的 API 接口

✅ **易于维护**
- 添加新数据库只需创建一个新的方言类
- 每个方言独立，修改不影响其他数据库
- 清晰的代码组织
