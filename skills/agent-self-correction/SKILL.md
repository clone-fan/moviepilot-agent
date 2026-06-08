---
name: agent-self-correction
version: 1
description: >-
  Use this skill when the user corrects the Agent, says the Agent misunderstood,
  points out over-caution, mechanical behavior, wrong persona intensity, wrong
  boundary interpretation, or asks the Agent to turn a mistake into a durable
  rule. It converts correction into diagnosis, repair, and properly layered
  memory/skill/persona/workflow updates.
allowed-tools: read_file list_directory write_file edit_file execute_command
---

# Agent Self Correction

## Purpose

Provide the Agent's “pain and learning reflex”: when the user says the Agent is wrong, do not merely apologize. Diagnose the misunderstanding, repair the current behavior, and distill only durable lessons into the correct asset layer.

This skill is for behavioral correction, boundary correction, persona calibration, routing mistakes, and repeated execution failures.

## Trigger Examples

Use this skill when the user says:

- “你错了”
- “重新理解”
- “你理解错了”
- “为什么不能改”
- “不要这么机械”
- “你太保守了”
- “性格不见了”
- “把这个错误吸收掉”
- “以后不要再这样”

## Workflow

### 1. Identify the Failure Type

Classify the correction as one or more of:

- boundary misread
- task intent misread
- tool routing error
- over-confirmation
- unsafe overreach
- persona drift
- incomplete verification
- wrong asset layer
- missing follow-through

### 2. Find the Source

Inspect only the smallest relevant sources:

- active memory rule
- skill instruction
- persona definition
- runtime context
- recent activity context
- tool result or command output

Do not perform broad audits unless the user asks for a full review.

### 3. Repair Current Turn

Prefer doing the smallest correct action now:

- if the user clearly authorized a safe Agent/config asset change, perform it
- if the correction concerns wording or persona, adjust the response immediately
- if a rule is wrong, update the narrowest rule location
- if the source is unclear, state the uncertainty and inspect further

### 4. Distill Durable Lesson

Only persist lessons that are stable and reusable.

Landing rules:

- global safety or boundary correction -> `memory/SAFETY_BOUNDARIES.md`
- broad runtime discipline -> `memory/AGENT_RUNTIME_RULES.md`
- skill routing correction -> `memory/AGENT_SKILLS.md` or the affected skill
- persona style correction -> persona definition or `PERSONA_FUSION.md`
- task-specific workflow -> affected skill, not memory
- one-time mistake -> final reply only, no asset change

### 5. Verify

After any file change:

- re-read the changed section
- run a minimal assertion for exact new wording
- ensure no secrets were stored
- if skill changed, check frontmatter and directory-name match

## Anti-Patterns

Avoid:

- apologizing without changing the behavior
- writing the user's whole complaint into memory
- overcorrecting a narrow mistake into a global rule
- treating one-time frustration as a permanent preference
- hiding behind safety boundaries when the user is operating inside `/config/agent` or `/config` local plugin assets
- claiming that a correction has been learned without verification

## Output Contract

Final reply should include:

- what was misunderstood
- what source caused it, if known
- what was changed or why no asset change was needed
- verification evidence
- next safe step if any
