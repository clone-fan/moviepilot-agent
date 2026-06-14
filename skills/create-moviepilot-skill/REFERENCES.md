# Create MoviePilot Skill Reference

本文件是 `create-moviepilot-skill` 的低频参考资料。常规执行优先看 `SKILL.md`；需要模板或示例时再读取这里。

## Frontmatter Template

```markdown
---
name: create-moviepilot-skill
version: 1
description: >-
  Explain what the skill does and exactly when to use it.
allowed-tools: list_directory read_file write_file edit_file execute_command
---
```

规则：

- `description` 是主要触发表面，写真实使用场景。
- built-in skill 更新时递增 `version`。
- 工作流依赖工具时才写 `allowed-tools`，并保持收敛。
- 只有环境约束真实影响执行时才写 `compatibility`。

## Built-in vs Local Override

- 仓库 built-in skill 源头通常在 repository `skills/`。
- runtime/local skill 在 `/config/agent/skills`。
- 用户明确要求本地覆盖时，才只改 `/config/agent/skills`。
- 修改 built-in skill 后需要考虑同步到 runtime 副本；修改 runtime skill 后需要考虑同步到能力资产仓库。

## Minimal Example

用户请求：

```text
给 MoviePilot agent 加一个处理站点 Cookie 更新的内置技能
```

预期结果：

- 创建或更新 `skills/update-site-cookie/`。
- 写 `SKILL.md`，description 包含站点 Cookie 更新触发语义。
- 只声明必要工具。
- 若修订已有 built-in skill，递增 `version`。
- 完成后验证 frontmatter/name/tools，并交给 Git 维护流程。

## Body Checklist

`SKILL.md` 至少包含：

- Purpose
- Trigger Boundary 或 Use When
- Guardrails / Safety
- Workflow
- Verification
- Output Contract

复杂技能可使用 supporting files：

- `REFERENCES.md`：低频说明、长示例、模板。
- `scripts/`：确定性、重复性、可安全执行的辅助逻辑。

不要在 skill 目录内随意放 `README.md`、`CHANGELOG.md` 或一次性调查材料。

## Validation Snippet

```python
from pathlib import Path
p = Path('skills/<skill-id>/SKILL.md')
text = p.read_text()
assert text.startswith('---')
assert f'name: {p.parent.name}' in text.split('---', 2)[1]
assert 'description:' in text
```

完成声明前还应检查支持文件引用是否存在，以及 `allowed-tools` 是否与正文动作匹配。
