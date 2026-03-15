# 开发规范（质量门禁与一致性）

本文件用于约束开发行为，保证“冻结内核 + 可扩展模块”长期可维护。

## 质量门禁（强制）

- 必须启用 pre-commit，且仓库根目录必须存在 `.pre-commit-config.yaml`
- 必须启用 flake8，且仓库根目录必须存在 `.flake8`

## 代码组织

- kernel：稳定层，只接受“通用能力”变更
- apps：业务模块层，每个模块自包含（models/selectors/services/api/hooks/handlers）
- plugs：可删除、实验性能力，不得反向污染 kernel 的抽象

## 分层职责

- models：只做数据约束，不做跨聚合业务流程
- selectors：只读查询，不做写入
- services：业务写入与规则，聚合事务边界
- api：输入输出适配（序列化、权限、分页、异常映射）
- hooks：对外扩展点定义（触发时机、payload 结构）
- handlers：对接其他模块事件或外部系统

## 事务边界

- 事务默认放在 service 层
- 跨模块写入尽量拆为：主模块强一致事务 + 事件驱动的后续联动

## 权限与审计

- 每个模块必须提供 `permissions.py`，且权限码稳定不随意变更
- 关键写入动作必须触发审计（由模块 hooks 或 kernel.audit 统一入口）

## 测试最小集

MVP 阶段建议至少覆盖：

- services 的关键写入路径（创建/修改/状态流转）
- selectors 的关键查询（过滤、分页、排序）
- api 的权限与错误码

## 新模块落地检查清单

新模块合入前必须满足：

- 本地提交前通过 pre-commit
- 存在 `docs/module_guides/<module>.md`，且描述清晰
- models / services / api 最小闭环可运行
- 权限码可被 rbac 注册
- 至少有一组 tests 覆盖关键写入逻辑
