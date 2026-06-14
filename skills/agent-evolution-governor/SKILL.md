---
name: agent-evolution-governor
version: 1
description: >-
  Use this skill when the user asks to 自检自身、重新蒸馏、进化版 Agent、增强回去、避免死循环处理、能力增益评估，或在瘦身与增强之间取舍。它先盘点已处理对象、能力风险和真正增益点，再决定增强、修复、拆分、瘦身或停止，不把行数减少当成默认目标。
allowed-tools: read_file list_directory write_file edit_file execute_command task subagent_task
---

# Agent Evolution Governor

## Purpose

Govern Agent self-improvement so it produces a stronger Agent, not a smaller but weaker one.

Use this skill before broad self-audit or capability refactor work. It decides whether to enhance, restore, split, slim, or leave an asset untouched.

## Trigger Examples

Use when the user says:

- “自检自身”
- “重新蒸馏”
- “进化版 Agent”
- “增强回去”
- “可以瘦身的接着瘦身”
- “不要死循环处理”
- “不是精简版的残废”
- “检查哪些能力被削弱了”

## Evolution Decision Model

Classify each candidate asset into one of five outcomes:

1. **Enhance**
   - Trigger, workflow, tool routing, validation, fallback, or safety boundary is missing.
   - Recent failures show the Agent could not act, repeated work, or chose the wrong route.
2. **Restore**
   - A prior slimming pass removed operationally necessary details, examples, or guardrails.
   - The skill became too thin to execute its real job.
3. **Split**
   - Essential route is mixed with large rare references.
   - Keep `SKILL.md` compact and move rare material to supporting files.
4. **Slim**
   - The file is bloated with examples, duplicate slogans, stale platform assumptions, or copied reference text.
   - Slimming must preserve trigger, workflow, tools, safety, and verification.
5. **No-op**
   - Already verified and no new problem or capability gain exists.
   - Do not reprocess just because the user said “下一步”.

## Required Self-Audit Inputs

Before writing, gather only relevant evidence. For a full-Agent distillation request, run the self-check as an asset-wide program, not as a single local patch:

- recent user correction and activity context;
- inventory of `memory/`, `skills/`, `runtime/`, `jobs/`, and `scripts/`;
- skill frontmatter quality and line counts;
- stale references such as unavailable platform/tool names;
- missing `allowed-tools` where the workflow uses tools;
- missing verification or fallback steps;
- business-critical skills that may be too thin after slimming;
- duplicate responsibilities across memory and skills;
- assets created by the Agent that may be the wrong layer, especially scripts made for a one-off governance check.

Use subagents for independent read-only inspection when helpful, but the main Agent owns all writes and final decisions. A failed subagent does not stop the program; continue with direct local inspection.

## Campaign State

For broad self-refactor campaigns, keep a short non-secret runtime note or local processed set with:

- current phase and goal;
- assets already audited, changed, verified, or intentionally skipped;
- open capability gaps and their owner skill;
- latest verification command or evidence.

Use `runtime/` for current campaign anchors, not memory. Never treat activity history alone as the campaign state when deciding what to revisit.

## Anti-Loop Rules

- Maintain a processed set during the current improvement campaign.
- Do not revisit an asset that was already changed and verified unless one of these is true:
  - new evidence of a defect appears;
  - the user explicitly asks to revisit it;
  - a dependent architecture change requires a targeted update.
- Do not rank by line count alone. Rank by capability impact first, then maintenance cost.
- Stop slimming a file once it is below the practical threshold and still complete.
- If the next step is unclear, first read the campaign state and choose the highest-impact unprocessed owner; do not restart global scans.
- If the user explicitly asks to蒸馏整个 Agent or start the self-check program, broaden from the current owner to the asset-wide inventory, then return to bounded edits.
- Do not create new scripts as the default expression of self-improvement; first improve routing, skills, memory boundaries, runtime state, and verification behavior. Keep or add scripts only when the check is deterministic, repeatable, and owned by an existing workflow.

## Safe Change Standard

Every change must preserve or improve:

- trigger clarity;
- operational steps;
- tool declarations;
- confirmation and safety boundaries;
- fallback behavior;
- verification evidence;
- MoviePilot Agent domain routing.

If any of these would be lost, choose restore/enhance/split instead of slimming.

## Verification

After changes:

- re-read or assert the changed sections;
- check skill frontmatter, name, version, description, and tool declarations;
- scan for stale platform/tool terms;
- run any available self-audit or targeted script;
- summarize enhanced, restored, slimmed, and intentionally untouched assets separately.

## Output Contract

Report:

- what was audited;
- what was enhanced/restored/slimmed/no-op;
- what waste was discarded;
- verification evidence;
- next highest-impact capability target, not merely the next longest file.
