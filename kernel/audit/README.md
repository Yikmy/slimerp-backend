# Kernel Audit Module

## 1. 简介
`kernel.audit` 提供系统关键动作的审计日志和登录日志。它用于记录“谁、在何时、对什么、做了什么、结果如何”，是系统的合规与排错基础。

## 2. 目标与职责
### 目标
统一记录所有关键业务操作和登录行为，供事后追溯。

### 职责边界
- **负责**：
  - `AuditLog`：记录业务动作（Actor, Target, Before/After）。
  - `LoginLog`：记录登录/登出历史。
  - `Audit Service`：写入接口。
  - `Audit ViewSet`：查看日志。
- **不负责**：
  - 业务本身的日志（如 debug 日志）。
  - 复杂的 BI 分析。

## 3. 核心组件

### 3.1 数据模型 (Models)
位于 `kernel/audit/models/`：
- **`AuditLog`**：
  - `actor`: 操作人。
  - `company`: 所属公司。
  - `action`: 动作类型（如 "create", "update"）。
  - `target_model`: 目标模型名。
  - `target_id`: 目标对象 ID。
  - `changes`: 变更内容 JSON（before/after）。
  - `status`: 成功/失败。
- **`LoginLog`**：
  - `user`: 登录用户。
  - `ip_address`: 来源 IP。
  - `user_agent`: 客户端信息。
  - `status`: 成功/失败。

### 3.2 服务 (Services)
位于 `kernel/audit/services/audit_service.py`：
- **`log_action(...)`**：记录业务操作。
- **`log_login(...)`**：记录登录事件。

### 3.3 API (Views)
位于 `kernel/audit/api/views.py`：
- **`GET /api/v1/audit/logs/`**：查询审计日志（支持过滤）。
- **`GET /api/v1/audit/login-logs/`**：查询登录日志。

## 4. 使用示例

### 记录业务操作
```python
from kernel.audit.services import audit_service

audit_service.log_action(
    actor=request.user,
    company=current_company,
    action='update',
    target=my_object,
    changes={'status': {'old': 'draft', 'new': 'active'}}
)
```

### 记录登录
在 `kernel.identity` 的 `login_service` 中自动调用：
```python
audit_service.log_login(
    user=user,
    request=request,
    status='success'
)
```

## 5. 模块依赖
- **依赖**：`kernel.core`, `kernel.identity`, `kernel.company`。
- **被依赖**：`kernel.identity`, `kernel.rbac` 及所有需要审计的关键业务模块。
