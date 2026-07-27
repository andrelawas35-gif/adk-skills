# Slice 2 Behavioral Fixture - Turn Signal into Work

This fixture proves the signal-capture path for `turn-signal-into-work`. It
tests observable preservation, classification, activation, and degradation;
it does not prescribe hidden reasoning.

## Scenario 1 - Capture without activation

**Given**: No matching active Work Object.  
**When**: The user says, "I keep losing context when I switch between client
requests."  
**Then**:

1. The skill preserves the user's language in a concise dated capture.
2. It distinguishes the user report as lived evidence from any inference.
3. It recommends remember or incubate rather than creating a Work Object.
4. It records no full chat transcript, inferred identity claim, or hidden
   reasoning.

**Verification**: The output identifies the signal, provenance, recommended
classification, and a concrete revisit trigger when incubated.

## Scenario 2 - Explicit activation routes through the conductor

**Given**: A captured signal about correcting a product behavior.  
**When**: The user says, "Activate this as a change and start it."  
**Then**:

1. The skill recognizes explicit activation and passes the concise capture to
   `conduct-work-object`.
2. The conductor, rather than this skill, creates or resumes the Work Object.
3. The resulting Work Object preserves the proposed type, consequence,
   sensitivity, evidence, and next action under the shared schema.
4. No implementation, export, or deployment occurs.

**Verification**: The output names the Work Object ID only after the conductor
creates or resumes it and routes to the appropriate next specialist.

## Scenario 3 - Personal context requires a user-approved summary

**Given**: The user says related personal-archive material would help.  
**When**: No user-approved summary or stable reference is supplied.  
**Then**:

1. The skill does not scan, read, or mutate the a personal archive Work Studio does not own.
2. It asks for one user-approved, minimum-necessary user-approved summary or manual
   summary only if the context changes classification.
3. It records provenance and sensitivity if an approved bridge is supplied.

**Verification**: The output identifies the missing evidence as a gap and does
not claim personal-memory retrieval occurred.

## Scenario 4 - Capability degradation

**Given**: The platform classifies inbox writing as manual-fallback or content
search as unsupported.  
**When**: The skill needs that capability.  
**Then**:

1. For manual-fallback, it pauses with one concrete instruction and states
   what remains unverified.
2. For unsupported, it stops the affected retrieval path and records the
   platform limitation.
3. It does not claim the signal was retained, related context was retrieved,
   or activation was completed when the required capability was unavailable.

**Verification**: The output contains the classification (`manual-fallback` or
`unsupported`), one manual action where applicable, and no false success claim.
