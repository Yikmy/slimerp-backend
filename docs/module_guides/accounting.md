# accounting 模块指南（MVP 记账核心）

## 范围

- 做什么：会计期间、会计科目、凭证（分录）、过账到总账分录的最小闭环
- 不做什么：完整应收应付流程、成本分摊、复杂报表（可后续扩展）

## 领域对象（建议）

- Period：year、month、status（open/closed）
- Account：code、name、type、is_active
- Journal：number、date、status（draft/submitted/posted/voided）
- JournalItem：journal_id、account_id、debit、credit、summary、customer_id（可选）
- GLEntry：posting_date、account_id、debit、credit、source_journal_id

## 状态与流转（MVP）

- draft：可编辑
- submitted：提交待审核（可选）
- posted：已过账，不可改动（仅允许冲销/更正单据）
- voided：作废（仅在未 posted 时允许）

## API 资源（建议）

路由前缀：`/api/accounting/`

- GET/POST `periods/`：期间维护
- GET/POST `accounts/`：科目维护
- GET `journals/`：凭证列表（支持 date/period/status 过滤）
- POST `journals/`：创建凭证（含分录）
- GET `journals/{id}/`：凭证详情
- PUT `journals/{id}/`：更新凭证（仅 draft）
- POST `journals/{id}/submit/`：提交
- POST `journals/{id}/post/`：过账（生成 GL entries）
- POST `journals/{id}/void/`：作废（仅 draft/submitted）
- GET `gl_entries/`：总账分录查询（支持 account/period/date 过滤）

## 关键校验（MVP）

- 凭证借贷平衡：sum(debit) == sum(credit)
- 过账只允许在 open period
- posted 凭证不可编辑

## 权限码（建议）

建议放在 `apps/accounting/permissions.py`，并在 RBAC 中注册：

- ACCOUNTING_READ
- ACCOUNTING_WRITE
- ACCOUNTING_POST

## 事件与 Hook（建议）

- accounting.journal_created
- accounting.journal_posted
- accounting.journal_voided

payload 最少包含：journal_id、operator_id、timestamp、period_id。

## 事务与依赖

- 过账是本模块的强一致事务边界：生成 GL entries 必须与 journal 状态变更同事务提交
- 其他模块（sales/purchase/warehouse）如需自动建凭证，建议通过 handlers 接收事件并创建 draft journal

## vibe coding 提示词模板

```text
你在一个 Django ERP 后端中实现 accounting 模块的一部分，必须遵守：
- 分层：models/selectors/services/api/hooks/handlers
- 事务在 services
- API 响应遵循 docs/api.md 的 envelope
- 权限码放在 permissions.py，授权由 kernel.rbac 处理
- 过账为强一致事务边界

本次要实现的资源/用例：
<在这里描述具体用例、字段、校验规则、权限、状态流转、事件>
```

