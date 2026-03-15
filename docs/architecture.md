# 架构协议（冻结内核 + 可扩展模块）

本文档用于约束“新模块”开发的一致性（vibe coding / 人工开发均适用），并作为前后端对齐的单一事实来源。

## 目标与边界

- 目标：以稳定的 kernel 承载通用能力，以 apps 承载可替换的业务模块，实现可拆分 MVP
- 边界：kernel 不放业务规则；业务规则只存在于 apps/<module>
- 依赖方向：apps 可以依赖 kernel；kernel 不依赖任何业务模块

## 分层约定（每个业务模块通用）

模块目录：`apps/<module>/`

- models：领域数据结构与约束（字段、唯一性、外键、状态字段）
- selectors：只读查询（列表、详情、报表查询、复杂过滤）
- services：写入与业务规则（创建/修改/流转/作废/过账等）
- api：对外接口（请求校验、序列化、权限、错误映射、分页）
- hooks：模块内扩展点（可被其他模块或 plug 订阅/触发）
- handlers：跨模块对接的适配层（接收事件、生成本模块动作）
- permissions.py：权限码枚举/常量（供 rbac 注册与前端对齐）

## kernel 约定（稳定层）

kernel 目标是“可复用、可预测、低变更”，建议只包含：

- core：BaseModel、事务封装、统一响应、通用异常、少量 utils
- identity：身份认证（用户、登录、会话）
- rbac：授权（角色、权限码、策略）
- audit：审计追踪（关键动作留痕）
- system_config：系统参数、模块开关
- support：轻量注册与事件接口（事件、hook、模块元信息）

kernel 对 apps 的唯一“了解方式”是通过注册/元信息读取（例如 module_meta/registry），禁止直接 import 业务模块实现。

## 模块之间如何协作

默认采用“同步接口 + 事件/Hook 扩展”的组合：

- 同步：一个模块通过对方提供的 service 或 api（建议优先 service）完成强一致协作
- 事件/Hook：用于弱一致、可选扩展、可插拔联动（例如审计写入、自动建账、通知）

跨模块依赖建议优先走 kernel.support 定义的事件接口，减少硬耦合。

## MVP 模块最小集

按冻结树的意图，MVP 建议只落地：

- customer：客户主数据
- material：物料主数据
- accounting：记账核心（会计科目/期间/凭证/过账最小闭环）

其余模块（sales/purchase/warehouse）只保留对接边界与占位，不进入 MVP 的强依赖链。

## 新模块生成协议（用于 vibe coding）

新模块在开始编码前必须输出以下“模块契约”，并存放在 `docs/module_guides/<module>.md`：

- 模块范围：做什么、不做什么
- 领域对象：表/核心字段/唯一性/关键状态
- API 面：路由前缀、资源、分页与过滤、错误码
- 权限：权限码列表与含义
- 事件与 Hook：对外发布/对外订阅清单
- 与其他模块依赖：调用关系与事务边界

## 目录布局建议

文档根目录：`backend/docs/`

- `docs/architecture.md`：架构协议（本文件）
- `docs/api.md`：API 契约与响应规范
- `docs/development.md`：开发规范（分层、测试、质量门禁）
- `docs/module_guides/*.md`：各模块契约与实现指南

## 工程决策（已冻结）

- API 框架：DRF
- 数据库：生产/预发采用 PostgreSQL；开发/测试允许默认 sqlite.db
- 多租户：不做
- 异步任务：允许引入，但不进入 kernel 的冻结范围；MVP 可先忽略
- 日志与追踪：参考 ERPNext，将用户操作留痕与系统任务执行记录区分建模与查询面
