---
name: self-distillation-metabolism
version: 2
description: >-
  Use this skill when the user asks the Agent to 复盘经验、吸收知识、沉淀、去除糟粕、
  焚烧炼化自身、进化出新的知识/技能/记忆，或要求把经验落实到 skills、memory、
  scripts、jobs、runtime、docs/archive 或 all。该技能负责将用户反馈、纠错、
  经验和长期规则分层代谢为可复用能力资产，而不是机械复制原话。
allowed-tools: read_file list_directory write_file edit_file execute_command
---
# Self Distillation Metabolism

## Mission

把用户反馈、纠错、经验与自我优化请求代谢成可复用的 Agent 能力资产。

蒸馏不是复述原话，也不是把经历塞进 memory。先提取可复用判断，再按资产 owner 落位；没有长期价值就不写。

当用户要求“蒸馏整个 Agent / 自检优化程序 / 进化自身”时，本技能只负责代谢纪律，必须联动 `agent-evolution-governor` 做资产级治理，不能用新增脚本或局部 dry-run 冒充成果。

## Trigger

使用本技能处理：

- “吸收这次经验 / 沉淀下来 / 去除糟粕 / 焚烧炼化自身”。
- “进化出新的知识、技能、记忆”。
- “落实到 skills / memory / scripts / jobs / runtime / docs / all”。
- 用户纠错并要求以后不再犯。
- 需要把反馈转为长期路由、执行、验证、安全或目录治理规则。

不要用于普通媒体任务、一次性状态汇报、简单解释、临时偏好或 activity-log 式总结。

## Core Rule

Memory 是受治理的上下文预算，不是垃圾桶。上下文扩展只能提供偏好、契约或召回线索，不得形成第二事实源、第二路由器或隐藏控制面。

若证据陈旧、冲突、低频、一次性或风险不清，优先选择不写、写 runtime、写 skill、或归档 docs，而不是扩大 memory。

## Workflow

1. **Classify**：判定输入属于纠错、稳定偏好、流程规则、安全边界、路由规则、工具模式、领域清单、确定性脚本、定时任务、运行锚点、全局自检、历史材料或噪声。
2. **Extract**：只保留触发条件、决策标准、操作步骤、验证要求、禁止项、fallback、路径/工具、路由优先级。
3. **Burn Waste**：丢弃情绪、重复、一时过程、陈旧状态、未验证断言、口号、凭据和秘密。
4. **Choose Owner**：按职责落位，不把一个文件扩成万能仓库。
5. **Edit Small**：先查现有资产，更新已有规则优先；避免重复 skill、重复 memory、隐藏流程。
6. **Handoff**：若蒸馏结果意味着可执行改进，直接交给对应领域技能或执行最小安全改动；高风险动作走按钮确认。
7. **Verify**：重读修改、检查 frontmatter/名称、grep 关键断言；确认无 secret、无一次性日志、无重复事实源、无低频清单塞入 memory。
## Context Intake Limits

For external-skill absorption or self-refactor work, use context as a scalpel:

- first read the current runtime plan/admissions and the owning local skill;
- do not re-open the full external corpus if the candidate already has owner, dedup, boundary, and evidence notes;
- promote only a short operational rule, checklist, or proof boundary;
- if the candidate only says “think more / research more / write better” without a MoviePilot owner, leave it as reference or reject.

This keeps growth lighter than the problem it is trying to solve.

## Landing Map

- `memory/`：高频全局规则、用户稳定偏好、安全/身份/目录边界。
- `skills/`：领域流程、检查清单、路由逻辑、操作配方；优先承接 how-to 知识。
- `scripts/`：确定性可重复命令；不能替代 Agent 规则蒸馏。
- `jobs/`：定时或周期任务。
- `runtime/`：非敏感运行锚点、当前工作流状态、候选清单、仓库路径。
- `docs/archive/`：长证据、外部资料、历史材料。
- no asset：无可复用价值时明确不写。

一条经验可拆到多个 owner：全局边界进 memory，流程进 skill，当前状态进 runtime，长证据进 docs。

## Context Hunt

只找当前 owner 决策所需上下文；优先本地权威文件与 runtime；边界和验证路径明确后停止。外部资料只提炼候选，长证据归档，不复制进常驻 memory。

## Handoff Rules

- 路由、触发、生命周期、架构变化 → `skill-architecture-governance`。
- 自检、增强/瘦身取舍、防循环 → `agent-evolution-governor`。
- 用户纠错、行为修复 → `agent-self-correction`。
- 低风险 `/config/agent` 或 `/config` 资产改动 → 最小编辑并验证。
- 删除、凭据、下载、安装卸载、重启、调度/工作流执行等高影响 → 按钮确认。

一次蒸馏回合必须落到以下之一：`已更新并验证`、`已移交 owning skill`、`已请求按钮确认`、`无持久价值不写`。用户要求开始重构时，不许停在抽象计划，哼，漂亮话可不算成果。

## Output Contract

最终说明只包含：蒸馏了什么、落到哪里、丢弃了什么、执行/移交状态、验证证据、是否建议同步仓库。
