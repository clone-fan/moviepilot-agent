---
name: media-identifier-rulecraft
version: 3
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
- publisher/release-group season labels that differ from TMDB seasons;
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

## Rule Formats

MoviePilot custom identifiers support four practical formats. Operators must have spaces around them.

1. **Block word** — remove matched text:

   ```text
   NoisyToken
   ```

2. **Replacement** — regex replacement:

   ```text
   Wrong\.Title => Correct.Title
   ```

3. **Episode offset** — modify episode number between delimiters:

   ```text
   S01E <> 1080p >> EP+13
   ```

4. **Combined rule** — replacement first, then offset:

   ```text
   Wrong\.S02E(?=.*Group) => Correct.S01E && S01E <> 1080p >> EP+13
   ```

Comment convention for maintainability:

```text
#作品名 Sxx【发布组】
```

## Regex Rulecraft

Use sample-specific anchors:

- title alias or original title;
- year/remake discriminator;
- release group/source tag;
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

## Worked Example: Jigokuraku / Hell's Paradise S02 Label

Scenario: torrent name says release-group `S02E01`, but TMDB has season 1 continuing to episode 25, so the real target is `S01E14`.

Sample:

```text
Jigokuraku.S02E01.2026.1080p.CR.WEB-DL.x264.AAC-ADWeb
```

Verification steps:

```text
search_media(title="Jigokuraku", media_type="tv")
query_media_detail(tmdb_id=117465, media_type="tv")
```

Mapping:

```text
S02E01 -> S01E14, so offset is EP+13
S02E02 -> S01E15
```

Narrow rule:

```text
#地狱乐 S02【ADWeb】
Jigokuraku.S02E(?=.*ADWeb) => Jigokuraku.S01E && S01E <> 1080p >> EP+13
```

Then save through `update_custom_identifiers` after querying existing identifiers, and verify:

```text
recognize_media(title="Jigokuraku.S02E01.2026.1080p.CR.WEB-DL.x264.AAC-ADWeb")
```

Expected effect: `S02E01 -> S01E14`; adjacent episodes continue by the same offset.

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

## Acquisition Chain Guard

For anime/TV releases, do not let resource pressure force unsafe global identifiers:

- confirm season/episode mapping before subscription or transfer retry uses the rule;
- if TMDB episode grouping is uncertain, pause identifier saving and continue with explicit media identity only when possible;
- after a rule is verified, re-run the original recognition/search/transfer step once instead of restarting the full media workflow.

## Output Requirements

Return:

- confirmed media identity and TMDB/Douban ID if used;
- offset math or episode-group reasoning;
- final rule lines with short `#` comments;
- anti-collision anchors used;
- duplicate/conflict result;
- recognition verification evidence or blocker.

Do not save uncertain TMDB mappings. Ask for a real filename sample or season/episode range when the mapping cannot be proven.
