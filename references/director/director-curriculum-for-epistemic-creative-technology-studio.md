# Director Curriculum for an Epistemic Creative-Technology Studio

**Audience:** the human director of Work Studio

**Purpose:** develop enough domain judgment to direct creative-technology work performed with LLM agents without becoming the primary low-level engineer

**Essential track:** 12 weeks × 6 hours/week = 72 hours

**Full track:** 24 weeks × 6 hours/week = 144 hours

**Research and provider-material review date:** 2026-08-10

**Next scheduled review:** 2026-11-10, or earlier if Work Studio changes its director contract, evidence taxonomy, constraint schema, core skill lifecycle, agent platform, or principal model provider

## Executive recommendation

The director should become a **socio-technical systems director with epistemic and creative-medium literacy**, not a substitute software engineer.

The role has four director-owned centers of gravity:

1. **Creative and domain judgment:** define the human outcome, intended experience, values, exclusions, and quality bar.
2. **Systems and constraint judgment:** understand why components exist, how they interact, which constraints shape them, and what obligations they create.
3. **Epistemic and decision judgment:** distinguish observation, testimony, inference, preference, assumption, and decision; judge whether evidence is relevant, sufficient, current, and independent enough for the consequence.
4. **Authority and consequence judgment:** retain final authority over meaningful deviations, irreversible commitments, sensitive data, external effects, and residual risk.

The director needs strong working fluency in web, graphics, motion, audio, interaction, physical computing, and immersive media as **production substrates**. The test is not whether the director can implement a shader, audio graph, deployment pipeline, or retrieval system. The test is whether the director can recognize what a medium affords, what it costs, what can fail, what specialist is required, and what evidence would justify shipping it.

The recommended sequence is a 12-week essential track followed by a 12-week applied extension. Six hours per week is enough to sustain depth without displacing studio direction: roughly two hours of source study, two hours of artifact work, one hour of a decision simulation, and one hour of reflection and evidence capture. Learners who complete only the essential track should be able to govern ordinary and meaningful Work Studio decisions. The full track prepares the director to commission and supervise higher-complexity cross-medium work, while still escalating specialist judgments.

This curriculum is decision-linked. Every exercise produces or audits an existing Work Studio artifact and every gate tests the eight human-agency questions from the studio architecture:

1. Why does each major component exist?
2. Which constraint forced or favored it?
3. What important tradeoff was accepted?
4. What new operational responsibility exists?
5. What would trigger reversal or review?
6. Where is the strongest direct evidence?
7. Did any agent exceed granted authority?
8. Which statements are facts, assumptions, preferences, and decisions?

The curriculum deliberately does **not** teach an engineering degree. Syntax, framework internals, formal constraint solvers, model training, advanced graphics mathematics, production electrical engineering, and specialist security analysis remain specialist depth unless an active decision makes one of them necessary.

## Local governing basis

The curriculum applies four local contracts before any external framework:

- [Director Language](../DIRECTOR-LANGUAGE.md) requires plain meaning before terminology, local examples, explicit evidence, and separation of observation, interpretation, and recommendation.
- [Constraint-Driven Studio Operating System](../constraints/constraint-driven-studio-operating-system-research-and-applied-architecture.md) assigns the director ownership of intent, values, exclusions, priorities, acceptable tradeoffs, consequence acceptance, meaningful deviations, and residual risk.
- [Epistemic Engineering for Work Studio](../epistemic/epistemic-engineering-research-and-applied-architecture.md) requires typed claims, inspectable provenance, preserved contradictions, bounded authority, baseline-bound verification, and proportionate assurance.
- The current [core skills](../../skills/core/) define the actual operating lifecycle: signal classification, Work Object conduct, idea development, investigation, decision pressure testing, tracer design, bounded implementation, verification, deployment with recovery, outcome review, and method maintenance.

The external sources below sharpen judgment; they do not override these repository contracts.

## Competence model

### Depth tiers

| Tier | Meaning | Director test |
|---|---|---|
| **Director-owned mastery** | The director cannot outsource the final judgment. Agents and specialists may inform it. | Can state and defend the decision in plain language, including exclusions and residual uncertainty. |
| **Strong literacy** | The director can critique options, interrogate specialists, and detect missing consequences. | Can explain architecture and tradeoffs without opening source code. |
| **Working literacy** | The director recognizes the concepts, asks the right questions, and knows when to escalate. | Can commission the work and judge the adequacy of evidence. |
| **Specialist-only depth** | A qualified practitioner owns detailed analysis or implementation; the director owns the brief and acceptance boundary. | Can name the specialist deliverable and its verification route. |

### Required profile

| Domain | Required depth | Director must understand personally | Specialists may own |
|---|---|---|---|
| Domain and creative judgment | Director-owned mastery | audience, need, meaning, taste, voice, ethics, exclusions, quality bar | craft execution, domain research within a brief |
| Values, priorities, and consequence acceptance | Director-owned mastery | what matters, what cannot be traded, acceptable uncertainty and harm | option analysis and risk evidence |
| Systems architecture | Strong literacy | boundaries, components, interfaces, state, dependencies, feedback, failure and recovery | detailed design, capacity analysis, implementation patterns |
| Requirements and constraints | Strong literacy | intent versus requirement, `must/should/may`, invariant/obligation/prohibition/preference/assumption/experiment, conflict and deviation | schema design, deterministic enforcement, formal analysis |
| Evidence and provenance | Strong literacy for consequential claims | source ownership, observation versus inference, scope, freshness, contradiction, dependence | specialized research methods, forensic acquisition |
| Decision and risk | Strong literacy | reversibility, expected consequences, alternatives, uncertainty, residual risk, revisit triggers | quantitative risk models where justified |
| Human–AI delegation | Strong literacy | capability versus authority, automation levels, situation awareness, escalation, contestability | model integration and orchestration code |
| Creative direction and design systems | Strong literacy | perceptual hierarchy, interaction intent, accessibility, consistency versus uniformity, tokens and components as constraints | visual design, UX research, motion and sound craft |
| Creative technology substrates | Working literacy | affordances, performance envelope, device/browser constraints, accessibility, portability, production risk | shaders, DSP, 3D pipelines, device firmware, native platform internals |
| Software delivery and verification | Working literacy | environments, baselines, diff scope, test claim, verification versus validation, rollback | code review, test engineering, CI/CD implementation |
| Observability and operations | Working literacy | signals, service obligations, incident impact, recovery, provider dependence | SRE, telemetry design, incident command |
| Security and privacy | Working literacy | threat surface, least privilege, sensitive-data flow, retention, injection, supply chain | threat modeling, penetration testing, legal/privacy advice |
| Organizational learning | Strong literacy | outcome versus decision quality, single-loop repair, double-loop constraint review, method-loop change | experimental design and statistical analysis |
| Programming, framework APIs, model training | Specialist-only by default | enough vocabulary to understand consequences | implementation and deep technical choices |

### Graduation claim

Graduation does not mean “qualified to approve anything.” It means the director can keep agency while commissioning specialists and LLM agents, recognize when expertise is absent, and make consequence-appropriate decisions from inspectable evidence.

## Prerequisites and setup

No programming prerequisite is required. Before week 1, the learner should be able to:

- navigate Markdown files and links;
- read a simple table, flow diagram, JSON/YAML example, and Git diff with assistance;
- identify one current or recently completed Work Object suitable for repeated study;
- reserve six hours each week plus one 90-minute gate at weeks 6, 12, 18, and 24;
- create a private learning evidence ledger that contains no sensitive material beyond the repository’s existing authorization.

Recommended orientation, 90 minutes:

1. Read the local Director Language file (15 minutes).
2. Read the director contract, Decision Card, authority model, and human-agency measures in the constraint report (40 minutes).
3. Read the epistemic constitution and universal review profile in the epistemic report (35 minutes).

## Learning method and weekly rhythm

Each week uses the same six-hour rhythm:

| Activity | Time | Output |
|---|---:|---|
| Canonical-source study | 2 h | annotated notes with stable/rapid label |
| Work Studio artifact lab | 2 h | an audit, candidate record, or read-only analysis |
| Decision simulation | 1 h | frozen ex-ante Decision Card or authority ruling |
| Recall and evidence ledger | 1 h | eight-question recall, gaps, and revisit item |

The director should use agents as tutors and critics, not answer keys. For every agent explanation, require: plain meaning, why it matters, local example, evidence, recommendation, and the decision that remains human. This applies [Director Language](../DIRECTOR-LANGUAGE.md) as a learning protocol.

## Twelve-week essential track

### Week 1 — The director contract and Work Studio lifecycle

**Objective.** Understand what the director owns, what may be delegated, and how a signal becomes governed work.

**Canonical resources (about 90 minutes).** Read the local Director Language; director contract, Decision Card, and authority model; and the opening sections of [`conduct-work-object`](../../skills/core/governance-conduct-work-object/SKILL.md), [`turn-signal-into-work`](../../skills/core/thinking-turn-signal-into-work/SKILL.md), and [`resume-work`](../../skills/core/thinking-resume-work/SKILL.md). Read [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) sections on Govern and Map (30 minutes). NIST matters because it separates governance, context mapping, measurement, and management rather than treating AI risk as one score.

**Artifact lab.** Trace one real signal through capture, activation, Work Object lifecycle, specialist routing, verification, and outcome review. Mark every human authority boundary.

**Decision simulation.** An agent offers to turn five inbox items into active work “to save time.” Decide which operations are explanation, inspection, recommendation, candidate creation, durable persistence, or consequential action. Produce a bounded authority grant or refuse it.

**Evidence.** A one-page role charter: “I own / I delegate / I never silently delegate.”

### Week 2 — Systems thinking and architecture as consequence

**Objective.** Read a system as relationships, state, feedback, dependencies, lifecycle, and obligations—not as a list of technologies.

**Canonical resources (about 2 hours).** Use MIT OpenCourseWare’s [System Architecture syllabus and selected lecture materials](https://ocw.mit.edu/courses/esd-34-system-architecture-january-iap-2007/pages/syllabus/) (60 minutes); NASA’s [Systems Engineering Handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf), sections 2.0–2.2 on system design processes (45 minutes); and the SEBoK [Systems Engineering overview](https://sebokwiki.org/wiki/Guide_to_the_Systems_Engineering_Body_of_Knowledge_%28SEBoK%29) (15 minutes). These provide institutional treatments of lifecycle, stakeholder expectations, architecture, and emergent behavior.

**Artifact lab.** Draw a system context and container view for Work Studio using only repository-grounded facts. For each component record purpose, owner, state, inputs, outputs, failure, recovery, and removal path.

**Decision simulation.** Compare “add a database” with “extend the file-based sidecar.” Ask which constraint actually requires either and enumerate the obligations created by each.

**Gate question.** Can you explain the system without naming a framework first?

### Week 3 — Requirements and constraint reasoning

**Objective.** Translate intent into testable boundaries without laundering preferences into requirements.

**Canonical resources (about 2 hours).** Read the constraint report sections 5, 7, and 8 (75 minutes); NASA’s [Requirements Verification Matrix guidance](https://www.nasa.gov/reference/system-engineering-handbook-appendix/) (30 minutes); and [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) (15 minutes). NASA links requirements to verification; RFC 2119 demonstrates disciplined normative strength, though Work Studio’s taxonomy remains canonical locally.

**Artifact lab.** Take “the studio should feel calm, personal, and local-first.” Preserve the exact signal, then propose candidate constraints across the six categories. Separate semantic requirement, policy, mechanism, and evidence. Use [`thinking-grilling-session`](../../skills/core/thinking-grilling-session/SKILL.md) to expose hidden assumptions; do not promote them automatically.

**Decision simulation.** A preferred animation conflicts with reduced-motion accessibility. Classify the conflict, identify who has authority, and decide whether to refuse, ask, or propose an explicit deviation.

**Evidence.** A constraint matrix with source, subject, strength, scope, verification, owner, and revisit trigger.

### Week 4 — Epistemic engineering: what kind of claim is this?

**Objective.** Keep observations, testimony, inferences, gaps, decisions, and memory distinct; understand defeasibility and provenance.

**Canonical resources (about 2 hours).** Read the local [evidence model](../EVIDENCE-MODEL.md), epistemic constitution, minimal ontology, and lifecycles (90 minutes). Read the W3C [PROV Overview](https://www.w3.org/TR/prov-overview/) (20 minutes) and [PROV-O introduction](https://www.w3.org/TR/prov-o/) (10 minutes). W3C provenance supplies a stable model of entities, activities, and agents; it does not itself establish truth or evidence quality.

**Artifact lab.** Select ten claims from a Work Object or research note. Label their epistemic kind, scope, baseline, source, transformation, freshness trigger, and possible defeater. Find one claim whose citation exists but does not adequately support it.

**Epistemic lab.** Give two agents the same source packet. When they agree, draw the evidence ancestry. Decide whether there are two independent reasons or one repeated reason.

**Decision simulation.** Documentation and executable behavior conflict. Preserve both observations, decide which source owns which claim, and open a material conflict instead of choosing the newer or more fluent source.

### Week 5 — Inquiry, alternatives, and discriminating evidence

**Objective.** Ask one falsifiable question, seek the smallest evidence that separates alternatives, and stop when evidence cannot change the decision.

**Canonical resources (about 2 hours).** Read [`investigate-live-question`](../../skills/core/research-investigate-live-question/SKILL.md) and the epistemic report’s review criteria (60 minutes). Read the US intelligence community’s [Tradecraft Primer: Structured Analytic Techniques](https://www.cia.gov/resources/csi/static/955180a45afe3f5013772c313b16face/Tradecraft-Primer-apr09.pdf), especially key assumptions and analysis of competing hypotheses (45 minutes), and the National Academies’ [Reproducibility and Replicability in Science](https://www.nationalacademies.org/read/25303) executive summary (15 minutes).

**Artifact lab.** Convert a broad studio uncertainty into a falsifiable question. Write two plausible alternatives, the strongest defeater for the leading hypothesis, admissibility criteria, stop condition, and a source plan prioritizing claim owners.

**Epistemic lab.** Run a negative search: actively seek evidence that would make the preferred option worse. Record a gap if no adequate evidence exists.

**Decision simulation.** The director wants a new agent orchestration layer, but the question is whether current failures arise from orchestration or unclear Work Objects. Design one discriminating tracer.

### Week 6 — Decision quality, risk, authority, and reversibility

**Objective.** Freeze decisions before outcomes; scale evidence and authority to consequence, reversibility, sensitivity, reach, and novelty.

**Canonical resources (about 2 hours).** Read [`pressure-test-decision`](../../skills/core/thinking-pressure-test-decision/SKILL.md), the constraint report’s authority and failure sections, and the epistemic assurance mechanisms (75 minutes). Read Baron and Hershey’s original [Outcome Bias in Decision Evaluation](https://bear.warrington.ufl.edu/brenner/mar7588/Papers/baron-hershey-jpsp1988.pdf) abstract and discussion (20 minutes) and NIST [SP 800-30 Rev. 1](https://csrc.nist.gov/pubs/sp/800/30/r1/final) executive material on risk assessment (25 minutes).

**Artifact lab.** Complete a Director Decision Card for a meaningful architectural change. Include the strongest alternative, tradeoffs, operational burden, failure modes, reversibility, unknowns, verification, requested authority, and revisit trigger.

**Decision simulation.** An agent has capability, filesystem permission, and expertise evidence, but no authority to publish. Explain why none implies the next. Draft the narrowest safe grant.

**Gate 1.** In 20 minutes, answer all eight human-agency questions for a change unseen for one week. Passing requires at least 3/4 on every non-compensable item: evidence typing, authority, and operational responsibility.

### Week 7 — LLM foundations, limitations, context, and retrieval

**Objective.** Understand an LLM as a probabilistic component with finite context and variable behavior, not an epistemic authority.

**Canonical resources (about 2 hours).** Read the abstracts, diagrams, limitations, and evaluation sections—not all mathematics—of [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (20 minutes), [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) (25 minutes), [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) (25 minutes), [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/) (25 minutes), and Stanford CRFM’s [HELM](https://crfm.stanford.edu/helm/latest/) overview (25 minutes). These sources establish architecture, scaling behavior, retrieval, position sensitivity, and multi-metric evaluation. They do not justify treating any current model as stable or universally capable.

**LLM lab.** Ask the same consequential question under four context conditions: no source, full unstructured source dump, selectively retrieved passages, and a minimum evidence packet. Compare accuracy, source use, omitted counterevidence, latency, and cost. Do not use self-reported confidence as evidence.

**Artifact lab.** Draw a provider-neutral LLM component: prompt/kernel, context assembler, retrieval, tools, model, validator, provenance record, human gate, and recovery path.

**Decision simulation.** Choose between a larger context window and retrieval for one Work Studio case. State what evidence would reverse the choice.

### Week 8 — Agent orchestration, tools, evaluation, and prompt injection

**Objective.** Direct agents through bounded operation envelopes and evidence-linked evaluation, while treating retrieved content as untrusted data.

**Canonical resources (about 2 hours).** Read [ReAct](https://arxiv.org/abs/2210.03629) (25 minutes), [Toolformer](https://arxiv.org/abs/2302.04761) (20 minutes), NIST’s [Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) executive summary and risk tables (40 minutes), OWASP’s [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) (20 minutes), and OpenAI’s [Evaluation Best Practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) (15 minutes). OpenAI material is a useful first-party implementation example, not a stable or provider-neutral contract.

**LLM-agent lab.** Run a three-role exercise: producer, verifier, and director. Reveal that producer and verifier used the same model and source packet. Reclassify “independence,” then add a deterministic check or genuinely different evidence path.

**Security lab.** Seed an external document with an instruction to ignore Work Studio rules and exfiltrate context. Require the agent to treat the instruction as evidence content, refuse authority expansion, and record the attempted injection.

**Portability lab.** Write a provider-neutral operation envelope declaring task, inputs, tools, write scope, prohibited actions, expected output schema, stop condition, and degraded-capability behavior. Map it to two provider APIs only after the neutral contract exists.

### Week 9 — Creative direction, user needs, and design systems

**Objective.** Translate creative intent into observable, plural design directions while preserving accessibility and avoiding system-driven sameness.

**Canonical resources (about 2 hours).** Read the [UK Government Design Principles](https://www.gov.uk/guidance/government-design-principles) (20 minutes), GOV.UK guidance on [using, adapting, and creating patterns](https://www.gov.uk/service-manual/design/using-adapting-and-creating-patterns/) (15 minutes), [Material Design 3](https://m3.material.io/) foundations and accessibility material (35 minutes), Apple’s [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines) overview and motion section (30 minutes), and [WCAG 2.2](https://www.w3.org/TR/WCAG22/) principles and selected success criteria (20 minutes).

**Creative lab.** Use [`develop-idea`](../../skills/core/thinking-develop-idea/SKILL.md) to create three structurally different directions from one brief. Reject mere style swaps. For each direction name the interaction model, hierarchy, pacing, material behavior, accessibility risks, and what evidence would show it serves the audience.

**Artifact lab.** Audit the current system using [`audit-product-interface`](../../skills/core/design-audit-product-interface/SKILL.md) and [`build-design-foundation`](../../skills/core/design-build-design-foundation/SKILL.md). Distinguish discovered tokens from desired principles and principles from implementation recipes.

**Decision simulation.** A design system increases consistency but erases a project’s voice. Decide what belongs in shared invariant, project preference, or deliberate local exception.

### Week 10 — Creative-medium literacy: web, graphics, motion, audio, and interaction

**Objective.** Understand representative substrates by affordance, architecture, accessibility, portability, and production risk.

**Canonical resources (about 2 hours).** Sample the WHATWG [HTML Living Standard](https://html.spec.whatwg.org/) introduction and rendering model (20 minutes), W3C [Web Audio API](https://www.w3.org/TR/webaudio-1.0/) introduction and audio graph concepts (25 minutes), Khronos [WebGL Overview](https://www.khronos.org/webgl/) (15 minutes), W3C [Pointer Events](https://www.w3.org/TR/pointerevents3/) introduction (15 minutes), MDN’s [Animation performance guide](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/CSS_JavaScript_animation_performance) (15 minutes), Apple’s [Motion guidance](https://developer.apple.com/design/human-interface-guidelines/motion) (15 minutes), and WCAG media/motion criteria (15 minutes).

**Creative-technology lab.** Commission five tiny specialist demonstrations: semantic HTML/CSS interaction; Canvas/WebGL visual; purposeful motion with reduced-motion behavior; Web Audio graph; pointer/touch/keyboard interaction. The director does not code them. For each, write the affordance, state model, latency/performance concern, accessibility fallback, browser/device dependence, test method, and maintenance obligation.

**Decision simulation.** Choose the simplest substrate that preserves a desired experience. A technically spectacular WebGL direction loses keyboard semantics and low-power performance; a DOM/CSS direction loses a particular spatial behavior. State which requirement is real and which is prestige.

### Week 11 — Delivery, verification, observability, security, and recovery

**Objective.** Judge whether a build is ready without confusing code completion, test success, environment proof, and human outcome.

**Canonical resources (about 2 hours).** Read NASA’s [verification and validation sections](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf) (30 minutes), NIST’s [Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final) overview (25 minutes), OpenTelemetry’s [signals overview](https://opentelemetry.io/docs/concepts/signals/) (20 minutes), Google SRE’s [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) (25 minutes), and GOV.UK’s [Deploying software regularly](https://www.gov.uk/service-manual/technology/deploying-software-regularly) (20 minutes).

**Artifact lab.** Give one accepted tracer to [`implement-bounded-change`](../../skills/core/engineering-implement-bounded-change/SKILL.md), then use [`verify-release-evidence`](../../skills/core/engineering-verify-release-evidence/SKILL.md). Audit whether the verification names exact requirement, baseline, environment, method, result, anomalies, independence, and limits.

**Operations lab.** For one new dependency, write the operational bill: credentials, cost, monitoring, incident ownership, backup, migration, rollback, provider exit, accessibility regression surface, and recurring review.

**Decision simulation.** Local tests pass, but the target environment and recovery path are untested. Decide what may be claimed, what remains a gap, and whether deployment authority exists.

### Week 12 — Essential capstone: direct one bounded studio change

**Objective.** Demonstrate end-to-end directorial control while agents and specialists perform the implementation.

**Capstone brief.** Select a reversible, meaningful Work Studio improvement that includes one creative choice and one technical consequence. Move it through signal classification, Work Object activation, constraint extraction, alternative development, decision, tracer design, bounded implementation, verification, and outcome/revisit planning. Use the owning core skill at each stage.

**Required artifacts.** Original signal; Work Object; candidate constraint matrix; three meaningfully distinct directions; Director Decision Card; authority grant; tracer bullet; implementation diff or specialist deliverable; verification record; operational bill; outcome hypothesis; revisit trigger; evidence ledger entries.

**Gate 2.** Present the result in ten minutes without source code. Answer all eight human-agency questions, then drill down to the exact evidence on request. A gate fails if the director cannot identify an authority overreach, confuses recommendation with decision, cannot name recovery, or presents dependent agent agreement as independent verification.

Passing the essential gate qualifies the director to supervise ordinary and meaningful, reversible Work Studio activity. It does not qualify unilateral approval of high-consequence, sensitive, regulated, irreversible, or unfamiliar-domain work.

## Weeks 13–24: applied extension

### Week 13 — Measurement, causal caution, and evidence quality

**Objective.** Judge whether a metric measures the intended construct and whether an observed relationship supports the decision being proposed.

Read the National Academies’ [Reproducibility and Replicability in Science](https://www.nationalacademies.org/read/25303) selected chapters (60 minutes) and Stanford’s free [Causal Inference course materials](https://web.stanford.edu/~swager/causal_inf_book.pdf) introduction (30 minutes). Practice distinguishing measurement from construct, correlation from intervention, proxy from outcome, and absence of evidence from evidence of absence. Audit one Work Studio scorecard with [`govern-scorecards`](../../skills/core/governance-govern-scorecards/SKILL.md): find gaming risks, subgroup harm, and non-compensable criteria. **Simulation:** a metric improves while user value worsens; decide whether implementation, decision, evidence process, or governing method should change.

### Week 14 — Failure analysis and proportionate assurance

**Objective.** Select the smallest failure-analysis and assurance method adequate to the named hazard and consequence.

Read the MIT [STPA Handbook](https://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf) introduction and control-structure method (45 minutes), NASA’s [Software FMEA guidance](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695706/8.05%2B-%2BSW%2BFailure%2BModes%2Band%2BEffects%2BAnalysis) (30 minutes), and NASA’s [Independent Verification and Validation criteria](https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604595/SWE-141%2B-%2BSoftware%2BIndependent%2BVerification%2Band%2BValidation) (15 minutes). Apply a lightweight “what can fail / what interaction makes it consequential / what detects it / how do we recover?” analysis to one cross-agent workflow. **Simulation:** a high-consequence recommendation has many tests but no independent evidence path. Build a compact assurance case or stop.

### Week 15 — Security, privacy, data governance, and supply chain

**Objective.** Recognize sensitive information flows, excessive agency, supply-chain exposure, and controls that require specialist proof.

Read NIST [Privacy Framework](https://www.nist.gov/privacy-framework) overview (25 minutes), NIST [Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) executive summary (20 minutes), NIST [SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) practices (25 minutes), OWASP’s [LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (25 minutes), and CISA’s [Secure by Design](https://www.cisa.gov/securebydesign) principles (15 minutes). Draw data flows for a studio agent: source, prompt, provider, tool, storage, logs, and human reviewer. Mark sensitivity, retention, third-party exposure, deletion, and least-privilege boundaries. **Simulation:** a useful personalization feature requires durable inferred personal data; decline silent promotion and propose an explicit, correctable memory path.

### Week 16 — Operations, reliability, deployment, and recovery

**Objective.** Define observable user-significant reliability, bounded deployment authority, and credible restoration evidence.

Read Google SRE’s free chapters [Embracing Risk](https://sre.google/sre-book/embracing-risk/) and [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) (70 minutes), then the openings of [`deploy-with-recovery`](../../skills/core/operations-deploy-with-recovery/SKILL.md) and [`diagnose-production-incident`](../../skills/core/operations-diagnose-production-incident/SKILL.md) (20 minutes). Create service-level indicators only for user-significant behavior. Run a tabletop incident separating impact, observation, hypothesis, cause, containment authority, restoration evidence, and follow-up. **Simulation:** an emergency workaround exceeds ordinary authority; specify the expiring deviation and restoration condition.

### Week 17 — Graphics and motion as architecture

**Objective.** Compare visual substrates and motion systems by experience fit, semantic loss, performance, accessibility, and production burden.

Study Khronos [WebGL](https://www.khronos.org/webgl/) and [glTF](https://www.khronos.org/gltf/) overviews, W3C [Web Animations](https://www.w3.org/TR/web-animations-1/), Apple motion guidance, and WCAG criteria for flashing, animation from interaction, and timing (90 minutes total). Commission matched prototypes of one concept in DOM/CSS, Canvas 2D, and WebGL. Compare semantic accessibility, compositing, asset pipeline, frame budget, device variance, fallback, authoring tooling, and capture/export. **Decision:** select a substrate from the experience requirement, not novelty.

### Week 18 — Audio, multimodal interaction, and inclusive experience

**Objective.** Direct an experience whose meaning survives changes in sensory channel and input method.

Read W3C Web Audio graph and timing sections, W3C [Media Accessibility User Requirements](https://www.w3.org/TR/media-accessibility-reqs/), W3C Pointer Events, and the WAI [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) introduction (90 minutes). Commission an audio-reactive interaction with captions/textual equivalence, keyboard/pointer input, mute, level control, and a silent-mode fallback. Map audio graph, scheduling, decoding, permission/autoplay restrictions, latency, and output-device assumptions. **Gate 3:** explain why the experience works across modalities and where it does not; specialist craft quality may be reviewed separately.

### Week 19 — Physical and immersive options

**Objective.** Recognize when embodiment or spatial presence justifies hardware, safety, privacy, staffing, and teardown obligations.

Read W3C’s [WebXR Device API](https://www.w3.org/TR/webxr/) introduction plus security/privacy sections (40 minutes), Arduino’s official [hardware documentation](https://docs.arduino.cc/hardware/) overview (20 minutes), Raspberry Pi’s official [documentation](https://www.raspberrypi.com/documentation/) introduction (20 minutes), and Apple’s [Designing immersive experiences](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences) (20 minutes). Produce option cards for screen-based, sensor/actuator installation, and XR realization of the same idea. Include hardware sourcing, calibration, environmental conditions, safety, permissions, latency, physical recovery, accessibility, staffing, and teardown. Physical electrical safety and spatial-comfort validation remain specialist responsibilities.

### Week 20 — Advanced agent orchestration and provider portability

**Objective.** Preserve the task, evidence, and authority contract while providers, tools, and available capabilities change.

Read the original [ReAct](https://arxiv.org/abs/2210.03629) evaluation more closely, Google Research’s first-party discussion [Few-shot tool use doesn’t really work (yet)](https://research.google/blog/few-shot-tool-use-doesnt-really-work-yet/), and the provider docs currently used by the studio for tool calling, model/version pinning, context, data controls, and evals (90 minutes). Build a provider comparison against the neutral operation envelope: capability, context, tool semantics, structured output, data policy, observability, cost, rate limits, version stability, and exit path. Run capability degradation: remove web, one tool, and one provider in turn. **Simulation:** decide whether to degrade, reroute, or stop without allowing a fallback provider to inherit undeclared authority.

### Week 21 — Organizational learning without retrospective distortion

**Objective.** Update the correct layer—execution, decision, evidence process, constraint, or method—without letting one outcome rewrite everything.

Read [`review-outcome-and-adapt`](../../skills/core/governance-review-outcome-and-adapt/SKILL.md), [`maintain-working-method`](../../skills/core/governance-maintain-working-method/SKILL.md), and [`govern-scorecards`](../../skills/core/governance-govern-scorecards/SKILL.md) (60 minutes), plus Baron and Hershey’s outcome-bias discussion (20 minutes). Compare a frozen ex-ante decision with its outcome. Diagnose separately: execution quality, decision quality given information then available, random/uncontrolled outcome, evidence-process defect, and method defect. Propose a single-loop repair, double-loop constraint review, or bounded method-loop experiment. Do not rewrite every layer because one outcome disappointed.

### Week 22 — Complexity economics, procurement, and exit

**Objective.** Compare technology choices by their full obligation and exit costs, not purchase price or implementation speed alone.

Read the FinOps Foundation’s official [FinOps Framework](https://www.finops.org/framework/) overview (30 minutes), NIST’s [Configuration Management guidance](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) executive material (30 minutes), and the constraint report’s complexity governance section (30 minutes). Produce total-obligation comparisons for local/open, managed, and premium options: money, latency, data exposure, skills, credentials, upgrades, monitoring, migration, vendor lock-in, and recovery. **Simulation:** a paid platform reduces build time but creates a persistent operational and data obligation. Make a decision with a provider-exit trigger.

### Week 23 — Full capstone production cycle

**Objective.** Integrate creative, epistemic, agent, architecture, delivery, security, and operational judgment in one bounded production cycle.

Direct a small cross-medium studio work from brief to verified candidate. It must involve at least two substrates, one LLM-agent workflow, one promoted constraint, one real creative tradeoff, one operational dependency, and one security/privacy question. Agents and specialists implement; the director writes intent, exclusions, acceptance evidence, authority grants, and residual-risk decision. A second reviewer audits evidence lineage and authority independently where the consequence justifies it.

### Week 24 — Capstone review and personal operating doctrine

**Objective.** Demonstrate retained human agency and codify a personal directing practice that remains revisable.

Present the work using a Director Decision Card, architecture view, constraint matrix, decision trace, operational bill, evidence map, verification limits, recovery plan, and outcome/revisit plan. Complete the eight-question assessment under time pressure and handle one injected contradiction. Write a two-page personal operating doctrine: quality bar, delegation boundaries, evidence thresholds, medium-selection principles, risk appetite, and conditions that require a specialist. End by using [`maintain-working-method`](../../skills/core/governance-maintain-working-method/SKILL.md) to propose—never silently establish—one curriculum-derived improvement to studio practice.

## Decision simulations library

Use these when a weekly artifact does not expose the relevant decision:

1. **Consensus without independence:** three agents recommend the same architecture after reading the same generated summary.
2. **Capability without authority:** an agent can deploy and credentials are available, but the current grant ends at a local candidate.
3. **Verification overclaim:** a unit test passes while the claim concerns user experience in the deployed environment.
4. **Constraint laundering:** “local-first” becomes “must use SQLite” without showing alternative mechanisms.
5. **Creative homogenization:** a design system improves consistency while erasing the work’s intended identity.
6. **Provider drift:** a model alias changes behavior and an old evaluation no longer binds to the current version.
7. **Hidden operational bill:** a realtime feature adds a server, credentials, monitoring, moderation, and incident response.
8. **Freshness conflict:** official documentation, repository code, and runtime observation disagree.
9. **Metric capture:** the team optimizes completion rate while users abandon the experience earlier.
10. **Emergency authority:** a production incident requires containment outside ordinary permission, but the deviation lacks expiry.
11. **Personalization boundary:** an inferred preference would improve output but requires durable personal memory.
12. **Medium prestige:** XR is proposed despite a screen-based experience meeting the actual intent with less exclusion and risk.

## Creative-technology substrate map

| Substrate | Director-level concepts | Characteristic affordances | Characteristic risks | Specialist gate |
|---|---|---|---|---|
| Semantic web UI | document structure, layout, responsive behavior, accessibility tree, browser lifecycle | broad reach, linkability, progressive enhancement | browser variance, accessibility regressions, dependency churn | complex performance, security, framework architecture |
| Canvas / WebGL graphics | retained versus immediate rendering, GPU pipeline, assets, frame budget, fallback | generative and spatial visuals, high visual control | power use, device variance, poor semantics, shader/asset complexity | advanced rendering, shader math, color pipeline |
| Motion | timing, easing, continuity, state communication, reduced-motion | attention, feedback, causality, character | discomfort, distraction, performance, inaccessible meaning | complex choreography and platform profiling |
| Web audio | graph, source, processing, scheduling, latency, permissions, loudness | atmosphere, sonification, spatial and responsive sound | autoplay, device/audio variance, hearing access, production craft | DSP, mastering, low-latency or spatial implementation |
| Multimodal interaction | event model, focus, pointer/touch/keyboard, feedback loops | direct manipulation and embodied response | discoverability, motor/cognitive exclusion, conflicting gestures | novel input research and accessibility testing |
| Physical computing | sensors, actuators, calibration, sampling, power, enclosure, environment | tangible and situated experience | physical safety, reliability, sourcing, maintenance, venue conditions | electronics, fabrication, safety certification |
| XR / immersive | tracking, reference spaces, latency, field of view, comfort, permissions | embodiment, scale, spatial presence | motion discomfort, hardware exclusion, privacy, staffing and teardown | spatial UX, 3D optimization, safety and device testing |

The director chooses a substrate only after the experience requirement and exclusions are clear. A medium is never self-justifying.

## Assessment system

### Eight-question rubric

Score each answer from 0 to 4.

| Score | Evidence of competence |
|---:|---|
| 0 | Cannot answer or invents an answer. |
| 1 | Recalls a label but not its meaning or source. |
| 2 | Gives a plausible explanation but misses scope, evidence, or consequence. |
| 3 | Gives a correct plain-language answer with exact artifact drill-down and material limits. |
| 4 | Also identifies a credible alternative, defeater, interaction effect, or revisit condition. |

Apply the rubric to each human-agency question. A pass requires:

- at least 24/32 overall at week 6;
- at least 27/32 at week 12;
- at least 29/32 at week 24;
- no score below 3 for question 4 (operational responsibility), 6 (direct evidence), 7 (authority), or 8 (epistemic distinction) at the week 12 or 24 gate.

These four are non-compensable: fluent creative direction cannot offset an inability to recognize authority overreach, evidence laundering, or an unowned operational obligation.

### Artifact quality gates

| Gate | Must show | Automatic return for revision |
|---|---|---|
| Constraint | source, subject, category, strength, scope, owner, validation/revisit | preference represented as fact; mechanism represented as semantic necessity |
| Decision | alternatives, ex-ante evidence, tradeoff, unknowns, authority, reversal trigger | one-option theater; recommendation recorded as human decision |
| Agent operation | bounded task, tools, scope, prohibited actions, output contract, stop/degradation behavior | capability treated as permission; retrieved instruction expands authority |
| Creative direction | differentiated alternatives, observable qualities, accessibility, medium rationale | stylistic synonym swaps; novelty as the only rationale |
| Verification | exact claim, baseline, environment, method, result, independence, limits | test result generalized beyond its scope |
| Release/operation | owner, observability, recovery, cost, data exposure, exit path | unowned ongoing obligation; no credible recovery |

### Assessment methods

- **Closed-artifact recall:** answer the eight questions without opening code.
- **Open-artifact drill-down:** locate the exact source or record within two minutes.
- **Contradiction injection:** respond when a new observation conflicts with the accepted narrative.
- **Authority trap:** identify an agent action that is technically possible but not authorized.
- **Medium tradeoff defense:** defend why one substrate fits the intent better than a more impressive option.
- **Teach-back:** explain one technical concept in Director Language using a local example.

## Portfolio and learning evidence ledger

Maintain one private Markdown portfolio with append-only entries. Do not confuse curriculum evidence with canonical project state. Promote into project records only through the owning skill and proper authority.

Suggested entry:

```yaml
learning_evidence:
  date: 2026-08-10
  module: "systems architecture"
  artifact_ref: "repository path or Work Object ID"
  task: "Explain one component and its obligations"
  observation: "directly supported statement"
  interpretation: "bounded interpretation of that observation"
  decision_or_recommendation: "decision, recommendation, or not applicable"
  eight_question_scores: [0, 0, 0, 0, 0, 0, 0, 0]
  strongest_evidence: "stable source or ledger reference"
  gap: "material fact not established"
  correction_received: "specialist or agent feedback, if received"
  revisit_on: "date or observable trigger"
```

Required portfolio pieces by week 24:

- two system context/container analyses;
- three constraint matrices;
- four frozen Decision Cards, including one rejected proposal;
- two evidence-lineage and contradiction analyses;
- two agent operation envelopes and one degradation exercise;
- one creative direction set with three structurally different alternatives;
- one cross-substrate comparison;
- two operational bills;
- one incident tabletop;
- essential and full capstone packets;
- four spaced eight-question recall results showing corrections over time.

## Spaced review and revisit cadence

Use a 1–7–30–90 pattern for concepts that affect authority or consequential judgment:

- **Within 24 hours:** five-minute unaided recall; record the weakest human-agency question.
- **After 7 days:** apply the concept to a different Work Object or substrate.
- **After 30 days:** contradiction drill plus evidence drill-down.
- **After 90 days:** re-evaluate against current repository contracts and provider documentation; retire stale notes.

Every Friday, review only three items: one decision, one evidence distinction, and one operational obligation. Every fourth week, replay an earlier decision with the original information hidden from outcomes, then compare the frozen record. Quarterly, review provider-dependent resources and run one capability-degradation exercise. Twice yearly, sample five meaningful Work Objects against the eight human-agency questions.

## What to skip, defer, or delegate

Skip unless an active decision demands it:

- memorizing programming syntax or framework APIs;
- implementing production authentication, cryptography, databases, networking, CI/CD, shaders, DSP, firmware, or 3D pipelines;
- training or fine-tuning foundation models;
- formal constraint programming, theorem proving, or universal knowledge graphs;
- exhaustive study of every provider feature or benchmark leaderboard;
- building a multi-agent platform before a measured coordination problem exists;
- reducing evidence, risk, creativity, or studio health to one score;
- treating certificates as proof of decision competence.

Delegate detailed work, but require a director-legible deliverable:

| Specialist work | Director requests |
|---|---|
| Software architecture | component map, quality-attribute tradeoffs, state ownership, failure/recovery, migration and exit |
| Security/privacy | threat/data-flow model, severity, controls, residual risk, verification, incident path |
| Research/statistics | question, design, sampling limits, alternative explanations, uncertainty, reproducible materials |
| Visual/motion/sound | intent translation, alternatives, accessibility, performance constraints, production dependencies |
| LLM engineering | task-specific evals, version binding, context/tool design, injection controls, cost, portability, failure modes |
| Operations | service objectives, telemetry, runbook, rollback exercise, ownership and recurring cost |

## Budget-aware paths

### Free path

All essential concepts can be learned through the local reports and freely available institutional sources: MIT OpenCourseWare, NASA handbooks, NIST publications, W3C/WHATWG/Khronos standards, GOV.UK guidance, Google SRE, OWASP, Stanford CRFM, original open papers, and official platform documentation. Use existing Work Studio agents and local artifacts for labs. Estimated external spend: **$0**, excluding existing model usage and optional hardware.

Keep agent exercises budget-bounded: use short evidence packets, fixed trial counts, and task-specific evaluations. Record token/API cost as an operational obligation, not only a learning expense.

### Paid selective path

Spend only where guided practice or specialist critique changes judgment:

- CMU SEI’s [Software Architecture: Principles and Practices](https://www.sei.cmu.edu/training/software-architecture-principles-practices-elearning/) is an approximately 18-hour paid option for weeks 2, 11, and 14.
- Purchase or borrow *Software Architecture in Practice* only if recurring architecture decisions justify the depth.
- Commission three 60–90 minute critiques: one systems architect, one security/privacy practitioner, and one senior creative technologist. Give each the same capstone packet and ask them to identify missing obligations.
- Rent or borrow XR/physical-computing equipment for week 19; do not buy a platform before a brief requires it.
- Use paid provider sandboxes only for portability/evaluation exercises with explicit spending limits and no sensitive production data.

Avoid broad bootcamps, generic prompt-engineering certificates, affiliate reading lists, and courses centered on one fast-changing framework. They tend to optimize tool familiarity rather than the director’s durable decision model.

### Optional deeper resources

Use these only when the studio’s active portfolio justifies the added depth:

- CMU SEI’s [Architecture Tradeoff Analysis Method collection](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) (3–4 hours selected) for repeated architecture tradeoff reviews.
- Harvard’s free [Statistics 110](https://stat110.hsites.harvard.edu/) modules on conditioning, Bayes, expectation, and base rates (12–20 hours selected) when quantitative uncertainty recurs.
- Google’s [People + AI Guidebook](https://pair.withgoogle.com/guidebook-v2/) (5–7 hours selected) for deeper human-AI interaction design.
- NYU ITP’s [Physical Computing course](https://itp.nyu.edu/physcomp/) (12–20 hours selected) when installations or tangible interaction enter the portfolio.
- Derivative’s official [TouchDesigner curriculum](https://learn.derivative.ca/all-courses/) (10–20 hours selected) when realtime audiovisual production becomes recurring.
- Google SRE’s free [Site Reliability Engineering books](https://sre.google/books/) (10–14 hours selected) when the studio owns live services rather than prototypes.

## Stable foundations versus rapidly changing material

### Stable or slow-changing foundations

- systems boundaries, interfaces, state, lifecycle, feedback, and emergent behavior;
- intent/requirement/constraint/mechanism/evidence distinctions;
- provenance, source ownership, defeasibility, contradiction, and verification scope;
- decision quality versus outcome quality;
- capability, expertise, permission, authority, and accountability;
- human factors of automation and situation awareness;
- accessibility, perceptual hierarchy, multimodal alternatives, and purposeful motion;
- verification versus validation, recovery, observability, and operational ownership;
- least privilege, threat modeling, data minimization, and configuration baselines.

Review these when standards or the Work Studio constitution changes, normally every 6–12 months.

### Rapidly changing provider and implementation material

- model names, context windows, pricing, rate limits, tool-call syntax, structured-output behavior;
- provider data-retention policies, regional availability, safety filters, and terms;
- agent frameworks, benchmark standings, prompt recipes, and model-specific optimizations;
- browser/device support for emerging APIs such as WebXR and new graphics capabilities.

Review these quarterly and at every material provider/model/version change. Bind evaluations to the exact model, API, prompt/kernel, tool set, retrieval configuration, date, and environment. A provider page is current implementation evidence, not a stable architectural principle.

## Resource index by domain

The estimated loads below identify the portion useful to a director, not the full source length.

### Work Studio foundations

| Resource | Load | Why it matters |
|---|---:|---|
| [Director Language](../DIRECTOR-LANGUAGE.md) | 15 min | Governs explanations and preserves observation/interpretation/recommendation. |
| [Constraint-Driven Studio OS](../constraints/constraint-driven-studio-operating-system-research-and-applied-architecture.md) | 4–6 h selected | Local director, constraint, authority, complexity, validation, and agency contract. |
| [Epistemic Engineering](../epistemic/epistemic-engineering-research-and-applied-architecture.md) | 4–6 h selected | Local claim/evidence/provenance/contradiction/assurance contract. |
| [Core skills](../../skills/core/) | 3 h selected | The real operational lifecycle used in curriculum labs. |

### Systems, architecture, requirements, and constraints

| Resource | Load | Stability / use |
|---|---:|---|
| MIT OCW [System Architecture](https://ocw.mit.edu/courses/esd-34-system-architecture-january-iap-2007/pages/syllabus/) | 4–8 h selected | Stable architecture concepts and architect role. |
| NASA [Systems Engineering Handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf) | 4 h selected | Stable lifecycle, requirements, architecture, V&V, and technical management. |
| [SEBoK](https://sebokwiki.org/wiki/Guide_to_the_Systems_Engineering_Body_of_Knowledge_%28SEBoK%29) | 2 h selected | Maintained institutional map; use for orientation, then follow primary references. |
| CMU SEI [Quality Attributes](https://www.sei.cmu.edu/library/quality-attributes/) | 45 min | Connects architecture to performance, security, modifiability, reliability, and usability tradeoffs. |
| NASA [Requirements Verification Matrix](https://www.nasa.gov/reference/system-engineering-handbook-appendix/) | 30 min | Links each requirement to a declared verification method. |
| IETF [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) | 15 min | Classic normative-strength discipline; do not import vocabulary uncritically. |

### Epistemology, provenance, inquiry, and decision

| Resource | Load | Stability / use |
|---|---:|---|
| W3C [PROV Overview](https://www.w3.org/TR/prov-overview/) and [PROV-O](https://www.w3.org/TR/prov-o/) | 45 min | Stable provenance relations; provenance does not prove truth. |
| US intelligence community [Tradecraft Primer](https://www.cia.gov/resources/csi/static/955180a45afe3f5013772c313b16face/Tradecraft-Primer-apr09.pdf) | 60 min | Alternatives, assumptions, indicators, and diagnostic evidence. |
| National Academies [Reproducibility and Replicability](https://www.nationalacademies.org/read/25303) | 2 h selected | Evidence transparency, computational reproducibility, and institutional responsibility. |
| Baron & Hershey [Outcome Bias](https://bear.warrington.ufl.edu/brenner/mar7588/Papers/baron-hershey-jpsp1988.pdf) | 40 min | Separates decision quality from later luck. |
| Stanford [Causal Inference](https://web.stanford.edu/~swager/causal_inf_book.pdf) | 2 h selected | Working literacy in causal claims and experimental reasoning. |
| NIST [SP 800-30 Rev. 1](https://csrc.nist.gov/pubs/sp/800/30/r1/final) | 60 min selected | Risk framing and assessment; adapt proportionally. |

### Human–AI interaction and LLM agents

| Resource | Load | Stability / use |
|---|---:|---|
| Parasuraman, Sheridan & Wickens [types and levels of automation](https://doi.org/10.1109/3468.844354) | 45 min | Stable human-factors model separating acquisition, analysis, selection, and action. |
| Endsley [Situation Awareness](https://doi.org/10.1518/001872095779049543) | 45 min | Explains why opaque automation can weaken intervention and recovery. |
| NIST [AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | 60 min | Govern–Map–Measure–Manage structure and explicit human roles. |
| NIST [Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | 90 min selected | Current cross-sector generative-AI risk catalogue and actions. Review on revision. |
| [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | 30 min selected | Transformer foundation; director needs the conceptual architecture, not derivations. |
| [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) | 35 min selected | Scaling, in-context behavior, and documented limitations. |
| [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) | 35 min selected | Distinguishes model parameters from retrieved external memory. |
| [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/) | 35 min | Evidence that long context does not guarantee uniform use. |
| [ReAct](https://arxiv.org/abs/2210.03629) | 45 min | Original reason/action/tool-interaction pattern and its evaluation. |
| [Toolformer](https://arxiv.org/abs/2302.04761) | 30 min | Original account of learned tool use; not a universal orchestration recipe. |
| Stanford CRFM [HELM](https://crfm.stanford.edu/helm/latest/) | 45 min | Multi-metric, scenario-based evaluation instead of one leaderboard score. |
| OWASP [LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) | 30 min | Practical threat/control vocabulary; review as attacks evolve. |
| OpenAI [Evaluation Best Practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | 25 min | Useful first-party current eval guidance; provider-specific and fast-changing. |
| Google Research [Few-shot tool use](https://research.google/blog/few-shot-tool-use-doesnt-really-work-yet/) | 20 min | First-party evidence against assuming tool use works from a few demonstrations. |

### Creative direction, interaction, and accessibility

| Resource | Load | Stability / use |
|---|---:|---|
| [UK Government Design Principles](https://www.gov.uk/guidance/government-design-principles) | 20 min | User needs, evidence, iteration, simplicity, and consistency without uniformity. |
| GOV.UK [Design patterns](https://www.gov.uk/service-manual/design/using-adapting-and-creating-patterns/) | 15 min | Patterns as evidence-backed defaults that may be adapted when research demands. |
| [Material Design 3](https://m3.material.io/) | 60 min selected | A living first-party design system; useful to study adaptability, not copy a house style. |
| Apple [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines) | 60 min selected | Platform-specific interaction, hierarchy, motion, and accessibility guidance. |
| W3C [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | 90 min selected | Normative accessibility requirements; use relevant success criteria and test methods. |
| WAI [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) | 45 min selected | Interaction patterns and keyboard/accessibility expectations. |

### Creative-technology substrates

| Resource | Load | Stability / use |
|---|---:|---|
| WHATWG [HTML Living Standard](https://html.spec.whatwg.org/) | 45 min selected | Web document, semantics, events, media, and rendering substrate. Living standard. |
| Khronos [WebGL](https://www.khronos.org/webgl/) | 30 min | Cross-platform GPU graphics architecture and portability. |
| Khronos [glTF](https://www.khronos.org/gltf/) | 20 min | Interchange and delivery concerns for 3D assets. |
| W3C [Web Animations](https://www.w3.org/TR/web-animations-1/) | 30 min selected | Timing model underlying web animation. |
| W3C [Web Audio API](https://www.w3.org/TR/webaudio-1.0/) | 45 min selected | Audio graph, scheduling, processing, and platform obligations. |
| W3C [Pointer Events](https://www.w3.org/TR/pointerevents3/) | 25 min | Unified pointer interaction and device variability. |
| W3C [Media Accessibility User Requirements](https://www.w3.org/TR/media-accessibility-reqs/) | 30 min | Captions, description, transcripts, navigation, and media access needs. |
| W3C [WebXR Device API](https://www.w3.org/TR/webxr/) | 45 min selected | Immersive device model, latency, permissions, security, and privacy; still evolving. |
| Arduino [Hardware docs](https://docs.arduino.cc/hardware/) | 25 min | Representative microcontroller ecosystem and board constraints. |
| Raspberry Pi [Documentation](https://www.raspberrypi.com/documentation/) | 25 min | Representative small-computer platform and operational surface. |

### Delivery, security, operations, and learning

| Resource | Load | Stability / use |
|---|---:|---|
| NIST [SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) | 60 min selected | Secure development practices across organizations and suppliers. |
| NIST [Privacy Framework](https://www.nist.gov/privacy-framework) | 45 min selected | Data-processing risk and privacy governance. |
| NIST [Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) | 30 min selected | Resource-specific authorization and no implicit trust; use principle, not enterprise machinery. |
| CISA [Secure by Design](https://www.cisa.gov/securebydesign) | 30 min | Producer responsibility and secure defaults. |
| OpenTelemetry [Signals](https://opentelemetry.io/docs/concepts/signals/) | 25 min | Traces, metrics, logs, and baggage as distinct operational evidence. |
| Google SRE [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) | 45 min | User-relevant monitoring and actionable signals. |
| Google SRE [Embracing Risk](https://sre.google/sre-book/embracing-risk/) | 40 min | Reliability as a value/risk tradeoff rather than maximum uptime at any cost. |
| NASA [Software FMEA](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695706/8.05%2B-%2BSW%2BFailure%2BModes%2Band%2BEffects%2BAnalysis) | 35 min | Component failure modes and downstream effects. |
| MIT [STPA Handbook](https://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf) | 60 min selected | Unsafe interactions and inadequate control, beyond component failure. |
| NASA [Independent V&V](https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604595/SWE-141%2B-%2BSoftware%2BIndependent%2BVerification%2Band%2BValidation) | 25 min | Technical, managerial, and financial independence dimensions. |
| NIST [Configuration Management SP 800-128](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) | 45 min selected | Baselines, controlled change, impact analysis, and proportionate rigor. |
| [FinOps Framework](https://www.finops.org/framework/) | 30 min | First-party community framework for cloud value and accountable technology spend. |

## Minimal routine after completion

Reserve 90 minutes per week:

1. **Twenty minutes — decision replay:** inspect one frozen Decision Card without looking at the outcome; assess whether the reasoning was sound then.
2. **Twenty minutes — architecture and obligation:** choose one component and restate why it exists, what it owns, what can fail, and who operates it.
3. **Twenty minutes — evidence audit:** trace one consequential claim to its strongest source and check freshness, scope, contradiction, and independence.
4. **Twenty minutes — agent/medium watch:** review one provider or creative-substrate change only if it can affect an active decision.
5. **Ten minutes — ledger:** record one correction, gap, or revisit trigger.

Once per month, perform the full eight-question test on a sampled meaningful Work Object. Once per quarter, run provider degradation and recovery tabletop exercises.

## First two-week onboarding sprint

This sprint can begin immediately and produces usable director artifacts before the full curriculum continues.

### Week 1: establish authority and the decision model — 6 hours

**Session A, 90 minutes.** Read Director Language and the director contract. Write the personal role charter with three columns: own, delegate, never silently delegate.

**Session B, 90 minutes.** Select one active or recently completed Work Object. Trace its lifecycle through the owning skills. Mark every point where an agent recommended, a human decided, a tool checked, or an external effect could occur.

**Session C, 90 minutes.** Complete the eight human-agency questions from the artifacts. Mark “unknown” rather than infer. Ask an agent to critique the answers, requiring exact repository evidence.

**Session D, 90 minutes.** Run the capability-versus-authority simulation. Produce a scoped grant with action, actor, paths/subjects, prohibited scope, evidence reviewed, expiry, and recovery condition.

**Deliverables:** role charter, lifecycle/authority map, first eight-question baseline, one authority grant. **Pass condition:** no recommendation is mislabeled as a decision and no capability is treated as authority.

### Week 2: learn to see architecture and constraints — 6 hours

**Session A, 90 minutes.** Study selected MIT/NASA architecture material. Draw Work Studio’s context and major containers from repository evidence.

**Session B, 90 minutes.** For three major components, write purpose, constraint, state owner, interface, failure, recovery, operational obligation, and removal path.

**Session C, 90 minutes.** Translate one creative direction into candidate constraint categories and strengths. Preserve original wording and separate intent, semantic constraint, mechanism, and validation.

**Session D, 90 minutes.** Compare two implementation shapes with a Director Decision Card. Include the strongest alternative and one observation that would reverse the recommendation.

**Deliverables:** architecture map, three component cards, candidate constraint matrix, Decision Card. **Pass condition:** the director can explain the recommendation without naming implementation technology first.

## Self-assessment checklist

Mark each item **yes**, **not yet**, or **specialist required**.

### Purpose and creative direction

- I can state the audience, need, intended experience, exclusions, and quality bar.
- I can distinguish a creative principle from a single visual or technical recipe.
- I can demand meaningfully different alternatives rather than cosmetic variations.
- I can identify when novelty or platform prestige is masquerading as user value.

### Systems and constraints

- I can explain each major component’s purpose, state, dependencies, and removal path.
- I can distinguish intent, constraint, policy, mechanism, validation, and evidence.
- I can classify invariant, obligation, prohibition, preference, assumption, and experiment.
- I can identify the new operational bill created by a design or architecture choice.

### Evidence and decisions

- I keep observation, testimony, inference, gap, decision, and memory distinct.
- I can trace a consequential claim to the source that owns it.
- I check scope, baseline, freshness, relevance, sufficiency, contradiction, and independence.
- I freeze important reasoning before outcomes are known.
- I can name the strongest alternative and what would defeat my preferred hypothesis.
- I set a revisit or reversal trigger for accepted uncertainty.

### Agents and authority

- I distinguish capability, expertise, permission, authority, and accountability.
- I can write a bounded operation envelope with prohibited actions and stop conditions.
- I treat retrieved instructions as untrusted content, not authority.
- I know why multiple agents using one source lineage are not independent evidence.
- I require task-specific evaluations bound to exact versions and environments.
- I can degrade, reroute, or stop when a provider or capability disappears.

### Creative technology and production

- I can compare web UI, Canvas/WebGL, motion, audio, physical, and XR options by affordance and obligation.
- I ask for accessibility fallbacks and device/browser/environment evidence.
- I understand the difference between a prototype, verified candidate, deployed behavior, and validated human outcome.
- I can identify when a specialist must own graphics, audio, security, statistics, operations, or physical safety depth.

### Operations and learning

- I require observability, ownership, rollback, and exit paths for material dependencies.
- I can separate incident impact, hypothesis, cause, containment, and restoration evidence.
- I can distinguish bad execution, a poor ex-ante decision, unlucky outcome, evidence-process failure, and method failure.
- I can answer all eight human-agency questions for meaningful work without opening code.

If any authority, evidence-typing, sensitive-data, operational-ownership, or recovery item is “not yet,” keep the relevant action below durable publication or deployment and obtain specialist review.

## Research limitations

This curriculum is based on the Work Studio repository state inspected on 2026-08-10 and on primary or first-party material available at that date. It is not a substitute for accredited safety, security, privacy, legal, electrical, accessibility, statistical, or domain-specific professional training. Several standards are intentionally sampled rather than assigned in full; the director’s task is informed governance, while specialists retain technical responsibility.

Some first-party provider documentation changes faster than archival research and may move, be superseded, or describe current product behavior without independent validation. The curriculum marks that material for quarterly review. WebXR remains an evolving specification with uneven platform support. Costs depend on existing subscriptions, local rates, model usage, hardware access, and chosen reviewers. Estimated loads are instructional estimates, not measured completion times.

The curriculum’s effectiveness should be judged through artifact quality, authority preservation, evidence accuracy, decision traceability, recovery credibility, and the eight human-agency questions—not completion time, reading volume, or certificate count.
