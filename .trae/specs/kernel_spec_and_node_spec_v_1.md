# Kernel Spec 与 Node Spec v1

## 目标

本文用于冻结 Django ERP 项目的 `kernel` 规格，并为第一阶段各核心能力定义可执行的 `node_spec`。

设计原则：

1. kernel 只放所有模块都会长期依赖的稳定能力。
2. 业务规则不进 kernel，业务状态机分散在各 app 内。
3. hook 只是扩展点，不承载主业务。
4. service 是主业务入口，API 只做输入输出适配。
5. 单用户多公司：`company` 作为平台级作用域进入 kernel。
6. warehouse、ledger、inventory 等仍属于业务模块，不进入 kernel。

***

## 一、Kernel 总体 Spec

### 1.1 kernel 的职责范围

kernel 负责以下稳定基础设施：

- core：基础模型、异常、API 响应、事务辅助、少量工具
- company：公司作用域、当前公司上下文、公司切换、公司归属校验
- identity：认证、登录、session/cookie、密码管理
- rbac：角色、权限码、授权关系、权限判断、策略扩展
- audit：关键动作审计与登录日志
- system\_config：系统参数与模块开关
- support：轻量 hook / registry / module meta / event facade

这些边界来自当前冻结版项目树，其中 kernel 已被限定为认证、授权、审计、配置与少量基础设施的稳定层，而业务模块如 accounting、sales、warehouse 各自维护状态与流程。

### 1.2 kernel 不负责的内容

以下内容不进入 kernel：

- 会计总账、应收应付、成本核算
- 仓库、库存、库存移动、盘点
- 销售/采购/生产等业务状态流转
- 复杂事件总线、动态模块发现、重量级服务注册中心

冻结版已将 support 收缩为轻量支撑层，替代了早期更重的 `share` 集成中心；同时各业务 app 自己持有 `states.py`、`transitions.py`、`services/flow_service.py`。

### 1.3 kernel 对业务模块提供的统一约束

每个业务 app 都遵守：

- models/
- selectors/
- services/
- permissions.py
- policies/
- api/
- hooks/
- tests/

会计、销售、仓储等模块都已按这个模式组织，并将状态定义与流转规则下沉到模块自身。fileciteturn4file13L1-L37 fileciteturn4file16L9-L30

***

## 二、Kernel 子系统 Spec

## 2.1 core spec

### 目标

提供最小共享基建，不放业务规则。

### 范围

- BaseModel
- SoftDeleteModel（可选）
- API 响应格式
- API 异常映射
- 分页基类
- transaction 原子事务辅助
- kernel 级常量 / 枚举 / 类型
- 少量纯函数工具

### 不做

- BaseDocument
- 通用状态机
- 业务校验器全集
- 业务事件总线

冻结版里 `core` 已明确只承担基础抽象模型、API 公共组件、数据库辅助封装、常量/枚举/异常与少量工具。fileciteturn4file7L1-L27

### 输出约束

- 所有业务模型继承 `BaseModel`
- 所有 API 统一响应结构
- 所有 service 异常可映射到统一 API 错误
- 所有关键写操作走 transaction helper

***

## 2.2 company spec

### 目标

支持单用户多公司模式，为全系统提供公司作用域。

### 范围

- Company 模型
- UserCompanyAccess / UserCompanyPreference
- 当前公司上下文解析
- 当前公司切换
- 业务对象 company 归属校验
- 查询默认按 current\_company 过滤

### 不做

- 多租户 schema 隔离
- 多账套引擎
- 仓库与库存组织
- 会计总账逻辑

### 关键规则

- 所有关键业务模型默认带 `company_id`
- 用户可以关联多个公司，但当前请求只绑定一个 current\_company
- 权限判定必须带公司作用域
- 切换公司要落 session 或显式请求头

***

## 2.3 identity spec

### 目标

确定“用户是谁、如何登录、会话如何维持”。

### 范围

- 自定义用户模型
- 登录 / 登出
- session / cookie 管理
- 当前用户信息接口
- 密码修改与密码校验
- 认证 backend（如需要）

### 不做

- 角色授权
- 细粒度权限策略
- 业务资源级访问控制

冻结版已将 identity 独立为身份认证子系统，包含 user 模型、login/session/password 服务、API 层与可选 auth backend。fileciteturn4file2L1-L19

### 输出约束

- API 认证统一走 session/cookie
- 认证失败抛标准异常
- 当前用户接口固定返回 user + current\_company + roles 概览

***

## 2.4 rbac spec

### 目标

确定“用户在某公司里能做什么”。

### 范围

- Role
- Permission
- RolePermission
- UserRole（建议带 company 维度）
- permission\_service
- role\_service
- grant\_service
- policy base / registry

### 不做

- 登录
- session 生命周期
- 业务流转本身

冻结版里 rbac 已被定义为角色、权限码与访问判断中心，并提供 policy registry 作为细粒度策略扩展点。fileciteturn4file6L13-L38 fileciteturn4file15L1-L16

### 关键规则

- 权限码格式固定：`module.resource.action`
- 接口层声明权限码
- service 层做关键二次校验
- 资源级复杂判断走 policy
- policy 入参至少包含 `user`, `company`, `resource`, `action`

***

## 2.5 audit spec

### 目标

记录关键动作与登录行为，供追责与排错。

### 范围

- AuditLog
- LoginLog
- audit\_service
- 通用 audit hooks

### 不做

- 审计替代业务日志
- 中央化事件总线
- 复杂 BI 报表

冻结版将 audit 约束为关键业务审计与登录日志，并通过 service/hook 组合接入。fileciteturn4file12L1-L13

### 关键规则

- 审计日志最少包含：谁、在哪个公司、何时、对什么对象、做了什么、结果如何
- 只记录关键动作，不记录所有读请求
- 登录日志与业务审计分表

***

## 2.6 system\_config spec

### 目标

保存系统参数与模块开关。

### 范围

- SystemConfig
- ModuleSwitch
- config\_service
- 配置查询与更新 API

### 不做

- 复杂动态插件装卸
- 远程配置中心

冻结版已明确 system\_config 只承载键值配置与模块启停开关。fileciteturn4file12L14-L25

### 关键规则

- 参数按 scope 分类：global / company / module
- 配置读取统一经 config\_service
- 不允许业务模块随意直查配置表

***

## 2.7 support spec

### 目标

提供轻量扩展支撑层，而不是重新引入重量级 share。

### 范围

- hooks.py：hook 定义与注册
- registry.py：固定入口注册器
- module\_meta.py：模块元信息读取
- events.py：轻量事件 facade（可选）

### 不做

- 动态模块发现
- 依赖图计算引擎
- 全功能 event bus
- service registry 容器

冻结版已将早期 `share` 的重型模块发现、依赖检查、事件总线与服务注册中心收缩为 `support` 轻量支撑层。fileciteturn4file9L1-L9 fileciteturn4file18L1-L13

### hook 规则

- hook 只做附加动作
- 没有 hook，主业务仍应成立
- hook 默认不承担主事务编排

***

## 三、Kernel 总体 node\_spec 模板

每个 node\_spec 都使用同一模板：

```md
# node_spec: <node_name>

## 1. 目标
## 2. 职责边界
## 3. 输入
## 4. 输出
## 5. 数据模型
## 6. 核心服务
## 7. API
## 8. 权限
## 9. 审计
## 10. 异常
## 11. 测试
## 12. 本节点不做什么
## 13. 与其他节点关系
```

***

## 四、Kernel 各功能 node\_spec

## 4.1 node\_spec: core.base\_model

### 1. 目标

统一所有模型的主键、时间戳、审计字段、软删除兼容入口。

### 2. 职责边界

只提供抽象字段与少量通用方法，不承载业务逻辑。

### 3. 输入

模型实例创建、更新、删除动作。

### 4. 输出

统一字段：id, created\_at, updated\_at, created\_by, updated\_by, is\_deleted（可选）。

### 5. 数据模型

抽象基类，不直接落业务表。

### 6. 核心服务

无；仅模型 mixin/abstract base。

### 7. API

无直接 API。

### 8. 权限

无。

### 9. 审计

字段更新由 audit service 消费。

### 10. 异常

无特定异常。

### 11. 测试

- 字段默认值
- 自动更新时间
- 软删除兼容性

### 12. 本节点不做什么

- 状态流转
- 业务编号生成

### 13. 与其他节点关系

被所有业务模型继承。

***

## 4.2 node\_spec: company.scope

### 1. 目标

为单用户多公司提供统一作用域。

### 2. 职责边界

负责当前公司识别、切换、归属校验；不负责业务账务。

### 3. 输入

- 当前请求 user
- session 中 current\_company\_id
- 显式切换公司请求

### 4. 输出

- current\_company
- user 可访问公司列表
- 归属校验结果

### 5. 数据模型

- Company
- UserCompanyAccess
- UserCompanyPreference

### 6. 核心服务

- company\_service.get\_current\_company(user, request)
- company\_service.switch\_company(user, company\_id)
- company\_service.assert\_company\_access(user, company)
- company\_service.bind\_company(queryset, company)

### 7. API

- GET /api/v1/companies/
- POST /api/v1/companies/switch/
- GET /api/v1/companies/current/

### 8. 权限

- 登录即可查看可访问公司
- 切换公司需有 access 记录

### 9. 审计

记录公司切换动作。

### 10. 异常

- CompanyNotFound
- CompanyAccessDenied
- CurrentCompanyMissing

### 11. 测试

- 单用户多公司切换
- 越权切换拦截
- 默认公司回退

### 12. 本节点不做什么

- 多租户隔离
- 仓库管理
- 总账管理

### 13. 与其他节点关系

rbac、audit、业务 app 查询都依赖 current\_company。

***

## 4.3 node\_spec: identity.auth

### 1. 目标

提供 session/cookie 认证闭环。

### 2. 职责边界

负责登录态，不负责授权。

### 3. 输入

用户名/密码、session、cookie。

### 4. 输出

登录成功态、当前用户信息、登出结果。

### 5. 数据模型

User。

### 6. 核心服务

- login\_service.login(username, password)
- login\_service.logout(request)
- session\_service.attach\_session(response, user)
- password\_service.change\_password(user, old, new)

### 7. API

- POST /api/v1/auth/login/
- POST /api/v1/auth/logout/
- GET /api/v1/auth/me/
- POST /api/v1/auth/change-password/

### 8. 权限

- login/logout 无业务权限要求
- me 需登录

### 9. 审计

- 登录成功/失败写 LoginLog
- 修改密码写 AuditLog

### 10. 异常

- InvalidCredentials
- AccountDisabled
- PasswordMismatch

### 11. 测试

- 登录成功/失败
- session 持久化
- me 接口返回 current\_company

### 12. 本节点不做什么

- 角色分配
- 业务资源授权

### 13. 与其他节点关系

依赖 company scope 输出 current\_company 概览；角色信息由 rbac 聚合。

***

## 4.4 node\_spec: rbac.permission\_engine

### 1. 目标

提供模块权限码 + 角色授权 + 策略校验。

### 2. 职责边界

负责“能不能做”，不负责“怎么做”。

### 3. 输入

user, company, permission\_code, resource(optional)。

### 4. 输出

允许/拒绝 + 拒绝原因。

### 5. 数据模型

- Role
- Permission
- RolePermission
- UserRole

### 6. 核心服务

- permission\_service.has\_perm(user, company, code, resource=None)
- role\_service.assign\_role(user, company, role)
- grant\_service.grant(role, permission)
- policy\_registry.resolve(code or resource\_type)

### 7. API

- GET /api/v1/rbac/roles/
- POST /api/v1/rbac/assign-role/
- POST /api/v1/rbac/grant/
- GET /api/v1/rbac/me-permissions/

### 8. 权限

rbac 管理接口仅限高权限角色。

### 9. 审计

记录角色分配、权限授予/回收。

### 10. 异常

- PermissionDenied
- RoleNotFound
- PermissionCodeNotFound

### 11. 测试

- 基础权限命中
- 公司维度隔离
- policy 拦截与放行

### 12. 本节点不做什么

- 用户登录
- 业务状态迁移

### 13. 与其他节点关系

identity 产出 user；company 提供作用域；业务模块在 permissions.py 与 policies/ 中接入。

***

## 4.5 node\_spec: audit.logger

### 1. 目标

记录关键行为链路。

### 2. 职责边界

只做留痕，不替代领域日志。

### 3. 输入

actor, company, action, target, before, after, result。

### 4. 输出

AuditLog / LoginLog。

### 5. 数据模型

- AuditLog
- LoginLog

### 6. 核心服务

- audit\_service.log\_action(...)
- audit\_service.log\_login(...)

### 7. API

- GET /api/v1/audit/logs/
- GET /api/v1/audit/login-logs/

### 8. 权限

审计查看仅限特定权限。

### 9. 审计

本节点自身不再二次审计。

### 10. 异常

- AuditWriteFailed（通常降级记录）

### 11. 测试

- 关键动作落日志
- 登录成功/失败落日志
- before/after 字段裁剪

### 12. 本节点不做什么

- 业务报表
- 全量请求埋点

### 13. 与其他节点关系

被 identity、rbac、业务 service、hook 共同调用。

***

## 4.6 node\_spec: system\_config.config\_service

### 1. 目标

统一系统参数读取入口。

### 2. 职责边界

负责配置读写与缓存，不负责业务解释。

### 3. 输入

key, scope, company(optional), module(optional)。

### 4. 输出

typed config value。

### 5. 数据模型

- SystemConfig
- ModuleSwitch

### 6. 核心服务

- config\_service.get(key, scope='global', company=None)
- config\_service.set(...)
- config\_service.is\_module\_enabled(module, company=None)

### 7. API

- GET /api/v1/config/
- POST /api/v1/config/
- GET /api/v1/config/module-switch/

### 8. 权限

配置管理仅限系统管理权限。

### 9. 审计

配置变更必须审计。

### 10. 异常

- ConfigKeyNotFound
- InvalidConfigValue

### 11. 测试

- global/company/module 三级读取
- 默认值回退
- 模块开关生效

### 12. 本节点不做什么

- 远程配置中心
- 动态插件生命周期

### 13. 与其他节点关系

业务模块通过 service 调用，不直接查表。

***

## 4.7 node\_spec: support.hooks\_registry

### 1. 目标

提供固定、可控的 hook 注册和调用。

### 2. 职责边界

只做扩展点管理，不做主流程编排。

### 3. 输入

hook\_name, callback, payload。

### 4. 输出

按顺序执行的 hook 调用结果。

### 5. 数据模型

无必须模型。

### 6. 核心服务

- register\_hook(name, callback, order=100)
- dispatch\_hook(name, payload)
- list\_hooks(name)

### 7. API

无公开业务 API；必要时仅内部 debug 接口。

### 8. 权限

无。

### 9. 审计

关键 hook 注册变更可记审计。

### 10. 异常

- HookNotFound
- HookExecutionError

### 11. 测试

- 顺序执行
- 单个 hook 异常是否中断
- payload 传递完整性

### 12. 本节点不做什么

- 复杂事件总线
- 跨模块主事务

### 13. 与其他节点关系

被 audit 和业务模块 hooks/ 使用。

***

## 五、第一批业务模块 node\_spec 建议顺序

基于冻结版，MVP 先落地 `customer`、`material`、`accounting` 最合理。冻结版已经明确这三个是首批优先模块。fileciteturn4file1L1-L12

建议顺序：

1. kernel.core
2. kernel.company
3. kernel.identity
4. kernel.rbac
5. kernel.audit
6. kernel.system\_config
7. apps.customer
8. apps.material
9. apps.accounting
10. apps.sales（再引入）
11. apps.warehouse（再引入）

***

## 六、下一步建议

下一步不要一下子把所有 app 的 node\_spec 全铺开，而是先做下面 3 份：

1. `kernel/company` 完整 node\_spec
2. `kernel/identity + rbac` 联动 node\_spec
3. `apps/accounting` node\_spec（以公司作用域为前提）

因为这三份会直接决定：

- 单用户多公司是否成立
- 登录和授权是否终于清晰
- 会计总账能否按公司隔离

只要这三份定住，后面的 customer/material/sales/warehouse 都会顺很多。
