# material 模块指南（MVP）

## 范围

- 做什么：物料主档、分类、计量单位、单位换算、条码、价格资料
- 不做什么：库存收发、采购/销售定价策略（由其他模块承担）

## 领域对象（建议）

- Item：sku/code、name、category_id、base_uom_id、status、spec、created_at
- Category：code、name、parent_id
- Uom：code、name
- UomConversion：from_uom、to_uom、factor
- Barcode：barcode、item_id、uom_id
- Price：item_id、price_type、currency、amount、valid_from、valid_to

## API 资源（建议）

路由前缀：`/api/material/`

- GET `items/`：分页列表（支持 name/code/barcode 搜索、category 过滤、status 过滤）
- POST `items/`：创建物料
- GET `items/{id}/`：物料详情（可聚合条码/价格/换算）
- PUT `items/{id}/`：更新物料
- DELETE `items/{id}/`：软删除或停用
- GET/POST `categories/`：分类维护
- GET/POST `uoms/`：单位维护
- GET/POST `conversions/`：单位换算维护
- GET/POST `barcodes/`：条码维护
- GET/POST `prices/`：价格资料维护

## 权限码（建议）

建议放在 `apps/material/permissions.py`，并在 RBAC 中注册：

- MATERIAL_READ
- MATERIAL_WRITE
- MATERIAL_PRICE_MANAGE

## 事件与 Hook（建议）

- material.item_created
- material.item_updated
- material.item_status_changed

payload 最少包含：item_id、operator_id、timestamp。

## 事务与依赖

- material 为主数据模块，不强依赖 warehouse
- warehouse/sales/purchase 如需引用物料信息，优先按需查询或订阅变更事件

## vibe coding 提示词模板

```text
你在一个 Django ERP 后端中实现 material 模块的一部分，必须遵守：
- 分层：models/selectors/services/api/hooks/handlers
- 事务在 services
- API 响应遵循 docs/api.md 的 envelope
- 权限码放在 permissions.py，授权由 kernel.rbac 处理

本次要实现的资源/用例：
<在这里描述具体用例、字段、校验规则、权限、事件>
```

