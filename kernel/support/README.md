# Kernel Support Module

## 1. 简介
`kernel.support` 提供系统轻量级的扩展机制，包括 Hook 管理、注册表服务和模块元数据。它是实现业务模块松耦合与扩展能力的关键基础设施。

## 2. 目标与职责
### 目标
提供稳定的扩展点（Hook）和元数据服务，避免复杂的动态事件总线，保持架构简单。

### 职责边界
- **负责**：
  - `Hook Registry`：Hook 的注册与按序执行。
  - `Module Meta`：已安装模块的元数据读取。
  - `Registry`：通用的键值注册表。
  - `Event Facade`（可选）：轻量级事件包装。
- **不负责**：
  - 复杂消息队列（RabbitMQ 等）。
  - 重量级动态插件管理。
  - 主业务流程编排。

## 3. 核心组件

### 3.1 Hook 系统 (Hooks)
位于 `kernel/support/hooks.py`：
- **`HooksRegistry`**：单例注册器。
  - `register_hook(name, callback, order)`：注册回调，支持优先级。
  - `dispatch_hook(name, payload)`：按序同步执行所有回调。
  - `list_hooks(name)`：查看挂载点。

### 3.2 注册表 (Registry)
位于 `kernel/support/registry.py`：
- **`SimpleRegistry`**：通用的字典式注册表，用于存储 Policy、Service 等。

### 3.3 模块元数据 (Module Meta)
位于 `kernel/support/module_meta.py`：
- **`get_installed_modules()`**：列出所有 Django App。
- **`get_module_meta(name)`**：获取指定模块详情。

## 4. 使用示例

### 定义并触发 Hook（在核心业务中）
```python
# sales/services/order_service.py
from kernel.support.hooks import dispatch_hook

def create_order(order_data):
    # ... 创建订单逻辑 ...
    order.save()
    
    # 触发 Hook，允许其他模块（如库存、积分）响应
    dispatch_hook('order.created', payload={'order': order})
```

### 注册 Hook（在扩展模块中）
```python
# warehouse/hooks.py
from kernel.support.hooks import register_hook

@register_hook('order.created', order=10)
def reserve_inventory(payload):
    order = payload['order']
    # 扣减库存逻辑
```

### 在 AppConfig.ready 中加载 Hook
```python
# warehouse/apps.py
def ready(self):
    import warehouse.hooks  # 确保 Hook 被注册
```

## 5. 模块依赖
- **依赖**：无（底层工具）。
- **被依赖**：全系统所有需要扩展点的业务模块。
