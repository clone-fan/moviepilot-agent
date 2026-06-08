---
name: media-identifier-rulecraft
version: 2
description: >-
  Use this skill for advanced MoviePilot/NASTool custom identifier rulecraft when simple generate-identifiers rules are not enough: anime or TV releases with non-standard seasons, absolute episode numbering, TMDB episode groups, noisy bilingual torrent names, conflicting years/resolutions/bit-depth numbers, direct metadata binding, or anti-collision regex design.
allowed-tools: query_custom_identifiers update_custom_identifiers recognize_media search_media query_media_detail query_episode_schedule
---

# Media Identifier Rulecraft

## Purpose

Advanced companion to `generate-identifiers`. Use this skill when a recognition fix needs TMDB season mapping, episode groups, absolute numbering, complex regex anchoring, or collision analysis.

For simple alias cleanup, noisy token removal, ordinary offset, or direct known-ID binding that does not require TMDB season research, route back to `generate-identifiers` and do not over-analyze.

## Advanced Triggers

Use this skill when the sample involves:

- anime seasons that do not match TMDB seasons;
- absolute episode numbering or second-cour offsets;
- specials inserted into main episode order;
- TMDB episode group decisions;
- multiple numeric distractors such as year, resolution, bit depth, source number, or franchise number;
- bilingual/noisy titles requiring defensive regex;
- failed recognition after a simple identifier rule.

## Core Principle

Custom identifiers are global preprocessing rules. Advanced rules must be narrow, identity-aware, and collision-resistant. Prefer confirmed TMDB/Douban binding when text recognition is fragile.

## Identity And Mapping Workflow

1. Confirm media identity with `search_media` or user-provided TMDB/Douban ID.
2. For TV/anime, inspect `query_media_detail` seasons.
3. If episode order is ambiguous, use `query_episode_schedule` or episode group information.
4. Compute mapping explicitly, for example `S03E01 -> TMDB S01E48`, so offset is `EP+47`.
5. Only then design the identifier rule.

## Regex Rulecraft

Use sample-specific anchors:

- title alias or original title;
- year/remake discriminator;
- group/source tag;
- season/episode marker;
- resolution/codec/file extension as boundary, not as broad target.

Patterns:

```text
(?i)Title.*?[Ss]03[Ee] => Clean.Title.{[tmdbid=12345;type=tv]}.S01E && S01E <> 2160p >> EP+47
(?<=Clean\.Title\.S05.*?)2024 => 2020
Title\.S02 => Title.S01 && S01E <> 2024 >> EP+12
```

Avoid broad rules like:

```text
S03E => S01E >> EP+47
```

## Anti-Collision Checklist

Before any `>> EP±N`, make sure the delimiter pair captures the real episode number, not another number.

Check and defend against:

- resolution: `1080p`, `2160p`;
- year: `2020`-`2026`;
- bit depth: `10bit`, `12bit`;
- source or group numbers;
- franchise title numbers;
- multiple episode ranges.

If multiple numeric distractors remain, strengthen anchors or use metadata binding.

## Save And Verify

- Query existing identifiers before saving.
- Skip exact duplicates and warn on functional conflicts.
- Save the full merged list only through `update_custom_identifiers`.
- Verify with `recognize_media` on the original sample.
- For risky offsets, test at least one adjacent episode or likely collision pattern when available.

## Output Requirements

Return:

- confirmed media identity and TMDB/Douban ID if used;
- offset math or episode-group reasoning;
- final rule lines with short `#` comments;
- anti-collision anchors used;
- duplicate/conflict result;
- recognition verification evidence or blocker.

Do not save uncertain TMDB mappings. Ask for a real filename sample or season/episode range when the mapping cannot be proven.
