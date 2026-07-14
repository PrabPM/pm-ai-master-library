# Volume 4 — Practical Product Design for Product Managers

## July 2026 field guide: evidence, systems, accessibility, fintech, and AI experiences

Edition date: 14 July 2026  
Companion to the ML/AI PM Masterclass  

This volume preserves the useful product-design foundations and fintech patterns in the supplied handbook, removes unsupported production claims, and updates the practice for July 2026. Examples use the fictional **PayFlow** product. They teach a method; they do not describe a real company or promise a result.

## How to use this volume

- Read Chapters 1–8 for the craft baseline.
- Use Chapters 9–12 for regulated and AI-enabled products.
- Use Chapters 13–15 as operating and interview playbooks.
- In every exercise, name the user, job, state, risk, measure, and recovery path.

# 1. Product design is decision design

Product design is the deliberate shaping of a user's path from intent to outcome. A PM co-owns the problem, constraints, evidence, success measures, and trade-offs. Designers own craft leadership; engineering owns implementation integrity; research and data help the team distinguish evidence from confidence.

Start with a decision brief:

| Field | Example |
|---|---|
| User | Finance operator reconciling payouts |
| Job | Explain a mismatch before the close deadline |
| Current pain | Three tools, unclear source of truth |
| Desired behavior | Investigate, document, resolve or escalate |
| Success | Median resolution time and correct-resolution rate |
| Guardrail | No increase in unauthorized overrides |
| Unknown | Which mismatch classes need human judgment? |

**Example.** “Build an AI reconciliation assistant” is a solution. “Reduce time to correctly explain a payout mismatch, without weakening maker-checker control” is a problem. The second statement permits non-AI answers and exposes the safety condition.

# 2. Research: reduce the riskiest uncertainty

Research is not a ceremony. Choose the smallest method that can change the decision.

- Interviews reveal language, motives, workarounds, and mental models.
- Contextual inquiry reveals actual sequences, interruptions, and shadow tools.
- Diary studies expose longitudinal behavior.
- Usability tests expose interaction failures; five sessions can find obvious issues, but are not a statistical guarantee.
- Instrumentation reveals what happened, not why.
- Experiments estimate causal effects when assignment and power are sound.

Write every finding as **observation → interpretation → implication → confidence**. Separate what a participant did from what the team inferred.

**Worked example.** Four operators copy transaction IDs into chat. Observation: copying occurs after the dashboard labels a mismatch “unknown.” Interpretation: the label does not suggest a next action. Implication: test reason codes and an escalation action. Confidence: medium; validate across shifts and mismatch types.

# 3. Jobs, journeys, and service blueprints

A job statement describes progress: “When settlement totals disagree, help me locate the responsible event so I can close the books confidently.” A journey maps the user's visible stages. A service blueprint adds backstage systems, people, policies, and failure points.

For a card dispute:

1. Notice: merchant sees a debit.
2. Understand: reason, amount, deadline, evidence needed.
3. Act: accept or contest.
4. Track: status and next milestone.
5. Resolve: decision, ledger effect, appeal path.

Behind those steps sit network files, evidence storage, permissions, notification jobs, ledger postings, and support policy. Design the backstage contract at the same time as the screen. A beautiful status page cannot repair an ambiguous state machine.

# 4. Information architecture and content

Organize around user objects and tasks, not the org chart. Name concepts consistently across UI, API, support, and analytics. Define a content model for every important object: identity, status, amount, time, owner, reason, available action, and provenance.

Use progressive disclosure: show the outcome and next action first; place calculation detail, raw events, and policy under expansion. Avoid hiding consequential terms.

**Before:** “Error 412. Contact support.”  
**After:** “This payout cannot be released because the bank account is still being verified. Verification usually completes within two business days. View verification or contact support.”

Microcopy should answer: What happened? Why? What can I do? What happens next? Never blame the user, and never use certainty the system cannot support.

# 5. Interaction design: states before screens

Model the state machine before high-fidelity mockups. At minimum include initial, loading, empty, partial, success, recoverable error, blocked, offline, stale, and unauthorized states. For long-running work include queued, processing, needs-input, canceled, timed-out, and completed-with-warnings.

For a transfer, distinguish **submitted**, **authorized**, **processing**, **settled**, **failed**, and **reversed**. “Complete” must have one operational meaning.

Design prevention and recovery together:

- Validate near the field, but do not erase input.
- Disable destructive actions only with a visible reason.
- Prefer undo for reversible actions.
- For irreversible actions, show scope, consequence, and confirmation.
- Preserve an audit trail for privileged actions.

**Example confirmation:** “Send USD 12,450.00 to Northwind LLC, account ending 1842, arriving 15 July? This cannot be canceled after processing begins.”

# 6. Visual hierarchy and responsive systems

Hierarchy communicates priority through position, size, weight, color, spacing, and grouping. Use typography and layout before adding decoration. A practical screen has one primary action, a small number of semantic colors, stable alignment, and enough whitespace to parse groups.

Design responsively from content priorities, not device labels. Test narrow width, zoom, long translations, large text, keyboard navigation, touch, poor network, and reduced motion. Tables need a deliberate small-screen behavior: priority columns, row details, horizontal scroll with a cue, or a task-specific card view.

Design tokens provide shared names for decisions such as color, spacing, type, radius, and motion. The Design Tokens Community Group published its first stable specification in October 2025. A token such as `color.action.primary` is more maintainable than copying `#175CD3` into many files.

# 7. Accessibility is a product requirement

Use WCAG 2.2 as the current baseline. It adds criteria relevant to modern product work, including focus visibility, dragging alternatives, minimum target size, consistent help, redundant entry, and accessible authentication. WCAG 2.2 was also approved as ISO/IEC 40500:2025. The European Accessibility Act has applied since 28 June 2025 to covered products and services, including banking services.

Accessibility definition of done:

- Complete the critical path using keyboard alone.
- Provide visible focus and logical focus order.
- Associate labels, instructions, errors, and status changes programmatically.
- Do not rely on color alone.
- Meet contrast and text-resize requirements.
- Give alternatives for drag, gesture, audio, and visual-only information.
- Use semantic elements before custom controls.
- Test with screen-reader and zoom users, not only automated tools.

**Worked audit.** A six-box OTP control steals focus, rejects paste, and announces each box as “edit text.” Replace it with one labeled input that accepts paste and autofill, permits password-manager use, reports errors in text, and does not impose a cognitive puzzle.

# 8. Prototyping and usability testing

Choose fidelity by question. Paper or wireframes test structure; clickable prototypes test flow and comprehension; coded prototypes test performance, accessibility, and technical feasibility. A prototype is evidence, not a commitment.

Use realistic tasks without telling participants what to click: “A customer says yesterday's transfer is missing. Find what happened and decide the next step.” Record success, error, time, confidence, and notable behavior. Ask for expectation before a click and interpretation after a result.

Prioritize findings by severity: frequency × impact × persistence. A rare error that moves money incorrectly outranks a common cosmetic hesitation.

# 9. Fintech patterns: trust, money, and control

Money screens need exact currency, timezone, effective date, fee, recipient, status, and source. Avoid binary “success/failure” when networks are asynchronous. Show the difference between available, pending, reserved, and settled balances.

**Pricing simulator.** Let a PM select merchant segment, card type, amount, and effective date. Show gross amount, each fee component, net amount, rule ID, and fallback used. A compare mode displays old versus proposed rules. Publishing requires a second approver and creates an immutable audit event.

**KYB onboarding.** Ask only for fields needed at the current risk tier. Explain why sensitive information is required. Save progress, expose verification status, offer document alternatives, and route uncertain cases to review instead of pretending the model is certain.

**Disputes.** Show deadline, evidence checklist, amount at risk, current owner, and next milestone. Preserve submitted evidence and explain late or invalid items.

# 10. Metrics and experiments

Use a metric tree: business outcome → user behavior → product signals → system health. Pair speed with quality and safety.

For reconciliation assistance:

- Outcome: correctly resolved mismatches per operator-hour.
- Quality: audited correct-resolution rate.
- Speed: median and p90 time to resolution.
- Adoption: eligible cases using the assistant.
- Guardrails: override rate, reopened cases, privacy incidents, operator workload.

Current web performance uses Core Web Vitals: Largest Contentful Paint, Interaction to Next Paint, and Cumulative Layout Shift. The “good” thresholds are LCP at most 2.5 seconds, INP at most 200 ms, and CLS at most 0.1, assessed at the 75th percentile.

Before an A/B test, define unit of randomization, primary metric, guardrails, minimum detectable effect, duration, exclusions, and stopping rule. Check novelty, network effects, and sample-ratio mismatch. Do not optimize a click if the real job is a correct financial outcome.

# 11. AI UX: calibrated help, provenance, and control

Design AI as a fallible subsystem. The interface must communicate what it did, what evidence it used, how current that evidence is, what it is uncertain about, and what the user can do next.

For retrieval-augmented answers, show citations at the claim level and support source inspection. “No supported answer found” is a valid outcome. Do not use a fluent model as the system of record, policy authority, calculator for money, or silent executor of irreversible actions.

**Agent approval card:**

| Field | Value |
|---|---|
| Goal | Retry 43 failed payouts |
| Proposed tools | Fetch status; create retry batch |
| Scope | Batch `PF-2026-07-14-09` only |
| Exclusions | 3 accounts under review |
| Effect | Creates new payment attempts |
| Approval | Two authorized operators |

Stream progress as durable events: planned, tool requested, tool succeeded/failed, waiting for approval, completed. Permit cancelation where safe. Store a trace for review, but minimize sensitive content.

# 12. Multimodal, voice, and real-time experiences

Voice and multimodal interfaces need a visible or audible confirmation loop. Repeat high-risk entities such as amount and recipient. Provide a screen fallback, captions, transcript controls, and a way to correct recognition before execution.

For real-time collaboration, distinguish local optimistic state from server-confirmed state. Show presence without implying approval. Resolve conflicts explicitly; never silently overwrite a policy or pricing rule. Design reconnect behavior and stale-state warnings.

# 13. Privacy, safety, and ethical design

Collect the minimum data needed for the stated purpose. Define retention, access, deletion, and secondary-use rules before launch. Sensitive inferences require stricter review than raw fields. Give users meaningful control, not consent theater.

Avoid dark patterns: disguised ads, hidden costs, obstruction, forced continuity, confirm-shaming, and urgency without evidence. For AI, test representational harm, disparate error rates, automation bias, prompt injection pathways, data leakage, and unsafe tool use.

A pre-launch risk review should name hazard, affected group, severity, likelihood, detection, mitigation, owner, and residual risk. “Human in the loop” is not a mitigation unless the human has time, context, authority, and a usable override.

# 14. Handoff, design QA, and operations

A complete handoff includes state model, responsive behavior, component/token references, content, analytics events, accessibility notes, permissions, API assumptions, edge cases, and acceptance criteria. Review the built product in the target environment.

Release checklist:

- Critical path works at 200% zoom and with keyboard.
- Loading, empty, error, stale, and unauthorized states are implemented.
- Amounts, dates, currencies, and rounding agree with the domain contract.
- Analytics names and properties match the measurement plan.
- Sensitive values are masked in logs and screenshots.
- Rollback, support, and incident ownership are known.

# 15. PM interview and case framework

Use **C-L-E-A-R**:

1. **Context:** user, job, environment, constraints.
2. **Learn:** evidence, unknowns, research plan.
3. **Explore:** alternatives and trade-offs.
4. **Align:** chosen experience, system states, risks.
5. **Result:** metrics, experiment, rollout, learning.

In a whiteboard case, narrate assumptions and prioritize one path. Include the failure and recovery path before polishing the happy path. Strong candidates connect a UI choice to user evidence, system behavior, and a measurable outcome.

**Practice prompt.** Design an AI assistant for chargeback evidence. Define eligible users, evidence sources, unsupported-claim behavior, human approval, deadline risk, privacy boundaries, quality evaluation, and rollout guardrails.

# 16. Templates and glossary

## One-page design brief

Problem; user and job; evidence; desired behavior; non-goals; constraints; state model; accessibility; metric and guardrails; risks; open questions; owner and decision date.

## Critique prompts

- What job and state is this screen serving?
- What is the primary action and consequence?
- What assumption is least supported?
- What happens with no data, stale data, slow data, or conflicting data?
- Can a keyboard and screen-reader user complete it?
- What would make the user trust or distrust the result?

## Essential terms

Affordance: cue about possible action. Constraint: rule limiting action. Design token: named design decision. Progressive disclosure: staged complexity. Service blueprint: user journey plus backstage system. State machine: allowed states and transitions. Usability: effectiveness, efficiency, and satisfaction. Accessibility: ability of people with disabilities to perceive, operate, understand, and robustly use the product. Guardrail: metric or control protecting against harm. Provenance: origin and transformation history of information.

# Current standards and primary references

- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*: https://www.w3.org/TR/WCAG22/
- W3C, *WCAG 2.2 approved as ISO/IEC 40500:2025*: https://www.w3.org/press-releases/2025/wcag22-iso-pas/
- European Commission, *EU becomes more accessible for all* (EAA application date): https://digital-strategy.ec.europa.eu/en/news/eu-becomes-more-accessible-all
- web.dev, *Web Vitals*: https://web.dev/articles/vitals
- Design Tokens Community Group, stable specification and format module: https://www.designtokens.org/

Verify jurisdiction-specific legal obligations with qualified counsel. Product and accessibility guidance here is educational, not legal advice.


<!-- COMPREHENSIVE-EDITION -->


# Applied curriculum and mastery labs

These labs turn the core chapters into portfolio-ready practice. Complete them with explicit assumptions and retain both the artifact and its review notes.

# Lab 01 — Research Plan: Merchant Kyb Onboarding

## Objective

Produce a reviewable research plan for merchant KYB onboarding. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its merchant KYB onboarding experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the research plan; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: recovery without data loss; explicit money and time semantics; and human approval for irreversible effects.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 02 — Interview Guide: Subscription Cancellation

## Objective

Produce a reviewable interview guide for subscription cancellation. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its subscription cancellation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the interview guide; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: keyboard and screen-reader completion; evidence-linked AI output; and guardrail metrics and rollback.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 03 — Evidence Synthesis: Cross-Border Transfer

## Objective

Produce a reviewable evidence synthesis for cross-border transfer. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its cross-border transfer experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the evidence synthesis; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit money and time semantics; least-privilege action scope; and clear system status.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 04 — Jobs-To-Be-Done Map: Chargeback Evidence

## Objective

Produce a reviewable jobs-to-be-done map for chargeback evidence. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its chargeback evidence experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the jobs-to-be-done map; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: evidence-linked AI output; human approval for irreversible effects; and recovery without data loss.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 05 — Service Blueprint: Agent-Assisted Operations

## Objective

Produce a reviewable service blueprint for agent-assisted operations. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its agent-assisted operations experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the service blueprint; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege action scope; guardrail metrics and rollback; and keyboard and screen-reader completion.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 06 — Information Architecture: Payment Failure Recovery

## Objective

Produce a reviewable information architecture for payment failure recovery. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payment failure recovery experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the information architecture; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: human approval for irreversible effects; clear system status; and explicit money and time semantics.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 07 — Task Flow: Enterprise Permissions

## Objective

Produce a reviewable task flow for enterprise permissions. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its enterprise permissions experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the task flow; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: guardrail metrics and rollback; recovery without data loss; and evidence-linked AI output.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 08 — State Machine: Mobile Checkout

## Objective

Produce a reviewable state machine for mobile checkout. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its mobile checkout experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the state machine; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: clear system status; keyboard and screen-reader completion; and least-privilege action scope.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 09 — Wireframe Critique: Payout Reconciliation

## Objective

Produce a reviewable wireframe critique for payout reconciliation. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payout reconciliation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the wireframe critique; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: recovery without data loss; explicit money and time semantics; and human approval for irreversible effects.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 10 — Content Model: Voice Payment Status

## Objective

Produce a reviewable content model for voice payment status. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its voice payment status experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the content model; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: keyboard and screen-reader completion; evidence-linked AI output; and guardrail metrics and rollback.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 11 — Accessibility Audit: Pricing-Rule Simulation

## Objective

Produce a reviewable accessibility audit for pricing-rule simulation. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its pricing-rule simulation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the accessibility audit; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit money and time semantics; least-privilege action scope; and clear system status.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 12 — Responsive Behavior Spec: Ai Support Search

## Objective

Produce a reviewable responsive behavior spec for AI support search. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its AI support search experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the responsive behavior spec; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: evidence-linked AI output; human approval for irreversible effects; and recovery without data loss.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 13 — Design-Token Proposal: Merchant Kyb Onboarding

## Objective

Produce a reviewable design-token proposal for merchant KYB onboarding. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its merchant KYB onboarding experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the design-token proposal; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege action scope; guardrail metrics and rollback; and keyboard and screen-reader completion.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 14 — Usability-Test Plan: Subscription Cancellation

## Objective

Produce a reviewable usability-test plan for subscription cancellation. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its subscription cancellation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the usability-test plan; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: human approval for irreversible effects; clear system status; and explicit money and time semantics.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 15 — Experiment Brief: Cross-Border Transfer

## Objective

Produce a reviewable experiment brief for cross-border transfer. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its cross-border transfer experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the experiment brief; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: guardrail metrics and rollback; recovery without data loss; and evidence-linked AI output.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 16 — Ai Answer Card: Chargeback Evidence

## Objective

Produce a reviewable AI answer card for chargeback evidence. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its chargeback evidence experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the AI answer card; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: clear system status; keyboard and screen-reader completion; and least-privilege action scope.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 17 — Agent Approval Flow: Agent-Assisted Operations

## Objective

Produce a reviewable agent approval flow for agent-assisted operations. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its agent-assisted operations experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the agent approval flow; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: recovery without data loss; explicit money and time semantics; and human approval for irreversible effects.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 18 — Risk Review: Payment Failure Recovery

## Objective

Produce a reviewable risk review for payment failure recovery. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payment failure recovery experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the risk review; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: keyboard and screen-reader completion; evidence-linked AI output; and guardrail metrics and rollback.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 19 — Handoff Package: Enterprise Permissions

## Objective

Produce a reviewable handoff package for enterprise permissions. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its enterprise permissions experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the handoff package; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit money and time semantics; least-privilege action scope; and clear system status.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 20 — Design Qa Report: Mobile Checkout

## Objective

Produce a reviewable design QA report for mobile checkout. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its mobile checkout experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the design QA report; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: evidence-linked AI output; human approval for irreversible effects; and recovery without data loss.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 21 — Research Plan: Subscription Cancellation

## Objective

Produce a reviewable research plan for subscription cancellation. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its subscription cancellation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the research plan; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege action scope; guardrail metrics and rollback; and keyboard and screen-reader completion.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 22 — Interview Guide: Cross-Border Transfer

## Objective

Produce a reviewable interview guide for cross-border transfer. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its cross-border transfer experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the interview guide; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: human approval for irreversible effects; clear system status; and explicit money and time semantics.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 23 — Evidence Synthesis: Chargeback Evidence

## Objective

Produce a reviewable evidence synthesis for chargeback evidence. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its chargeback evidence experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the evidence synthesis; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: guardrail metrics and rollback; recovery without data loss; and evidence-linked AI output.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 24 — Jobs-To-Be-Done Map: Agent-Assisted Operations

## Objective

Produce a reviewable jobs-to-be-done map for agent-assisted operations. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its agent-assisted operations experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the jobs-to-be-done map; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: clear system status; keyboard and screen-reader completion; and least-privilege action scope.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 25 — Service Blueprint: Payment Failure Recovery

## Objective

Produce a reviewable service blueprint for payment failure recovery. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payment failure recovery experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the service blueprint; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: recovery without data loss; explicit money and time semantics; and human approval for irreversible effects.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 26 — Information Architecture: Enterprise Permissions

## Objective

Produce a reviewable information architecture for enterprise permissions. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its enterprise permissions experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the information architecture; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: keyboard and screen-reader completion; evidence-linked AI output; and guardrail metrics and rollback.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 27 — Task Flow: Mobile Checkout

## Objective

Produce a reviewable task flow for mobile checkout. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its mobile checkout experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the task flow; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit money and time semantics; least-privilege action scope; and clear system status.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 28 — State Machine: Payout Reconciliation

## Objective

Produce a reviewable state machine for payout reconciliation. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payout reconciliation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the state machine; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: evidence-linked AI output; human approval for irreversible effects; and recovery without data loss.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 29 — Wireframe Critique: Voice Payment Status

## Objective

Produce a reviewable wireframe critique for voice payment status. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its voice payment status experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the wireframe critique; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege action scope; guardrail metrics and rollback; and keyboard and screen-reader completion.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 30 — Content Model: Pricing-Rule Simulation

## Objective

Produce a reviewable content model for pricing-rule simulation. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its pricing-rule simulation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the content model; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: human approval for irreversible effects; clear system status; and explicit money and time semantics.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 31 — Accessibility Audit: Ai Support Search

## Objective

Produce a reviewable accessibility audit for AI support search. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its AI support search experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the accessibility audit; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: guardrail metrics and rollback; recovery without data loss; and evidence-linked AI output.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 32 — Responsive Behavior Spec: Merchant Kyb Onboarding

## Objective

Produce a reviewable responsive behavior spec for merchant KYB onboarding. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its merchant KYB onboarding experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the responsive behavior spec; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: clear system status; keyboard and screen-reader completion; and least-privilege action scope.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 33 — Design-Token Proposal: Subscription Cancellation

## Objective

Produce a reviewable design-token proposal for subscription cancellation. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its subscription cancellation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the design-token proposal; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: recovery without data loss; explicit money and time semantics; and human approval for irreversible effects.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 34 — Usability-Test Plan: Cross-Border Transfer

## Objective

Produce a reviewable usability-test plan for cross-border transfer. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its cross-border transfer experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the usability-test plan; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: keyboard and screen-reader completion; evidence-linked AI output; and guardrail metrics and rollback.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 35 — Experiment Brief: Chargeback Evidence

## Objective

Produce a reviewable experiment brief for chargeback evidence. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its chargeback evidence experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the experiment brief; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit money and time semantics; least-privilege action scope; and clear system status.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 36 — Ai Answer Card: Agent-Assisted Operations

## Objective

Produce a reviewable AI answer card for agent-assisted operations. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its agent-assisted operations experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the AI answer card; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: evidence-linked AI output; human approval for irreversible effects; and recovery without data loss.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 37 — Agent Approval Flow: Payment Failure Recovery

## Objective

Produce a reviewable agent approval flow for payment failure recovery. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payment failure recovery experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the agent approval flow; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege action scope; guardrail metrics and rollback; and keyboard and screen-reader completion.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 38 — Risk Review: Enterprise Permissions

## Objective

Produce a reviewable risk review for enterprise permissions. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its enterprise permissions experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the risk review; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: human approval for irreversible effects; clear system status; and explicit money and time semantics.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 39 — Handoff Package: Mobile Checkout

## Objective

Produce a reviewable handoff package for mobile checkout. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its mobile checkout experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the handoff package; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: guardrail metrics and rollback; recovery without data loss; and evidence-linked AI output.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 40 — Design Qa Report: Payout Reconciliation

## Objective

Produce a reviewable design QA report for payout reconciliation. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payout reconciliation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the design QA report; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: clear system status; keyboard and screen-reader completion; and least-privilege action scope.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 41 — Research Plan: Cross-Border Transfer

## Objective

Produce a reviewable research plan for cross-border transfer. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its cross-border transfer experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the research plan; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: recovery without data loss; explicit money and time semantics; and human approval for irreversible effects.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 42 — Interview Guide: Chargeback Evidence

## Objective

Produce a reviewable interview guide for chargeback evidence. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its chargeback evidence experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the interview guide; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: keyboard and screen-reader completion; evidence-linked AI output; and guardrail metrics and rollback.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 43 — Evidence Synthesis: Agent-Assisted Operations

## Objective

Produce a reviewable evidence synthesis for agent-assisted operations. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its agent-assisted operations experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the evidence synthesis; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit money and time semantics; least-privilege action scope; and clear system status.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 44 — Jobs-To-Be-Done Map: Payment Failure Recovery

## Objective

Produce a reviewable jobs-to-be-done map for payment failure recovery. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payment failure recovery experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the jobs-to-be-done map; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: evidence-linked AI output; human approval for irreversible effects; and recovery without data loss.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 45 — Service Blueprint: Enterprise Permissions

## Objective

Produce a reviewable service blueprint for enterprise permissions. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its enterprise permissions experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the service blueprint; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege action scope; guardrail metrics and rollback; and keyboard and screen-reader completion.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 46 — Information Architecture: Mobile Checkout

## Objective

Produce a reviewable information architecture for mobile checkout. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its mobile checkout experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the information architecture; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: human approval for irreversible effects; clear system status; and explicit money and time semantics.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 47 — Task Flow: Payout Reconciliation

## Objective

Produce a reviewable task flow for payout reconciliation. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payout reconciliation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the task flow; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: guardrail metrics and rollback; recovery without data loss; and evidence-linked AI output.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# Lab 48 — State Machine: Voice Payment Status

## Objective

Produce a reviewable state machine for voice payment status. The exercise tests whether a product manager and design partner can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its voice payment status experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the state machine; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: clear system status; keyboard and screen-reader completion; and least-privilege action scope.
5. Define one primary measure, two diagnostic measures, two guardrails, and a rollback trigger.

## Deliverable

A one-page decision summary, the working artifact, a validation checklist, and a short recommendation. A reviewer must be able to reproduce the reasoning without asking what the denominator, state, permission, or source of truth means.

## Model approach

Begin with the invariant: the system must not create a confident but incorrect outcome. Bound the first release to one eligible segment, record exclusions, and preserve a manual recovery path. Separate observed evidence from interpretation. Instrument entry, completion, failure class, recovery, and downstream correctness. Pilot behind a feature flag or controlled cohort; review qualitative evidence alongside aggregate metrics before broadening scope.

## Acceptance checks

- The grain and time boundary are explicit.
- Every important state has an owner and next action.
- Sensitive data and privileged actions are minimized.
- The recommendation includes trade-offs, residual risk, and a testable next step.
- The result can be audited after a failure.


# End-to-end cases

Use these cases for interview practice, portfolio narratives, and cross-functional reviews. Each case should produce an executive recommendation plus inspectable working artifacts.

# Case Study 01 — Redesign KYB without lowering fraud controls

## Executive brief

PayFlow must redesign kyb without lowering fraud controls while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce recovery without data loss, evidence-linked AI output, and guardrail metrics and rollback. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 02 — Explain a delayed payout

## Executive brief

PayFlow must explain a delayed payout while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce keyboard and screen-reader completion, least-privilege action scope, and clear system status. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 03 — Build a pricing simulator

## Executive brief

PayFlow must build a pricing simulator while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce explicit money and time semantics, human approval for irreversible effects, and recovery without data loss. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 04 — Contest a chargeback

## Executive brief

PayFlow must contest a chargeback while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce evidence-linked AI output, guardrail metrics and rollback, and keyboard and screen-reader completion. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 05 — Design accessible authentication

## Executive brief

PayFlow must design accessible authentication while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce least-privilege action scope, clear system status, and explicit money and time semantics. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 06 — Recover an interrupted transfer

## Executive brief

PayFlow must recover an interrupted transfer while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce human approval for irreversible effects, recovery without data loss, and evidence-linked AI output. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 07 — Introduce an AI support answer

## Executive brief

PayFlow must introduce an ai support answer while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce guardrail metrics and rollback, keyboard and screen-reader completion, and least-privilege action scope. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 08 — Approve an agent-created retry batch

## Executive brief

PayFlow must approve an agent-created retry batch while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce clear system status, explicit money and time semantics, and human approval for irreversible effects. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 09 — Design enterprise role management

## Executive brief

PayFlow must design enterprise role management while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce recovery without data loss, evidence-linked AI output, and guardrail metrics and rollback. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 10 — Reduce checkout failure

## Executive brief

PayFlow must reduce checkout failure while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce keyboard and screen-reader completion, least-privilege action scope, and clear system status. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 11 — Handle a real-time collaboration conflict

## Executive brief

PayFlow must handle a real-time collaboration conflict while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce explicit money and time semantics, human approval for irreversible effects, and recovery without data loss. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 12 — Launch a voice status experience

## Executive brief

PayFlow must launch a voice status experience while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce evidence-linked AI output, guardrail metrics and rollback, and keyboard and screen-reader completion. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Reusable operating templates

Copy these structures into briefs, reviews, and launch packets. Remove fields only when they are demonstrably irrelevant.

# Operating Template 01 — Opportunity brief

Use this template when preparing a opportunity brief for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 02 — Research plan

Use this template when preparing a research plan for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 03 — Interview guide

Use this template when preparing a interview guide for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 04 — Observation-to-insight sheet

Use this template when preparing a observation-to-insight sheet for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 05 — JTBD statement

Use this template when preparing a jtbd statement for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 06 — Journey map

Use this template when preparing a journey map for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 07 — Service blueprint

Use this template when preparing a service blueprint for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 08 — State inventory

Use this template when preparing a state inventory for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 09 — Content specification

Use this template when preparing a content specification for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 10 — Accessibility definition of done

Use this template when preparing a accessibility definition of done for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 11 — Usability test script

Use this template when preparing a usability test script for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 12 — Experiment plan

Use this template when preparing a experiment plan for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 13 — Design critique agenda

Use this template when preparing a design critique agenda for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 14 — AI UX disclosure card

Use this template when preparing a ai ux disclosure card for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 15 — Agent action approval

Use this template when preparing a agent action approval for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 16 — Risk register

Use this template when preparing a risk register for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 17 — Analytics event plan

Use this template when preparing a analytics event plan for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 18 — Handoff checklist

Use this template when preparing a handoff checklist for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 19 — Design QA checklist

Use this template when preparing a design qa checklist for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Operating Template 20 — Portfolio case-study outline

Use this template when preparing a portfolio case-study outline for product design work.

## Header

Owner; reviewers; decision date; version; status; linked evidence; affected users and systems.

## Required fields

1. Decision or question: one sentence, with the action it will inform.
2. Scope and non-goals: eligible population, exclusions, time boundary, and dependencies.
3. Definitions: grain, states, measures, permissions, and source of truth.
4. Evidence: observations, quantitative baseline, limitations, and confidence.
5. Proposed approach: sequence, alternatives considered, and trade-offs.
6. Failure handling: prevention, detection, recovery, escalation, and audit.
7. Measurement: primary outcome, diagnostics, guardrails, sample or rollout plan.
8. Operations: owner, support path, monitoring, rollback, and review date.

## Quality gate

The document is ready only when another practitioner can identify what changes, who is affected, what may fail, how correctness is checked, and what evidence will cause the team to continue, revise, or stop.


# Terminology mastery checklist

The core chapters introduce these terms in context. Use this checklist for revision and interviews: recognition is not mastery until you can connect a term to a decision, implementation, failure mode, and verification method.

## Mastery set 1

**affordance**, **constraint**, **feedback**, **mapping**, **mental model**, **information scent**, **progressive disclosure**, **recognition over recall**, **error prevention**, **undo**, **state machine**, **empty state**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.

## Mastery set 2

**responsive design**, **design token**, **component**, **pattern library**, **service blueprint**, **journey map**, **jobs to be done**, **usability**, **accessibility**, **WCAG**, **focus order**, **accessible name**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.

## Mastery set 3

**contrast**, **target size**, **screen reader**, **reduced motion**, **cognitive load**, **plain language**, **content model**, **microcopy**, **dark pattern**, **privacy by design**, **prototype**, **moderated test**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.

## Mastery set 4

**unmoderated test**, **task success**, **severity**, **metric tree**, **guardrail**, **sample ratio mismatch**, **INP**, **LCP**, **CLS**, **provenance**, **citation**, **calibration**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.

## Mastery set 5

**human in the loop**, **automation bias**, **agent**, **tool call**, **approval boundary**, **audit trail**, **least privilege**, **multimodal**, **latency budget**, **optimistic UI**, **stale state**, **maker-checker**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.

## Mastery set 6

**idempotency**, **reconciliation**, **finality**, **design QA**, **acceptance criterion**, **design debt**, **design ops**, **RACI**, **rollout**, **rollback**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.
