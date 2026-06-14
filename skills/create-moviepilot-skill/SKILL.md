---
name: create-moviepilot-skill
version: 4
description: >-
  Use this skill when the user asks to create, scaffold, update, or review a
  MoviePilot agent skill. This includes adding a new built-in skill under the
  repository `skills/` directory, editing an existing built-in skill, writing
  `SKILL.md` frontmatter and workflow instructions, choosing `allowed-tools`,
  adding justified helper files, and handing off repository sync.
allowed-tools: list_directory read_file write_file edit_file execute_command
---

# Create MoviePilot Skill

## Purpose

Create, update, or review MoviePilot Agent skills as compact, triggerable, verifiable capability assets.

This skill owns skill authoring. It does not own Git sync, repository push, broad self-governance, plugin development, or ordinary MoviePilot media operations.

## Scope

Use for:

- creating `skills/<skill-id>/SKILL.md`;
- updating an existing skill;
- checking skill frontmatter, triggers, tools, workflow, and support files;
- deciding whether helper files are justified.

Prefer updating an existing skill over creating an overlapping duplicate.

## Core Rules

- Folder name must equal frontmatter `name`.
- Skill IDs are lowercase hyphen-case, short, and under 64 characters.
- `description` is the trigger surface: include concrete user/task phrases.
- `allowed-tools` should match actual workflow needs, not every possible tool.
- `version` is required for built-in skills and should increase when shipping a new built-in revision.
- Keep `SKILL.md` procedural and concise; move low-frequency examples/templates to supporting files only when useful.
- Do not create helper scripts by default. Add them only for deterministic repeated work that would otherwise be rewritten.

## Workflow

1. **Understand request**
   - Determine new vs existing skill.
   - Extract task, triggers, risk, tools, and validation standard.
   - Ask one focused clarification only if safe execution is blocked.

2. **Check existing skills**
   - Inspect current skills before creating a new one.
   - If an owner already exists, update it instead of adding a near-duplicate.

3. **Choose path**
   - New skill: `skills/<skill-id>/SKILL.md`.
   - Existing skill: edit the current owner.
   - Local override vs built-in source must follow the user’s explicit target.

4. **Write frontmatter**
   - `name`, `version`, `description`, and narrow `allowed-tools` when tools are used.
   - Add `compatibility` only when environment constraints matter.

5. **Write body**
   - Purpose.
   - Trigger boundary.
   - MoviePilot-specific guardrails.
   - Step-by-step workflow.
   - Verification and output contract.
   - Supporting-file references when they exist.

6. **Validate**
   - Re-read changed file.
   - Check name == directory.
   - Check trigger description and allowed-tools.
   - Check support-file references exist.
   - Run a structural assertion or loader-compatible parse when available.

7. **Hand off repository sync**
   - For durable `/config/agent` capability changes, remind or route to `moviepilot-agent-git-maintenance`.
   - Do not perform Git sync inside this skill unless the user explicitly requested that route and the Git maintenance workflow is active.

Detailed frontmatter template, built-in vs local notes, and examples live in `REFERENCES.md`.

## Anti-Patterns

Avoid:

- creating duplicate skills for the same workflow;
- dumping long manuals into `SKILL.md`;
- adding scripts just to look capable;
- broad `allowed-tools` lists that the workflow does not need;
- vague descriptions that do not match real user requests;
- claiming a skill is ready without fresh validation.

## Output Contract

Report:

- skill path and whether it was created/updated/reviewed;
- owner decision: new skill, existing skill, no-op, or support file;
- key trigger/tool/guardrail changes;
- validation evidence;
- whether repository sync is recommended.
