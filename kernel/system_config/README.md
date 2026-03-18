# Kernel System Config Module

## 1. 简介
`kernel.system_config` 提供系统参数的统一管理，包括键值对配置和模块开关。它支持全局、公司级和模块级三层作用域，是系统灵活配置的中心。

## 2. 目标与职责
### 目标
集中管理系统行为参数，支持多层级覆盖（Global > Company > Module）。

### 职责边界
- **负责**：
  - `SystemConfig`：配置表读写。
  - `ModuleSwitch`：模块启用/禁用。
  - `Config Service`：提供统一读取接口（带缓存）。
  - `Config API`：前端配置管理。
- **不负责**：
  - 配置的具体业务解释（各模块自行消费）。
  - 远程配置中心（如 Nacos）。

## 3. 核心组件

### 3.1 数据模型 (Models)
位于 `kernel/system_config/models/config.py`：
- **`SystemConfig`**：
  - `key`：配置键（如 "site.title"）。
  - `value`：JSON 存储的值。
  - `scope`：作用域（Global, Company, Module）。
  - `company` / `module`：关联 ID（根据 scope）。
- **`ModuleSwitch`**：
  - `module_name`：Django App 名。
  - `is_enabled`：是否启用。
  - `company`：公司覆盖（可选）。

### 3.2 服务 (Services)
位于 `kernel/system_config/services/config_service.py`：
- **`get(key, scope, company=None)`**：读取配置（优先公司级覆盖）。
- **`set(key, value, scope, company=None)`**：写入配置。
- **`is_module_enabled(module, company=None)`**：检查模块开关。

### 3.3 API (Views)
位于 `kernel/system_config/api/views.py`：
- **`GET /api/v1/config/`**：获取所有配置。
- **`POST /api/v1/config/`**：更新配置。
- **`GET /api/v1/config/module-switch/`**：查询模块状态。

## 4. 使用示例

### 读取配置
```python
from kernel.system_config.services import config_service

# 读取当前公司特定的配置，无则回退到全局
site_title = config_service.get('site.title', company=request.company) or 'Default ERP'
```

### 检查模块开关
```python
if config_service.is_module_enabled('apps.accounting', company=current_company):
    # 显示会计菜单
    pass
```

### 初始化默认配置
在 migrations 或 startup 脚本中：
```python
config_service.set('default_currency', 'CNY', scope='global')
```

## 5. 模块依赖
- **依赖**：`kernel.core`, `kernel.company`。
- **被依赖**：全系统所有需要参数化控制的业务模块。
