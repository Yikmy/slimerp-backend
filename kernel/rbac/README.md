# Kernel RBAC Module

## 1. 简介
`kernel.rbac` (Role-Based Access Control) 是系统的权限控制中心，负责定义“用户能做什么”。它管理角色、权限码、授权关系，并提供权限校验引擎。

## 2. 目标与职责
### 目标
提供细粒度的权限控制，支持按公司维度授权，并可通过策略扩展。

### 职责边界
- **负责**：
  - `Role`：角色定义。
  - `Permission`：权限码定义 (`module.resource.action`)。
  - `RolePermission`：角色与权限绑定。
  - `UserRole`：用户按公司分配角色。
  - `Permission Engine`：校验用户在特定公司下是否拥有特定权限。
  - `Policy Registry`：复杂资源级权限的扩展点。
- **不负责**：
  - 用户登录认证。
  - 业务逻辑的具体执行。

## 3. 核心组件

### 3.1 数据模型 (Models)
位于 `kernel/rbac/models/rbac.py`：
- **`Role`**：业务角色（如 "Sales Manager"）。
- **`Permission`**：原子权限（如 "sales.order.create"）。
- **`RolePermission`**：角色-权限多对多关联。
- **`UserRole`**：用户-角色-公司关联（`user_id`, `company_id`, `role_id`）。

### 3.2 服务 (Services)
位于 `kernel/rbac/services/`：
- **`permission_service.py`**:
  - `has_perm(user, company, code, resource=None)`：核心校验入口。
- **`role_service.py`**:
  - `assign_role(user, company, role)`：分配角色。
- **`grant_service.py`**:
  - `grant(role, permission)`：授予角色权限。
- **`policy_registry.py`**:
  - `resolve(code)`：获取复杂策略类。

### 3.3 API (Views)
位于 `kernel/rbac/api/views.py`：
- **`GET /api/v1/rbac/roles/`**：角色列表。
- **`POST /api/v1/rbac/assign-role/`**：分配角色。
- **`POST /api/v1/rbac/grant/`**：授予权限。
- **`GET /api/v1/rbac/me-permissions/`**：获取当前用户的所有权限码。

## 4. 使用示例

### 定义新权限
在业务模块的 `permissions.py` 中：
```python
# customer/permissions.py
CUSTOMER_CREATE = 'customer.customer.create'
# 需要在数据库中创建 Permission 记录
```

### 校验权限 (Service层)
```python
from kernel.rbac.services import permission_service

if not permission_service.has_perm(user, company, 'customer.customer.create'):
    raise PermissionDenied("Cannot create customer")
```

### 校验权限 (View层)
```python
class CustomerCreateView(APIView):
    permission_classes = [HasPerm('customer.customer.create')]
    # ...
```

## 5. 模块依赖
- **依赖**：`kernel.core`, `kernel.identity`, `kernel.company`。
- **被依赖**：全系统所有需要鉴权的业务 API。
