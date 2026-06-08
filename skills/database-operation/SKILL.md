---
name: database-operation
version: 5
description: >-
  Use this skill when SQL against the MoviePilot database is needed because
  existing MoviePilot tools cannot answer or fix the request. Applies to raw
  statistics, schema inspection, record repair, cleanup, or maintenance. Prefer
  read-only queries; writes, deletes, cleanup, and batch updates require explicit
  confirmation and fresh verification.
allowed-tools: execute_command read_file
---

# Database Operation

## Purpose

Use SQL only as a fallback when MCP tools, slash commands, plugin tools, or MoviePilot APIs cannot provide the needed state or repair path.

Database access is powerful and risky. The default mode is read-only inspection.

## Safety Rules

- Prefer existing MoviePilot tools before raw SQL.
- Do not expose, store, or echo database passwords, tokens, cookies, or private data.
- Use read-only `SELECT` first to prove the target records and impact.
- Ask explicit confirmation before `UPDATE`, `DELETE`, `INSERT`, cleanup, schema changes, or batch operations.
- For writes, use a transaction when supported and verify affected rows.
- Never run broad writes without a narrow `WHERE` clause and a prior matching `SELECT`.
- Desensitize user-facing results: hide secrets, cookies, tokens, passkeys, and large personal fields.

## Connection Source

Read database type and connection details from `<system_info>`.

Do not write credentials into memory, skills, replies, scripts, or repositories. When composing commands, keep credentials only inside the immediate command environment if required.

## Read-Only Workflow

1. Confirm that SQL is necessary.
2. Identify database type: PostgreSQL or SQLite.
3. Inspect available tables/schema when field names are uncertain.
4. Run the smallest `SELECT` query.
5. Summarize only relevant, desensitized results.

## Write Workflow

Before any write:

1. Run a `SELECT` showing the exact target rows.
2. Explain the intended change and risk.
3. Ask for explicit confirmation.
4. Use a transaction where practical.
5. Verify affected row count and re-query the target rows.
6. Report the verification evidence.

## PostgreSQL Templates

List tables:

```bash
PGPASSWORD='<password>' psql -h <host> -p <port> -U <user> -d <database> \
  -c "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename;"
```

Inspect table:

```bash
PGPASSWORD='<password>' psql -h <host> -p <port> -U <user> -d <database> -c "\d <table>"
```

Read query:

```bash
PGPASSWORD='<password>' psql -h <host> -p <port> -U <user> -d <database> \
  -c "SELECT ... FROM <table> WHERE ... LIMIT 50;"
```

Transactional write pattern:

```sql
BEGIN;
-- SELECT target rows first
-- UPDATE/DELETE with a narrow WHERE clause
-- SELECT target rows again
COMMIT; -- or ROLLBACK;
```

## SQLite Templates

List tables:

```bash
sqlite3 -header -column <DB_PATH> "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
```

Inspect schema:

```bash
sqlite3 <DB_PATH> ".schema <table>"
```

Read query:

```bash
sqlite3 -header -column <DB_PATH> "SELECT ... FROM <table> WHERE ... LIMIT 50;"
```

## Common Read Patterns

Use schema inspection instead of memorizing table fields. Common areas:

- downloads: download history and downloader file records;
- transfers: source, target, status, and error message records;
- subscriptions: state, season, filters, missing episodes, and history;
- sites: site config, user data, statistics, and auth-sensitive fields;
- media server/library: media item mappings and paths;
- config/plugin/workflow/message tables for system state.

Avoid selecting secret-bearing columns unless the user explicitly authorized a narrow diagnostic need; never print raw secret values.

## Verification

A database task is complete only when evidence matches the claim:

- read/statistics task → query output supports the answer;
- write/fix task → affected row count and post-change `SELECT` confirm the exact change;
- cleanup task → before/after counts confirm scope;
- failed query → report the exact SQL/tool error and do not infer results.
