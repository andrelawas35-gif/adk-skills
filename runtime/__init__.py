"""Work Studio local runtime package (Phase 2).

The runtime contract layer lives here, isolated from the canonical CLI writer
(`tools/ws`, which stays dependency-free stdlib). Strict envelope validation
and generated JSON Schema snapshots live under this package; the single source
of enum truth remains `tools/ws/schema.py`.
"""
