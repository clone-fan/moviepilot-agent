---
name: media-identifier-rulecraft
version: 1
description: >-
  Use this skill when generating or reviewing advanced MoviePilot/NASTool custom
  media identifier rules for difficult recognition cases, especially anime or TV
  releases with non-standard seasons, absolute episode numbering, noisy bilingual
  torrent names, conflicting years/resolutions/bit-depth numbers, TMDB binding,
  TMDB episode groups, or defensive regex requirements. This complements
  generate-identifiers with distilled rulecraft patterns for regex anchoring,
  metadata injection, episode offsets, anti-collision checks, and de-duplicated
  output.
allowed-tools: query_custom_identifiers update_custom_identifiers recognize_media search_media query_media_detail query_episode_schedule
---

# Media Identifier Rulecraft

Use this skill to turn messy torrent/file naming patterns into safe MoviePilot custom identifier rules. It is a distilled companion to `generate-identifiers`; use it when the case needs more than a simple alias replacement.

## Core Principle

Custom identifiers are global preprocessing rules. Prefer narrow, defensive, sample-specific rules that fix the provided naming pattern without polluting unrelated media.

## Rule Syntax

Operators require spaces around them.

| Format | Purpose |
|---|---|
| `pattern` | Block/remove a globally safe token |
| `pattern => replacement` | Regex replacement or metadata binding |
| `front <> back >> EP±N` | Episode offset between delimiters |
| `pattern => replacement && front <> back >> EP±N` | Replacement first, then offset only if replacement matched |

Metadata binding targets:

```text
{[tmdbid=12345;type=tv]}
{[tmdbid=12345;type=tv;g=episode_group_id;s=1;e=1]}
{[doubanid=12345;type=movie]}
```

Use TMDB binding for cross-language titles, duplicate names, TMDB season mismatches, and hard scraping failures.

## Regex Rulecraft

Use regex to match the noisy source name while preserving a clean recognition stream.

- Use `.*?` to cross noisy bilingual segments, years, group tags, and quality tags.
- Use `[Ss]\d+[Ee]\d+` or `[Ss]03[Ee]` instead of fixed case season markers.
- Use `(?=.*ADWeb)` or similar positive lookahead to scope a rule to a release group/source.
- Use `(?=.*2024)` to distinguish remakes or same-title releases.
- Use `(?<=Title\.S05.*?)2024 => 2020` only for tightly scoped local year rewriting.
- Escape literal dots and brackets: `Jujutsu\.Kaisen`, `\[Group\]`.

Bad broad pattern:

```text
S03E => S01E >> EP+47
```

Better scoped pattern:

```text
(?i)Jujutsu.*?[Ss]03[Ee] => Jujutsu.Kaisen.{[tmdbid=95479;type=tv]}.S01E && S01E <> 2160p >> EP+47
```

## Episode Offset Mapping

Use offsets when release naming and TMDB episode numbering disagree.

- User season to TMDB absolute season: `S03E01 -> S01E48` means `S03E => S01E >> EP+47`.
- Absolute numbering to split season: subtract the previous episode count, e.g. `EP-12`.
- Special episodes inserted into the main order may require explicit S00 mappings plus range offsets.

Before choosing an offset, verify the real TMDB structure when possible:

1. `search_media` for exact identity.
2. `query_media_detail` for seasons.
3. `query_episode_schedule` when gaps or part breaks decide the mapping.

## Anti-Collision Checklist

Before any `>> EP±N`, inspect the replacement text and likely source name for numeric actors that may be mistaken as episode numbers.

Add defensive exclusions with `&& front <> number` or the correct delimiter pair for:

| Interference | Examples | Defensive pattern |
|---|---|---|
| Resolution | `1080p`, `2160p` | `&& S01E <> 2160p` |
| Year | `2020`, `2024`, `2025`, `2026` | `&& S01E <> 2026` |
| Bit depth | `10bit`, `12bit` | `&& S01E <> 10bit` |
| Other title numbers | franchise years, part numbers | add the narrowest exclusion |

If multiple numbers remain near the episode marker, prefer stronger source anchors or explicit metadata binding.

## Generation Workflow

1. Identify the intended media, TMDB/Douban ID, type, season, and episode mapping.
2. Extract unique anchors from the sample: title alias, original title, year, season/episode marker, group, source, resolution, codec, file extension.
3. Choose the smallest rule format that fixes the issue.
4. If scraping is fragile, inject `{[tmdbid=...;type=...]}` instead of relying on text only.
5. If using `EP±N`, run the anti-collision checklist and add exclusions.
6. Query existing identifiers before saving; skip exact duplicates and warn on functional conflicts.
7. Save the full merged identifier list only through `update_custom_identifiers`.
8. Verify with `recognize_media` when a sample is available.

## Few-Shot Patterns

### Multi-season anime collapsed into TMDB S01

```text
# Jujutsu Kaisen user S03 -> TMDB S01 absolute episodes
咒术回战.*?[Ss]03[Ee] => Jujutsu.Kaisen.{[tmdbid=95479;type=tv]}.S01E && S01E <> 2160p >> EP+47
(?i)Jujutsu.*?[Ss]03[Ee] => Jujutsu.Kaisen.{[tmdbid=95479;type=tv]}.S01E && S01E <> 2160p >> EP+47
```

### Scoped year rewrite for long-running Chinese animation

```text
(?<=Swallowed\.Star\.S04.*?)2023 => 2020
(?<=Swallowed\.Star\.S05.*?)2024 => 2020
Swallowed\.Star\.S04 => Swallowed.Star.S01 && S01 <> 2020 >> EP+85
```

### Specials inserted into main episode order

```text
Ultraman\.Arc\.S01E01 => Ultraman.Arc.S00E01
Ultraman\.Arc\.S01E08 => Ultraman.Arc.S00E02
Ultraman\.Arc\.S01E(0[2-7]) => Ultraman.Arc.S01E\1 && S01 <> 2024 >> EP-1
Ultraman\.Arc\.S01E(09|1[0-7]) => Ultraman.Arc.S01E\1 && S01 <> 2024 >> EP-2
```

### Long alias normalized before season offset

```text
Hazure\.Skill\.Kinomi\.Master\.Skill\.no\.Mi.*?Nitsuite => Kinomi.Master
(?<=Kinomi\.Master\.S02.+?)2025 => 2024
Kinomi\.Master\.S02 => Kinomi.Master.S01 && S01E <> 2024 >> EP+12
```

## Output Requirements

- Return one rule per line, with a short `#` comment before related rules.
- Do not output duplicate rules for the same mapping logic.
- Do not save broad global cleanup rules unless the user explicitly asks.
- Mention the offset math and the anti-collision exclusions used.
- If the TMDB mapping is uncertain, ask for a real filename sample or confirm the season/episode range before saving.
