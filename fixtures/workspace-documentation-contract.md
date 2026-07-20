# Workspace Documentation Contract Behavioral Fixture

## Scenario 1 — Empty workspace bootstrap

Given an empty project and explicit bootstrap authority, the conductor creates
`WORKSPACE-DOCUMENTATION-CONTRACT.md` and its empty registered
`.work-studio/component-ledger.md`. It does not create `CONTEXT.md`, a Work
Object, architecture, test, deployment, or evidence templates.

## Scenario 2 — Docs-only workspace

Given existing documents and no contract, the conductor inspects them, reports
the contract gap, and asks for scoped bootstrap authority. It does not rename,
move, or register those documents automatically.

## Scenario 3 — Code without docs

Given source code and no registered domain context, a specialist reports a
Missing Artifact Gap and recommends the smallest creation. It never claims the
code establishes undocumented project intent.

## Scenario 4 — Missing reference

Given a required registered artifact absent from its canonical location, the
skill inspects the registry, reports the gap, recommends creation, and waits
for scoped authority instead of imitating retrieval.

## Scenario 5 — Conflicting and stale records

Given two conflicting records, the skill compares owner, provenance, freshness,
and canonical status, then surfaces a material conflict for an accountable
decision. It does not pick the newest file or average their claims.

## Scenario 6 — Generated adapter drift

Given a generated adapter that differs from its canonical source, regeneration
follows source validation and drift checking. The adapter is not directly
edited, and cleanup needs separate authority.
