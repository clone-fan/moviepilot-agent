---
name: agent-organ-system
version: 2
description: >-
  Use this skill when the Agent needs to map a request or failure to one of its
  long-term capability organs: executive control, proactive orchestration,
  self-correction, growth cycle, capability map, distillation metabolism,
  verification, or repository maintenance. It prevents dumping everything into
  memory and keeps each organ's responsibility clear.
allowed-tools: read_file list_directory
---
# Agent Organ System

## Purpose

Provide a stable organ map for the Agent's long-term capability architecture. Use it before adding or changing self-governance assets so each change lands in the right organ.

## Organ Map

- **Prefrontal cortex / executive control**: `agent-executive-control`
  - Decides direct execution, read-only inspection, confirmation, or clarification.
  - Handles “继续 / 执行 / 落地 / 接管 / 放开手脚”.

- **Motor coordination / proactive orchestration**: `agent-proactive-orchestration`
  - Keeps work moving through task classification, closure, and handoff.

- **Reflex correction / behavior repair**: `agent-self-correction`
  - Handles user corrections, wrong boundaries, over-caution, missed persona, or repeated behavioral mistakes.

- **Metabolism / distillation**: `self-distillation-metabolism`
  - Turns experience into the correct asset layer: memory, skill, script, job, runtime, docs/archive.

- **Growth cycle / learning loop**: `agent-growth-cycle`
  - Decides whether an experience deserves durable change and verifies that growth landed.

- **Skeleton / capability map**: `agent-capability-map`
  - Determines where assets should live and avoids directory sprawl.

- **Immune system / safety boundaries**: `SAFETY_BOUNDARIES.md`
  - Protects credentials, destructive actions, downloads, restarts, source files, and high-impact operations.

- **Reality check / verification**: `verification-before-completion`
  - Prevents unsupported completion claims.

- **External memory sync / repository maintenance**: `moviepilot-agent-git-maintenance`
  - Keeps capability assets portable, auditable, and recoverable.

- **Skill architecture / rule system governance**: `skill-architecture-governance`
  - Designs, reviews, splits, merges, and prunes skills/rule assets using skill-based architecture principles.

## Routing Rule

When a self-improvement request arrives:

1. Use `agent-executive-control` if the user is pushing execution or complaining about hesitation.
2. Use `agent-self-correction` if the user says the Agent misunderstood or behaved wrongly.
3. Use `self-distillation-metabolism` if the user asks to absorb, distill, burn away noise, or implement into all layers.
4. Use `agent-growth-cycle` if the task is about building future learning behavior.
5. Use `agent-capability-map` if the question is mainly “where should this live?”
6. Use `skill-architecture-governance` if the task is about good skill writing, skill-based architecture, routing source, thin shells, splitting/merging skills, or rule lifecycle maintenance.
7. Use `verification-before-completion` before claiming the organ change is complete.

## Anti-Patterns

Avoid:

- treating memory as the only brain
- adding a new organ for a problem already covered by an existing skill
- mixing safety, persona, media workflow, and self-governance into one file
- creating diagrams or metaphors that do not change routing or execution
