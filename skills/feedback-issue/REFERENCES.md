# Feedback Issue Reference

本文件是 `feedback-issue` 的低频脚本与 payload 参考。常规路由优先看 `SKILL.md`；只有明确进入上游 issue 准备流程时再读取这里。

## Required Scripts

从 MoviePilot 仓库根目录运行，使用当前 MoviePilot 环境可用的 `python` 或 `python3`。

```bash
python <skill_dir>/scripts/collect_feedback_diagnostics.py ...
python <skill_dir>/scripts/prepare_feedback_issue.py ...
python <skill_dir>/scripts/submit_feedback_issue.py ...
```

`skill_dir` 使用 Agent skills 列表中的实际路径。如果技能已复制到 runtime config 目录，使用复制后的路径。

## Collect Diagnostics

```bash
python <skill_dir>/scripts/collect_feedback_diagnostics.py \
  --original-user-request "<用户原话>" \
  --keyword "TMDB" \
  --keyword "RecognizeError" \
  --time-window-minutes 30
```

脚本输出 JSON。保留：

- `diagnostics_file`
- `runtime_dir`

如果返回 `success=false` 且 reason 为 `no_explicit_feedback_intent`，停止本技能，回到本地诊断。

## Draft JSON Schema

在 `runtime_dir` 中创建 draft JSON，不要放到仓库源码树。

```json
{
  "title": "[错误报告]: <一句中文症状摘要>",
  "version": "v2.x.x",
  "environment": "Docker",
  "issue_type": "主程序运行问题",
  "description": "## 现象\n- ...\n\n## 复现步骤\n1. ...\n\n## 期望行为\n- ...\n\n## 已定位 / 推测\n- ...\n\n## 已尝试的处理\n- ...",
  "original_user_request": "<用户原话>",
  "diagnostics_file": "<collect 脚本返回的 diagnostics_file>"
}
```

Allowed values:

| Field | Values |
|---|---|
| `environment` | `Docker` / `Windows` |
| `issue_type` | `主程序运行问题` / `插件问题` / `其他问题` |

## Prepare Preview

```bash
python <skill_dir>/scripts/prepare_feedback_issue.py \
  --draft-file "<runtime_dir>/draft.json"
```

成功后读取 `preview_file` 并完整展示给用户。预览包含脱敏后的日志摘录，便于用户检查敏感内容。

确认话术：

```text
请确认以上内容是否提交到 MoviePilot 上游仓库。回复「确认」提交，或回复「修改：...」调整。
```

## Submit

确认后运行：

```bash
python <skill_dir>/scripts/submit_feedback_issue.py \
  --payload-file "<payload_file from prepare>" \
  --username "<current admin username if known>"
```

结果处理：

- `success=true`：返回 `issue_url`。
- `reason=no_token` / `no_permission` / `rate_limited` / `github_unavailable` / `network_error` / `invalid_payload`：返回 `prefill_url`，让用户在 GitHub 完成提交。
- `reason=duplicate` / `rate_limited_user`：不要立即重试。

## Required Before Filing

- Reproduce or inspect local evidence.
- Separate configuration/user-data problems from MoviePilot defects.
- Remove secrets, tokens, cookies, private paths, account details from logs.
- Include version, environment, expected behavior, actual behavior, and minimal reproduction steps.

## Verification

Before claiming an issue draft is ready:

- re-read the generated draft and preview;
- scan logs/snippets for sensitive information;
- confirm target repository and issue type;
- confirm user has explicitly approved submission before running submit.
