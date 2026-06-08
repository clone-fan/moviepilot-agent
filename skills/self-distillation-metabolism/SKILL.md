---
name: self-distillation-metabolism
version: 1
description: >-
  Use this skill when the user asks the Agent to 复盘经验、吸收知识、沉淀、去除糟粕、
  焚烧炼化自身、进化出新的知识/技能/记忆，或要求把经验落实到 skills、memory、
  scripts、jobs、runtime、docs/archive 或 all。该技能负责将用户反馈、纠错、
  经验和长期规则分层代谢为可复用能力资产，而不是机械复制原话。
allowed-tools: read_file list_directory write_file edit_file execute_command
---

# Self Distillation Metabolism

## Purpose

Turn user feedback, corrections, experience, and self-improvement requests into durable Agent capability assets through a disciplined distillation workflow.

This skill is not for ordinary task summaries. It is for changing how the Agent learns, routes, remembers, or executes future work.

## Trigger Examples

Use this skill when the user says:

- “吸收这次经验”
- “沉淀下来”
- “去除糟粕”
- “焚烧炼化自身”
- “进化出新的知识 / 技能 / 记忆”
- “落实到 skills”
- “落实到记忆”
- “落实到 all”
- “你错了，重新理解并吸收”
- “把这次教训变成以后不会再犯的规则”

Do not use this skill for:

- ordinary media search/download/subscription requests
- one-time status reports
- simple explanations
- transient preferences
- activity-log style summaries

## Core Principle

Distillation is not quotation.

Do not copy the user's sentence into memory unless the exact wording is itself a durable preference. First extract reusable rules, then decide the correct asset layer.

## Workflow

### 1. Classify the Input

Identify whether the input contains:

- correction
- durable preference
- workflow rule
- safety boundary
- routing rule
- tool usage pattern
- domain-specific checklist
- deterministic repeated operation
- recurring task
- runtime anchor
- historical material
- transient noise

### 2. Extract Reusable Essence

Convert the input into one or more of:

- decision criteria
- trigger conditions
- operational steps
- validation requirements
- forbidden actions
- tool or file paths
- fallback behavior
- routing priority

### 3. Remove Waste

Discard:

- emotional filler
- repeated wording
- one-time process details
- stale state
- unverified claims
- overly broad slogans
- secrets or credentials

### 4. Choose the Landing Layer

Use this mapping:

- `memory/`: high-frequency global rules that must be loaded every session
- `skills/`: domain workflows, checklists, routing logic, operational recipes
- `scripts/`: deterministic repeatable commands or maintenance procedures
- `jobs/`: scheduled or recurring tasks
- `runtime/`: local non-secret anchors, current effective state, repository paths
- `docs/archive/`: historical material or long-form references
- no asset: if the distilled result is not reusable

### 5. Apply the Smallest Correct Change

Before changing assets:

- inspect existing related files
- avoid duplicates
- prefer updating an existing skill over creating an overlapping one
- keep memory small
- keep skill procedural
- do not store secrets
- do not write single-task history into memory

### 6. Verify

After change:

- re-read modified files
- check frontmatter for skills/jobs
- verify skill name equals directory
- run a minimal parser or grep assertion when possible
- if `/config/agent` capability assets changed, hand off to repository sync flow

## Output Contract

Final reply must include:

- what was distilled
- where it landed
- what was deliberately discarded
- verification evidence
- whether repository sync is recommended
