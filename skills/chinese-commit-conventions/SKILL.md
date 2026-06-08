---
version: 2
name: chinese-commit-conventions
description: 中文 commit 与 changelog 配置参考——Conventional Commits 中文适配、commitlint/husky/commitizen 中文模板、conventional-changelog 中文配置。仅在用户显式 /chinese-commit-conventions 时调用，不要根据上下文自动触发。
---

# 中文 Git 提交规范

## Trigger Boundary

这是显式触发型参考技能。仅当用户明确点名 `/chinese-commit-conventions`，或明确要求中文 commit、Conventional Commits 中文适配、commitlint/husky/commitizen、changelog 配置时使用。

不要让本技能抢占 MoviePilot 媒体、站点、下载、订阅、转移、Agent Git 维护或系统排障路线。

## Core Principle

提交规范的目标是让历史可读、变更可追溯、Changelog 可生成。工具链服务规范，不要为了“格式漂亮”牺牲提交的原子性和真实含义。

## Commit 格式

```text
<type>(<scope>): <subject>

<body>

<footer>
```

中文团队推荐：

- `type` 保留英文，便于工具链识别。
- `scope` 用中文模块名或团队约定英文名。
- `subject` 用中文动宾短语，不加句号。
- `body` 说明背景、方案和影响范围。

示例：

```text
feat(用户模块): 添加手机号一键登录功能

- 接入运营商一键登录 SDK
- 登录失败自动降级到短信验证码

Closes #128
```

## Type 约定

| type | 含义 | 示例场景 |
|---|---|---|
| `feat` | 新功能 | 添加注册模块 |
| `fix` | 缺陷修复 | 修复登录白屏 |
| `docs` | 文档 | 更新 API 文档 |
| `style` | 格式 | 调整缩进，不改逻辑 |
| `refactor` | 重构 | 拆分服务类 |
| `perf` | 性能 | 优化查询速度 |
| `test` | 测试 | 补充单元测试 |
| `build` | 构建/依赖 | 升级构建工具 |
| `ci` | CI/CD | 调整流水线 |
| `chore` | 杂项维护 | 更新脚本、配置 |
| `revert` | 回滚 | 回滚某次提交 |

## Subject 规则

- 必填，建议不超过 50 个中文字符。
- 使用动宾短语：`添加 xxx`、`修复 xxx`、`优化 xxx`。
- 不写空泛描述：`更新代码`、`修复问题`、`改了一些东西`。
- 末尾不加句号。

好的示例：

```text
feat(权限): 添加基于 RBAC 的细粒度权限控制
fix(支付): 修复微信支付回调签名验证失败的问题
perf(列表页): 优化大数据量表格的虚拟滚动渲染
```

## Body 与 Footer

Body 用于说明：

- 为什么改：背景或问题原因。
- 怎么改：方案摘要。
- 影响什么：模块、接口、配置、数据或部署影响。

模板：

```text
<改动背景和原因>

技术方案：
- <方案要点 1>
- <方案要点 2>

影响范围：<受影响模块或服务>
```

Footer 常用于关联 Issue 或标注不兼容变更：

```text
Closes #128
Refs #129
Jira: PROJ-456
禅道: #789
```

## Breaking Change

出现以下情况必须标注：

- 数据库表结构或迁移方式不兼容。
- 公共 API 参数、返回值或状态码不兼容。
- 配置文件格式或必填项变化。
- 运行环境、依赖版本或部署流程不兼容。

格式二选一：

```text
feat(接口)!: 重构用户信息返回结构
```

或：

```text
BREAKING CHANGE: /api/user/info 返回结构变更
- avatar 字段移入 profile 对象
- 移除 nickname，统一使用 displayName
迁移方式：前端同步调整字段路径。
```

## commitlint 中文配置要点

安装：

```bash
npm install -D @commitlint/cli @commitlint/config-conventional husky lint-staged
```

核心配置：

```js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'chore', 'ci', 'revert'
    ]],
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],
    'subject-empty': [2, 'never'],
    'subject-case': [0],
    'subject-max-length': [2, 'always', 100],
    'header-max-length': [2, 'always', 120],
    'body-max-line-length': [1, 'always', 200],
    'footer-max-line-length': [1, 'always', 200]
  }
}
```

Husky 钩子：

```bash
npx husky init
# .husky/commit-msg
npx --no -- commitlint --edit "$1"
# .husky/pre-commit
npx lint-staged
```

commitizen 可选，用于交互式提交：

```bash
npm install -D commitizen cz-conventional-changelog
# package.json scripts: { "commit": "cz" }
```

## Changelog 配置要点

```bash
npm install -D conventional-changelog-cli conventional-changelog-conventionalcommits
```

`package.json`：

```json
{
  "scripts": {
    "changelog": "conventional-changelog -p conventionalcommits -i CHANGELOG.md -s",
    "changelog:all": "conventional-changelog -p conventionalcommits -i CHANGELOG.md -s -r 0"
  }
}
```

中文分组可在 `.versionrc.js` 或 release 工具配置中映射：

```js
module.exports = {
  types: [
    { type: 'feat', section: '新功能' },
    { type: 'fix', section: '缺陷修复' },
    { type: 'perf', section: '性能优化' },
    { type: 'refactor', section: '代码重构' },
    { type: 'docs', section: '文档更新' },
    { type: 'test', section: '测试' },
    { type: 'chore', section: '构建/工具', hidden: true },
    { type: 'ci', section: '持续集成', hidden: true },
    { type: 'style', section: '代码格式', hidden: true }
  ]
}
```

## 团队落地步骤

1. 先统一 type、scope 和 Breaking Change 规则。
2. 配置 commitlint + husky，让规则可执行。
3. 在 README 或 CONTRIBUTING 中写 1 页以内的提交规范。
4. Review 时关注提交是否原子、描述是否真实。
5. 每季度按团队反馈调整规则，避免规范过度复杂。

## 提交前检查清单

- type 是否准确。
- scope 是否能表达影响范围。
- subject 是否清楚、具体、无句号。
- 一次提交是否只做一件事。
- body 是否说明原因、方案和影响。
- Breaking Change 是否已标注迁移方式。
- Issue/需求/Bug 是否已关联。
- 没有把密钥、Token、Cookie、`.env` 写进提交。

## Output Contract

回答时只给与用户请求相关的提交规范或工具配置，不要展开整套手册。若修改了 Agent 能力资产，完成后执行结构验证，并提醒是否需要同步仓库。
