# API 契约（后端对前端的稳定面）

本文件定义后端 API 的一致性约束，确保模块扩展时接口风格不漂移。

## 技术栈约束

- API 实现框架：DRF（Django REST Framework）

## 路由与版本

- API 前缀：`/api/`
- 模块前缀：`/api/<module>/`
- 版本策略：MVP 阶段不强制版本号；一旦对外发布再引入 `/api/v1/`

## 认证与授权

- 认证：由 `kernel.identity` 统一处理
- 授权：由 `kernel.rbac` 统一处理，权限码由各模块的 `permissions.py` 提供
- 前端约定：后端返回的权限码集合可用于动态菜单与按钮显隐

## 统一响应结构

推荐固定 envelope：

```json
{
  "success": true,
  "code": "OK",
  "message": "",
  "data": {}
}
```

错误返回：

```json
{
  "success": false,
  "code": "VALIDATION_ERROR",
  "message": "field x is required",
  "data": null
}
```

约束：

- `code` 为稳定机器可读错误码，禁止仅依赖 message 文案
- `message` 为面向用户的可读信息，允许本地化
- `data` 为 payload；失败时建议为 null

## 分页与过滤

列表接口统一支持：

- `page`：从 1 开始
- `page_size`：默认 20，最大值由后端限制
- `ordering`：字段名列表，支持 `-field` 表示倒序

返回建议包含：

```json
{
  "success": true,
  "code": "OK",
  "message": "",
  "data": {
    "items": [],
    "page": 1,
    "page_size": 20,
    "total": 0
  }
}
```

## 错误码建议（MVP 最小集）

- OK
- VALIDATION_ERROR
- UNAUTHORIZED
- FORBIDDEN
- NOT_FOUND
- CONFLICT
- INTERNAL_ERROR

各模块可在此基础上扩展业务错误码，但必须文档化到对应 module_guide 中。

## 幂等与并发

- 写接口如需幂等，约定 `Idempotency-Key` 请求头
- 并发冲突建议用资源版本号（例如 `version` 字段或 `updated_at`）实现乐观锁
