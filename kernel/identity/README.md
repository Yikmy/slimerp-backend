# Kernel Identity Module

## 1. 简介
`kernel.identity` 提供系统的用户认证和身份管理功能。它实现了自定义用户模型（User）、认证流程（Login/Logout）、会话管理（Session）和基础的用户信息服务。

## 2. 目标与职责
### 目标
解决“你是谁”的问题，确保用户能够安全登录并维持会话。

### 职责边界
- **负责**：
  - `User` 模型：核心身份载体。
  - `Authentication`：用户名/密码校验。
  - `Session/Cookie`：登录态维持。
  - `Password Management`：修改密码、重置密码。
  - `Me API`：当前用户信息接口。
- **不负责**：
  - **授权**：不包含角色和权限管理（由 `kernel.rbac` 负责）。
  - **多公司关联**：不包含用户与公司的具体业务关联（由 `kernel.company` 负责）。

## 3. 核心组件

### 3.1 数据模型 (Models)
位于 `kernel/identity/models/user.py`：
- **`User`**: 继承自 `AbstractBaseUser` 和 `BaseModel`。
  - `username`, `email`：核心标识。
  - `password`：Django 加密存储。
  - `is_active`, `is_staff`：基础状态。
  - *不包含* 业务字段（如部门、职位）。

### 3.2 服务 (Services)
位于 `kernel/identity/services/`：
- **`login_service.py`**:
  - `login(username, password)`：校验凭证并建立 Session。
  - `logout(request)`：清除 Session。
- **`password_service.py`**:
  - `change_password(user, old_pwd, new_pwd)`：修改密码逻辑。
- **`session_service.py`**:
  - `attach_session(response, user)`：处理 Cookie 和 Session。

### 3.3 API (Views)
位于 `kernel/identity/api/views.py`：
- **`POST /api/v1/auth/login/`**：用户登录。
- **`POST /api/v1/auth/logout/`**：用户登出。
- **`GET /api/v1/auth/me/`**：获取当前用户信息及关联公司。
- **`POST /api/v1/auth/change-password/`**：修改密码。

## 4. 使用示例

### 调用登录服务
```python
from kernel.identity.services import login_service

try:
    user = login_service.login(username='admin', password='password')
except AuthenticationError:
    # 处理失败
```

### 获取当前用户
在 View 中：
```python
def get(self, request):
    user = request.user  # Django 标准 AuthenticationMiddleware 注入
    # ...
```

## 5. 模块依赖
- **依赖**：`kernel.core`, `kernel.audit` (记录登录日志)。
- **被依赖**：`kernel.company`, `kernel.rbac` 以及全系统所有需要鉴权的模块。
