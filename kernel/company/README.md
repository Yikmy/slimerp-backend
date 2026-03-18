# Kernel Company Module

## 1. 简介
`kernel.company` 提供单用户多公司（Multi-Company）架构支持，定义了公司作用域。它负责公司管理、用户关联以及当前请求的上下文解析，是实现数据隔离的关键。

## 2. 目标与职责
### 目标
支持单用户属于多个公司，并在请求中明确当前操作的公司作用域。

### 职责边界
- **负责**：
  - `Company` 模型定义。
  - `UserCompanyAccess`：用户与公司关联。
  - `UserCompanyPreference`：用户偏好（如默认公司）。
  - `Context Service`：解析请求头，注入 `current_company`。
  - `Company Service`：公司切换、创建、查询。
- **不负责**：
  - 多租户物理隔离（Schema 隔离）。
  - 具体的业务账务逻辑。

## 3. 核心组件

### 3.1 数据模型 (Models)
位于 `kernel/company/models/company.py`：
- **`Company`**：企业实体，拥有 `name`, `code`, `tax_id` 等字段。
- **`UserCompanyAccess`**：用户与公司的多对多关系。
- **`UserCompanyPreference`**：用户默认登录公司设置。

### 3.2 服务 (Services)
位于 `kernel/company/services/company_service.py`：
- **`get_current_company(user, request)`**：获取当前请求的公司上下文。
- **`switch_company(user, company_id)`**：切换当前上下文。
- **`assert_company_access(user, company)`**：校验权限。
- **`bind_company(queryset, company)`**：查询集过滤。

### 3.3 API (Views)
位于 `kernel/company/api/views.py`：
- **`GET /api/v1/companies/`**：获取当前用户可访问的公司列表。
- **`POST /api/v1/companies/switch/`**：切换公司。
- **`GET /api/v1/companies/current/`**：获取当前生效公司。

## 4. 使用示例

### 获取当前公司上下文
在 View 或 Service 中：
```python
from kernel.company.services import company_service

def my_view(request):
    current_company = company_service.get_current_company(request.user, request)
    # 业务逻辑必须基于 current_company
    items = MyItem.objects.filter(company=current_company)
```

### 校验归属权
```python
company_service.assert_company_access(user, target_company)
```

## 5. 模块依赖
- **依赖**：`kernel.core`, `kernel.identity` (User 模型)。
- **被依赖**：`kernel.rbac`, `kernel.audit`, `kernel.system_config` 以及所有需要区分公司数据的业务模块。
