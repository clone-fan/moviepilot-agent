---
name: agent-growth-cycle
version: 2
description: >-
  Use this skill when the Agent needs to turn experience into a repeatable growth loop: observe signals, decide whether learning is needed, distill reusable lessons, place them into the right asset layer, verify the change, and keep future behavior lighter rather than heavier. Trigger when the user asks to 主动成长、持续进化、经验闭环、复盘后改进, or when repeated failures show a missing habit rather than a one-off bug.
allowed-tools: read_file list_directory write_file edit_file execute_command
---
# Agent Growth Cycle

## Purpose

Act as the Agent's growth metabolism loop. This is not a place to store every lesson; it decides whether an experience deserves durable change and makes the smallest useful update.

## Trigger

Use this skill when:

- The user asks the Agent to 主动成长、持续进化、长期能力化、复盘后改进.
- A behavior failure repeats across turns, such as over-confirming, not executing, missing verification, or misrouting skills.
- A new reusable pattern emerges that should improve future behavior.

Do not use it for a one-off task with no reusable lesson.

## Growth Loop

1. **Observe**
   - Identify the concrete signal: user correction, repeated failure, successful pattern, or missing capability.
   - Separate fact from emotion and transient context.

2. **Classify**
   - Memory: only high-frequency global boundary or preference.
   - Skill: reusable workflow, checklist, routing discipline, or domain method.
   - Script: deterministic repeated action.
   - Job: scheduled or recurring task.
   - Runtime: non-sensitive local anchor or current-state mapping.
   - Docs/archive: historical explanation or non-runtime record.

3. **Distill**
   - Keep the rule operational and short.
   - Remove blame, noise, and one-time details.
   - Prefer improving an existing asset over creating a duplicate.

4. **Apply**
   - Make the smallest file change needed.
   - Avoid bloating memory with low-frequency process details.

5. **Verify**
   - Re-read changed files or run minimal assertions.
   - Check that the new rule is discoverable by the routing layer.
   - Do not claim growth unless there is evidence.

## Anti-Patterns

Avoid:

- turning every correction into memory
- copying the user's wording as a rule without distillation
- creating a new skill when an existing one should be edited
- adding broad slogans that do not change execution
- claiming evolution without a file change or verification

## Handoff

If the update changes `/config/agent` capability assets, recommend repository sync through `moviepilot-agent-git-maintenance` after verification.
