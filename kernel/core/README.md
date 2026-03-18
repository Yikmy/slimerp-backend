# Kernel Core Module

## 1. 简介
`kernel.core` 是整个 ERP 系统的基石，提供所有模块必须依赖的基础设施。它不包含任何具体业务逻辑，仅提供抽象模型、工具函数、异常定义和数据库辅助工具。

## 2. 目标与职责
### 目标
提供最小共享基建，统一模型规范和 API 响应格式。

### 职责边界
- **负责**：
  - `BaseModel`：所有业务模型的基类。
  - `SoftDeleteModel`：软删除支持。
  - `API Response`：统一的 API 响应格式封装。
  - `Exceptions`：通用异常定义。
  - `Transaction Helper`：原子事务辅助工具。
- **不负责**：
  - 具体业务实体（如 User, Company）。
  - 复杂状态机。
  - 业务规则校验。

## 3. 核心组件

### 3.1 数据模型 (Models)
位于 `kernel/core/models/base.py`：
- **`BaseModel`**: 抽象基类，包含：
  - `id`: UUID 主键。
  - `created_at` / `updated_at`: 自动时间戳。
  - `created_by` / `updated_by`: 创建人与更新人（关联 User）。
  - `is_deleted`: 软删除标记。
  - **Managers**:
    - `objects`: 过滤掉已软删除的记录。
    - `all_objects`: 包含所有记录（含软删除）。

### 3.2 数据库工具 (DB)
位于 `kernel/core/db/transaction.py`：
- 提供事务封装工具，确保关键操作的原子性。

### 3.3 API 响应 (API)
位于 `kernel/core/api/responses.py`：
- 定义了统一的 API 返回结构（如 `code`, `message`, `data`）。

### 3.4 异常 (Exceptions)
位于 `kernel/core/exceptions.py`：
- 定义系统级基础异常，供其他模块继承。

## 4. 使用示例

### 定义新模型
```python
from kernel.core.models import BaseModel
from django.db import models

class MyBusinessModel(BaseModel):
    name = models.CharField(max_length=100)
    # id, created_at, is_deleted 等字段已自动包含
```

### 使用软删除
```python
obj = MyBusinessModel.objects.get(id=xxx)
obj.delete()  # 软删除，设置 is_deleted=True

# 查询不到已删除对象
obj = MyBusinessModel.objects.filter(id=xxx).first()  # None

# 恢复
obj = MyBusinessModel.all_objects.get(id=xxx)
obj.restore()
```

## 5. 模块依赖
- **被依赖**：被 `kernel` 下所有其他模块及 `apps` 下所有业务模块依赖。
- **依赖**：无（最底层模块）。
