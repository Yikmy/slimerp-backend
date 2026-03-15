# customer 模块指南（MVP）

## 范围

- 做什么：客户主档维护、分组、联系人、地址、信用额度与账期信息
- 不做什么：销售订单、应收核销、价格策略（由其他模块承担）

## 领域对象（建议）

- Customer：code、name、status、tax_id、payment_terms、created_at
- CustomerGroup：code、name
- CustomerContact：name、phone、email、is_primary
- CustomerAddress：country、province、city、detail、is_default
- CustomerCredit：credit_limit、credit_days、risk_level

## API 资源（建议）

路由前缀：`/api/customer/`

- GET `customers/`：分页列表（支持 name/code 模糊搜索、group 过滤、status 过滤）
- POST `customers/`：创建客户
- GET `customers/{id}/`：客户详情（可聚合联系人/地址/信用信息）
- PUT `customers/{id}/`：更新客户
- DELETE `customers/{id}/`：软删除或停用
- GET/POST `groups/`：客户分组
- GET/POST `customers/{id}/contacts/`：联系人
- GET/POST `customers/{id}/addresses/`：地址
- PUT `customers/{id}/credit/`：信用与账期配置

## 权限码（建议）

建议放在 `apps/customer/permissions.py`，并在 RBAC 中注册：

- CUSTOMER_READ
- CUSTOMER_WRITE
- CUSTOMER_CREDIT_MANAGE

## 事件与 Hook（建议）

- customer.created
- customer.updated
- customer.status_changed

payload 最少包含：customer_id、operator_id、timestamp。

## 事务与依赖

- customer 为主数据模块，避免强依赖 accounting
- accounting 如需生成应收或账龄视图，优先通过事件/Hook 获取客户信息快照或按需查询

## vibe coding 提示词模板

将以下内容作为“新模块/新资源”生成输入，保持实现一致：

```text
你在一个 Django ERP 后端中实现 customer 模块的一部分，必须遵守：
- 分层：models/selectors/services/api/hooks/handlers
- 事务在 services
- API 响应遵循 docs/api.md 的 envelope
- 权限码放在 permissions.py，授权由 kernel.rbac 处理

本次要实现的资源/用例：
<在这里描述具体用例、字段、校验规则、权限、事件>
```

