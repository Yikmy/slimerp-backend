# Django ERP 后端冻结版结构说明

版本：当前会话冻结稿  
目的：将 `Tree_revised.md` 改写为“目录/文件即职责说明”的可读版本，便于后续按 kernel + MVP（物料 / 客户 / 记账）推进。

## 标注版项目树

```text
backend/
├── manage.py                 # Django 项目管理入口
├── requirements/             # 依赖清单目录，按环境拆分安装包
│   ├── base.txt              # 通用依赖
│   ├── dev.txt               # 开发环境依赖
│   └── prod.txt              # 生产环境依赖
├── pyproject.toml            # 项目元数据与工具配置（可选）
├── README.md                 # 项目总览、启动方式与设计说明
├── docs/                     # 非代码文档目录
│   ├── architecture/         # 架构设计文档
│   ├── api/                  # API 设计与接口约定文档
│   ├── development/          # 开发规范、流程与约束
│   └── module_guides/        # 各业务模块接入与扩展说明
│
├── config/                   # Django 配置入口目录
│   ├── __init__.py           # Python 包标记
│   ├── urls.py               # 根路由注册
│   ├── asgi.py               # ASGI 启动入口
│   ├── wsgi.py               # WSGI 启动入口
│   └── settings/             # 分环境设置目录
│       ├── __init__.py       # Python 包标记
│       ├── base.py           # 通用设置
│       ├── dev.py            # 开发环境设置
│       └── prod.py           # 生产环境设置
│
├── kernel/                   # 冻结内核：稳定规则与公共基础设施
│   ├── __init__.py           # Python 包标记
│   ├── apps.py               # Django app 注册配置
│   │
│   ├── core/                 # 内核基础层：少量共享基建，不放业务规则
│   │   ├── __init__.py       # Python 包标记
│   │   ├── models/           # 基础抽象模型目录
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── base.py       # BaseModel：基础字段与通用模型能力
│   │   │   └── soft_delete.py# 软删除抽象（可选）
│   │   ├── api/              # API 层公共组件
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── responses.py  # 统一成功/失败返回结构
│   │   │   ├── exceptions.py # API 异常到响应的映射
│   │   │   └── pagination.py # 分页基础类
│   │   ├── db/               # 数据库辅助封装
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   └── transaction.py# 原子事务辅助封装
│   │   ├── constants.py      # 仅内核级常量
│   │   ├── enums.py          # 仅内核级枚举
│   │   ├── exceptions.py     # 内核基础异常定义
│   │   ├── typing.py         # 公共类型别名与协议（若保留）
│   │   └── utils/            # 少量纯函数工具，避免长成杂物间
│   │       ├── __init__.py   # Python 包标记
│   │       ├── datetime_utils.py # 日期时间辅助函数
│   │       ├── number_utils.py   # 数值处理辅助函数
│   │       └── string_utils.py   # 字符串处理辅助函数
│   │
│   ├── identity/             # 身份认证：用户是谁、如何登录、会话如何维持
│   │   ├── __init__.py       # Python 包标记
│   │   ├── apps.py           # Django app 注册配置
│   │   ├── models/           # 身份模型目录
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   └── user.py       # 自定义用户模型
│   │   ├── services/         # 认证相关服务
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── login_service.py   # 登录、登出与会话处理
│   │   │   ├── session_service.py # session/cookie 封装
│   │   │   └── password_service.py# 密码修改与校验
│   │   ├── api/              # 认证接口层
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── urls.py       # 认证路由
│   │   │   ├── views.py      # 认证接口视图
│   │   │   └── serializers.py# 认证接口序列化
│   │   ├── backends/         # Django 认证后端扩展
│   │   │   └── auth_backend.py # 自定义认证逻辑（可选）
│   │   └── migrations/       # 数据库迁移文件
│   │
│   ├── rbac/                 # 授权控制：角色、权限码与访问判断
│   │   ├── __init__.py       # Python 包标记
│   │   ├── apps.py           # Django app 注册配置
│   │   ├── models/           # 权限模型目录
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── role.py       # 角色定义
│   │   │   ├── permission.py # 权限码定义
│   │   │   ├── role_permission.py # 角色-权限关联
│   │   │   └── user_role.py  # 用户-角色关联
│   │   ├── services/         # 授权服务层
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── permission_service.py # 权限判定入口
│   │   │   ├── role_service.py       # 角色管理服务
│   │   │   └── grant_service.py      # 授权/回收服务
│   │   ├── policies/         # 细粒度授权策略
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── base.py       # 策略接口基类
│   │   │   └── registry.py   # 策略注册表（轻量）
│   │   ├── api/              # 权限管理接口层
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── urls.py       # 权限路由
│   │   │   ├── views.py      # 权限接口视图
│   │   │   └── serializers.py# 权限接口序列化
│   │   └── migrations/       # 数据库迁移文件
│   │
│   ├── audit/                # 审计追踪：关键动作留痕
│   │   ├── __init__.py       # Python 包标记
│   │   ├── apps.py           # Django app 注册配置
│   │   ├── models/           # 审计模型目录
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── audit_log.py  # 关键业务审计日志
│   │   │   └── login_log.py  # 登录行为日志
│   │   ├── services/         # 审计服务层
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   └── audit_service.py # 审计写入与查询入口
│   │   ├── hooks/            # 审计扩展点
│   │   │   └── audit_hooks.py# 通用审计 hook
│   │   └── migrations/       # 数据库迁移文件
│   │
│   ├── system_config/        # 系统参数与模块开关
│   │   ├── __init__.py       # Python 包标记
│   │   ├── apps.py           # Django app 注册配置
│   │   ├── models/           # 配置模型目录
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── system_config.py # 键值配置
│   │   │   └── module_switch.py # 模块启停开关
│   │   ├── services/         # 配置服务层
│   │   │   └── config_service.py # 配置读取与写入
│   │   ├── api/              # 配置接口层
│   │   │   ├── urls.py       # 配置路由
│   │   │   └── views.py      # 配置接口视图
│   │   └── migrations/       # 数据库迁移文件
│   │
│   └── support/              # 轻量支撑层：注册、hook、元信息、事件接口
│       ├── __init__.py       # Python 包标记
│       ├── events.py         # 轻量事件发布接口（可选）
│       ├── hooks.py          # Hook 定义与注册工具
│       ├── module_meta.py    # 模块元信息读取
│       └── registry.py       # 固定入口注册器
│
├── apps/                     # 业务模块目录
│   ├── __init__.py           # Python 包标记
│   │
│   ├── customer/             # 客户主数据模块
│   │   ├── __init__.py       # Python 包标记
│   │   ├── apps.py           # Django app 注册配置
│   │   ├── README.md         # 模块说明与边界
│   │   ├── models/           # 客户数据模型目录
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── customer.py   # 客户主档
│   │   │   ├── group.py      # 客户分组
│   │   │   ├── contact.py    # 客户联系人
│   │   │   ├── address.py    # 客户地址
│   │   │   └── credit.py     # 信用额度与账期信息
│   │   ├── selectors/        # 客户查询封装
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   └── customer_selectors.py # 客户查询集合
│   │   ├── services/         # 客户业务服务
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── customer_service.py # 客户主业务入口
│   │   │   └── credit_service.py   # 信用控制逻辑
│   │   ├── permissions.py    # 客户模块权限码定义
│   │   ├── api/              # 客户接口层
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── urls.py       # 客户路由
│   │   │   ├── views.py      # 客户接口视图
│   │   │   ├── serializers.py# 客户序列化定义
│   │   │   └── filters.py    # 客户筛选器
│   │   ├── hooks/            # 客户扩展点
│   │   │   └── customer_hooks.py # 客户模块 hook
│   │   ├── fixtures/         # 初始或测试数据
│   │   ├── migrations/       # 数据库迁移文件
│   │   └── tests/            # 模块测试
│   │
│   ├── material/             # 物料主数据模块
│   │   ├── __init__.py       # Python 包标记
│   │   ├── apps.py           # Django app 注册配置
│   │   ├── README.md         # 模块说明与边界
│   │   ├── models/           # 物料数据模型目录
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── item.py       # 物料主档
│   │   │   ├── category.py   # 物料分类
│   │   │   ├── uom.py        # 计量单位
│   │   │   ├── conversion.py # 单位换算
│   │   │   ├── barcode.py    # 条码信息
│   │   │   └── price.py      # 价格资料
│   │   ├── selectors/        # 物料查询封装
│   │   ├── services/         # 物料业务服务
│   │   │   ├── item_service.py  # 物料主业务入口
│   │   │   └── price_service.py # 价格处理逻辑
│   │   ├── permissions.py    # 物料模块权限码定义
│   │   ├── api/              # 物料接口层
│   │   ├── hooks/            # 物料扩展点
│   │   ├── fixtures/         # 初始或测试数据
│   │   ├── migrations/       # 数据库迁移文件
│   │   └── tests/            # 模块测试
│   │
│   ├── accounting/           # 会计模块（MVP 先做记账核心）
│   │   ├── __init__.py       # Python 包标记
│   │   ├── apps.py           # Django app 注册配置
│   │   ├── README.md         # 模块说明与边界
│   │   ├── models/           # 会计数据模型目录
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── period.py     # 会计期间
│   │   │   ├── account.py    # 会计科目
│   │   │   ├── journal.py    # 凭证主表
│   │   │   ├── journal_item.py # 凭证明细
│   │   │   ├── gl_entry.py   # 总账分录
│   │   │   ├── receivable.py # 应收记录
│   │   │   ├── payable.py    # 应付记录
│   │   │   └── cost_center.py# 成本中心
│   │   ├── states.py         # 会计单据状态定义
│   │   ├── transitions.py    # 会计状态迁移规则
│   │   ├── selectors/        # 会计查询与报表查询
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── journal_selectors.py # 凭证查询
│   │   │   └── report_selectors.py  # 报表查询
│   │   ├── services/         # 会计业务服务
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── journal_service.py   # 建单、修改、作废
│   │   │   ├── flow_service.py      # 提交、确认、付款等动作入口
│   │   │   ├── posting_service.py   # 过账逻辑
│   │   │   ├── reconciliation_service.py # 核销逻辑
│   │   │   ├── aging_service.py     # 账龄分析
│   │   │   ├── cost_service.py      # 成本归集与分摊
│   │   │   └── reporting_service.py # 会计报表服务
│   │   ├── policies/         # 会计细粒度授权策略
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   └── journal_policy.py # 凭证操作策略
│   │   ├── permissions.py    # 会计模块权限码定义
│   │   ├── api/              # 会计接口层
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── urls.py       # 会计路由
│   │   │   ├── views.py      # 会计接口视图
│   │   │   ├── serializers.py# 会计序列化定义
│   │   │   └── filters.py    # 会计筛选器
│   │   ├── hooks/            # 会计扩展点
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── flow_hooks.py # 流转后的扩展动作
│   │   │   └── audit_hooks.py# 会计审计 hook
│   │   ├── handlers/         # 对接其他模块的入账处理
│   │   │   ├── sales_handlers.py    # 销售相关入账处理
│   │   │   ├── purchase_handlers.py # 采购相关入账处理
│   │   │   └── inventory_handlers.py# 库存相关入账处理
│   │   ├── fixtures/         # 初始或测试数据
│   │   ├── migrations/       # 数据库迁移文件
│   │   └── tests/            # 模块测试
│   │
│   ├── sales/                # 销售模块
│   │   ├── __init__.py       # Python 包标记
│   │   ├── apps.py           # Django app 注册配置
│   │   ├── README.md         # 模块说明与边界
│   │   ├── models/           # 销售数据模型目录
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── order.py      # 销售订单主表
│   │   │   ├── order_item.py # 销售订单明细
│   │   │   ├── quotation.py  # 报价单
│   │   │   └── price_list.py # 价格表
│   │   ├── states.py         # 销售单据状态定义
│   │   ├── transitions.py    # 销售状态迁移规则
│   │   ├── selectors/        # 销售查询封装
│   │   ├── services/         # 销售业务服务
│   │   │   ├── sales_order_service.py # 销售主业务入口
│   │   │   ├── flow_service.py        # 销售流转动作入口
│   │   │   └── pricing_service.py     # 定价逻辑
│   │   ├── policies/         # 销售细粒度授权策略
│   │   ├── permissions.py    # 销售模块权限码定义
│   │   ├── api/              # 销售接口层
│   │   ├── hooks/            # 销售扩展点
│   │   ├── handlers/         # 销售对外联动处理
│   │   ├── fixtures/         # 初始或测试数据
│   │   ├── migrations/       # 数据库迁移文件
│   │   └── tests/            # 模块测试
│   │
│   ├── purchase/             # 采购模块
│   │   ├── __init__.py       # Python 包标记
│   │   ├── apps.py           # Django app 注册配置
│   │   ├── README.md         # 模块说明与边界
│   │   ├── models/           # 采购数据模型目录
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── order.py      # 采购订单主表
│   │   │   ├── order_item.py # 采购订单明细
│   │   │   ├── receipt.py    # 采购收货单
│   │   │   └── return_doc.py # 采购退货单
│   │   ├── states.py         # 采购单据状态定义
│   │   ├── transitions.py    # 采购状态迁移规则
│   │   ├── selectors/        # 采购查询封装
│   │   ├── services/         # 采购业务服务
│   │   │   ├── purchase_service.py # 采购主业务入口
│   │   │   └── flow_service.py     # 采购流转动作入口
│   │   ├── policies/         # 采购细粒度授权策略
│   │   ├── permissions.py    # 采购模块权限码定义
│   │   ├── api/              # 采购接口层
│   │   ├── hooks/            # 采购扩展点
│   │   ├── handlers/         # 采购对外联动处理
│   │   ├── fixtures/         # 初始或测试数据
│   │   ├── migrations/       # 数据库迁移文件
│   │   └── tests/            # 模块测试
│   │
│   ├── warehouse/            # 仓储与库存模块
│   │   ├── __init__.py       # Python 包标记
│   │   ├── apps.py           # Django app 注册配置
│   │   ├── README.md         # 模块说明与边界
│   │   ├── models/           # 仓储数据模型目录
│   │   │   ├── __init__.py   # Python 包标记
│   │   │   ├── warehouse.py  # 仓库主档
│   │   │   ├── stock_balance.py # 库存结存
│   │   │   ├── stock_movement.py # 库存移动记录
│   │   │   └── stock_count.py    # 盘点单
│   │   ├── states.py         # 仓储单据状态定义
│   │   ├── transitions.py    # 仓储状态迁移规则
│   │   ├── selectors/        # 仓储查询封装
│   │   ├── services/         # 仓储业务服务
│   │   │   ├── inventory_service.py # 库存主业务入口
│   │   │   ├── movement_service.py  # 出入库与调拨逻辑
│   │   │   └── flow_service.py      # 仓储流转动作入口
│   │   ├── policies/         # 仓储细粒度授权策略
│   │   ├── permissions.py    # 仓储模块权限码定义
│   │   ├── api/              # 仓储接口层
│   │   ├── hooks/            # 仓储扩展点
│   │   ├── handlers/         # 仓储对外联动处理
│   │   ├── fixtures/         # 初始或测试数据
│   │   ├── migrations/       # 数据库迁移文件
│   │   └── tests/            # 模块测试
│   │
│   └── plugs/                # 插件目录：不确定或实验性能力先放这里
│       ├── __init__.py       # Python 包标记
│       ├── print/            # 打印输出插件
│       ├── backup/           # 备份相关插件
│       └── llm/              # LLM 辅助能力插件
│
└── scripts/                  # 运维与开发辅助脚本
    ├── bootstrap_dev.sh      # 初始化开发环境
    ├── load_fixtures.sh      # 导入测试/初始数据
    └── run_checks.sh         # 运行检查、测试与静态校验

```

## 冻结说明

- kernel 作为冻结层，优先保证认证、授权、审计、配置与少量基础设施稳定。
- MVP 先落地 `customer`、`material`、`accounting`，跑真实业务后再决定是否扩大模块。
- `plugs/` 用于承接不确定、实验性、可删除的能力，避免污染 kernel。


## 单用户多公司补充说明（v2 增补）

### 结论

本蓝图默认从“单用户多公司”出发，而不是“多租户多用户”。
因此需要在 `kernel` 中增加 `company` 作为**全局作用域边界**，但不要继续把 `warehouse`、`ledger`、`inventory` 之类业务概念塞进 `kernel`。

### 为什么 `company` 应该进入 kernel

`company` 是所有业务模块都会依赖的稳定边界，至少会影响：

- 当前会话正在操作哪个公司
- 用户对哪些公司有访问权限
- 业务数据归属于哪个公司
- 查询默认在哪个公司范围内执行
- 审计日志属于哪个公司
- 系统配置是否允许按公司覆盖

因此，`company` 适合作为 kernel 的公共基础能力。

### 为什么 `warehouse` 不应该进入 kernel

即便系统支持多仓库，`warehouse` 仍然只是库存领域概念，而不是所有模块的公共基础。
它应该由 `apps/warehouse` 自己维护，包括：

- 仓库主档
- 入库 / 出库 / 调拨 / 盘点
- 当前库存结存
- 库存移动台账

也就是说：

- `company` = 平台级作用域
- `warehouse` = 业务模块能力
- `general ledger` = accounting 模块能力

### 推荐新增目录（最小增补）

在 `kernel/` 下新增：

```text
kernel/
└── company/                 # 公司作用域：单用户多公司边界
    ├── __init__.py
    ├── apps.py
    ├── models/
    │   ├── __init__.py
    │   ├── company.py       # 公司主档
    │   └── user_company.py  # 用户可访问公司关联
    ├── services/
    │   ├── company_service.py       # 公司管理
    │   └── company_context_service.py # 当前公司上下文切换
    ├── api/
    │   ├── urls.py
    │   ├── views.py
    │   └── serializers.py
    └── migrations/
```

### 推荐字段约定

后续关键业务模型默认包含 `company` 归属，例如：

- customer.customer
- material.item
- accounting.period
- accounting.account
- accounting.journal
- accounting.gl_entry
- sales.order
- purchase.order
- warehouse.warehouse
- warehouse.stock_balance
- warehouse.stock_move

但这并不意味着这些概念进入 kernel；只是它们**带有 company 外键**。

### 关于总账和 hook

总账不应该放进 kernel。
正确做法是：

- `apps/accounting` 负责会计期间、科目、凭证、分录、应收应付
- 其他业务模块通过明确的 service / handler 调用触发会计处理
- hook 只作为扩展点，不作为总账归属地

所以，不建议说“总账交给 hook”；更准确的说法是：

- 总账属于 accounting 模块
- hook 只是 accounting 或其他模块在流转后触发的附加动作

### 多仓库的建议（先简单化）

库存先不要做成 ERPNext 那么复杂。
第一阶段建议：

- 一个 company 下允许多个 warehouse
- 不做复杂库位
- 不做批次 / 序列号 / 波次 / 高级预留
- 只支持入库、出库、调拨、盘点

这样既支持多仓库，也不会把 kernel 做胖。

### 架构原则（建议冻结）

1. 只有所有模块都必须依赖、且长期稳定的边界，才进入 kernel。
2. `company` 属于作用域边界，因此进入 kernel。
3. `warehouse`、`inventory`、`ledger` 都属于业务能力，因此留在各自模块。
4. 业务模型可以统一带 `company_id`，但业务概念本身不提升为 kernel 概念。
