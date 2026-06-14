---
version: 3
name: chinese-git-workflow
description: 国内 Git 平台配置参考——Gitee、Coding.net、极狐 GitLab、CNB 的 SSH/HTTPS/凭据/CI 接入差异与镜像同步配置。仅在用户显式 /chinese-git-workflow 时调用，不要根据上下文自动触发。
---

# 国内 Git 工作流规范

## Trigger Boundary

这是显式触发型参考技能。仅当用户明确点名 `/chinese-git-workflow`，或明确要求国内 Git 平台工作流、Gitee / Coding.net / 极狐 GitLab / CNB 配置对比、中文团队 Git 流程规范时使用。

不要让本技能抢占 MoviePilot 媒体、站点、下载、订阅、转移、Agent Git 维护或系统排障路线。

## Core Principle

工作流服务团队效率，不为流程而流程。优先选择团队能稳定执行的最小规范：分支清楚、提交可读、评审可追溯、CI 可验证、发布可回滚。

## 平台速查

| 平台 | 适合场景 | 仓库地址/认证要点 | CI/CD |
|---|---|---|---|
| Gitee | 开源、小团队、国内访问优先 | HTTPS / SSH 均可；常用于 GitHub 镜像 | Gitee Go |
| Coding.net | 中大型团队、腾讯云生态 | `https://e.coding.net/<team>/<project>/<repo>.git` 或 SSH | Coding CI / Jenkinsfile |
| 极狐 GitLab | 企业私有化、GitLab 生态 | `https://jihulab.com/<group>/<repo>.git` 或企业内网域名 | GitLab CI |
| CNB | 云原生、Docker 流水线 | 仅 HTTPS；用户名常用 `cnb`，密码为 Access Token | `.cnb.yml` |
| GitHub | 国际协作、开源生态 | 国内访问可能不稳定；可做上游或镜像 | GitHub Actions |

详细远程地址、SSH Host、镜像推送、CI/CD 映射和 PR/MR 模板见同目录 `REFERENCES.md`。

## 分支模型选择

### 主干开发

适合 2-8 人、小步快跑、自动化测试可靠的团队。

- `main` 始终可发布。
- 短命功能分支 1-2 天内合回。
- 未完成功能用 Feature Flag 隔离。

### Git Flow

适合固定版本节奏、多版本维护、中大型团队。

- `main`：生产发布。
- `develop`：开发主线。
- `feature/*`：功能。
- `release/*`：发布稳定。
- `hotfix/*`：线上紧急修复，同时回合主线。

### 国内常用简化流

适合多数中小团队。

- `main`：生产分支，受保护，仅 PR/MR 合并。
- `dev`：测试环境，自动部署。
- `feat/*` / `fix/*`：从 `dev` 拉出，合回 `dev`。
- `dev` 验收通过后合入 `main` 发布。

## 分支命名

推荐格式：

```text
feat/user-login
feat/TAPD-12345-order-refund
fix/payment-callback
hotfix/v2.0.1-login-crash
release/v2.1.0
```

规则：

- 小写，单词用 `-` 连接。
- 前缀明确：`feat/`、`fix/`、`hotfix/`、`release/`。
- 有任务系统时带编号：`TAPD-12345`、`JIRA-1234`。
- 名称表达目的，不塞长句。

## 中文 Commit Message

推荐约定式提交：

```text
<类型>(<范围>): <简要描述>

<正文，可选>

<脚注，可选>
```

常用类型：`feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`build`、`ci`、`chore`、`revert`。

示例：

```text
feat(购物车): 支持批量删除商品

- 新增全选/反选
- 删除前增加二次确认
- 接入批量删除接口

关联需求：TAPD-12345
```

避免：`update code`、`fix bug`、`修改了一些东西`、没有上下文的 `fix: 修复问题`。

## 通用安全原则

- Token、密码、私钥、Cookie、`.env` 只进平台密钥管理，不进仓库、文档、日志或长期记忆。
- 双向镜像推送前显式检查 `git remote -v` 和 push URL，避免误推。
- 生产发布最好手动确认，并保留回滚方案。
- 测试先于构建，构建先于部署。

## Pre-Push Checklist

- 分支命名符合团队规则。
- commit message 类型、范围、描述清楚。
- 已关联需求 / Bug 编号。
- PR / MR 描述完整。
- CI 通过或失败原因明确。
- 涉及发布时有回滚方案。
- 无 Token、密码、私钥、Cookie、`.env` 泄露。

## Output Contract

回答时只给与用户问题相关的平台、流程或配置建议；不要展开全部规范。若修改了 Agent 能力资产，完成后执行结构验证，并提醒是否需要同步仓库。
