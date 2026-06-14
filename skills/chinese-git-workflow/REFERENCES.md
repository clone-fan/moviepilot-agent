# 国内 Git 平台配置参考

本文件是 `/chinese-git-workflow` 的低频参考资料。常规回答优先读取 `SKILL.md`，只有用户明确要平台配置、CI 模板或远程命令时再看这里。

## 远程与凭据配置要点

### Gitee

```bash
git remote add origin https://gitee.com/<org>/<repo>.git
# SSH 推荐单独 Host 与 key
# Host gitee.com
#   HostName gitee.com
#   User git
#   IdentityFile ~/.ssh/gitee_ed25519
```

双向镜像推送时，显式检查 push URL，避免误推：

```bash
git remote set-url --add --push origin https://gitee.com/<org>/<repo>.git
git remote set-url --add --push origin https://github.com/<org>/<repo>.git
git remote -v
```

### Coding.net

```bash
git remote add origin https://e.coding.net/<team>/<project>/<repo>.git
git remote add origin git@e.coding.net:<team>/<project>/<repo>.git
```

### 极狐 GitLab

```bash
git remote add origin https://jihulab.com/<group>/<repo>.git
# 企业私有化：
# git remote add origin https://gitlab.yourcompany.com/<group>/<repo>.git
```

### CNB

```bash
git remote add origin https://cnb.cool/<org>/<repo>.git
# HTTPS 认证：用户名 cnb，密码使用个人 Access Token。
```

不要把 Token 写进仓库、文档、日志或长期记忆。

## CI/CD 映射

| 能力 | Gitee Go | Coding CI | 极狐 GitLab CI | CNB |
|---|---|---|---|---|
| 触发 | `triggers` | Jenkinsfile / 平台配置 | `only` / `rules` | `push` / `pull_request` |
| 运行环境 | 平台 step | Jenkins agent | `image` | 每条流水线指定 Docker image |
| 缓存/制品 | cache / artifacts | stash / 制品库 | cache / artifacts | 参考官方配置 |
| 变量/密钥 | 环境变量配置 | 凭据管理 | CI/CD Variables | Access Token / 环境变量 |
| 生产发布 | 手动 / 规则 | 手动阶段 | `when: manual` | 页面或配置触发 |

通用原则：测试先于构建，构建先于部署；生产发布最好手动确认；密钥只进平台密钥管理，不进仓库。

## PR/MR 模板要点

模板应至少包含：

```markdown
## 变更说明
## 变更类型
- [ ] feat
- [ ] fix
- [ ] refactor
- [ ] docs
## 关联需求/Bug
## 影响范围
## 测试方法与结果
## 部署注意事项
## 截图/录屏（如涉及 UI）
```

常见位置：

- Gitee：`.gitee/PULL_REQUEST_TEMPLATE.md`
- GitLab / Coding：`.gitlab/merge_request_templates/default.md`

## 常用本地配置

```bash
git config --global core.quotepath false
git config --global init.defaultBranch main
git config --global pull.rebase false
# 如需 GitHub 代理，按实际环境单独配置，不写入项目仓库。
```

`.gitignore` 至少排除：IDE 目录、依赖目录、构建产物、`.env*`、系统文件、临时文件。
