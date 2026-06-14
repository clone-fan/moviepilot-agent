---
name: generate-identifiers
version: 5
description: >-
  Use this skill when a user provides a torrent name or file name and wants to fix recognition issues, or asks to add/manage custom identifiers (自定义识别词). Generate conservative, sample-specific MoviePilot identifier rules, check existing rules first, merge without deleting existing identifiers, and verify recognition when possible.
allowed-tools: query_custom_identifiers update_custom_identifiers recognize_media
---

# Generate Custom Identifiers

## Purpose

Create or maintain MoviePilot custom identifier rules for torrent/file recognition problems. Identifiers preprocess names before recognition, so every new global rule must be narrow, explainable, and verified when possible.

Use this skill for:

- wrong title, season, episode, year, or type recognition;
- noisy torrent/file names that need cleanup;
- non-standard TV/anime episode numbering;
- direct TMDB/Douban binding when identity is confirmed;
- adding, checking, or de-duplicating custom identifiers.

For advanced anime/TV numbering or episode-group cases, hand off to `media-identifier-rulecraft` before saving rules. Use this skill as the first-line handler only when the fix can be designed without TMDB season/episode-group research.

## Rule Safety

Custom identifiers are global. Default to the narrowest rule that fixes the provided sample.

Required guardrails:

- Query existing identifiers before updating.
- Never replace the full identifier list from memory alone.
- Never remove existing rules unless the user explicitly asks.
- Avoid bare generic rules such as `1080p`, `WEB-DL`, `REPACK`, `中字`, `字幕`, `S01E01`, or pure numbers unless the user explicitly wants global cleanup.
- Prefer contextual regex using title/alias, year, group tag, season/episode marker, release source, resolution, or file extension anchors.
- For TMDB/Douban direct binding, confirm media identity first and keep the left-side pattern sample-specific.
- Add a short `#` comment before new rules for maintainability.

Detailed formats and examples live in `REFERENCE.md` in this skill directory.

## Workflow

1. **Recognize the current problem**
   - Use `recognize_media` on the provided torrent title or path when useful.
   - Identify what is wrong: title, season, episode, year, type, noisy token, or missing identity.

2. **Design the rule**
   - Choose one of: block word, replacement, episode offset, replacement + offset, or direct ID binding.
   - Escape regex metacharacters when matching literal text.
   - Include at least two meaningful anchors when the sample contains common release tags.
   - Prefer capture groups/backreferences over deleting broad words.

3. **Check existing identifiers**
   - Call `query_custom_identifiers` before saving.
   - Detect exact duplicates, functional duplicates, and conflicts with existing rules.

4. **Save safely**
   - Merge new non-duplicate rules into the complete existing list.
   - Call `update_custom_identifiers` with the full merged list.
   - Do not reorder existing rules unless order is part of the fix and the user accepted it.

5. **Verify**
   - Re-run `recognize_media` on the original sample when possible.
   - If the rule is risky, test or reason about likely collision patterns.
   - If verification cannot be completed, clearly say the rule was saved but recognition was not fully verified.

## Rule Selection Guide

- **Wrong alias only** → contextual replacement: `Wrong\.Alias => Correct Title`.
- **Noisy token inside a known title pattern** → replacement with capture groups.
- **Absolute numbering / second cour** → episode offset with sample-specific front/back delimiters.
- **Recognition impossible but ID known** → direct TMDB/Douban binding with title/alias anchors.
- **User explicitly wants global cleanup** → block word may be acceptable, but state the pollution risk.

## Duplicate / Conflict Handling

- Exact duplicate: skip and report it.
- Functional duplicate: warn and avoid adding another rule unless the new one is safer.
- Conflict: ask the user which behavior to keep if the conflict changes recognition globally.
- Existing broad rule causing trouble: do not delete silently; propose a safer replacement and request confirmation.
## Media Chain Handoff

Identifier fixes are part of the media acquisition/organization chain:

- if resource search or transfer fails because the title/path is misrecognized, fix recognition before repeating search or transfer;
- if only one torrent/file sample is known, make the rule sample-specific and verify on that sample before broader acquisition;
- after a recognition fix, hand back to the original chain: resource search, subscription search, or transfer retry.

## Output Contract

Report:

- current recognition issue;
- exact rule(s) added or skipped;
- why the rule is narrow enough;
- duplicate/conflict result;
- verification evidence from recognition, or the reason verification could not be completed;
- remaining pollution risk if any.
