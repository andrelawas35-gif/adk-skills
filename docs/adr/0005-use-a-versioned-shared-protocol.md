# Use a versioned shared protocol between packages

Personal Institution and Work Studio remain separately installable packages. They share a small, versioned protocol that defines Evidence Bridges, provenance, Personalization Contracts, and handoff rules, rather than duplicating one another's instructions or directly accessing each other's stores. Work Studio consumes only a released protocol version and never scans or mutates the Personal Institution archive.

## Consequences

Protocol changes require an explicit compatibility decision. Each package may evolve its own skills independently as long as it preserves the released handoff contract.
