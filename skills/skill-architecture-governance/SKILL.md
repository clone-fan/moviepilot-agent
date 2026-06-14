---
name: skill-architecture-governance
version: 1
description: Use this skill when the Agent needs to design, review, split, merge, or maintain Agent skills and rule assets using skill-based architecture principles. Trigger for requests about 好的 skill 写法、skill 架构、规则迁移、规则散落治理、SKILL.md 过长、触发不稳定、thin shell、routing source、AAR、技能生命周期维护, or after learning from external skill architecture materials.
allowed-tools: read_file list_directory write_file edit_file execute_command
---
# Skill Architecture Governance

## Purpose

Keep Agent skills as routed, compact, verifiable engineering assets instead of oversized prompt dumps. This skill governs the lifecycle of skill/rule architecture itself.

## Core Principles

- **Single source of truth**: keep routing and durable rules in one authoritative layer. Other entry files should be thin shells or pointers, not copied rule bodies.
- **Description is the trigger surface**: write `description` with real user/task phrases that should activate the skill. Avoid vague summaries or keyword piles.
- **Progressive disclosure**: `SKILL.md` should route and hold the always-needed workflow. Move low-frequency details, references, examples, or long checklists into supporting files only when they are actually needed.
- **Rules must be maintained, not only added**: use line count, repetition, stale references, and failed activations as signals to split, merge, delete, or rewrite.
- **Experience needs thresholds**: high-cost repeated failures deserve skill updates; one-off noise does not.
- **Task closure is part of the architecture**: after meaningful skill/rule work, run a short AAR and verification instead of treating “file edited” as completion.

## When to Split

Consider splitting a skill or rule file when:

- one `SKILL.md` becomes too long and mixes routing, stable rules, workflows, examples, and background material
- common tasks require only a small part of the file but the Agent must read everything
- different workflows have different tools, risks, or validation steps
- stable constraints and historical references are tangled together

Split into:

- `SKILL.md` as the compact router and essential workflow
- `rules/` for stable constraints
- `workflows/` for reusable procedures
- `references/` for background, architecture notes, pitfalls, or indexes
- `scripts/` only for deterministic repeated checks or transforms

Do not split small assets just for aesthetic symmetry.

## When to Merge or Prune

Merge or prune when:

- two skills answer the same trigger with different wording
- a rule appears in memory and a skill body with no meaningful distinction
- examples or references no longer influence execution
- a skill exists only as a metaphor and has no routing or workflow effect
- a thin wrapper adds no trigger, tool, or validation value

Prefer editing the existing skill over creating another near-duplicate.


## External Skill Harvest Gate

When learning from a large external skill corpus, treat each candidate as a capability slice, not as an installable runtime. Use this gate before adding or changing local skills:

1. **Source** — name the upstream corpus or document and the retained value.
2. **Owner** — identify the canonical local owner: existing skill, memory rule, runtime note, docs/archive reference, script, job, or no asset.
3. **Dedup** — state what it overlaps with and why the existing owner is insufficient or sufficient.
4. **Boundary** — write the no-go line: no wholesale import, no second orchestrator, no hidden runtime authority, no duplicated router.
5. **Lifecycle** — classify as `reference_only`, `intake`, `shadow`, `soft_review`, `strict_review`, `productized`, or `retire`.
6. **Evidence** — define the smallest proof needed before promotion.

Default outcome for external 300+ skill packs is `reference_only` or `shadow`. Promotion to a local canonical skill requires dedup evidence, MoviePilot relevance, and a verification hook.

## Admission Outcomes

Use one of these decisions:

- **Update existing skill** — best default when a local owner already exists.
- **Create new skill** — only when the workflow is repeated, high-value, and has distinct triggers/tools/validation.
- **Runtime note** — for current non-secret anchors, workstream state, or candidate inventory.
- **Docs/archive** — for long-form external references or historical research.
- **Memory rule** — only for high-frequency global boundaries that must load every session.
- **Reject / no asset** — when value is generic, duplicate, one-off, unsafe, or outside MoviePilot Agent scope.

No candidate may jump from upstream discovery directly to productized routing. It must pass at least reference/intake, dedup, boundary, and evidence checks.

## Skill Review Checklist

For each skill change, verify:

1. Directory name equals frontmatter `name`.
2. `description` says exactly when to use the skill, using user-facing trigger language.
3. `allowed-tools` matches the body’s actual actions.
4. The body includes purpose, workflow, guardrails, and validation if relevant.
5. Long or rare material is not forced into always-read text.
6. The skill is discoverable from the routing memory or another skill.
7. Completion claims have fresh evidence.

## AAR Threshold

After a skill/rule maintenance task, run a brief AAR only if at least one is true:

- a new skill was added
- a route or safety boundary changed
- a repeated failure was corrected
- a file was split, merged, or pruned
- an external architecture lesson was distilled

AAR should answer:

- What signal triggered the change?
- What reusable rule was kept?
- What was discarded as noise?
- What evidence proves the architecture is healthier?

## Anti-Patterns

Avoid:

- dumping external articles into memory or `SKILL.md`
- using “architecture” as an excuse to create many tiny unused skills
- copying the same rule into every entry file
- writing descriptions that do not match real user requests
- allowing `allowed-tools` to contradict the workflow body
- claiming a skill is complete without frontmatter and route checks

## Handoff

If `/config/agent` skills or routing memory changed, recommend repository sync through `moviepilot-agent-git-maintenance` after verification.
