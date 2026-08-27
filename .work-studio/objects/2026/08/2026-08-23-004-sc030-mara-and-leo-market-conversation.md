---
schema_version: 1
id: 2026-08-23-004
title: SC030 — Mara and Leo market conversation
type: project
status: active
state: explore
consequence: meaningful
sensitivity: ordinary
domain: [ideation, architecture]
created_at: 2026-08-23T23:17:42Z
updated_at: 2026-08-25T00:11:20Z
next_action: Report V0 tracer outcome (Direction-to-evidence pipeline validated; ws direction --record evidence-format defect) to WO 2026-08-23-001, then route SC030 to outcome review.









---
## Intent

V0 tracer scene for the Director Console. SC030 is a market conversation
between Mara and Leo — Mara tries to hide that she recognizes something,
Leo may already know. This Work Object serves as the first real Scene Object
in the system, testing the 4-layer screenplay structure, the Director Layer
beat table, Direction input, and Scene Board rendering.

## Success evidence

- [x] 4-layer screenplay (Story/Drama/Direction/Realization) written
- [x] Director Layer beat table populated
- [x] At least one Direction typed and structured as evidence
- [x] Scene Board HTML renders this scene correctly
- [x] Decisions section records at least one creative decision

## Constraints and non-goals

**Constraints:**
- This is a tracer — minimal but real. The scene must be genuine enough to
  test the production workflow, not a placeholder.
- All persistence through `tools/ws` CLI.
- Direction objects recorded as `[testimony]` evidence.

**Non-goals:**
- Not producing a finished, polished screenplay — enough to test the system.
- Not building the full hierarchy (Project → Sequence → Scene) yet — that's V1.
- Not rendering in Blender or ComfyUI — that's V3/V4.

## Scene Thesis

- **Thesis:** Mara tries to hide recognition.
- **Turn:** Leo reveals he may already know.
- **Character state:** Mara: controlled → threatened
- **Audience state:** Leo seems unaware → Leo probably knows
- **Directorial rules:** restraint, no melodrama, stillness > gesturing

## Screenplay

### Layer A — Story

A crowded outdoor market. Mara buys fruit from a vendor. Leo approaches
casually, as if they're acquaintances. They exchange pleasantries. Leo
mentions a name — Mara's hand stops. She recovers. Leo watches her recover.
He leaves. Mara stays, pretending to browse.

### Layer B — Drama

Leo is testing whether Mara reacts to the name. Mara's reaction confirms
his suspicion but she doesn't know that. The audience should realize by the
end of the scene that Leo came here specifically to test her — the casual
encounter was staged. The dramatic tension is in what Leo already knows vs.
what Mara thinks he knows.

### Layer C — Direction

The audience should feel the shift from ordinary to dangerous without any
character announcing it. The scene should feel like a normal market
conversation until beat 03, when the name lands. After that, the audience
should notice Mara's control — her effort to seem normal becomes visible.
Leo's ease should feel increasingly deliberate. By beat 06, the audience
should suspect Leo planned this.

### Layer D — Realization

- **Location:** outdoor market, midday, warm light, crowd noise
- **Camera language:** starts wide (market context), tightens as tension
  rises, ends on Mara alone
- **Sound:** market ambience (constant), no score until beat 05 (low drone),
  dialogue always mixed under ambience level
- **Performance register:** naturalistic, understated, physical stillness as
  emotional signal
- **Key prop:** glass of tea (Mara's hands tell the story)

## Director Layer

| Beat | Screenplay | Director Intent | Performance | Production |
|------|-----------|-----------------|-------------|------------|
| 01 | Market establishing. Mara at vendor stall. | Ordinary day. Audience settles into the world. | Mara relaxed, browsing fruit | camera: WS establishing, lens: 35mm, audio: market full |
| 02 | Leo approaches. "Didn't expect to see you here." | Casual encounter. Nothing alarming yet. | Both relaxed, social distance | camera: 2-shot MS, lens: 50mm, audio: market + dialogue |
| 03 | Leo: "I ran into Karim yesterday." Mara's hand stops on the glass. | The name lands. Mara's body betrays her before she can control it. | hand freeze: 0.4s, then controlled recovery, eyes stay on fruit | camera: MCU Mara, lens: 85mm, audio: market drops 3dB |
| 04 | LEO: "You tell me." / Mara looks down. | Leo tests Mara. Audience realizes he suspects her. | gaze delayed, restrained voice, hand remains still | camera: MC Leo, lens: compressed, audio: market ambience |
| 05 | Mara: "Karim. Which Karim?" She picks up an apple. | Mara deflects. The deflection is too controlled — audience sees it. | forced casual, picks up apple as prop business | camera: OTS Leo→Mara, lens: 85mm, audio: low drone begins |
| 06 | Leo smiles. "The one you don't remember." He leaves. | Leo confirms his suspicion. He planned this. | Leo's smile: knowing, not cruel. Turns and walks. | camera: MS Leo exit, lens: 50mm, audio: drone + market |
| 07 | Mara alone. Hand on the glass. Vendor speaks. She doesn't hear. | Aftermath. Mara realizes Leo knows. | frozen stillness, vendor voice inaudible to her | camera: CU Mara's hand on glass, lens: 100mm macro, audio: market fades to room tone |

## Decisions and revisit triggers

### Decision 1 — Adopt the director's Direction: recognition stays understated, protect wide framing and silence, no melodrama

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | SC030 scene treatment — beats 03–07. The recognition beat becomes less obvious; wide framing and silence are protected; melodrama is avoided. This is the creative decision the V0 tracer was built to record. |
| **Authorization** | Director Direction (recorded as [testimony] evidence): "This scene feels too sentimental. Keep the wide framing and silence, but make the recognition less obvious. Avoid melodrama." |
| **Confidence** | medium |
| **Actor** | director |
| **Revisit trigger** | If Scene Board rendering or realization makes the recognition unreadable (too hidden or too obvious), or the scene drifts back into melodrama. |
| **Rationale** | The director's Direction is the first structured Direction recorded against a Scene Object; adopting it exercises the Direction → structured object → evidence recording pipeline while keeping the tracer minimal and genuine. |

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|
| [testimony] | director | Direction (direction): This scene feels too sentimental. Keep the wide framing and silence, but make the recognition less obvious. Avoid melodrama.<br>Protect: wide framing, silence<br>Change: less obvious<br>Avoid: melodrama |
| [system] | system | 4-layer screenplay (Story/Drama/Direction/Realization) written in this object |
| [system] | system | Director Layer beat table populated with 7 beats |
| [system] | system | Scene Board HTML renders this scene (layer tabs + 7-beat table) |
| [testimony] | director | Creative decision recorded: adopt the director's Direction (Decision 1) — recognition understated, protect wide framing and silence, no melodrama |
| [testimony] | director | Direction (direction): Desktop tracer verification: keep the wide market framing and the quiet pause while making the recognition beat less obvious.<br>  Protect: wide market framing, quiet pause while making the recognition beat less obvious<br>  Change: less obvious |
## Open questions

- Whether SC030 belongs to a specific Sequence (SQ01?) — deferred to V1
  when the full hierarchy is built.

## Next move

Report the V0 tracer outcome to WO `2026-08-23-001` (Director Console): the
Direction → structured object → evidence recording pipeline works, with one
defect — `ws direction --record` writes multi-line evidence text that breaks
the Evidence ledger table format. Then route SC030 to outcome review.

## History
### 2026-08-23T23:18:43Z — Activate V0 tracer scene with 4-layer screenplay

- **State:** explore
- **Status:** active
- **Actor:** system
- **Rationale:** V0 tracer scene created with 4-layer screenplay (Story/Drama/Direction/Realization) and 7-beat Director Layer table. Moving to explore to test Direction input pipeline.
### 2026-08-23T23:42:19Z — Reconcile V0 tracer: Direction evidence format fixed, Decision 1 recorded, success checklist completed

- **State:** explore
- **Status:** active
- **Actor:** conductor
- **Rationale:** Director confirmed 'Complete tracer reconciliation': fixed the CLI-generated multi-line Direction evidence row to a valid table row, recorded Decision 1 (adopt the director's Direction), checked the five genuinely-done success items with backing evidence, and aligned next_action. Validation defect in ws direction --record (multi-line text breaks Evidence ledger table) to be reported to WO 2026-08-23-001.

## Relationships

  REL-2026_08_23_004-001:
    type: depends_on
    from: wo:2026-08-23-004
    to: wo:2026-08-24-008
    basis: "V1 tracer Decision 2"
    created_at: 2026-08-25T00:11:20Z
