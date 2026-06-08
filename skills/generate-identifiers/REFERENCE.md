# Generate Identifiers Reference

## Rule Formats

Operators must include spaces around them.

1. Block word:

```text
SomeUniqueAlias
```

2. Replacement:

```text
被替换词 => 替换词
被替换词 => {[tmdbid=12345;type=tv;s=1;e=1]}
被替换词 => {[doubanid=xxx;type=movie]}
```

3. Episode offset:

```text
前定位词 <> 后定位词 >> EP-12
```

4. Replacement + episode offset:

```text
被替换词 => 替换词 && 前定位词 <> 后定位词 >> EP-12
```

Comments start with `#`.

## Narrow Rule Examples

Avoid broad global rules:

```text
REPACK
1080p
S01E01 => {[tmdbid=12345;type=tv;s=1;e=1]}
```

Prefer sample-specific rules:

```text
(My\.Show\.2024\.)REPACK(\.1080p) => \1\2
Some\.Weird\.Name(?:\.S01E\d+)?(?:\.1080p)? => {[tmdbid=12345;type=tv;s=1]}
\[Baha\] <> \[1080P\] >> EP-12
OldTitle => NewTitle && \[Baha\] <> \[1080P\] >> EP-12
```

## WordsMatcher Logic

`app/core/meta/words.py` processes custom identifiers in order:

1. Skip empty lines and lines beginning with `#`.
2. Detect combined replacement + offset when ` => `, ` && `, ` >> ` and ` <> ` are all present.
3. Detect replacement when ` => ` is present.
4. Detect episode offset when ` >> ` and ` <> ` are present.
5. Otherwise treat the rule as a block word.
6. Combined rules run replacement first; episode offset applies only when replacement succeeds.
7. Per-subscription `custom_words` takes precedence over global `CustomIdentifiers`.

## Verification Ideas

- Re-run recognition on the original torrent/file sample.
- Test likely collision patterns when the rule contains common release words.
- For TMDB binding, confirm media identity through `search_media` or known user-provided ID before saving.
- If recognition cannot be run, state that the rule was saved but not fully verified.
