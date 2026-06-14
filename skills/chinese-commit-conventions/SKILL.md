---
version: 3
name: chinese-commit-conventions
description: 中文 commit 与 changelog 配置参考——Conventional Commits 中文适配、commitlint/husky/commitizen 中文模板、conventional-changelog 中文配置。仅在用户显式 /chinese-commit-conventions 时调用，不要根据上下文自动触发。
---

# 中文 Git 提交规范

## Trigger Boundary

这是显式触发型参考技能。仅当用户明确点名 `/chinese-commit-conventions`，或明确要求中文 commit、Conventional Commits 中文适配、commitlint / husky / commitizen、changelog 配置时使用。

不要让本技能抢占 MoviePilot 媒体、站点、下载、订阅、转移、Agent Git 维护或系统排障路线。

## Core Principle

提交规范的目标是让历史可读、变更可追溯、Changelog 可生成。工具链服务规范，不要为了“格式漂亮”牺牲提交的原子性和真实含义。

## Commit Format

```text
<type>(<scope>): <subject>

<body>

<footer>
```

中文团队推荐：

- `type` 保留英文，便于工具链识别。
- `scope` 使用中文模块名或团队约定英文名。
- `subject` 使用中文动宾短语，不加句号。
- `body` 说明背景、方案和影响范围。
- `footer` 关联 Issue、需求、缺陷或 Breaking Change。

常用类型：

| type | 含义 |
|---|---|
| `feat` | 新功能 |
| `fix` | 缺陷修复 |
| `docs` | 文档 |
| `style` | 格式，不改逻辑 |
| `refactor` | 重构 |
| `perf` | 性能优化 |
| `test` | 测试 |
| `build` | 构建或依赖 |
| `ci` | CI/CD |
| `chore` | 杂项维护 |
| `revert` | 回滚 |

## Subject Rules

- 必填，建议不超过 50 个中文字符。
- 使用动宾短语：`添加 xxx`、`修复 xxx`、`优化 xxx`。
- 不写空泛描述：`更新代码`、`修复问题`、`改了一些东西`。
- 末尾不加句号。

示例：

```text
feat(权限): 添加基于 RBAC 的细粒度权限控制
fix(支付): 修复微信支付回调签名验证失败的问题
perf(列表页): 优化大数据量表格的虚拟滚动渲染
```

## Body / Footer / Breaking Change

Body 用于说明：

- 为什么改：背景或问题原因。
- 怎么改：方案摘要。
- 影响什么：模块、接口、配置、数据或部署影响。

Footer 常用于：

```text
Closes #128
Refs #129
Jira: PROJ-456
禅道: #789
```

出现数据库、公共 API、配置格式、运行环境或部署流程不兼容时，必须标注 Breaking Change：

```text
feat(接口)!: 重构用户信息返回结构
```

或：

```text
BREAKING CHANGE: /api/user/info 返回结构变更
迁移方式：前端同步调整字段路径。
```

## Tooling Reference

详细 `commitlint`、`husky`、`commitizen`、`conventional-changelog` 和 `.versionrc.js` 中文分组配置见同目录 `REFERENCES.md`。

使用原则：

1. 先统一 type、scope 和 Breaking Change 规则。
2. 再配置 commitlint + husky，让规则可执行。
3. 在 README 或 CONTRIBUTING 中保持 1 页以内提交规范。
4. Review 时关注提交是否原子、描述是否真实。
5. 每季度按团队反馈调整规则，避免规范过度复杂。

## 提交前检查清单

- type 是否准确。
- scope 是否能表达影响范围。
- subject 是否清楚、具体、无句号。
- 一次提交是否只做一件事。
- body 是否说明原因、方案和影响。
- Breaking Change 是否已标注迁移方式。
- Issue / 需求 / Bug 是否已关联。
- 没有把密钥、Token、Cookie、`.env` 写进提交。

## Output Contract

回答时只给与用户请求相关的提交规范或工具配置，不要展开整套手册。若修改了 Agent 能力资产，完成后执行结构验证，并提醒是否需要同步仓库。
