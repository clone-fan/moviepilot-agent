# 中文 Commit 工具配置参考

本文件是 `/chinese-commit-conventions` 的低频参考资料。常规回答优先读取 `SKILL.md`，只有用户明确要工具配置模板时再看这里。

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

## 完整示例

```text
feat(用户模块): 添加手机号一键登录功能

- 接入运营商一键登录 SDK
- 登录失败自动降级到短信验证码

Closes #128
```
