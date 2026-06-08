# Identifier Skill Dispatch

Use this file as the tie-breaker when a recognition-word task could match both `generate-identifiers` and `media-identifier-rulecraft`.

## First-Line Route: generate-identifiers

Use `generate-identifiers` when the request can be solved by normal custom identifier operations:

- simple wrong alias replacement;
- noisy token removal scoped to a known title pattern;
- ordinary episode offset where the target season/episode is clear;
- direct TMDB/Douban binding when the user already provides or confirms the ID;
- checking, adding, de-duplicating, or safely saving global custom identifiers.

## Escalation Route: media-identifier-rulecraft

Escalate to `media-identifier-rulecraft` before saving when any of these appear:

- anime or TV season numbering does not match TMDB;
- absolute episode numbering or second-cour mapping is needed;
- TMDB episode group may be required;
- specials are inserted into the main order;
- years, resolutions, bit depth, franchise numbers, or source numbers can collide with episode parsing;
- bilingual/noisy titles need defensive regex beyond a simple contextual replacement;
- recognition still fails after a normal identifier rule.

## Dispatch Rule

Default to the simplest safe skill. Escalate only when the rule needs media-identity research or collision-resistant mapping. After advanced rulecraft decides the mapping, saving still follows the same safe custom-identifier flow: query existing rules, merge full list, update, then verify recognition.
