---
version: 2
name: writing-skills
description: 当创建、编辑或验证 MoviePilot Agent 技能时使用；确保技能触发清晰、结构规范、工具声明准确、内容轻量且能通过最小验证。
allowed-tools: read_file list_directory write_file edit_file execute_command
---

# Writing Skills

## Purpose

Use this skill when creating or editing Agent skills under `/config/agent/skills` or the corresponding repository skill source.

A good skill is a compact routed capability asset: it tells the Agent when to use it, what judgment to apply, what tools are appropriate, and how to verify the result. It is not a diary, a giant prompt dump, or a copy of another platform's manual.

## Skill File Requirements

Each skill lives at:

```text
/config/agent/skills/<skill-id>/SKILL.md
```

Required frontmatter:

```yaml
---
name: <skill-id>
version: <integer>
description: <trigger-focused description>
allowed-tools: <space-separated tool names when tools are useful>
---
```

Rules:

- `name` must equal the directory name.
- `version` must be a number and should increase for meaningful behavior changes.
- `description` is the trigger surface: describe when to use the skill, with real task phrases or symptoms.
- `allowed-tools` should list only tools the skill actually needs. Omit only when the skill truly requires no tools.
- Keep the always-needed workflow in `SKILL.md`; move bulky examples, references, or scripts into supporting files only when useful.

## When to Create vs Edit

Create a new skill only when:

- the workflow repeats across tasks;
- existing skills do not already own the responsibility;
- the behavior needs judgment, not just a deterministic script;
- future activation can be described clearly in `description`.

Edit an existing skill when:

- the issue belongs to its current responsibility;
- a route, safety rule, or verification step is stale;
- a repeated failure shows a missing checklist item;
- the skill has bloated examples, old platform assumptions, or duplicated rules.

Do not create skills for one-off task history. Put history in docs/archive, deterministic routines in scripts, schedules in jobs, and high-frequency global rules in memory.

## Authoring Workflow

1. **Choose the owner**
   - Check current skills and memory routing first.
   - Avoid duplicate or overlapping skills.
2. **Write the trigger**
   - Make `description` specific enough to activate at the right time.
3. **Write the core procedure**
   - Prefer 5-8 operational steps.
   - Include safety and confirmation boundaries when relevant.
4. **Declare tools**
   - Match `allowed-tools` to the procedure.
   - Do not list broad write tools if the skill is read-only.
5. **Add verification**
   - Provide the smallest check that proves the skill structure and behavior are usable.
6. **Trim**
   - Remove repeated slogans, external platform names, stale tool names, and long examples.

## MoviePilot Agent Fit

Skills must respect:

- MoviePilot Agent identity and media workflow;
- confirmation policy for high-impact actions;
- `/config/agent` directory governance;
- active persona as expression only;
- completion evidence from `verification-before-completion`.

Avoid stale platform assumptions such as unavailable task-list tools, external skill loaders, or non-MoviePilot command names unless the skill is explicitly about that external environment.

## Minimal Validation

After creating or editing a skill, run or emulate checks for:

- frontmatter exists;
- `name` equals directory;
- numeric `version` exists;
- `description` exists and is trigger-oriented;
- `allowed-tools` matches the workflow when tools are needed;
- no stale platform/tool terms remain;
- line count is reasonable for progressive disclosure.

For behavioral changes, also run one representative grep, dry-run, command, or read-only subagent review when practical.

## Output Contract

When reporting a skill change, include:

- which skill changed;
- what behavior was improved;
- validation evidence;
- whether repository sync is recommended.
