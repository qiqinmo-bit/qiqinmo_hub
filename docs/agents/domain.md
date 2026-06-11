# Domain Docs — Multi-Context

This repo uses a **multi-context** layout. A `CONTEXT-MAP.md` at the repo root points to per-context `CONTEXT.md` files for each subsystem.

## Layout

```
CONTEXT-MAP.md          ← root map pointing to each context
docs/adr/               ← architecture decision records (global)
<subsystem>/CONTEXT.md  ← per-subsystem context
```

## Consumer rules

1. Skills that need domain context (`improve-codebase-architecture`, `diagnose`, `tdd`) first read `CONTEXT-MAP.md` to identify relevant contexts.
2. For a given task, read the `CONTEXT.md` of the subsystem being modified.
3. ADRs live in `docs/adr/` and cover cross-cutting decisions.
