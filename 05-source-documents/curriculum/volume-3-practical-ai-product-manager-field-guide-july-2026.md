# PART I — THE AI PM OPERATING SYSTEM

## 1. What an excellent AI PM actually owns

An AI PM does not need to be the best model builder in the room. The job is to make uncertainty manageable: select a valuable problem, define acceptable behavior, assemble the data and evaluation system, shape a trustworthy experience, align specialists, and own the business result after launch. Technical fluency matters because every architecture choice changes product behavior, cost, risk, and speed.

### The vocabulary that changes the decision

### AI product

**Plain English.** A product whose value or behavior materially depends on learned or generative models.

**PM decision.** Decide whether AI is core, assistive, or merely implementation detail.

**Evidence to request.** User outcome plus model-quality and system-quality metrics.

**Watch for.** Calling any workflow with an API an AI product.

### Probabilistic behavior

**Plain English.** The same or similar input can produce different outputs or confidence levels.

**PM decision.** Specify ranges, abstention, review, and fallback instead of one perfect answer.

**Evidence to request.** Distribution of outcomes across a representative eval set.

**Watch for.** Writing deterministic acceptance criteria for nondeterministic behavior.

### AI PM

**Plain English.** The accountable product leader connecting user value, model behavior, data, UX, economics, and risk.

**PM decision.** Make trade-offs visible and assign owners for each layer.

**Evidence to request.** Decision log, eval scorecard, adoption, margin, and incident rates.

**Watch for.** Becoming a translator who never makes a decision.

### Model layer

**Plain English.** The learned component that maps inputs to predictions, rankings, representations, or generated content.

**PM decision.** Choose task capability and operating constraints before a vendor name.

**Evidence to request.** Task success, calibration, latency, cost, and safety.

**Watch for.** Benchmark shopping without testing the real workflow.

### Application layer

**Plain English.** Prompts, retrieval, tools, policies, code, UI, and feedback wrapped around a model.

**PM decision.** Treat most product quality as a system property.

**Evidence to request.** End-to-end task completion and recovery rate.

**Watch for.** Blaming the base model for orchestration or UX defects.

### Human-in-the-loop

**Plain English.** A designed handoff where people review, approve, correct, or take over.

**PM decision.** Place humans where impact or uncertainty justifies the delay.

**Evidence to request.** Escalation precision, reviewer load, override quality, and time-to-resolution.

**Watch for.** Adding manual review everywhere without capacity math.

### The operating playbook

1. Write the user decision or job in one sentence.

2. Name the minimum intelligence needed, including a non-AI baseline.

3. Define model, system, user, business, and risk metrics separately.

4. Map every failure to prevention, detection, response, and owner.

5. Keep a dated decision log and an eval-backed release gate.

### Say this in the room

- ‘The model is one component; the product is the controlled system around it.’

- ‘What failure rate is acceptable for this user and consequence?’

- ‘Show me the eval slice, not only the average.’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 2. Opportunity framing and minimum viable intelligence

Strong AI strategy starts with a painful decision or workflow, not a fashionable capability. The core PM move is to identify the minimum viable intelligence: the least complex mechanism that creates a meaningful outcome at an acceptable risk and cost. Rules, search, analytics, classical ML, generative AI, and agents are alternatives—not a maturity ladder.

### The vocabulary that changes the decision

### Minimum viable intelligence

**Plain English.** The least sophisticated intelligence that produces the target outcome.

**PM decision.** Start with rules or retrieval if they satisfy the job.

**Evidence to request.** Incremental outcome versus baseline per dollar and per unit risk.

**Watch for.** Starting with an autonomous agent because it demos well.

### AI suitability

**Plain English.** A structured test of value, data, tolerance for error, feedback, and economics.

**PM decision.** Reject use cases with weak data or catastrophic unreviewed failure.

**Evidence to request.** Feasibility score plus expected value under realistic error rates.

**Watch for.** Treating technical possibility as product viability.

### Task decomposition

**Plain English.** Breaking a workflow into observable steps with different uncertainty and permissions.

**PM decision.** Automate low-risk, measurable steps before the whole job.

**Evidence to request.** Success and error by step; handoff rate between steps.

**Watch for.** Evaluating only the final answer and hiding the weak stage.

### Baseline

**Plain English.** The simplest current process or model against which improvement is measured.

**PM decision.** Require a heuristic, search, or human baseline before model work.

**Evidence to request.** Lift, saved time, cost, and error change versus baseline.

**Watch for.** Comparing only against a previous model or public benchmark.

### Fault tolerance

**Plain English.** How much error a workflow can absorb before harm exceeds value.

**PM decision.** Match autonomy and review to consequence, reversibility, and detectability.

**Evidence to request.** Severity-weighted error and expected loss.

**Watch for.** Using raw accuracy as a proxy for risk.

### Reversibility

**Plain English.** How easily a wrong action can be undone.

**PM decision.** Allow more autonomy for cheap, observable, reversible actions.

**Evidence to request.** Rollback time, recovery success, and user remediation burden.

**Watch for.** Treating an editable draft like an irreversible payment.

### Expected value

**Plain English.** Probability-weighted benefit minus probability-weighted harm and total cost.

**PM decision.** Translate model metrics into money, time, trust, or safety.

**Evidence to request.** EV = gains from correct actions − losses from errors − operating cost.

**Watch for.** Selling accuracy improvements without business sensitivity analysis.

### The operating playbook

1. Map the current workflow, time, errors, and owners.

2. List decision points and the information available at each.

3. Score consequence, reversibility, observability, and frequency.

4. Select the simplest mechanism per step.

5. Pilot where value is measurable and blast radius is bounded.

### Say this in the room

- ‘Which user decision improves if this prediction is right?’

- ‘What is the non-model baseline?’

- ‘Where is autonomy earned rather than assumed?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

# PART II — TECHNICAL FLUENCY WITHOUT THE THEATER

## 3. ML essentials every PM must speak

Classical machine learning remains the right answer for many ranking, risk, forecasting, propensity, and anomaly problems. PMs need enough vocabulary to shape labels, metrics, thresholds, and monitoring. Volume 2 contains the mathematical depth; this chapter is the meeting-room layer.

### The vocabulary that changes the decision

### Supervised learning

**Plain English.** Learning a mapping from examples with known targets.

**PM decision.** Confirm that labels represent the decision you truly care about.

**Evidence to request.** Holdout performance, calibration, and stability by slice.

**Watch for.** Using convenient proxy labels that encode the old process.

### Unsupervised learning

**Plain English.** Finding structure without target labels, such as clusters or anomalies.

**PM decision.** Use for exploration or prioritization, then validate human meaning.

**Evidence to request.** Cluster stability, separation, downstream usefulness.

**Watch for.** Naming clusters as if the algorithm discovered causal personas.

### Feature

**Plain English.** An input signal supplied to a model.

**PM decision.** Ask whether it is available, fresh, lawful, and stable at decision time.

**Evidence to request.** Coverage, freshness, drift, missingness, and leakage tests.

**Watch for.** Using future information or post-outcome fields.

### Label

**Plain English.** The outcome a supervised model learns to predict.

**PM decision.** Define timing, quality, ambiguity, and adjudication.

**Evidence to request.** Inter-annotator agreement, latency, noise, and prevalence.

**Watch for.** Assuming database fields are ground truth.

### Precision

**Plain English.** Among predicted positives, the fraction truly positive.

**PM decision.** Optimize when false positives are expensive.

**Evidence to request.** TP / (TP + FP), by segment and threshold.

**Watch for.** Reporting precision without recall or base rate.

### Recall

**Plain English.** Among actual positives, the fraction found.

**PM decision.** Optimize when misses are expensive.

**Evidence to request.** TP / (TP + FN), by segment and threshold.

**Watch for.** Maximizing recall while overwhelming operations.

### Calibration

**Plain English.** Whether predicted probabilities match observed frequencies.

**PM decision.** Use calibrated scores for risk tiers and expected-value decisions.

**Evidence to request.** Reliability curves, Brier score, expected calibration error.

**Watch for.** Interpreting an uncalibrated score of 0.8 as 80% probability.

### Drift

**Plain English.** A meaningful change in inputs, relationships, or outcomes over time.

**PM decision.** Define which drift triggers investigation, retraining, or policy change.

**Evidence to request.** Feature, prediction, concept, and performance drift.

**Watch for.** Retraining automatically on every statistical alert.

### The operating playbook

1. Specify prediction moment and action moment.

2. Write label definition and exclusion rules.

3. Choose cost-sensitive metrics and operating thresholds.

4. Demand slice analysis for important populations and environments.

5. Define post-launch ground-truth delay and monitoring cadence.

### Say this in the room

- ‘What decision-time data is actually available?’

- ‘Which error is more expensive at this threshold?’

- ‘Is the score calibrated enough for this policy?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 4. Foundation models, tokens, context, and reasoning

Foundation models are broadly trained models adapted through instructions, context, tools, retrieval, or additional training. Their fluent output can disguise uncertainty, so PMs must distinguish capability from reliability. Model names change quickly; the durable choice is a capability-and-constraint profile tested on your workload.

### The vocabulary that changes the decision

### Foundation model

**Plain English.** A broadly trained model reusable across many downstream tasks and modalities.

**PM decision.** Decide whether broad capability outweighs cost, control, and specialization needs.

**Evidence to request.** Task evals, safety, latency, price, context, and deployment constraints.

**Watch for.** Equating parameter count or brand with product quality.

### Large language model

**Plain English.** A model trained primarily to predict and generate sequences of tokens.

**PM decision.** Use when language understanding or generation is central.

**Evidence to request.** Task success, factuality, instruction following, and cost.

**Watch for.** Treating fluent language as verified knowledge.

### Token

**Plain English.** A model’s unit of text processing; words may split into several tokens.

**PM decision.** Budget context and output in tokens, not pages.

**Evidence to request.** Input tokens, output tokens, cache hit rate, and truncation rate.

**Watch for.** Ignoring multilingual token inflation.

### Context window

**Plain English.** The maximum token budget available for instructions, inputs, history, retrieved evidence, and output.

**PM decision.** Allocate context deliberately and test long-context degradation.

**Evidence to request.** Useful-context recall, truncation, latency, and cost.

**Watch for.** Stuffing everything into context instead of retrieving and prioritizing.

### Reasoning model

**Plain English.** A model optimized to spend additional inference computation on complex tasks.

**PM decision.** Use where added quality exceeds latency and cost.

**Evidence to request.** Pass rate by task difficulty and compute setting.

**Watch for.** Paying for deep reasoning on extraction or templated work.

### Temperature

**Plain English.** A sampling control affecting output diversity, not factual certainty.

**PM decision.** Use low variation for repeatable workflows and higher variation for ideation.

**Evidence to request.** Variance and task success across repeated runs.

**Watch for.** Claiming temperature zero makes output deterministic or true.

### Structured output

**Plain English.** Generation constrained to a schema such as JSON.

**PM decision.** Use when downstream code or UI requires predictable fields.

**Evidence to request.** Schema-valid rate and semantic field accuracy.

**Watch for.** Valid JSON that contains incorrect meaning.

### Multimodality

**Plain English.** A model’s ability to process or produce multiple media types.

**PM decision.** Evaluate each modality and cross-modal interaction separately.

**Evidence to request.** Per-modality accuracy, synchronization, latency, and accessibility.

**Watch for.** Assuming text strength transfers to spatial, audio, or video tasks.

### The operating playbook

1. Write a model-agnostic capability profile.

2. Build a representative eval before vendor comparison.

3. Test at realistic context length and concurrency.

4. Pin production versions and record model/config changes.

5. Maintain a fallback for outage, regression, or policy change.

### Say this in the room

- ‘The model catalog is a market snapshot; our eval is the decision record.’

- ‘How much of this context is useful evidence?’

- ‘Does extra reasoning improve this task enough to pay for it?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 5. Prompting and context engineering

Prompting is interface design for a probabilistic component. Context engineering is broader: selecting instructions, examples, user state, retrieved evidence, tools, memory, schemas, and policies for each turn. A production prompt is versioned behavior, not clever prose hidden in a notebook.

### The vocabulary that changes the decision

### System instruction

**Plain English.** The highest-level behavioral guidance supplied by the application.

**PM decision.** Keep stable policy, role, boundaries, and output contract here.

**Evidence to request.** Instruction adherence and regression pass rate.

**Watch for.** Placing secrets or authorization rules in a prompt.

### Few-shot example

**Plain English.** A small set of input-output demonstrations in context.

**PM decision.** Use examples to define ambiguous format or judgment.

**Evidence to request.** Lift on target evals versus added tokens and bias.

**Watch for.** Examples that leak labels or narrow behavior incorrectly.

### Context engineering

**Plain English.** Assembling the right instructions, evidence, tools, memory, and state for a task.

**PM decision.** Treat context as a designed, measured pipeline.

**Evidence to request.** Context utilization, grounding, task success, and token efficiency.

**Watch for.** Optimizing wording while sending stale or irrelevant context.

### Prompt template

**Plain English.** A versioned structure with controlled variables.

**PM decision.** Separate stable instructions from untrusted user or retrieved content.

**Evidence to request.** Regression pass rate by template version.

**Watch for.** String concatenation that blurs trusted and untrusted instructions.

### Prompt injection

**Plain English.** Content that attempts to redirect model behavior or tool use.

**PM decision.** Assume untrusted text may contain adversarial instructions.

**Evidence to request.** Attack success rate, blocked actions, and detection coverage.

**Watch for.** Relying on a stronger system prompt as the sole defense.

### Chain of thought

**Plain English.** Intermediate reasoning behavior, sometimes internal and sometimes elicited.

**PM decision.** Evaluate final correctness and auditable evidence; do not require hidden reasoning disclosure.

**Evidence to request.** Task success and verifiable intermediate artifacts.

**Watch for.** Treating verbose reasoning as proof.

### Prompt caching

**Plain English.** Reusing computation for repeated prompt prefixes.

**PM decision.** Design stable prefixes where privacy and vendor semantics allow.

**Evidence to request.** Cache hit rate, latency, and cost savings.

**Watch for.** Caching user-specific or stale context under unsafe keys.

### The operating playbook

1. Define task, audience, boundaries, evidence, and output schema.

2. Separate trusted instructions from untrusted content.

3. Include only examples that represent intended variation.

4. Create adversarial and edge-case regression tests.

5. Version prompt, model, retrieval, tools, and policy together.

### Say this in the room

- ‘Prompt quality cannot compensate for missing evidence.’

- ‘This content is data, not an instruction.’

- ‘What changed in the full behavior bundle?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 6. RAG, search, embeddings, and knowledge systems

Retrieval-augmented generation (RAG) supplies external evidence at inference time. It can improve freshness, domain grounding, citations, and access control, but it does not guarantee truth. A RAG product is a search system plus a generation system plus a permission system, each with separate failure modes.

### The vocabulary that changes the decision

### Embedding

**Plain English.** A vector representation that places semantically related items near each other.

**PM decision.** Choose models and dimensionality using retrieval evals on your domain.

**Evidence to request.** Recall@k, ranking quality, latency, and index cost.

**Watch for.** Assuming semantic similarity equals factual relevance.

### Vector database

**Plain English.** A store optimized for nearest-neighbor search over embeddings.

**PM decision.** Evaluate filtering, tenancy, freshness, deletion, scale, and operations.

**Evidence to request.** Query latency, recall, ingest lag, and deletion SLA.

**Watch for.** Selecting on demo speed without access-control design.

### Chunking

**Plain English.** Splitting documents into retrievable units.

**PM decision.** Tune boundaries, size, overlap, and metadata to user questions.

**Evidence to request.** Evidence recall, context precision, citation granularity.

**Watch for.** Blind fixed-size chunks that sever tables or procedures.

### Hybrid retrieval

**Plain English.** Combining lexical and semantic retrieval.

**PM decision.** Use when exact identifiers and conceptual matches both matter.

**Evidence to request.** Recall and nDCG against either method alone.

**Watch for.** Adding components without ablation tests.

### Reranker

**Plain English.** A second-stage model that reorders retrieved candidates.

**PM decision.** Use when first-stage recall is good but top results are noisy.

**Evidence to request.** nDCG, MRR, context precision, and added latency.

**Watch for.** Reranking too few candidates to recover missing evidence.

### Grounding

**Plain English.** Constraining or supporting output with authoritative evidence.

**PM decision.** Define allowed sources and behavior when evidence is absent.

**Evidence to request.** Citation entailment, faithfulness, and abstention quality.

**Watch for.** Calling any retrieved text grounding.

### GraphRAG

**Plain English.** Retrieval that uses entities and relationships, often alongside text search.

**PM decision.** Use for connected questions spanning documents or records.

**Evidence to request.** Multi-hop answer accuracy and provenance completeness.

**Watch for.** Building a knowledge graph without stable entities or questions.

### Access-aware retrieval

**Plain English.** Filtering evidence according to the user’s permissions at query time.

**PM decision.** Make authorization deterministic outside the model.

**Evidence to request.** Unauthorized-retrieval rate must be zero; audit coverage.

**Watch for.** Retrieving broadly and asking the model not to reveal it.

### The operating playbook

1. Create question-evidence-answer triples from real work.

2. Measure retrieval before generation.

3. Preserve source, date, owner, and permissions in metadata.

4. Require citations that resolve to exact evidence.

5. Test stale, missing, conflicting, poisoned, and unauthorized content.

### Say this in the room

- ‘Did retrieval fail, or did generation misuse good evidence?’

- ‘What is the source of truth and its freshness SLA?’

- ‘Authorization happens before context reaches the model.’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 7. Agents, tools, MCP, A2A, and workflow automation

An agent is a system that uses a model to choose or sequence actions toward a goal. Agency is a spectrum: from one constrained tool call to long-running, multi-agent work. More autonomy increases the number of paths, permissions, and failure modes. Start with a deterministic workflow and add model-directed choice only where it creates measurable value.

### The vocabulary that changes the decision

### Tool calling

**Plain English.** A model selects a named function and structured arguments; application code executes it.

**PM decision.** Expose narrow, typed functions with explicit authorization.

**Evidence to request.** Tool selection, argument accuracy, execution success, and recovery.

**Watch for.** Saying the model executes tools when the application does.

### Agent

**Plain English.** A model-centered loop that observes, decides, acts, and updates state.

**PM decision.** Define goal, stop conditions, budgets, permissions, and supervision.

**Evidence to request.** Task success, step count, intervention, cost, and unsafe-action rate.

**Watch for.** Calling a scripted chain an agent to imply intelligence.

### Workflow

**Plain English.** A mostly predefined sequence of steps and branches.

**PM decision.** Prefer for repeatable, regulated, or high-volume operations.

**Evidence to request.** Completion, exception, cycle time, and determinism.

**Watch for.** Adding open-ended planning where rules already work.

### MCP

**Plain English.** An open protocol for connecting AI applications to tools, resources, and contextual services.

**PM decision.** Use to standardize integration, while evaluating auth and server trust.

**Evidence to request.** Connection reliability, tool correctness, permission scope, and auditability.

**Watch for.** Treating protocol compatibility as security certification.

### A2A

**Plain English.** An open protocol for discovery and task exchange among independent agent systems.

**PM decision.** Use when opaque agents must interoperate across teams or vendors.

**Evidence to request.** Discovery accuracy, task completion, identity, and traceability.

**Watch for.** Confusing agent-to-agent coordination with tool connectivity.

### Memory

**Plain English.** Stored state used across turns or tasks, ranging from session history to durable profiles.

**PM decision.** Define purpose, retention, consent, correction, and deletion.

**Evidence to request.** Usefulness, stale-memory rate, privacy incidents, and retrieval precision.

**Watch for.** Saving everything and calling it personalization.

### Human approval gate

**Plain English.** A deterministic checkpoint before consequential action.

**PM decision.** Require approval for high-impact, ambiguous, or irreversible steps.

**Evidence to request.** Approval precision, reviewer burden, bypass rate, and delay.

**Watch for.** A generic confirmation button with no understandable preview.

### Least privilege

**Plain English.** Giving each agent and tool only the permissions needed for the current task.

**PM decision.** Use scoped identities, narrow functions, and short-lived credentials.

**Evidence to request.** Permission exceptions, denied attempts, and blast radius.

**Watch for.** One powerful service account shared by every agent.

### The operating playbook

1. Start with a state diagram and deterministic happy path.

2. Define every tool’s inputs, outputs, scopes, side effects, and owner.

3. Set step, time, token, spend, retry, and recursion budgets.

4. Require preview and approval for consequential writes.

5. Trace each decision, tool call, result, identity, and policy outcome.

### Say this in the room

- ‘MCP connects an application to capabilities; A2A coordinates independent agents.’

- ‘What is the narrowest permission this step needs?’

- ‘What stops the loop?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 8. Multimodal, voice, vision, document, image, and video AI

Multimodal systems combine perception and generation across text, image, audio, video, and structured data. The UX bar is higher because timing, spatial references, accessibility, provenance, and user consent become first-class. Evaluate the complete interaction, not isolated model demos.

### The vocabulary that changes the decision

### Computer vision

**Plain English.** Models that classify, detect, segment, describe, or reason over images and video.

**PM decision.** Specify spatial task, environment, and acceptable misses.

**Evidence to request.** Per-class precision/recall, IoU, robustness, and review rate.

**Watch for.** Testing only curated images.

### OCR

**Plain English.** Converting visual text into machine-readable text, often with layout information.

**PM decision.** Treat OCR confidence and document structure as inputs to downstream logic.

**Evidence to request.** Character/word error, field accuracy, and document completion.

**Watch for.** Passing low-confidence text silently into decisions.

### Document AI

**Plain English.** Extraction and reasoning that preserves fields, tables, layout, and document type.

**PM decision.** Design per document family and exception path.

**Evidence to request.** Field F1, table accuracy, provenance, and straight-through processing.

**Watch for.** One prompt for every form and scan quality.

### Speech-to-text

**Plain English.** Transcribing audio into text, optionally with timestamps and speakers.

**PM decision.** Test accents, noise, code-switching, jargon, and consent.

**Evidence to request.** Word error, entity accuracy, diarization error, and latency.

**Watch for.** Optimizing average WER while missing critical names or numbers.

### Text-to-speech

**Plain English.** Generating spoken audio from text with controllable voice and style.

**PM decision.** Design pronunciation, interruption, disclosure, and fallback.

**Evidence to request.** Naturalness, pronunciation accuracy, time-to-first-audio, and complaints.

**Watch for.** Impersonation-like voices without consent or disclosure.

### Realtime model

**Plain English.** A low-latency streaming model for interactive audio or multimodal sessions.

**PM decision.** Budget turn latency across capture, network, model, tools, and playback.

**Evidence to request.** End-to-end latency, interruption success, and task completion.

**Watch for.** Measuring model latency but not conversational latency.

### Image/video generation

**Plain English.** Models that synthesize or edit visual media from instructions and references.

**PM decision.** Define rights, provenance, brand control, and review.

**Evidence to request.** Prompt adherence, visual defects, policy violations, and editability.

**Watch for.** Treating aesthetic quality as production readiness.

### Content provenance

**Plain English.** Metadata or signals that record origin and transformations of media.

**PM decision.** Preserve provenance across creation, editing, export, and publishing.

**Evidence to request.** Coverage, verification success, and metadata survival.

**Watch for.** Assuming watermarks alone solve deception.

### The operating playbook

1. Capture realistic devices, noise, lighting, accents, and document damage.

2. Evaluate critical entities and moments, not only aggregate similarity.

3. Design interruption, correction, replay, and accessible alternatives.

4. Disclose synthetic media where context requires it.

5. Keep source and transformation provenance through the workflow.

### Say this in the room

- ‘What is the critical field or moment that cannot be wrong?’

- ‘Can the user interrupt and correct naturally?’

- ‘Where does provenance survive export?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 9. Adaptation: fine-tuning, preference optimization, and synthetic data

Adaptation changes model behavior through additional training or learned components. It is appropriate when repeated prompting or retrieval cannot reliably create the required style, task behavior, or efficiency. It does not inject a live database of facts; use retrieval for frequently changing knowledge.

### The vocabulary that changes the decision

### Fine-tuning

**Plain English.** Additional training on task- or domain-specific examples.

**PM decision.** Use when behavior is repeated, data is strong, and gains survive evals.

**Evidence to request.** Task lift, regression, safety, training and serving cost.

**Watch for.** Fine-tuning to memorize facts that change weekly.

### Instruction tuning

**Plain English.** Training on instruction-response examples to improve task following.

**PM decision.** Use for consistent task behavior across many prompts.

**Evidence to request.** Instruction adherence and generalization to held-out tasks.

**Watch for.** Training on outputs that encode weak policies.

### PEFT

**Plain English.** Parameter-efficient fine-tuning that updates a small set of parameters.

**PM decision.** Use to reduce adaptation compute and store multiple variants.

**Evidence to request.** Quality versus full tuning, adapter size, and serving complexity.

**Watch for.** Assuming cheap training means cheap lifecycle management.

### LoRA

**Plain English.** A PEFT method that learns low-rank weight updates.

**PM decision.** Use for efficient specialization when supported by the model stack.

**Evidence to request.** Task lift, rank sensitivity, merge/serve overhead.

**Watch for.** Creating many ungoverned adapters.

### Quantization-aware adaptation

**Plain English.** Training or adapting with reduced numerical precision constraints.

**PM decision.** Use when deployment memory or latency is tight.

**Evidence to request.** Quality loss, throughput, memory, and hardware compatibility.

**Watch for.** Optimizing size before validating critical slices.

### Preference optimization

**Plain English.** Training from pairwise or scored preferences, including DPO-style methods.

**PM decision.** Use when desired behavior is easier to compare than specify.

**Evidence to request.** Win rate, judge reliability, safety and diversity regression.

**Watch for.** Collecting preferences without clear rubric or rater calibration.

### Synthetic data

**Plain English.** Model-generated examples used for training, testing, or augmentation.

**PM decision.** Use to cover rare cases, but validate realism and contamination.

**Evidence to request.** Utility on real holdout data, diversity, and error amplification.

**Watch for.** Training and testing on data from the same generator.

### Distillation

**Plain English.** Training a smaller model to imitate a stronger teacher.

**PM decision.** Use to reduce cost or latency for a bounded task.

**Evidence to request.** Retained task quality, latency, cost, and edge-case loss.

**Watch for.** Distilling teacher errors and hidden policy violations.

### The operating playbook

1. Prove the gap cannot be solved more simply.

2. Create a clean train/dev/test split with real holdout data.

3. Write data rights, provenance, and removal rules.

4. Run broad regression and safety tests, not only target-task lift.

5. Version base model, dataset, recipe, adapter, and eval results.

### Say this in the room

- ‘Retrieval changes what the model can see; fine-tuning changes how it behaves.’

- ‘What real holdout proves the synthetic data helped?’

- ‘What regressions did specialization introduce?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 10. Model selection, build/buy/host, and the July 2026 market

Model selection is a portfolio decision, not a leaderboard contest. Closed APIs can accelerate launch; open-weight models can improve control, customization, locality, or economics at sufficient scale. Production architecture may route among multiple models. Because catalogs move quickly, use dated snapshots only for discovery and pin decisions to your eval evidence.

### The vocabulary that changes the decision

### Closed model API

**Plain English.** A hosted proprietary model accessed as a service.

**PM decision.** Use for speed and managed capability when terms and controls fit.

**Evidence to request.** Quality, price, rate limits, residency, retention, and change policy.

**Watch for.** Assuming hosted means enterprise-ready for your data.

### Open-weight model

**Plain English.** Downloadable weights under a specific license, not necessarily open-source training.

**PM decision.** Use when control, locality, adaptation, or scale economics justify operations.

**Evidence to request.** License, quality, hardware, serving, security, and support.

**Watch for.** Calling weights open source without checking data, code, and license.

### Model router

**Plain English.** Logic that selects a model based on task, risk, cost, or confidence.

**PM decision.** Use when workloads are heterogeneous and routing can be evaluated.

**Evidence to request.** Routing accuracy, fallback rate, blended quality, latency, and cost.

**Watch for.** A cheap-first cascade that silently harms rare high-value tasks.

### Small language model

**Plain English.** A lower-capacity model optimized for cost, speed, privacy, or edge deployment.

**PM decision.** Use for bounded, frequent tasks with strong evals.

**Evidence to request.** Task-specific pass rate and total cost of ownership.

**Watch for.** Dismissing small models based on broad benchmark rank.

### Model-as-a-service

**Plain English.** Managed inference with vendor-operated infrastructure.

**PM decision.** Use when operational simplicity outweighs control requirements.

**Evidence to request.** SLA, quotas, observability, support, and exit time.

**Watch for.** No contingency for deprecation or region outage.

### Self-hosting

**Plain English.** Operating model weights and inference infrastructure yourself or through a managed host.

**PM decision.** Use when control or economics clearly exceed operational burden.

**Evidence to request.** Utilization, uptime, staffing, security, and amortized cost.

**Watch for.** Comparing GPU price with API price while ignoring people and idle capacity.

### Model portfolio

**Plain English.** A governed set of models assigned to approved tasks and risk tiers.

**PM decision.** Manage models as products with owners, versions, and retirement plans.

**Evidence to request.** Coverage, duplication, incident rate, spend, and migration readiness.

**Watch for.** Every team independently adding vendors.

### The operating playbook

1. Freeze a representative eval and traffic profile.

2. Compare at matched quality, context, latency, and concurrency.

3. Review data terms, retention, training use, residency, indemnity, and audit support.

4. Run exit and failover tests before dependency becomes critical.

5. Re-evaluate on a cadence without chasing every release.

### Say this in the room

- ‘We choose the system on our workload, not the benchmark headline.’

- ‘What is our migration time if this model disappears?’

- ‘Compare total cost at matched quality.’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

# PART III — BUILDING A PRODUCTION AI SYSTEM

## 11. Inference, serving, GPUs, latency, and scale

Inference is the production work of turning inputs into model outputs. User experience and gross margin depend on the full serving path: queues, preprocessing, retrieval, model computation, tool calls, safety checks, networks, and rendering. PMs should manage latency as a budget and cost as a workload model.

### The vocabulary that changes the decision

### Inference

**Plain English.** Running a trained model to produce a prediction or generation.

**PM decision.** Define performance at realistic input/output lengths and concurrency.

**Evidence to request.** End-to-end latency, throughput, errors, and cost per successful task.

**Watch for.** Quoting provider speed from a tiny prompt.

### GPU

**Plain English.** Parallel hardware commonly used for model training and inference.

**PM decision.** Match memory, precision, batch, and utilization to workload.

**Evidence to request.** Utilization, memory, tokens/sec, power, and cost.

**Watch for.** Assuming more expensive hardware always lowers unit cost.

### Time to first token

**Plain English.** Delay before the first generated token reaches the user.

**PM decision.** Optimize perceived responsiveness for streaming interactions.

**Evidence to request.** P50/P95 TTFT under realistic load.

**Watch for.** Fast first token followed by an unusably slow stream.

### Inter-token latency

**Plain English.** Delay between streamed output tokens.

**PM decision.** Optimize conversational flow and reading experience.

**Evidence to request.** P50/P95 time per output token.

**Watch for.** Reporting only total latency.

### Throughput

**Plain English.** Amount of work served per unit time.

**PM decision.** Plan capacity using realistic concurrency and sequence lengths.

**Evidence to request.** Requests/sec or tokens/sec at target SLA.

**Watch for.** Maximizing throughput while violating tail latency.

### Continuous batching

**Plain English.** Dynamically grouping inference work to improve accelerator use.

**PM decision.** Use for concurrent traffic, then tune fairness and latency.

**Evidence to request.** Utilization, throughput, P95 latency, and queue time.

**Watch for.** Large batches that starve interactive users.

### KV cache

**Plain English.** Stored attention state that avoids recomputing prior tokens during generation.

**PM decision.** Budget memory and reuse for long or repeated contexts.

**Evidence to request.** Cache memory, hit rate, evictions, and concurrency.

**Watch for.** Ignoring that long contexts reduce serving capacity.

### Quantization

**Plain English.** Reducing numerical precision to lower memory and increase speed.

**PM decision.** Use after task and safety regression tests.

**Evidence to request.** Memory, throughput, cost, and quality delta by slice.

**Watch for.** Accepting small average loss that breaks a critical edge case.

### The operating playbook

1. Create latency budgets for every stage.

2. Load-test realistic prompts, outputs, tools, and concurrency.

3. Separate interactive, batch, and premium traffic classes.

4. Track cost per successful user task, not per request alone.

5. Design capacity, fallback, degradation, and overload behavior.

### Say this in the room

- ‘Where is the P95 latency budget being spent?’

- ‘What is cost per successful task at production concurrency?’

- ‘How does context length change capacity?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 12. Data strategy, labeling, lineage, and feedback loops

Data strategy is the plan for obtaining, governing, improving, and learning from the information that creates product value. More data is not automatically better; relevant, representative, lawful, fresh, and well-labeled data is. Feedback loops need deliberate signal design or they amplify popularity, bias, and automation errors.

### The vocabulary that changes the decision

### Data contract

**Plain English.** A documented agreement about schema, meaning, quality, ownership, and change.

**PM decision.** Use between producing and consuming teams for critical signals.

**Evidence to request.** Freshness, completeness, validity, and breaking-change incidents.

**Watch for.** Treating schema compatibility as semantic compatibility.

### Data lineage

**Plain English.** Traceability from source through transformations to model and output.

**PM decision.** Require for debugging, deletion, audit, and trust.

**Evidence to request.** Lineage coverage and time to identify affected products.

**Watch for.** A dashboard with no field-level provenance.

### Point-in-time correctness

**Plain English.** Using only information available at the historical decision moment.

**PM decision.** Require for training and backtesting predictive systems.

**Evidence to request.** Leakage tests and offline-online parity.

**Watch for.** Joining the latest customer state to old outcomes.

### Annotation

**Plain English.** Human or automated assignment of labels or judgments.

**PM decision.** Define rubric, training, adjudication, quality, and worker conditions.

**Evidence to request.** Agreement, gold-set accuracy, cost, and turnaround.

**Watch for.** Majority vote on genuinely ambiguous policy.

### Active learning

**Plain English.** Selecting the most informative examples for labeling.

**PM decision.** Use when labels are expensive and uncertainty can guide sampling.

**Evidence to request.** Lift per labeled example and coverage of rare cases.

**Watch for.** Sampling only uncertain cases and losing representativeness.

### Weak supervision

**Plain English.** Combining noisy heuristics or sources to create probabilistic labels.

**PM decision.** Use to bootstrap when gold labels are scarce.

**Evidence to request.** Downstream lift against a clean holdout.

**Watch for.** Hiding heuristic bias behind a generated label.

### Feedback loop

**Plain English.** Product interactions that produce signals for improvement.

**PM decision.** Design explicit, attributable, and debiased feedback.

**Evidence to request.** Signal coverage, quality, delay, and effect on outcomes.

**Watch for.** Using clicks as universal truth.

### Data minimization

**Plain English.** Collecting and retaining only what is necessary for the purpose.

**PM decision.** Make purpose, retention, and deletion part of the product spec.

**Evidence to request.** Fields collected, retention compliance, and deletion SLA.

**Watch for.** Keeping raw prompts forever ‘for improvement.’

### The operating playbook

1. Inventory every source, owner, purpose, right, and retention rule.

2. Define labels and ambiguity before collecting at scale.

3. Build representative slices and rare-event coverage.

4. Separate product feedback, ground truth, and engagement proxies.

5. Test deletion through raw data, features, indexes, caches, and derivatives.

### Say this in the room

- ‘What did this field mean at decision time?’

- ‘Is this feedback a truth signal or an engagement signal?’

- ‘Can we honor deletion end to end?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 13. Evaluation: the discipline that separates demos from products

An eval is a repeatable test of behavior on defined examples with explicit scoring. High-performing teams treat evals as product infrastructure: they encode the user job, risk tolerance, and release bar. No single score is enough; use a portfolio of deterministic checks, human judgment, model-based grading, simulation, and online outcomes.

### The vocabulary that changes the decision

### Golden set

**Plain English.** A curated, versioned set of representative examples and expected behavior.

**PM decision.** Use for regression and release decisions, with protected holdout slices.

**Evidence to request.** Coverage, agreement, pass rate, and contamination checks.

**Watch for.** A tiny set authored only by the project team.

### Task success rate

**Plain English.** Fraction of cases where the user’s intended task is completed acceptably.

**PM decision.** Make the primary metric end-to-end and rubric-based.

**Evidence to request.** Success overall, by slice, and by failure severity.

**Watch for.** Substituting similarity metrics for useful completion.

### LLM-as-judge

**Plain English.** A model scores outputs using a rubric.

**PM decision.** Use for scale after calibrating against expert judgments.

**Evidence to request.** Agreement, bias, position sensitivity, and cost.

**Watch for.** Letting the same model family grade itself without controls.

### Pairwise evaluation

**Plain English.** Choosing the better of two outputs rather than assigning absolute scores.

**PM decision.** Use for preference and model comparisons.

**Evidence to request.** Win rate with confidence intervals and tie rate.

**Watch for.** No blinding or randomized output order.

### RAG evaluation

**Plain English.** Separate measurement of retrieval quality and grounded answer quality.

**PM decision.** Diagnose context recall, precision, faithfulness, and citation correctness.

**Evidence to request.** Recall@k, context precision, answer relevance, citation entailment.

**Watch for.** One answer score that cannot locate the defect.

### Agent evaluation

**Plain English.** Testing plans, tool selection, arguments, policy, recovery, and final outcome.

**PM decision.** Evaluate trajectories and side effects, not only final text.

**Evidence to request.** Task success, unsafe actions, steps, recovery, and cost.

**Watch for.** Rewarding a lucky final answer after unsafe actions.

### Adversarial evaluation

**Plain English.** Testing malicious, ambiguous, stressed, or out-of-distribution inputs.

**PM decision.** Maintain threat- and abuse-case suites in release gates.

**Evidence to request.** Attack success, unsafe action, data leakage, and refusal quality.

**Watch for.** A one-time red-team event before launch.

### Online evaluation

**Plain English.** Measurement with real users or production traffic.

**PM decision.** Use staged exposure with guardrails after offline qualification.

**Evidence to request.** Outcome lift, complaints, incidents, retention, and margin.

**Watch for.** A/B testing behavior that has not passed safety gates.

### The operating playbook

1. Start from user jobs and costly failures.

2. Sample real distributions plus strategic edge cases.

3. Write rubrics with positive, negative, and borderline examples.

4. Calibrate automated graders against qualified humans.

5. Version dataset, scorer, model, prompt, retrieval, tools, and policy.

### Say this in the room

- ‘What behavior does this score represent?’

- ‘Show the failure taxonomy and worst slices.’

- ‘Did the agent succeed safely, efficiently, and reproducibly?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 14. AI UX: trust, uncertainty, control, and graceful failure

AI UX should help users form the correct mental model: what the system can do, what evidence it used, how uncertain it is, and how to correct or take control. Trust is calibrated reliance, not maximum confidence. The best pattern often augments a workflow with previews and reversible drafts before automating it.

### The vocabulary that changes the decision

### Calibrated trust

**Plain English.** Users rely on the system in proportion to its real capability.

**PM decision.** Design evidence, limits, and recovery so reliance matches performance.

**Evidence to request.** Appropriate acceptance, verification, overrides, and harmful reliance.

**Watch for.** Marketing confidence that encourages overreliance.

### Abstention

**Plain English.** The system declines or escalates when evidence or confidence is insufficient.

**PM decision.** Define abstention conditions and a useful next path.

**Evidence to request.** Abstention precision, coverage, and recovery success.

**Watch for.** A generic ‘I cannot help’ dead end.

### Editable output

**Plain English.** AI output presented as a draft the user can modify.

**PM decision.** Use for creative or knowledge work where control matters.

**Evidence to request.** Edit distance, acceptance, completion time, and satisfaction.

**Watch for.** Counting unedited acceptance as proof of correctness.

### Citation UX

**Plain English.** Showing evidence and linking claims to exact sources.

**PM decision.** Use where verification and provenance matter.

**Evidence to request.** Citation coverage, entailment, click-through, and verification time.

**Watch for.** Decorative citations that do not support claims.

### Confidence display

**Plain English.** A representation of uncertainty or evidence strength.

**PM decision.** Show only when calibrated, actionable, and understandable.

**Evidence to request.** Calibration, comprehension, and decision quality.

**Watch for.** A precise percentage generated without statistical meaning.

### Progressive autonomy

**Plain English.** Increasing automation as evidence, controls, and user trust mature.

**PM decision.** Move from suggest to draft to approve to auto-act by risk tier.

**Evidence to request.** Override, error, incident, and autonomy-eligibility rates.

**Watch for.** One autonomy setting for all actions.

### Graceful degradation

**Plain English.** Preserving a useful safe experience during model, tool, or data failure.

**PM decision.** Define fallback content, manual paths, and status messaging.

**Evidence to request.** Fallback success, recovery time, and abandonment.

**Watch for.** Spinning indefinitely or silently returning stale output.

### Audit trail

**Plain English.** A human-readable and machine-queryable record of inputs, versions, evidence, actions, and approvals.

**PM decision.** Build for support, investigation, compliance, and user trust.

**Evidence to request.** Trace completeness and time to reconstruct a decision.

**Watch for.** Logging model text without identity, source, or version.

### The operating playbook

1. Map uncertainty and consequence at each user step.

2. Choose suggest, draft, approve, or auto-act deliberately.

3. Show evidence and source freshness where users can act on it.

4. Provide correction, undo, escalation, and accessible alternatives.

5. Test failure-state copy and fallbacks with real users.

### Say this in the room

- ‘Trust should be earned and calibrated, not designed as persuasion.’

- ‘What can the user inspect, correct, and undo?’

- ‘What useful state remains when AI is unavailable?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 15. Safety, security, privacy, and red teaming

AI safety concerns harmful behavior and impacts; security concerns adversarial compromise of confidentiality, integrity, and availability; privacy concerns appropriate data processing and individual rights. They overlap but require distinct owners and controls. Agentic systems raise risk because generated text can select real actions.

### The vocabulary that changes the decision

### Prompt injection

**Plain English.** Untrusted content manipulates model instructions or tool behavior.

**PM decision.** Treat all external content as untrusted and isolate authority.

**Evidence to request.** Attack success, secret leakage, unauthorized actions, and coverage.

**Watch for.** Trying to ‘solve’ injection with prompt wording alone.

### Jailbreak

**Plain English.** An input designed to bypass model safety behavior.

**PM decision.** Test abuse cases and apply layered policy enforcement.

**Evidence to request.** Unsafe response rate and refusal quality.

**Watch for.** Measuring refusal rate without false refusals.

### Excessive agency

**Plain English.** Too much functionality, permission, or autonomy allows damaging action.

**PM decision.** Minimize tools, scopes, side effects, and autonomous writes.

**Evidence to request.** Unsafe-action rate, blast radius, and approval bypass.

**Watch for.** A broad tool behind a friendly agent persona.

### Data exfiltration

**Plain English.** Unauthorized extraction of sensitive information through outputs, tools, logs, or retrieval.

**PM decision.** Enforce access outside the model and inspect data flows.

**Evidence to request.** Leakage tests, DLP alerts, and affected-record count.

**Watch for.** Relying on the model to remember confidentiality.

### Model supply chain

**Plain English.** Models, datasets, adapters, code, and dependencies that can be compromised.

**PM decision.** Track provenance, signatures, licenses, vulnerabilities, and vendors.

**Evidence to request.** Verified artifacts, patch SLA, and dependency exposure.

**Watch for.** Downloading untrusted weights into production.

### Red teaming

**Plain English.** Structured adversarial testing by people and automation.

**PM decision.** Run before launch and continuously after system changes.

**Evidence to request.** Coverage, severity, remediation time, and recurrence.

**Watch for.** A theatrical one-day exercise with no regression suite.

### Privacy threat model

**Plain English.** Analysis of how personal or sensitive data can be collected, inferred, exposed, or retained.

**PM decision.** Perform for prompts, logs, training, retrieval, memory, and vendors.

**Evidence to request.** Data-flow coverage, rights requests, leakage, and retention compliance.

**Watch for.** Reviewing only the model provider’s privacy page.

### Sandbox

**Plain English.** An isolated environment limiting code, files, network, and system effects.

**PM decision.** Use for untrusted code or tool execution with resource limits.

**Evidence to request.** Escape attempts, policy violations, and containment success.

**Watch for.** Calling a container a sandbox without network and credential controls.

### The operating playbook

1. Draw trust boundaries and data flows.

2. Threat-model identities, prompts, retrieval, memory, tools, outputs, and logs.

3. Enforce authorization and policy in deterministic systems.

4. Minimize permissions and require approval for consequential actions.

5. Turn every red-team finding into a regression test and owner.

### Say this in the room

- ‘The model is not the authorization layer.’

- ‘Which untrusted content can influence this action?’

- ‘What is the maximum blast radius of one bad trajectory?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 16. Responsible AI, governance, standards, and July 2026 regulation

Governance is the operating system for accountable AI decisions: inventory, risk tiering, evidence, approvals, monitoring, incidents, and retirement. Legal requirements vary by role, sector, geography, and system use. As of 14 July 2026, EU AI Act implementation is approaching another major application date on 2 August 2026, while some high-risk timelines have been changed or proposed through later political agreements; verify final legal text and local counsel before acting.

### The vocabulary that changes the decision

### Risk tiering

**Plain English.** Classifying systems by impact, autonomy, data, users, and legal category.

**PM decision.** Apply proportionate evidence, approval, and monitoring.

**Evidence to request.** Inventory coverage, tier accuracy, and overdue controls.

**Watch for.** Tiering by model size rather than use and consequence.

### Algorithmic impact assessment

**Plain English.** A documented analysis of purpose, affected people, benefits, risks, and mitigations.

**PM decision.** Use before high-impact deployment and material change.

**Evidence to request.** Assessment completeness and closure of mitigations.

**Watch for.** A compliance form completed after launch.

### Model card

**Plain English.** A structured record of model purpose, data, performance, limitations, and use constraints.

**PM decision.** Require from builders or vendors and connect to system evidence.

**Evidence to request.** Coverage, freshness, and unresolved limitations.

**Watch for.** Treating a model card as the whole product risk assessment.

### System card

**Plain English.** Documentation of the end-to-end system, evaluations, safeguards, and limitations.

**PM decision.** Use for complex generative and agentic products.

**Evidence to request.** Evidence completeness and release-gate traceability.

**Watch for.** Documenting only the base model.

### NIST AI RMF

**Plain English.** A voluntary US framework organized around Govern, Map, Measure, and Manage.

**PM decision.** Use as a common risk-management vocabulary and evidence map.

**Evidence to request.** Outcome coverage and control effectiveness.

**Watch for.** Using the framework as a checkbox list.

### ISO/IEC 42001

**Plain English.** An AI management-system standard based on continual improvement.

**PM decision.** Use to structure organization-wide policy, roles, risk, and audit.

**Evidence to request.** Management-system effectiveness and corrective actions.

**Watch for.** Confusing certification with product safety.

### EU AI Act

**Plain English.** A risk-based EU regulation with obligations depending on actor and use category.

**PM decision.** Determine provider/deployer role, category, geography, and application date with counsel.

**Evidence to request.** Control readiness and evidence for applicable obligations.

**Watch for.** Assuming every AI feature has the same obligations.

### AI literacy

**Plain English.** Organizational capability to understand appropriate use, limits, and risks.

**PM decision.** Train by role and measure behavior, not attendance alone.

**Evidence to request.** Scenario performance, policy adherence, and incident trends.

**Watch for.** A generic annual awareness video.

### The operating playbook

1. Maintain an AI system inventory and accountable owner.

2. Classify use, impact, users, geography, actor role, and autonomy.

3. Map required evidence to design, data, eval, security, UX, and operations.

4. Set material-change triggers for renewed review.

5. Verify current laws, guidance, and standards with qualified specialists.

### Say this in the room

- ‘Govern the use case and system, not just the model.’

- ‘Which role and application date apply to us?’

- ‘What evidence shows this control works in practice?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 17. MLOps, LLMOps, observability, and release engineering

MLOps and LLMOps are the practices that make AI systems reproducible, deployable, observable, and maintainable. A release is a bundle of model, prompt, data, retrieval, tool, policy, and application changes. Observability should let the team reconstruct a failed outcome without indiscriminately retaining sensitive content.

### The vocabulary that changes the decision

### Model registry

**Plain English.** A controlled catalog of model versions, metadata, approvals, and deployment state.

**PM decision.** Use as the source of truth for promotion and retirement.

**Evidence to request.** Registered coverage, approval status, and rollback readiness.

**Watch for.** A file store with no governance state.

### Experiment tracking

**Plain English.** Recording datasets, code, parameters, runs, metrics, and artifacts.

**PM decision.** Require reproducibility for consequential decisions.

**Evidence to request.** Reproducible run rate and missing metadata.

**Watch for.** Selecting a run whose data cannot be reconstructed.

### CI/CD for AI

**Plain English.** Automated validation and staged delivery of code plus AI behavior changes.

**PM decision.** Gate schema, data, eval, safety, security, and performance.

**Evidence to request.** Gate pass rate, escaped regressions, and lead time.

**Watch for.** Deploying prompt edits outside release controls.

### Shadow deployment

**Plain English.** Running a candidate on production inputs without affecting users.

**PM decision.** Use to measure realistic behavior and cost safely.

**Evidence to request.** Agreement, slice regressions, latency, and resource load.

**Watch for.** Logging sensitive shadow outputs without purpose controls.

### Canary

**Plain English.** Exposing a small controlled share to a new version.

**PM decision.** Use with auto-pause guardrails and rapid rollback.

**Evidence to request.** Outcome, incidents, latency, cost, and rollback time.

**Watch for.** A canary too small to observe rare high-severity failures.

### Trace

**Plain English.** A connected record of steps, spans, tool calls, retrieval, and timings for one request or task.

**PM decision.** Use for debugging agents and multi-stage pipelines.

**Evidence to request.** Trace coverage, sampling, overhead, and diagnosis time.

**Watch for.** Capturing sensitive content by default.

### SLO

**Plain English.** A target reliability level for a user-relevant service measure.

**PM decision.** Define for latency, availability, freshness, quality, and recovery.

**Evidence to request.** Compliance and error-budget burn.

**Watch for.** An uptime SLO that ignores unusable outputs.

### Rollback

**Plain English.** Returning safely to a previously qualified configuration.

**PM decision.** Pre-plan compatibility, state, and data implications.

**Evidence to request.** Time to detect, decide, and restore.

**Watch for.** Rolling back code while leaving a changed index or policy.

### The operating playbook

1. Create one version manifest for the behavior bundle.

2. Automate deterministic and behavioral gates.

3. Use shadow, canary, ramp, and rollback based on risk.

4. Trace enough to diagnose while minimizing sensitive content.

5. Run game days for provider outage, regression, leakage, and cost spikes.

### Say this in the room

- ‘Which component changed in the behavior bundle?’

- ‘Can we reproduce this exact trajectory?’

- ‘What automatically pauses the rollout?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

# PART IV — PRODUCT EXECUTION AND ECONOMICS

## 18. Unit economics, latency-quality-cost trade-offs, and FinOps

AI economics are workload economics. Cost depends on input size, output size, reasoning effort, retrieval, tool calls, retries, cache behavior, model route, hosting utilization, and human review. The useful denominator is usually cost per successful task or per business outcome—not price per token.

### The vocabulary that changes the decision

### Cost per successful task

**Plain English.** Total variable and allocated cost divided by acceptably completed tasks.

**PM decision.** Use as the primary unit metric for AI workflows.

**Evidence to request.** Model + retrieval + tools + infra + review + retries / successes.

**Watch for.** Optimizing cheap calls that fail and are retried.

### Gross margin

**Plain English.** Revenue minus direct delivery cost as a share of revenue.

**PM decision.** Model AI usage and support cost by customer and feature.

**Evidence to request.** Contribution margin by cohort and workload.

**Watch for.** Unlimited usage pricing with unbounded inference cost.

### Token economics

**Plain English.** How input, output, cached, and reasoning tokens drive hosted-model cost.

**PM decision.** Reduce unnecessary context and outputs after protecting quality.

**Evidence to request.** Tokens and dollars by feature, tenant, and success.

**Watch for.** Blanket token limits that truncate valuable tasks.

### Cache

**Plain English.** Stored result or computation reused for equivalent work.

**PM decision.** Use where freshness, privacy, and invalidation are understood.

**Evidence to request.** Hit rate, quality, staleness, and savings.

**Watch for.** Semantic reuse across users or permissions.

### Cascade

**Plain English.** Trying a cheaper model first and escalating uncertain cases.

**PM decision.** Use when confidence or task type predicts quality reliably.

**Evidence to request.** Escalation, blended success, latency, and savings.

**Watch for.** Cheap model errors that look confident and never escalate.

### Rate limit

**Plain English.** A cap on request or token volume over time.

**PM decision.** Design quotas, queues, priorities, and vendor headroom.

**Evidence to request.** Throttle rate, queue time, and dropped work.

**Watch for.** Discovering provider limits during launch.

### Cost guardrail

**Plain English.** A budget or anomaly rule that pauses, degrades, or alerts.

**PM decision.** Use by tenant, workflow, tool, and incident mode.

**Evidence to request.** Budget burn, anomalies caught, and false alarms.

**Watch for.** A monthly invoice review after runaway loops.

### Value sensitivity

**Plain English.** How business outcome changes across model-quality or adoption scenarios.

**PM decision.** Run downside/base/upside analysis before investment.

**Evidence to request.** NPV or payback across error, volume, and cost assumptions.

**Watch for.** A single ROI number built from best-case assumptions.

### The operating playbook

1. Build a request-level cost ledger across all components.

2. Measure successful-task denominator and human exception cost.

3. Model P50 and P95 workloads, not an average prompt.

4. Test routing, caching, batching, and shorter output with eval protection.

5. Create per-tenant quotas and loop/retry spend limits.

### Say this in the room

- ‘What does one successful user job cost end to end?’

- ‘Which quality loss buys this saving?’

- ‘How does margin change at the 95th-percentile workload?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 19. The AI PRD and behavior contract

An AI PRD must describe more than features. It should bind user value to behavior, evidence, uncertainty, data, metrics, controls, economics, and operations. Engineers need enough precision to build a testable system; reviewers need enough evidence to understand risk; users need an experience that communicates limits.

### The vocabulary that changes the decision

### Behavior contract

**Plain English.** A testable description of expected, allowed, disallowed, and fallback behavior.

**PM decision.** Write examples and rubrics for normal, edge, and adversarial cases.

**Evidence to request.** Contract coverage and release pass rate.

**Watch for.** Vague instructions such as ‘be accurate and safe.’

### Eval contract

**Plain English.** The datasets, rubrics, graders, thresholds, slices, and owners governing release.

**PM decision.** Agree before model optimization begins.

**Evidence to request.** Gate stability, disagreement, and escaped failures.

**Watch for.** Changing the test after seeing results.

### Data contract

**Plain English.** Requirements for source, fields, freshness, rights, quality, and deletion.

**PM decision.** Attach to each critical input and output.

**Evidence to request.** Contract SLOs and incidents.

**Watch for.** A dataset name without ownership or semantics.

### Autonomy policy

**Plain English.** Rules mapping action risk to suggest, draft, approve, or auto-act.

**PM decision.** Specify per tool and action, not per agent persona.

**Evidence to request.** Unauthorized actions, approvals, overrides, and incidents.

**Watch for.** ‘Human in the loop’ with no defined checkpoint.

### Failure taxonomy

**Plain English.** A shared classification of ways the system can fail.

**PM decision.** Use to drive evals, UX, alerts, and ownership.

**Evidence to request.** Coverage, severity, recurrence, and time to mitigate.

**Watch for.** A catch-all hallucination bucket.

### Nonfunctional requirement

**Plain English.** A requirement for latency, availability, privacy, security, accessibility, cost, or scale.

**PM decision.** Make targets measurable by traffic class and risk tier.

**Evidence to request.** SLO compliance and error-budget burn.

**Watch for.** ‘Fast’ or ‘enterprise-grade’ without numbers.

### Launch gate

**Plain English.** Evidence and approvals required before exposure increases.

**PM decision.** Make objective, risk-tiered, and reversible.

**Evidence to request.** Gate exceptions and post-launch incidents.

**Watch for.** Executive enthusiasm overriding missing evidence silently.

### The operating playbook

1. State user job, current baseline, and target outcome.

2. Define system boundary and why AI is appropriate.

3. Specify behavior with examples, abstention, fallback, and autonomy.

4. Attach eval, data, security, privacy, economics, and observability plans.

5. Name launch gates, owners, escalation, rollback, and retirement triggers.

### Say this in the room

- ‘What is the behavior contract, not just the feature description?’

- ‘Which evidence qualifies this for launch?’

- ‘Who owns each failure class after launch?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 20. Discovery, prototyping, and technical feasibility

AI prototyping should reduce the largest uncertainty, not maximize demo polish. A concierge test may validate demand; a prompt-and-spreadsheet prototype may validate information flow; a coded vertical slice may validate latency and tool integration. Keep prototypes clearly separated from production claims and sensitive data.

### The vocabulary that changes the decision

### Wizard-of-Oz test

**Plain English.** Users experience an automated-looking service partly operated by humans.

**PM decision.** Use to validate value and interaction before expensive automation.

**Evidence to request.** Demand, completion, willingness to pay, and operator effort.

**Watch for.** Concealing material human involvement in sensitive contexts.

### Concierge test

**Plain English.** A high-touch manual service that learns the workflow and desired outcome.

**PM decision.** Use for discovery with a small number of users.

**Evidence to request.** Repeated jobs, outcome value, and process variance.

**Watch for.** Scaling manual work before identifying repeatable structure.

### Technical spike

**Plain English.** Time-boxed engineering work to answer a feasibility question.

**PM decision.** Use for unknowns such as latency, permissions, or model capability.

**Evidence to request.** Decision reached, evidence quality, and follow-up risk.

**Watch for.** A spike that becomes unowned production code.

### Vertical slice

**Plain English.** A thin end-to-end implementation across UI, data, model, and operations.

**PM decision.** Use to reveal integration and experience constraints.

**Evidence to request.** End-to-end success, latency, cost, and exceptions.

**Watch for.** A backend demo with no real user or permission path.

### Prototype eval

**Plain English.** A small but representative test used during discovery.

**PM decision.** Use before interpreting demo anecdotes.

**Evidence to request.** Task pass rate and failure patterns.

**Watch for.** Testing only prompts that were used to tune the prototype.

### Feasibility envelope

**Plain English.** The range of inputs and conditions where the system works acceptably.

**PM decision.** Use to scope the initial product honestly.

**Evidence to request.** Coverage of target traffic and boundary failure rate.

**Watch for.** Presenting average quality as universal capability.

### Production gap

**Plain English.** The work between a demo and a reliable, secure, governed service.

**PM decision.** Make the gap visible in roadmap and cost.

**Evidence to request.** Open requirements across eval, safety, data, infra, UX, and ops.

**Watch for.** Calling an API proof-of-concept 80% done.

### The operating playbook

1. Name the riskiest assumption: desirability, data, capability, UX, economics, or compliance.

2. Choose the cheapest experiment that can falsify it.

3. Use synthetic or approved data and narrow permissions.

4. Record both successes and failure boundaries.

5. End with a decision: stop, reshape, deepen, or productionize.

### Say this in the room

- ‘Which uncertainty will this prototype retire?’

- ‘What is the demonstrated feasibility envelope?’

- ‘What remains between this demo and a production service?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 21. Experimentation, launch, adoption, and change management

A technically good AI feature can fail because users do not understand when to use it, managers do not redesign the workflow, or operations cannot absorb exceptions. Launch is a staged learning system. Measure exposure, activation, repeated use, outcome, quality, trust, cost, and harm separately.

### The vocabulary that changes the decision

### Shadow mode

**Plain English.** Producing outputs without affecting user decisions.

**PM decision.** Use to compare with current process and observe real distributions.

**Evidence to request.** Agreement, counterfactual value, latency, and cost.

**Watch for.** Assuming agreement with the old process proves correctness.

### A/B test

**Plain English.** Randomized comparison of product variants.

**PM decision.** Use after safety qualification when interference and spillovers are manageable.

**Evidence to request.** Outcome lift with confidence intervals and guardrails.

**Watch for.** Testing a risky behavior before offline evaluation.

### Interleaving

**Plain English.** Mixing ranked outputs from two systems for sensitive comparison.

**PM decision.** Use for search or recommendation ranking with less traffic.

**Evidence to request.** Preference attribution and win rate.

**Watch for.** Using where outcomes cannot be attributed cleanly.

### Guardrail metric

**Plain English.** A measure that must not degrade while optimizing a primary outcome.

**PM decision.** Define user, risk, operational, and economic guardrails.

**Evidence to request.** Threshold breaches and time to detect.

**Watch for.** A long dashboard with no stopping rule.

### Feature adoption

**Plain English.** Meaningful use by the intended user for the intended job.

**PM decision.** Measure activation, repeat, depth, and retained outcome.

**Evidence to request.** Eligible → exposed → tried → succeeded → repeated funnel.

**Watch for.** Counting button clicks as adoption.

### Workflow change

**Plain English.** Redesign of roles, decisions, handoffs, and incentives around the AI system.

**PM decision.** Plan training, policy, operations, and management behavior.

**Evidence to request.** Cycle time, exception load, override, and role clarity.

**Watch for.** Dropping AI into the old workflow and expecting transformation.

### Champion/challenger

**Plain English.** A qualified candidate competes with the current production system.

**PM decision.** Use for controlled continuous improvement.

**Evidence to request.** Lift, stability, cost, and rollback readiness.

**Watch for.** Replacing the champion on one aggregate score.

### The operating playbook

1. Launch internal or low-risk cohorts first.

2. Instrument the full adoption and outcome funnel.

3. Train users on appropriate use, limits, verification, and escalation.

4. Staff exceptions and support before exposure grows.

5. Hold scheduled evidence reviews with explicit ramp or rollback decisions.

### Say this in the room

- ‘Adoption means a successful repeated job, not a click.’

- ‘What changes in the human workflow?’

- ‘Which guardrail automatically stops the ramp?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 22. Go-to-market, pricing, packaging, and customer trust

AI value is not ‘access to a model.’ Customers buy faster work, better decisions, new capability, or lower risk. Packaging should align price with durable value while protecting margin and setting realistic expectations. Enterprise buyers need evidence about data use, security, reliability, governance, and exit—not superlatives.

### The vocabulary that changes the decision

### AI-native product

**Plain English.** A product whose workflow or value proposition is designed around learned or generative capability.

**PM decision.** Use the label only when AI changes the job, not just copywriting.

**Evidence to request.** Outcome differentiation, retention, and defensibility.

**Watch for.** A conventional product with a chat box.

### AI-enabled feature

**Plain English.** AI augments an existing workflow or product capability.

**PM decision.** Package based on incremental value and cost.

**Evidence to request.** Adoption, outcome lift, attach rate, and margin.

**Watch for.** Forcing AI into every plan without user need.

### Usage pricing

**Plain English.** Charging by requests, tokens, minutes, images, or completed actions.

**PM decision.** Use when usage correlates with value and customers can predict spend.

**Evidence to request.** Revenue, gross margin, variance, and bill disputes.

**Watch for.** Exposing technical tokens customers cannot forecast.

### Outcome pricing

**Plain English.** Charging based on an achieved business result.

**PM decision.** Use only where outcome attribution and risk sharing are clear.

**Evidence to request.** Verified outcomes, disputes, margin, and gaming.

**Watch for.** Claiming causality for correlated results.

### Fair-use limit

**Plain English.** A policy bounding expensive or abusive consumption within a package.

**PM decision.** Make transparent, measurable, and paired with controls.

**Evidence to request.** Limit hits, upgrades, churn, and margin.

**Watch for.** Vague throttling after customers build dependence.

### Trust center

**Plain English.** A maintained destination for security, privacy, governance, reliability, and AI documentation.

**PM decision.** Use to make evidence discoverable and current.

**Evidence to request.** Diligence cycle time and document freshness.

**Watch for.** Marketing claims without control evidence.

### Expectation setting

**Plain English.** Communicating capability, limitations, and user responsibilities.

**PM decision.** Use in sales, onboarding, UI, and support.

**Evidence to request.** Expectation gaps, complaints, overrides, and renewal.

**Watch for.** Promising human-level accuracy.

### The operating playbook

1. Name the customer outcome in operational terms.

2. Quantify willingness to pay and total cost to serve by segment.

3. Choose pricing meter customers understand and can control.

4. Publish clear data, model, limitation, and reliability commitments.

5. Equip sales and support with approved claims and escalation paths.

### Say this in the room

- ‘We sell the completed job, not the token.’

- ‘Which customer-controlled meter predicts the bill?’

- ‘What evidence supports this claim?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

# PART V — ENTERPRISE LEADERSHIP

## 23. Vendor diligence, procurement, contracts, and exit planning

AI procurement is product architecture. A vendor decision shapes data flows, model change risk, reliability, rights, security, cost, and future leverage. Diligence should connect contractual promises to technical controls and operating evidence. Always design an exit path before switching cost grows.

### The vocabulary that changes the decision

### Data retention

**Plain English.** How long a provider stores prompts, outputs, files, logs, or state.

**PM decision.** Verify defaults, controls, exceptions, backups, and deletion evidence.

**Evidence to request.** Retention configuration and deletion SLA.

**Watch for.** ‘Zero retention’ that excludes abuse logs or integrations.

### Training use

**Plain English.** Whether customer data may improve or train provider models.

**PM decision.** Require explicit terms for all services and subprocessors.

**Evidence to request.** Policy exceptions and audit evidence.

**Watch for.** Assuming API data and consumer-product data share terms.

### Data residency

**Plain English.** The geographic location where data is processed or stored.

**PM decision.** Map each service, failover, support, and subprocessor path.

**Evidence to request.** In-region coverage and exception events.

**Watch for.** A storage region that ignores processing or support access.

### Model change policy

**Plain English.** How a provider versions, deprecates, and changes behavior.

**PM decision.** Require notice, pinned versions where possible, and migration support.

**Evidence to request.** Notice period, regressions, and migration time.

**Watch for.** Using a ‘latest’ alias for regulated production.

### Indemnity

**Plain English.** Contractual allocation of specified third-party claims or losses.

**PM decision.** Review scope, exclusions, caps, and product usage requirements with counsel.

**Evidence to request.** Coverage gaps and unresolved exceptions.

**Watch for.** Treating indemnity as proof of lawful training data.

### SLA

**Plain English.** A contractual service commitment with remedies.

**PM decision.** Align uptime, latency, support, and recovery to product needs.

**Evidence to request.** SLA compliance and business impact.

**Watch for.** Credits that do not compensate operational harm.

### Exit plan

**Plain English.** A tested path to replace, export, or shut down a vendor dependency.

**PM decision.** Define data export, compatibility, evals, timeline, and fallback.

**Evidence to request.** Time to migrate, switching cost, and recovered artifacts.

**Watch for.** Discovering proprietary state cannot be exported.

### The operating playbook

1. Map every data category and processing path.

2. Run security, privacy, legal, architecture, reliability, and financial diligence.

3. Test claims with a sandbox and your evals.

4. Negotiate change notice, support, audit, deletion, and exit terms.

5. Keep a replacement architecture and migration runbook current.

### Say this in the room

- ‘Show how the contract maps to the technical control.’

- ‘What data persists outside the primary request?’

- ‘How many weeks to migrate at today’s traffic?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 24. Stakeholder communication: engineering, data, design, legal, CFO, and board

Executive fluency is the ability to translate the same system into the decision language of each stakeholder without distorting the truth. The PM should bring one shared evidence base and change the emphasis: feasibility for engineering, behavior for design, exposure for legal and security, economics for finance, and portfolio risk for the board.

### The vocabulary that changes the decision

### Decision memo

**Plain English.** A concise record of context, options, evidence, recommendation, risks, and owner.

**PM decision.** Use for consequential architecture, vendor, launch, and policy choices.

**Evidence to request.** Decision cycle time and reopened decisions.

**Watch for.** A narrative that hides alternatives and uncertainty.

### Architecture review

**Plain English.** Cross-functional evaluation of system boundaries, data, dependencies, scale, and controls.

**PM decision.** Bring product behavior and traffic assumptions, not a vendor wish list.

**Evidence to request.** Open risks and closure rate.

**Watch for.** Leaving UX, support, and failure behavior out.

### Risk acceptance

**Plain English.** Explicit authorization to proceed with a known residual risk.

**PM decision.** Name scope, rationale, duration, owner, and review date.

**Evidence to request.** Expired exceptions and realized incidents.

**Watch for.** Informal ‘we’re okay with it’ in chat.

### Board metric

**Plain English.** A portfolio-level measure of value, exposure, resilience, or governance.

**PM decision.** Use a small set tied to strategy and material risk.

**Evidence to request.** Value realized, high-risk inventory, incidents, and concentration.

**Watch for.** Reporting token volume as strategic progress.

### North-star metric

**Plain English.** The primary measure of recurring user value created.

**PM decision.** Pair with quality, risk, cost, and adoption guardrails.

**Evidence to request.** Successful valuable jobs per active customer.

**Watch for.** A model metric or vanity usage count.

### Decision log

**Plain English.** A dated record of what was decided, evidence, assumptions, and revisit trigger.

**PM decision.** Maintain for fast-moving model and policy choices.

**Evidence to request.** Traceability and timely reviews.

**Watch for.** No record of why the current system exists.

### The operating playbook

1. Lead with the decision required and by when.

2. Use one diagram: user, data, model, tools, controls, human, outcome.

3. Separate facts, assumptions, uncertainties, and recommendations.

4. Translate technical metrics into business and risk consequences.

5. Record owner, evidence, exception, and revisit trigger.

### Say this in the room

- ‘The decision today is X; here are the three viable options.’

- ‘This quality gain costs Y and changes exposure Z.’

- ‘What evidence would change our recommendation?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 25. Vertical playbooks: fintech, health, commerce, SaaS, support, and internal ops

Architecture follows consequence and workflow. The same model can be appropriate as a draft assistant and unacceptable as an autonomous decision-maker. Vertical expertise means knowing the domain’s ground truth, latency, regulation, human roles, abuse cases, and error costs—not merely changing example nouns.

### The vocabulary that changes the decision

### Fintech AI

**Plain English.** AI in payments, fraud, credit, onboarding, service, compliance, or finance operations.

**PM decision.** Prioritize explainability, loss asymmetry, real-time constraints, and audit.

**Evidence to request.** Expected loss, false positives, latency, complaints, and regulatory outcomes.

**Watch for.** Using generative text as the decision authority for money movement.

### Health AI

**Plain English.** AI supporting clinical, administrative, research, or patient workflows.

**PM decision.** Separate wellness, operations, decision support, and regulated functions.

**Evidence to request.** Safety, sensitivity, subgroup performance, escalation, and clinical utility.

**Watch for.** A general chatbot presented as medical judgment.

### Commerce AI

**Plain English.** AI for discovery, merchandising, pricing, content, service, and operations.

**PM decision.** Optimize user value, catalog truth, seller fairness, and conversion quality.

**Evidence to request.** Qualified conversion, returns, margin, diversity, and complaints.

**Watch for.** Engagement gains from misleading generated content.

### B2B SaaS copilot

**Plain English.** AI embedded in professional software to accelerate user work.

**PM decision.** Ground in tenant data with permissions and editable artifacts.

**Evidence to request.** Task completion, time saved, retention, and data isolation.

**Watch for.** Cross-tenant retrieval or generic chat detached from workflow.

### Customer-support AI

**Plain English.** Classification, retrieval, drafting, summarization, quality, and automation for service.

**PM decision.** Tier autonomy by intent, policy certainty, and consequence.

**Evidence to request.** Resolution, containment, CSAT, reopen, compliance, and escalation.

**Watch for.** Optimizing deflection while customers fail silently.

### Internal-ops agent

**Plain English.** AI acting across enterprise tools for employees.

**PM decision.** Use least privilege, identity propagation, approvals, and audit.

**Evidence to request.** Cycle time, successful actions, exceptions, and unsafe-action rate.

**Watch for.** One agent with broad access to email, files, and systems.

### Recommendation system

**Plain English.** Ranking items or actions for a user or context.

**PM decision.** Balance relevance with diversity, novelty, fairness, and business constraints.

**Evidence to request.** Long-term value, satisfaction, coverage, and ecosystem health.

**Watch for.** Short-term click optimization that narrows choice.

### The operating playbook

1. Define the domain decision and accountable professional.

2. Quantify error costs and required response time.

3. Map regulated data, explanation, recordkeeping, and appeal needs.

4. Pilot as decision support before higher autonomy.

5. Monitor user, subgroup, ecosystem, operational, and financial effects.

### Say this in the room

- ‘What is the accountable human or policy authority?’

- ‘Which error harms whom, and can it be reversed?’

- ‘What domain ground truth arrives after launch?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

# PART VI — OPERATING UNDER PRESSURE

## 26. Failure modes, incident response, and postmortems

AI incidents include harmful outputs, data exposure, unauthorized actions, systematic bias, model regression, stale retrieval, cost explosions, and silent workflow failure. Good incident response favors containment and evidence over debating whether the model ‘meant’ something. Postmortems improve the system, not the blame story.

### The vocabulary that changes the decision

### Hallucination

**Plain English.** Generated content unsupported by evidence or inconsistent with reality.

**PM decision.** Reduce through task design, evidence, verification, abstention, and UX.

**Evidence to request.** Severity-weighted unsupported claims and user impact.

**Watch for.** Treating every wrong output as the same failure.

### Silent failure

**Plain English.** The system appears successful but produces wrong, incomplete, or unexecuted results.

**PM decision.** Add independent verification and outcome reconciliation.

**Evidence to request.** Mismatch, non-execution, and delayed detection rates.

**Watch for.** Trusting a fluent confirmation message.

### Model regression

**Plain English.** A new version performs worse on important behavior or slices.

**PM decision.** Pin, evaluate, canary, monitor, and rollback.

**Evidence to request.** Regression suite failures and escaped impact.

**Watch for.** Accepting vendor ‘improvements’ without retesting.

### Retrieval poisoning

**Plain English.** Malicious or low-quality content enters the knowledge path.

**PM decision.** Control sources, provenance, ingestion, ranking, and content trust.

**Evidence to request.** Poison retrieval and attack success rates.

**Watch for.** Indexing all accessible content equally.

### Runaway agent

**Plain English.** A loop repeats actions, calls, or retries, causing harm or spend.

**PM decision.** Set hard budgets, idempotency, stop conditions, and circuit breakers.

**Evidence to request.** Step count, retries, duplicate actions, and spend anomalies.

**Watch for.** Relying on a natural-language instruction to stop.

### Incident severity

**Plain English.** A tier based on impact, scope, sensitivity, reversibility, and obligations.

**PM decision.** Predefine response, leadership, communication, and review by tier.

**Evidence to request.** Time to classify, contain, recover, and notify.

**Watch for.** Severity based only on number of users.

### Postmortem

**Plain English.** A structured analysis of timeline, impact, causes, detection, response, and actions.

**PM decision.** Focus on contributing system conditions and tested remediation.

**Evidence to request.** Action closure and recurrence.

**Watch for.** ‘The model hallucinated’ as root cause.

### The operating playbook

1. Contain: disable action, model, tool, source, or cohort.

2. Preserve evidence with access controls.

3. Assess affected users, data, actions, jurisdictions, and obligations.

4. Recover with a qualified version and reconciled state.

5. Convert findings into design changes, tests, monitoring, and training.

### Say this in the room

- ‘Contain first; attribution can follow.’

- ‘What independent record confirms the action occurred?’

- ‘Which system condition allowed this failure to reach the user?’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 27. The unchallenged-in-the-office AI PM playbook

Credibility comes from consistently asking the question that moves the decision forward. Do not perform expertise with acronyms. Clarify the user job, request evidence, expose trade-offs, name risk, and assign the next action. The strongest AI PM makes specialists feel understood and executives feel the system is governable.

### The vocabulary that changes the decision

### Technical judgment

**Plain English.** Choosing among mechanisms based on evidence and constraints.

**PM decision.** Develop through eval reviews, architecture walkthroughs, incidents, and hands-on prototypes.

**Evidence to request.** Decision quality and avoided rework.

**Watch for.** Memorizing terms without knowing when they matter.

### Product intuition

**Plain English.** A practiced sense for user value, behavior, and adoption.

**PM decision.** Build from observation, prototypes, and outcome reviews.

**Evidence to request.** Hypotheses validated and user outcome lift.

**Watch for.** Confusing personal enthusiasm with demand.

### Evidence hierarchy

**Plain English.** Ordering evidence from anecdotes to reproducible tests and real outcomes.

**PM decision.** Match claim strength to evidence strength.

**Evidence to request.** Decisions supported by representative tests and production data.

**Watch for.** A polished demo overruling failed evals.

### Trade-off statement

**Plain English.** A concise explanation of what improves, what worsens, and for whom.

**PM decision.** Use in every model, scope, autonomy, and launch recommendation.

**Evidence to request.** Decision speed and later surprise.

**Watch for.** Saying one option is ‘best’ without constraints.

### Office artifact

**Plain English.** A reusable document that makes alignment and execution easier.

**PM decision.** Maintain decision memo, one-page PRD, eval card, risk register, and launch scorecard.

**Evidence to request.** Reuse, freshness, and decision cycle time.

**Watch for.** Producing documents nobody uses.

### Operating cadence

**Plain English.** Regular reviews for quality, cost, incidents, risks, vendors, and roadmap.

**PM decision.** Set frequency by change rate and consequence.

**Evidence to request.** Actions closed and signals caught early.

**Watch for.** Governance meetings detached from delivery.

### The operating playbook

1. Before a meeting, write the decision, evidence, options, and recommendation.

2. Ask one layer deeper: data, threshold, slice, permission, fallback, or unit cost.

3. Translate specialist input into product consequence and owner.

4. End with a documented decision or named evidence gap.

5. Revisit assumptions when models, traffic, policy, or users change.

### Say this in the room

- ‘Let me translate the architecture choice into user behavior and cost.’

- ‘Which slice disproves the average?’

- ‘I do not need certainty; I need the next reversible decision.’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

## 28. Career plan, interview brief, and 30–60–90 days

A senior AI PM interview tests product sense, technical depth, execution, metrics, leadership, and responsible judgment. Demonstrate a repeatable operating system: frame the job, choose the minimum intelligence, define the data and eval plan, design trust and controls, model economics, and stage the launch. Speak in decisions and evidence.

### The vocabulary that changes the decision

### AI product sense

**Plain English.** Ability to find valuable AI-suitable problems and shape an appropriate experience.

**PM decision.** Show alternatives, minimum intelligence, trust, and adoption.

**Evidence to request.** Quality of assumptions, prioritization, and user reasoning.

**Watch for.** Starting with model capability instead of user pain.

### Technical fluency

**Plain English.** Ability to reason about data, models, RAG, agents, evals, serving, and failure.

**PM decision.** Explain trade-offs in plain language and ask precise questions.

**Evidence to request.** Correctness, depth, and connection to product behavior.

**Watch for.** Reciting architecture names without constraints.

### Execution story

**Plain English.** A structured account of ambiguity, decision, alignment, delivery, and outcome.

**PM decision.** Use specific evidence, trade-offs, and what changed after learning.

**Evidence to request.** Outcome, role clarity, and reflection.

**Watch for.** A team success story with no personal decisions.

### Failure story

**Plain English.** A candid account of a miss, response, and durable system improvement.

**PM decision.** Choose a consequential learning with clear ownership.

**Evidence to request.** Depth of diagnosis and changed behavior.

**Watch for.** A disguised success or blaming engineering/model.

### Portfolio narrative

**Plain English.** A coherent explanation of the problems and capabilities your work proves.

**PM decision.** Map projects to product, technical, business, and leadership skills.

**Evidence to request.** Coverage and credible artifacts.

**Watch for.** A list of demos with no outcomes or lessons.

### 30–60–90 plan

**Plain English.** A staged plan to learn, align, decide, and deliver.

**PM decision.** Use 30 days for map, 60 for evidence, 90 for a bounded result.

**Evidence to request.** Relationships, baseline, decisions, pilot, and operating cadence.

**Watch for.** Promising a transformation before understanding systems.

### The operating playbook

1. Prepare six stories: strategy, zero-to-one, scale, conflict, failure, and responsible trade-off.

2. Practice one system design across RAG, agent, classical ML, and non-AI alternatives.

3. Use metric trees and failure taxonomies aloud.

4. Bring artifacts with confidential details removed.

5. End answers with result, learning, and how the system changed.

### Say this in the room

- ‘I would first define the consequence and non-AI baseline.’

- ‘Here is the eval and launch gate I would use.’

- ‘The trade-off I owned was X for Y because evidence Z.’

:::callout Proof of command

Do not merely define these terms. Connect the term to a user consequence, an eval, a cost, a control, and the next owner. That is the difference between AI vocabulary and AI product judgment.

:::

---PAGE---

# Appendix A. The one-page AI opportunity brief

## Decision
State the decision required, owner, and date. Example: “Approve a four-week shadow pilot for policy-answer drafting in US support.”

## User and job
- Primary user and workflow moment.
- Current pain in time, error, risk, or missed value.
- Current process and non-AI baseline.

## Minimum viable intelligence
Describe why rules, search, analytics, classical ML, generation, or an agent is appropriate for each step. State what will remain human.

## Evidence plan
List target outcomes; task, system, risk, and business metrics; eval set and slices; launch threshold; and falsifying result.

## Operating envelope
Define supported inputs, languages, documents, users, permissions, context length, latency, and volume. Name unsupported cases.

## Risk and controls
For each severe failure: prevention, detection, response, recovery, and accountable owner.

## Economics
Estimate volume, total cost per successful task, human exception cost, expected value, margin effect, and downside sensitivity.

## Next reversible step
Choose stop, discovery, prototype, shadow, canary, or scale. Include time, cohort, budget, and exit criteria.

# Appendix B. AI PRD skeleton

## 1. Problem and outcome
User job; existing baseline; why now; target outcome; exclusions; evidence of demand.

## 2. System boundary
Inputs → preprocessing → retrieval/data → model → tools → policy → human → output → feedback. Identify owners and external dependencies.

## 3. Behavior contract
Write examples of expected, acceptable, disallowed, abstaining, escalating, and fallback behavior. Include unsupported languages and conditions.

## 4. Autonomy matrix
| Action class | Consequence | Reversible? | Mode | Approval | Verification |
|---|---|---|---|---|---|
| Read/search | Low | Yes | Auto | None | Source and permission checks |
| Draft | Medium | Yes | Suggest | User edits | Schema and policy checks |
| External write | High | Sometimes | Approve | Named user | Preview, authorization, idempotency |
| Money/legal/clinical action | Very high | Often no | Human-owned | Qualified authority | Independent system of record |

## 5. Evaluation contract
Dataset source and version; slices; rubrics; graders; calibration; task, retrieval, tool, safety, latency, and cost metrics; thresholds; owner.

## 6. Data and privacy
Purpose, source, rights, minimization, lineage, residency, retention, deletion, training use, feedback, and sensitive attributes.

## 7. Security and safety
Threat model, trust boundaries, untrusted content, permissions, secrets, sandbox, rate limits, abuse, red-team suite, and incident plan.

## 8. UX and accessibility
Mental model, evidence, confidence, edit/undo, escalation, failure state, synthetic disclosure, accessible alternative, and support.

## 9. Reliability and economics
Traffic profile, P50/P95 latency, throughput, SLOs, provider quotas, degradation, total cost per successful task, guardrails, and margin.

## 10. Release and ownership
Shadow/canary/ramp; launch gate; rollback; monitoring; on-call; review cadence; material changes; retirement.

# Appendix C. Eval scorecard

| Layer | Metric | Slice | Threshold | Current | Owner | Release action |
|---|---|---|---|---|---|---|
| Task | Successful completion | Core job | Product-specific | — | PM | Block below threshold |
| Retrieval | Recall@k | Rare policy | Product-specific | — | Search | Diagnose source/chunk/ranker |
| Grounding | Supported claims | High consequence | Product-specific | — | AI Eng | Abstain or block |
| Tool | Correct call + args | Write actions | Product-specific | — | Eng | Require approval |
| Safety | Severe attack success | Adversarial | Zero target | — | Security | Block release |
| UX | Successful recovery | Failure state | Product-specific | — | Design | Fix fallback |
| System | P95 latency | Peak load | SLO | — | Platform | Capacity/fallback |
| Economics | Cost/success | P95 workload | Budget | — | PM/Finance | Route/cache/limit |

Rubric rule: define a passing output, a clearly failing output, and the ambiguous border. Calibrate graders on all three. Report confidence intervals where sampling matters. Never hide severe failures inside an average.

# Appendix D. Model and vendor decision matrix

Score only after running the same workload. Weight criteria by product need.

| Criterion | Questions |
|---|---|
| Task quality | Does it pass our golden set and worst slices? |
| Grounding/tools | Are citations, schemas, function calls, and long tasks reliable? |
| Safety/security | What attacks, controls, reports, and admin features exist? |
| Data terms | Retention, training use, residency, subprocessors, deletion, audit? |
| Reliability | Regions, quotas, support, SLA, deprecation, pinned versions? |
| Performance | P50/P95 latency at real context, output, concurrency, and tool load? |
| Economics | Total cost per successful task, not list price alone? |
| Control | Fine-tuning, routing, observability, policy, deployment, export? |
| Exit | Time, data, state, compatibility, eval, and fallback required to migrate? |

# Appendix E. Agent tool card

For every tool record: purpose; owner; read/write; side effects; input/output schema; authentication; permission scope; allowed users; data classification; rate limit; timeout; retries; idempotency; approval; audit event; rollback; failure behavior; and red-team cases.

Agent-level budgets: maximum steps, elapsed time, model calls, tool calls, spend, retries, recursion depth, generated bytes, and external writes. The application—not the prompt—must enforce hard limits.

# Appendix F. AI incident runbook

1. **Detect and classify.** What happened, who or what is affected, and is harm ongoing?
2. **Contain.** Disable model/version, prompt, retrieval source, tool, permission, tenant, feature, or traffic cohort.
3. **Preserve.** Secure traces, versions, approvals, source data, tool results, and system-of-record evidence.
4. **Assess.** Determine actions, data, users, scope, severity, reversibility, legal or contractual obligations, and communications.
5. **Recover.** Reconcile external state, remediate users, deploy a qualified configuration, and monitor recurrence.
6. **Learn.** Identify technical and organizational contributors; add tests, controls, alerts, docs, owners, and deadlines.

Postmortem sections: executive summary; user/business impact; timeline; detection; response; contributing causes; what worked; what failed; corrective actions; evidence of completion; and recurrence review date.

# Appendix G. 30–60–90 day plan for a new AI PM

## Days 1–30: map reality
- Observe users and operations; map the actual workflow.
- Inventory AI systems, vendors, datasets, owners, costs, risks, incidents, and commitments.
- Read evals, traces, support tickets, model cards, contracts, and postmortems.
- Baseline outcome, adoption, quality, latency, unit cost, and exception load.
- Build relationships with engineering, data, design, research, operations, security, privacy, legal, finance, sales, and support.

## Days 31–60: create shared evidence
- Publish the metric tree and failure taxonomy.
- Repair or create a representative golden set and release scorecard.
- Clarify system boundary, data contracts, autonomy matrix, and risk owners.
- Identify the highest-value reversible bet and the largest operational debt.
- Establish quality, cost, incident, vendor, and governance cadence.

## Days 61–90: deliver a bounded result
- Ship or qualify one measurable improvement through shadow/canary.
- Close one material reliability, security, data, or cost gap.
- Present a portfolio roadmap with value, dependencies, evidence, and stop criteria.
- Document decisions, reusable artifacts, and the next learning loop.

# Appendix H. Meeting questions that signal real command

## Discovery
- What user decision changes, and what is the current baseline?
- What is the minimum viable intelligence?
- Which failure would make the product not worth shipping?

## Data and ML
- What exactly is the label, and when does ground truth arrive?
- Is every feature available at decision time?
- Which segment is hidden by the average?

## RAG and agents
- Did retrieval fail, or did generation misuse good evidence?
- Which content is untrusted, and where is authorization enforced?
- What are the stop conditions, budgets, and approval boundaries?

## Evaluation and launch
- Does the eval represent production frequency and consequence?
- How were automated graders calibrated?
- Which metric automatically pauses rollout?

## Economics and vendors
- What is total cost per successful task at P95 workload?
- What behavior can change without notice?
- How long would migration take, and have we tested it?

## Executive review
- What decision is required today?
- What do we know, assume, and still need to learn?
- What evidence would reverse the recommendation?

# Appendix I. July 2026 technology radar

This radar separates durable capability patterns from fast-moving product names. “Adopt” means production-ready only after your own evals and controls; “trial” means bounded experimentation; “watch” means the concept is strategically relevant but specifications, economics, or reliability may still move quickly.

| Area | July 2026 posture | What an AI PM should know |
|---|---|---|
| Hosted multimodal models | Adopt selectively | Compare task quality, realtime behavior, tools, data terms, change policy, and total cost. |
| Open-weight models | Adopt selectively | Strong option for control, locality, adaptation, and scale economics when operations and licenses are understood. |
| Small and edge models | Adopt for bounded jobs | Excellent for classification, extraction, privacy-sensitive, offline, and high-volume workflows with task-specific evals. |
| Reasoning and test-time scaling | Adopt by task | Spend extra compute only where verifiable task lift exceeds latency and cost. |
| RAG and hybrid search | Adopt | Treat retrieval, generation, source rights, freshness, and access control as separate product layers. |
| Tool calling and constrained agents | Adopt with controls | Use narrow schemas, least privilege, budgets, approvals, tracing, and deterministic authorization. |
| Long-running and multi-agent workflows | Trial | Require trajectory evals, identity, state, recovery, spend limits, and proof that decomposition beats one agent or workflow. |
| MCP | Adopt selectively | Useful integration standard; server trust, OAuth scopes, tool semantics, and spec version remain product responsibilities. |
| A2A | Trial | Useful for independent agent interoperability when organizational or vendor boundaries justify it. |
| MCP Apps and protocol extensions | Watch/Trial | Treat pre-final or emerging extensions as moving dependencies and pin the specification used. |
| Coding agents and vibe coding | Adopt with SDLC controls | Powerful for prototyping and delivery; require review, tests, secret hygiene, dependency checks, and accountable ownership. |
| Deep research and AI search | Adopt for evidence work | Measure source recall, citation support, synthesis quality, latency, and user verification—not eloquence. |
| Realtime voice and multimodal agents | Trial/Adopt by workflow | Design interruption, ephemeral credentials, consent, tool latency, fallback, and accessible alternatives. |
| Computer-use agents | Trial in bounded environments | UI automation is flexible but fragile; sandbox, restrict permissions, verify state, and keep consequential actions behind approval. |
| Synthetic data | Adopt selectively | Useful for coverage and rarity, but validate against real holdouts and prevent generator monoculture. |
| RLVR, GRPO, and environment-based training | Watch/Adopt for verifiable domains | Most compelling where outcomes can be checked automatically; product rubrics still need user relevance. |
| Physical AI and robotics foundation models | Watch/Trial | Add physical safety, simulation, sensor drift, real-world recovery, and hardware lifecycle to the PM stack. |
| Provenance and synthetic-media controls | Adopt | Preserve source and transformation metadata; disclosure and watermarking are layers, not complete solutions. |

## Provider landscape without leaderboard theater

As of this edition, serious product discovery commonly includes frontier API providers, hyperscaler model platforms, open-weight ecosystems, specialist inference providers, and domain models. Provider and family names should be treated as a shortlist generator. The production choice comes from a frozen workload, representative eval, risk review, matched latency/concurrency test, contractual diligence, and exit plan.

## The quarterly refresh ritual

1. Re-run the golden set on approved incumbent and credible challengers.
2. Review deprecations, preview-to-stable changes, context/tool behavior, and data terms.
3. Recalculate cost per successful task at actual traffic and cache rates.
4. Revisit concentration, exit time, open-weight alternatives, and portability.
5. Promote only with regression, security, governance, canary, and rollback evidence.

---PAGE---

# Appendix J. July 2026 terminology glossary

The glossary is intentionally PM-centric: each definition tells you what the term changes in a product decision. Definitions from the main chapters are consolidated with additional operating vocabulary.


## 3


### 30–60–90 plan

A staged plan to learn, align, decide, and deliver. PM relevance: Use 30 days for map, 60 for evidence, 90 for a bounded result.


## A


### A/B test

Randomized comparison of product variants. PM relevance: Use after safety qualification when interference and spillovers are manageable.


### A2A

An open protocol for discovery and task exchange among independent agent systems. PM relevance: Use when opaque agents must interoperate across teams or vendors.


### Abstention

The system declines or escalates when evidence or confidence is insufficient. PM relevance: Define abstention conditions and a useful next path.


### Access-aware retrieval

Filtering evidence according to the user’s permissions at query time. PM relevance: Make authorization deterministic outside the model.


### Accuracy

Fraction of predictions that are correct; misleading on imbalanced problems unless paired with class-specific metrics.


### Activation function

A nonlinear transformation inside a neural network that enables it to learn complex relationships.


### Active learning

Selecting the most informative examples for labeling. PM relevance: Use when labels are expensive and uncertainty can guide sampling.


### Adapter

A small trainable component attached to a frozen model for efficient specialization.


### Adversarial evaluation

Testing malicious, ambiguous, stressed, or out-of-distribution inputs. PM relevance: Maintain threat- and abuse-case suites in release gates.


### Adversarial example

An intentionally perturbed input designed to cause an incorrect model response.


### Agent

A model-centered loop that observes, decides, acts, and updates state. PM relevance: Define goal, stop conditions, budgets, permissions, and supervision.


### Agent card

Metadata that describes an agent's identity, capabilities, endpoints, and interaction requirements in an interoperability protocol.


### Agent evaluation

Testing plans, tool selection, arguments, policy, recovery, and final outcome. PM relevance: Evaluate trajectories and side effects, not only final text.


### Agentic RAG

A retrieval system where a model chooses searches, sources, iterations, or tools rather than following one fixed query path.


### AGI

Artificial general intelligence, a disputed concept for broadly human-level capability; not a useful production requirement by itself.


### AI browser

A browser experience where models search, summarize, navigate, or act across web interfaces; permissions and source verification are central.


### AI gateway

A control layer for model routing, authentication, quotas, logging, policy, caching, and vendor abstraction.


### AI literacy

Organizational capability to understand appropriate use, limits, and risks. PM relevance: Train by role and measure behavior, not attendance alone.


### AI PM

The accountable product leader connecting user value, model behavior, data, UX, economics, and risk. PM relevance: Make trade-offs visible and assign owners for each layer.


### AI product

A product whose value or behavior materially depends on learned or generative models. PM relevance: Decide whether AI is core, assistive, or merely implementation detail.


### AI product sense

Ability to find valuable AI-suitable problems and shape an appropriate experience. PM relevance: Show alternatives, minimum intelligence, trust, and adoption.


### AI search

Search that combines retrieval, generation, synthesis, and citations rather than returning only ranked links.


### AI suitability

A structured test of value, data, tolerance for error, feedback, and economics. PM relevance: Reject use cases with weak data or catastrophic unreviewed failure.


### AI-enabled feature

AI augments an existing workflow or product capability. PM relevance: Package based on incremental value and cost.


### AI-native product

A product whose workflow or value proposition is designed around learned or generative capability. PM relevance: Use the label only when AI changes the job, not just copywriting.


### Algorithmic impact assessment

A documented analysis of purpose, affected people, benefits, risks, and mitigations. PM relevance: Use before high-impact deployment and material change.


### Alignment

Efforts to make model behavior follow intended goals, values, and constraints; it does not replace application controls.


### Annotation

Human or automated assignment of labels or judgments. PM relevance: Define rubric, training, adjudication, quality, and worker conditions.


### Anomaly detection

Finding observations that differ substantially from expected patterns.


### Answer engine

A product that synthesizes direct answers from retrieved sources; source coverage and attribution are key product metrics.


### API

An application programming interface: a defined way for software systems to request capabilities or exchange data.


### API gateway

A control point for authentication, routing, quotas, logging, and policy across API traffic.


### Application layer

Prompts, retrieval, tools, policies, code, UI, and feedback wrapped around a model. PM relevance: Treat most product quality as a system property.


### Architecture review

Cross-functional evaluation of system boundaries, data, dependencies, scale, and controls. PM relevance: Bring product behavior and traffic assumptions, not a vendor wish list.


### Artifact

A versioned output of AI work such as a model, adapter, prompt, dataset, index, report, or generated file.


### Artificial intelligence

A broad family of computational systems that perform tasks associated with perception, prediction, generation, reasoning, or action.


### Attention

A neural mechanism that weights relationships among input positions; central to transformers.


### Attribution

A method for estimating which inputs influenced an output, or for assigning an outcome to an intervention.


### Audit trail

A human-readable and machine-queryable record of inputs, versions, evidence, actions, and approvals. PM relevance: Build for support, investigation, compliance, and user trust.


### AUROC

Area under the receiver operating characteristic curve; measures ranking across thresholds but can look strong on imbalanced data.


### Autonomy policy

Rules mapping action risk to suggest, draft, approve, or auto-act. PM relevance: Specify per tool and action, not per agent persona.


### Autoscaling

Automatically changing compute capacity in response to load or policy.


### Average precision

A precision-recall summary useful for imbalanced classification and ranking.


## B


### B2B SaaS copilot

AI embedded in professional software to accelerate user work. PM relevance: Ground in tenant data with permissions and editable artifacts.


### Backpropagation

The algorithm used to compute gradients through a neural network for training.


### Baseline

The simplest current process or model against which improvement is measured. PM relevance: Require a heuristic, search, or human baseline before model work.


### Batch inference

Processing accumulated requests asynchronously for throughput and lower cost rather than interactive latency.


### Behavior contract

A testable description of expected, allowed, disallowed, and fallback behavior. PM relevance: Write examples and rubrics for normal, edge, and adversarial cases.


### Benchmark

A standardized test for comparison; useful for discovery but weaker than an eval on the real product workload.


### Bias

A systematic error or disparity; also a mathematical intercept term. Always clarify which meaning is intended.


### Bias-variance trade-off

The tension between overly simple models that underfit and overly sensitive models that overfit.


### BM25

A strong lexical search ranking method based on term frequency and document statistics.


### Board metric

A portfolio-level measure of value, exposure, resilience, or governance. PM relevance: Use a small set tied to strategy and material risk.


### Brier score

Mean squared error of probabilistic predictions; lower is better and reflects calibration plus discrimination.


## C


### Cache

Stored result or computation reused for equivalent work. PM relevance: Use where freshness, privacy, and invalidation are understood.


### Calibrated trust

Users rely on the system in proportion to its real capability. PM relevance: Design evidence, limits, and recovery so reliance matches performance.


### Calibration

Whether predicted probabilities match observed frequencies. PM relevance: Use calibrated scores for risk tiers and expected-value decisions.


### Canary

Exposing a small controlled share to a new version. PM relevance: Use with auto-pause guardrails and rapid rollback.


### Canary token

A unique marker used to detect unexpected disclosure or access.


### Cascade

Trying a cheaper model first and escalating uncertain cases. PM relevance: Use when confidence or task type predicts quality reliably.


### Causal inference

Methods for estimating the effect of an intervention rather than mere association.


### Chain of thought

Intermediate reasoning behavior, sometimes internal and sometimes elicited. PM relevance: Evaluate final correctness and auditable evidence; do not require hidden reasoning disclosure.


### Champion/challenger

A qualified candidate competes with the current production system. PM relevance: Use for controlled continuous improvement.


### Chunking

Splitting documents into retrievable units. PM relevance: Tune boundaries, size, overlap, and metadata to user questions.


### CI/CD for AI

Automated validation and staged delivery of code plus AI behavior changes. PM relevance: Gate schema, data, eval, safety, security, and performance.


### Citation UX

Showing evidence and linking claims to exact sources. PM relevance: Use where verification and provenance matter.


### Classification

Predicting a discrete category such as fraud/not fraud or intent type.


### CLIP

A family of contrastively trained vision-language representations used to relate images and text.


### Closed model API

A hosted proprietary model accessed as a service. PM relevance: Use for speed and managed capability when terms and controls fit.


### Clustering

Grouping similar observations without target labels.


### Coding agent

An agent that reads, edits, runs, and verifies software work across a repository and development environment.


### Cold start

Limited data or interaction history for a new user, item, market, or product.


### Commerce AI

AI for discovery, merchandising, pricing, content, service, and operations. PM relevance: Optimize user value, catalog truth, seller fairness, and conversion quality.


### Computer use

An agent capability that operates graphical interfaces through screenshots, clicks, typing, and other actions.


### Computer vision

Models that classify, detect, segment, describe, or reason over images and video. PM relevance: Specify spatial task, environment, and acceptable misses.


### Concierge test

A high-touch manual service that learns the workflow and desired outcome. PM relevance: Use for discovery with a small number of users.


### Confabulation

Another term for plausible but unsupported generated content; often called hallucination.


### Confidence display

A representation of uncertainty or evidence strength. PM relevance: Show only when calibrated, actionable, and understandable.


### Confusion matrix

Counts of true positives, false positives, true negatives, and false negatives at a threshold.


### Consent

A valid user permission for a defined data use or interaction; requirements depend on context and law.


### Content filter

A component that detects or blocks content according to policy; false positives and false negatives both matter.


### Content provenance

Metadata or signals that record origin and transformations of media. PM relevance: Preserve provenance across creation, editing, export, and publishing.


### Context engineering

Assembling the right instructions, evidence, tools, memory, and state for a task. PM relevance: Treat context as a designed, measured pipeline.


### Context precision

The share of retrieved context that is relevant to the question.


### Context recall

The share of necessary evidence successfully retrieved into context.


### Context window

The maximum token budget available for instructions, inputs, history, retrieved evidence, and output. PM relevance: Allocate context deliberately and test long-context degradation.


### Contextual bandit

A learning setup that chooses actions using context and observes reward only for the chosen action.


### Continuous batching

Dynamically grouping inference work to improve accelerator use. PM relevance: Use for concurrent traffic, then tune fairness and latency.


### Contrastive learning

Learning representations by pulling related examples together and pushing unrelated examples apart.


### Copilot

A user-facing assistant that augments human work while generally leaving authority with the user.


### Cost guardrail

A budget or anomaly rule that pauses, degrades, or alerts. PM relevance: Use by tenant, workflow, tool, and incident mode.


### Cost per successful task

Total variable and allocated cost divided by acceptably completed tasks. PM relevance: Use as the primary unit metric for AI workflows.


### Counterfactual

A reasoned estimate of what would have happened under a different action.


### Cross-encoder

A reranking model that jointly processes query and candidate for richer relevance scoring.


### Cross-validation

Repeated train/validation splits used to estimate generalization when data is limited.


### Customer-support AI

Classification, retrieval, drafting, summarization, quality, and automation for service. PM relevance: Tier autonomy by intent, policy certainty, and consequence.


## D


### Data augmentation

Creating transformed or synthetic examples to increase coverage or robustness.


### Data contract

Requirements for source, fields, freshness, rights, quality, and deletion. PM relevance: Attach to each critical input and output.


### Data drift

A change in the distribution of model inputs.


### Data exfiltration

Unauthorized extraction of sensitive information through outputs, tools, logs, or retrieval. PM relevance: Enforce access outside the model and inspect data flows.


### Data leakage

Sensitive data exposure, or in ML, inappropriate use of information unavailable at prediction time.


### Data lineage

Traceability from source through transformations to model and output. PM relevance: Require for debugging, deletion, audit, and trust.


### Data minimization

Collecting and retaining only what is necessary for the purpose. PM relevance: Make purpose, retention, and deletion part of the product spec.


### Data poisoning

Manipulating training, retrieval, or feedback data to corrupt system behavior.


### Data residency

The geographic location where data is processed or stored. PM relevance: Map each service, failover, support, and subprocessor path.


### Data retention

How long a provider stores prompts, outputs, files, logs, or state. PM relevance: Verify defaults, controls, exceptions, backups, and deletion evidence.


### Decision log

A dated record of what was decided, evidence, assumptions, and revisit trigger. PM relevance: Maintain for fast-moving model and policy choices.


### Decision memo

A concise record of context, options, evidence, recommendation, risks, and owner. PM relevance: Use for consequential architecture, vendor, launch, and policy choices.


### Decision threshold

The score cutoff that turns a probability or ranking signal into an action.


### Deep learning

Machine learning with multi-layer neural networks that learn representations from data.


### Deep research

A long-running research workflow that plans searches, gathers sources, synthesizes evidence, and produces a cited result.


### Demographic parity

A fairness criterion requiring equal positive prediction rates across groups; it may conflict with other criteria.


### Dense retrieval

Embedding-based semantic retrieval using vector similarity.


### Diffusion model

A generative model that learns to reverse a noise process, widely used for image, audio, and video generation.


### Digital human

A synthetic interactive persona combining generated voice, face, motion, and language; consent, disclosure, and impersonation risk matter.


### Digital twin

A computational representation of a physical or operational system used for monitoring or simulation.


### Direct preference optimization

A method that tunes a model directly from preferred versus rejected outputs without a separate reward-model loop.


### Disparate impact

A disproportionate adverse effect on a protected or affected group, regardless of intent.


### Distillation

Training a smaller model to imitate a stronger teacher. PM relevance: Use to reduce cost or latency for a bounded task.


### Document AI

Extraction and reasoning that preserves fields, tables, layout, and document type. PM relevance: Design per document family and exception path.


### Drift

A meaningful change in inputs, relationships, or outcomes over time. PM relevance: Define which drift triggers investigation, retraining, or policy change.


## E


### Editable output

AI output presented as a draft the user can modify. PM relevance: Use for creative or knowledge work where control matters.


### Embedding

A vector representation that places semantically related items near each other. PM relevance: Choose models and dimensionality using retrieval evals on your domain.


### Embedding dimension

The number of coordinates in a vector representation; more dimensions are not automatically better.


### Encryption at rest

Protecting stored data using cryptography.


### Encryption in transit

Protecting data while moving between systems.


### Ensemble

A combination of multiple models whose aggregate often improves robustness or accuracy.


### Ephemeral token

A short-lived credential designed to reduce exposure in client-side or realtime connections.


### Equal opportunity

A fairness criterion often requiring equal true-positive rates across groups.


### Error budget

The amount of unreliability tolerated by an SLO before change or release policy tightens.


### EU AI Act

A risk-based EU regulation with obligations depending on actor and use category. PM relevance: Determine provider/deployer role, category, geography, and application date with counsel.


### Eval contract

The datasets, rubrics, graders, thresholds, slices, and owners governing release. PM relevance: Agree before model optimization begins.


### Evaluation flywheel

A loop where production failures and user corrections become curated eval cases, fixes, and release gates.


### Evidence hierarchy

Ordering evidence from anecdotes to reproducible tests and real outcomes. PM relevance: Match claim strength to evidence strength.


### Excessive agency

Too much functionality, permission, or autonomy allows damaging action. PM relevance: Minimize tools, scopes, side effects, and autonomous writes.


### Execution story

A structured account of ambiguity, decision, alignment, delivery, and outcome. PM relevance: Use specific evidence, trade-offs, and what changed after learning.


### Exit plan

A tested path to replace, export, or shut down a vendor dependency. PM relevance: Define data export, compatibility, evals, timeline, and fallback.


### Expectation setting

Communicating capability, limitations, and user responsibilities. PM relevance: Use in sales, onboarding, UI, and support.


### Expected value

Probability-weighted benefit minus probability-weighted harm and total cost. PM relevance: Translate model metrics into money, time, trust, or safety.


### Experiment tracking

Recording datasets, code, parameters, runs, metrics, and artifacts. PM relevance: Require reproducibility for consequential decisions.


### Explainability

Methods and interfaces that help people understand system behavior; useful explanations are audience- and decision-specific.


## F


### F1 score

The harmonic mean of precision and recall; it hides threshold economics and true negatives.


### Failure story

A candid account of a miss, response, and durable system improvement. PM relevance: Choose a consequential learning with clear ownership.


### Failure taxonomy

A shared classification of ways the system can fail. PM relevance: Use to drive evals, UX, alerts, and ownership.


### Fair-use limit

A policy bounding expensive or abusive consumption within a package. PM relevance: Make transparent, measurable, and paired with controls.


### Fault tolerance

How much error a workflow can absorb before harm exceeds value. PM relevance: Match autonomy and review to consequence, reversibility, and detectability.


### Feasibility envelope

The range of inputs and conditions where the system works acceptably. PM relevance: Use to scope the initial product honestly.


### Feature

An input signal supplied to a model. PM relevance: Ask whether it is available, fresh, lawful, and stable at decision time.


### Feature adoption

Meaningful use by the intended user for the intended job. PM relevance: Measure activation, repeat, depth, and retained outcome.


### Feature store

Infrastructure for defining, computing, versioning, and serving ML features consistently.


### Federated learning

Training across decentralized data holders while keeping raw data local, with important privacy caveats.


### Feedback loop

Product interactions that produce signals for improvement. PM relevance: Design explicit, attributable, and debiased feedback.


### Few-shot example

A small set of input-output demonstrations in context. PM relevance: Use examples to define ambiguous format or judgment.


### Fine-tuning

Additional training on task- or domain-specific examples. PM relevance: Use when behavior is repeated, data is strong, and gains survive evals.


### Fintech AI

AI in payments, fraud, credit, onboarding, service, compliance, or finance operations. PM relevance: Prioritize explainability, loss asymmetry, real-time constraints, and audit.


### Foundation model

A broadly trained model reusable across many downstream tasks and modalities. PM relevance: Decide whether broad capability outweighs cost, control, and specialization needs.


### Foundation-model operations

The practices for selecting, evaluating, serving, monitoring, and governing systems built on foundation models.


### Function calling

A model emits a structured request to invoke an application-defined function.


## G


### Generative AI

Models that synthesize content such as text, code, images, audio, video, or structured data.


### Golden set

A curated, versioned set of representative examples and expected behavior. PM relevance: Use for regression and release decisions, with protected holdout slices.


### GPU

Parallel hardware commonly used for model training and inference. PM relevance: Match memory, precision, batch, and utilization to workload.


### Graceful degradation

Preserving a useful safe experience during model, tool, or data failure. PM relevance: Define fallback content, manual paths, and status messaging.


### Gradient

The direction and magnitude of change in loss with respect to model parameters.


### Gradient descent

An optimization family that iteratively updates parameters to reduce loss.


### GraphRAG

Retrieval that uses entities and relationships, often alongside text search. PM relevance: Use for connected questions spanning documents or records.


### Gross margin

Revenue minus direct delivery cost as a share of revenue. PM relevance: Model AI usage and support cost by customer and feature.


### Ground truth

The best available reference outcome; it may still contain delay, ambiguity, and measurement error.


### Grounding

Constraining or supporting output with authoritative evidence. PM relevance: Define allowed sources and behavior when evidence is absent.


### GRPO

Group relative policy optimization, a reinforcement-learning method that compares rewards among sampled outputs within a group.


### Guardrail

A deterministic or probabilistic control that detects, constrains, blocks, or escalates risky behavior.


### Guardrail metric

A measure that must not degrade while optimizing a primary outcome. PM relevance: Define user, risk, operational, and economic guardrails.


## H


### Hallucination

Generated content unsupported by evidence or inconsistent with reality. PM relevance: Reduce through task design, evidence, verification, abstention, and UX.


### Health AI

AI supporting clinical, administrative, research, or patient workflows. PM relevance: Separate wellness, operations, decision support, and regulated functions.


### HNSW

A graph-based approximate nearest-neighbor index commonly used for vector search.


### Holdout set

Data protected from training and tuning, used for an unbiased final estimate.


### Human approval gate

A deterministic checkpoint before consequential action. PM relevance: Require approval for high-impact, ambiguous, or irreversible steps.


### Human feedback

Ratings, comparisons, corrections, demonstrations, or outcomes supplied by people for evaluation or learning.


### Human-in-the-loop

A designed handoff where people review, approve, correct, or take over. PM relevance: Place humans where impact or uncertainty justifies the delay.


### Hybrid retrieval

Combining lexical and semantic retrieval. PM relevance: Use when exact identifiers and conceptual matches both matter.


## I


### Idempotency

A property ensuring repeated execution of the same request does not create duplicate side effects.


### Image/video generation

Models that synthesize or edit visual media from instructions and references. PM relevance: Define rights, provenance, brand control, and review.


### Incident severity

A tier based on impact, scope, sensitivity, reversibility, and obligations. PM relevance: Predefine response, leadership, communication, and review by tier.


### Indemnity

Contractual allocation of specified third-party claims or losses. PM relevance: Review scope, exclusions, caps, and product usage requirements with counsel.


### Inference

Running a trained model to produce a prediction or generation. PM relevance: Define performance at realistic input/output lengths and concurrency.


### Inference endpoint

A network-accessible service that runs a model.


### Instruction tuning

Training on instruction-response examples to improve task following. PM relevance: Use for consistent task behavior across many prompts.


### Inter-token latency

Delay between streamed output tokens. PM relevance: Optimize conversational flow and reading experience.


### Interleaving

Mixing ranked outputs from two systems for sensitive comparison. PM relevance: Use for search or recommendation ranking with less traffic.


### Internal-ops agent

AI acting across enterprise tools for employees. PM relevance: Use least privilege, identity propagation, approvals, and audit.


### Interpretability

The degree to which a person can understand the mechanism or drivers of a model output.


### IoU

Intersection over union, a measure of overlap used for detection and segmentation.


### ISO/IEC 42001

An AI management-system standard based on continual improvement. PM relevance: Use to structure organization-wide policy, roles, risk, and audit.


## J


### Jailbreak

An input designed to bypass model safety behavior. PM relevance: Test abuse cases and apply layered policy enforcement.


## K


### Knowledge graph

Entities and typed relationships represented as a graph for query and reasoning.


### KV cache

Stored attention state that avoids recomputing prior tokens during generation. PM relevance: Budget memory and reuse for long or repeated contexts.


## L


### Label

The outcome a supervised model learns to predict. PM relevance: Define timing, quality, ambiguity, and adjudication.


### Large language model

A model trained primarily to predict and generate sequences of tokens. PM relevance: Use when language understanding or generation is central.


### Latency percentile

A distribution point such as P95: 95 percent of observations are at or below it.


### Launch gate

Evidence and approvals required before exposure increases. PM relevance: Make objective, risk-tiered, and reversible.


### Learning rate

The step size used when updating model parameters during training.


### Least privilege

Giving each agent and tool only the permissions needed for the current task. PM relevance: Use scoped identities, narrow functions, and short-lived credentials.


### License

Terms governing use, modification, distribution, commercial rights, and obligations for code, data, or model weights.


### LLM-as-judge

A model scores outputs using a rubric. PM relevance: Use for scale after calibrating against expert judgments.


### Log loss

A probability-sensitive classification loss that heavily penalizes confident wrong predictions.


### Long context

A large context window; useful only when the model can locate and apply relevant information reliably.


### LoRA

A PEFT method that learns low-rank weight updates. PM relevance: Use for efficient specialization when supported by the model stack.


## M


### Machine learning

Methods that learn patterns from data to make predictions, representations, decisions, or generated outputs.


### Managed service

A provider-operated system that reduces infrastructure work but introduces contractual and dependency considerations.


### Material change

A modification significant enough to trigger renewed testing, review, notice, or approval.


### MCP

An open protocol for connecting AI applications to tools, resources, and contextual services. PM relevance: Use to standardize integration, while evaluating auth and server trust.


### MCP Apps

An emerging MCP extension pattern for tool-provided interactive user interfaces; confirm the active specification before production use.


### Memory

Stored state used across turns or tasks, ranging from session history to durable profiles. PM relevance: Define purpose, retention, consent, correction, and deletion.


### Memory tier

A defined retention layer such as turn, session, workspace, or durable profile, each with separate purpose and deletion rules.


### Metadata filter

A deterministic constraint on retrieval based on fields such as tenant, date, region, type, or permission.


### Minimum viable intelligence

The least sophisticated intelligence that produces the target outcome. PM relevance: Start with rules or retrieval if they satisfy the job.


### Mixture of experts

A model architecture that routes each token or input through a subset of specialized parameter blocks.


### Model card

A structured record of model purpose, data, performance, limitations, and use constraints. PM relevance: Require from builders or vendors and connect to system evidence.


### Model change policy

How a provider versions, deprecates, and changes behavior. PM relevance: Require notice, pinned versions where possible, and migration support.


### Model collapse

Degradation that can occur when training repeatedly on low-quality model-generated data without sufficient real data and controls.


### Model extraction

An attack that attempts to reproduce or steal model behavior through queries or access.


### Model inversion

An attack that infers information about training data from model behavior.


### Model layer

The learned component that maps inputs to predictions, rankings, representations, or generated content. PM relevance: Choose task capability and operating constraints before a vendor name.


### Model portfolio

A governed set of models assigned to approved tasks and risk tiers. PM relevance: Manage models as products with owners, versions, and retirement plans.


### Model registry

A controlled catalog of model versions, metadata, approvals, and deployment state. PM relevance: Use as the source of truth for promotion and retirement.


### Model regression

A new version performs worse on important behavior or slices. PM relevance: Pin, evaluate, canary, monitor, and rollback.


### Model risk management

Governance for identifying, validating, approving, monitoring, and challenging model risks.


### Model router

Logic that selects a model based on task, risk, cost, or confidence. PM relevance: Use when workloads are heterogeneous and routing can be evaluated.


### Model supply chain

Models, datasets, adapters, code, and dependencies that can be compromised. PM relevance: Track provenance, signatures, licenses, vulnerabilities, and vendors.


### Model version pinning

Selecting a fixed model snapshot to reduce unplanned behavior changes.


### Model-as-a-service

Managed inference with vendor-operated infrastructure. PM relevance: Use when operational simplicity outweighs control requirements.


### MRR

Mean reciprocal rank, which rewards placing the first relevant result near the top.


### Multimodality

A model’s ability to process or produce multiple media types. PM relevance: Evaluate each modality and cross-modal interaction separately.


## N


### nDCG

Normalized discounted cumulative gain, a ranking metric that values graded relevance near the top.


### Neural network

A parameterized layered function trained from data.


### NIST AI RMF

A voluntary US framework organized around Govern, Map, Measure, and Manage. PM relevance: Use as a common risk-management vocabulary and evidence map.


### Non-determinism

Variation in system output or trajectory caused by sampling, parallelism, model updates, or external state.


### Nonfunctional requirement

A requirement for latency, availability, privacy, security, accessibility, cost, or scale. PM relevance: Make targets measurable by traffic class and risk tier.


### North-star metric

The primary measure of recurring user value created. PM relevance: Pair with quality, risk, cost, and adoption guardrails.


## O


### Observability

The ability to infer system state and diagnose behavior from metrics, logs, traces, and evidence.


### OCR

Converting visual text into machine-readable text, often with layout information. PM relevance: Treat OCR confidence and document structure as inputs to downstream logic.


### Office artifact

A reusable document that makes alignment and execution easier. PM relevance: Maintain decision memo, one-page PRD, eval card, risk register, and launch scorecard.


### Offline evaluation

Testing on stored or simulated cases before affecting live users.


### Online evaluation

Measurement with real users or production traffic. PM relevance: Use staged exposure with guardrails after offline qualification.


### Online feature

A feature computed or retrieved at decision time under strict freshness and latency constraints.


### Open source

Software whose source is available under an open-source license; do not automatically apply the term to model weights.


### Open-weight model

Downloadable weights under a specific license, not necessarily open-source training. PM relevance: Use when control, locality, adaptation, or scale economics justify operations.


### Operating cadence

Regular reviews for quality, cost, incidents, risks, vendors, and roadmap. PM relevance: Set frequency by change rate and consequence.


### Out-of-distribution

Inputs that differ materially from the data or conditions on which performance was established.


### Outcome pricing

Charging based on an achieved business result. PM relevance: Use only where outcome attribution and risk sharing are clear.


### Overfitting

Learning training-specific patterns that fail to generalize.


## P


### Pairwise evaluation

Choosing the better of two outputs rather than assigning absolute scores. PM relevance: Use for preference and model comparisons.


### Parameter

A learned numerical value inside a model.


### Parameter count

The number of learned values in a model; a weak standalone proxy for useful capability.


### PEFT

Parameter-efficient fine-tuning that updates a small set of parameters. PM relevance: Use to reduce adaptation compute and store multiple variants.


### Perplexity

A next-token prediction metric; lower values do not directly guarantee better product behavior.


### Physical AI

AI systems that perceive, reason, and act in physical environments, including robots and autonomous machines.


### PII

Personally identifiable information; definitions and obligations vary by jurisdiction and context.


### Plugin

A packaged extension that adds capabilities or integrations; it must be governed as code and supply-chain dependency.


### Point-in-time correctness

Using only information available at the historical decision moment. PM relevance: Require for training and backtesting predictive systems.


### Policy engine

Deterministic software that evaluates authorization or business rules outside the model.


### Portfolio narrative

A coherent explanation of the problems and capabilities your work proves. PM relevance: Map projects to product, technical, business, and leadership skills.


### Post-training

Training after broad pretraining, including instruction, preference, safety, or task adaptation.


### Postmortem

A structured analysis of timeline, impact, causes, detection, response, and actions. PM relevance: Focus on contributing system conditions and tested remediation.


### Precision

Among predicted positives, the fraction truly positive. PM relevance: Optimize when false positives are expensive.


### Precision-recall curve

A view of classification trade-offs across thresholds, especially useful for rare positives.


### Preference optimization

Training from pairwise or scored preferences, including DPO-style methods. PM relevance: Use when desired behavior is easier to compare than specify.


### Pretraining

Large-scale training on broad data before downstream adaptation.


### Privacy threat model

Analysis of how personal or sensitive data can be collected, inferred, exposed, or retained. PM relevance: Perform for prompts, logs, training, retrieval, memory, and vendors.


### Privacy-enhancing technology

Techniques such as differential privacy, secure computation, or trusted execution that reduce data exposure.


### Probabilistic behavior

The same or similar input can produce different outputs or confidence levels. PM relevance: Specify ranges, abstention, review, and fallback instead of one perfect answer.


### Product intuition

A practiced sense for user value, behavior, and adoption. PM relevance: Build from observation, prototypes, and outcome reviews.


### Production gap

The work between a demo and a reliable, secure, governed service. PM relevance: Make the gap visible in roadmap and cost.


### Progressive autonomy

Increasing automation as evidence, controls, and user trust mature. PM relevance: Move from suggest to draft to approve to auto-act by risk tier.


### Prompt caching

Reusing computation for repeated prompt prefixes. PM relevance: Design stable prefixes where privacy and vendor semantics allow.


### Prompt injection

Untrusted content manipulates model instructions or tool behavior. PM relevance: Treat all external content as untrusted and isolate authority.


### Prompt management

Versioning, testing, approving, deploying, and monitoring prompts and related configuration.


### Prompt template

A versioned structure with controlled variables. PM relevance: Separate stable instructions from untrusted user or retrieved content.


### Prototype eval

A small but representative test used during discovery. PM relevance: Use before interpreting demo anecdotes.


### Provenance

Traceable origin and transformation history for data, evidence, models, or media.


### Pseudonymization

Replacing direct identifiers with controlled substitutes; the data may remain personal data.


## Q


### Quantization

Reducing numerical precision to lower memory and increase speed. PM relevance: Use after task and safety regression tests.


### Quantization-aware adaptation

Training or adapting with reduced numerical precision constraints. PM relevance: Use when deployment memory or latency is tight.


## R


### RAG

Retrieval-augmented generation, which retrieves external evidence and supplies it to a generative model.


### RAG evaluation

Separate measurement of retrieval quality and grounded answer quality. PM relevance: Diagnose context recall, precision, faithfulness, and citation correctness.


### Rate limit

A cap on request or token volume over time. PM relevance: Design quotas, queues, priorities, and vendor headroom.


### Rate limiting

Restricting traffic or actions over time to protect reliability, cost, and security.


### Realtime model

A low-latency streaming model for interactive audio or multimodal sessions. PM relevance: Budget turn latency across capture, network, model, tools, and playback.


### Reasoning effort

A configurable amount of inference computation allocated to solving a task, trading quality against time and cost.


### Reasoning model

A model optimized to spend additional inference computation on complex tasks. PM relevance: Use where added quality exceeds latency and cost.


### Recall

Among actual positives, the fraction found. PM relevance: Optimize when misses are expensive.


### Recall@k

Whether relevant items appear within the top k retrieved or ranked results.


### Recommendation feedback loop

A dynamic where recommendations shape future interaction data and can reinforce popularity or bias.


### Recommendation system

Ranking items or actions for a user or context. PM relevance: Balance relevance with diversity, novelty, fairness, and business constraints.


### Red teaming

Structured adversarial testing by people and automation. PM relevance: Run before launch and continuously after system changes.


### Redaction

Removing or masking sensitive content from data or output.


### Regression

Predicting a continuous numeric value; also a decline in behavior after change, depending on context.


### Reinforcement learning

Learning a policy from rewards obtained through interaction or simulated experience.


### Representation learning

Learning useful feature vectors from raw data.


### Reranker

A second-stage model that reorders retrieved candidates. PM relevance: Use when first-stage recall is good but top results are noisy.


### Responsible AI

Practices for developing and using AI with accountability, safety, fairness, privacy, transparency, and human considerations.


### Retrieval freshness

How quickly updated source information becomes available to queries.


### Retrieval poisoning

Malicious or low-quality content enters the knowledge path. PM relevance: Control sources, provenance, ingestion, ranking, and content trust.


### Reversibility

How easily a wrong action can be undone. PM relevance: Allow more autonomy for cheap, observable, reversible actions.


### Reward hacking

A system exploiting a reward definition in a way that improves the metric but harms the intended goal.


### Risk acceptance

Explicit authorization to proceed with a known residual risk. PM relevance: Name scope, rationale, duration, owner, and review date.


### Risk tiering

Classifying systems by impact, autonomy, data, users, and legal category. PM relevance: Apply proportionate evidence, approval, and monitoring.


### RLAIF

Reinforcement learning from AI feedback, where model-generated judgments supplement or replace some human ratings.


### RLHF

Reinforcement learning from human feedback, a family of methods for aligning behavior to human preferences.


### RLVR

Reinforcement learning with verifiable rewards, using automatically checkable outcomes such as tests or exact answers.


### Robotics foundation model

A broadly trained model adapted to perception, planning, or action across robotic tasks.


### ROC curve

True-positive rate versus false-positive rate across thresholds.


### Rollback

Returning safely to a previously qualified configuration. PM relevance: Pre-plan compatibility, state, and data implications.


### Runaway agent

A loop repeats actions, calls, or retries, causing harm or spend. PM relevance: Set hard budgets, idempotency, stop conditions, and circuit breakers.


## S


### Sampling

Selecting output tokens from a probability distribution, controlling variation and diversity.


### Sandbox

An isolated environment limiting code, files, network, and system effects. PM relevance: Use for untrusted code or tool execution with resource limits.


### Schema

A formal description of data fields, types, relationships, and constraints.


### Self-hosting

Operating model weights and inference infrastructure yourself or through a managed host. PM relevance: Use when control or economics clearly exceed operational burden.


### Semantic cache

Reuse of outputs for meaningfully similar inputs, requiring strict privacy, permission, and freshness design.


### Semantic search

Retrieval based on representation similarity rather than exact terms alone.


### Sensitive attribute

A characteristic requiring special protection or fairness analysis depending on context and law.


### Sequence length

The number of tokens in model input or output, a major driver of memory, latency, and cost.


### Service account

A non-human identity used by software; scope and rotation are crucial for agent security.


### Shadow deployment

Running a candidate on production inputs without affecting users. PM relevance: Use to measure realistic behavior and cost safely.


### Shadow mode

Producing outputs without affecting user decisions. PM relevance: Use to compare with current process and observe real distributions.


### SHAP

A family of feature-attribution methods based on cooperative game theory.


### Silent failure

The system appears successful but produces wrong, incomplete, or unexecuted results. PM relevance: Add independent verification and outcome reconciliation.


### Simulation eval

Evaluation in a controlled environment that models users, tools, or world dynamics before real exposure.


### Skill

A reusable instruction-and-resource package that teaches an agent a workflow; trust, scope, versioning, and permissions still apply.


### SLA

A contractual service commitment with remedies. PM relevance: Align uptime, latency, support, and recovery to product needs.


### SLO

A target reliability level for a user-relevant service measure. PM relevance: Define for latency, availability, freshness, quality, and recovery.


### Small language model

A lower-capacity model optimized for cost, speed, privacy, or edge deployment. PM relevance: Use for bounded, frequent tasks with strong evals.


### Small model

A relatively lower-capacity model chosen for bounded capability, efficiency, locality, or cost.


### Sparse retrieval

Retrieval based on term or learned sparse representations, often strong for exact identifiers.


### Speculative decoding

Using a draft model or method to propose tokens that a target model verifies, improving speed when acceptance is high.


### Speech-to-text

Transcribing audio into text, optionally with timestamps and speakers. PM relevance: Test accents, noise, code-switching, jargon, and consent.


### Streaming

Returning partial output as it becomes available rather than waiting for completion.


### Structured output

Generation constrained to a schema such as JSON. PM relevance: Use when downstream code or UI requires predictable fields.


### Structured prediction

Predicting interdependent outputs such as sequences, trees, or labels with relationships.


### Supervised learning

Learning a mapping from examples with known targets. PM relevance: Confirm that labels represent the decision you truly care about.


### Synthetic data

Model-generated examples used for training, testing, or augmentation. PM relevance: Use to cover rare cases, but validate realism and contamination.


### Synthetic media

AI-generated or materially altered image, audio, video, or text.


### System card

Documentation of the end-to-end system, evaluations, safeguards, and limitations. PM relevance: Use for complex generative and agentic products.


### System instruction

The highest-level behavioral guidance supplied by the application. PM relevance: Keep stable policy, role, boundaries, and output contract here.


## T


### Task decomposition

Breaking a workflow into observable steps with different uncertainty and permissions. PM relevance: Automate low-risk, measurable steps before the whole job.


### Task success rate

Fraction of cases where the user’s intended task is completed acceptably. PM relevance: Make the primary metric end-to-end and rubric-based.


### Technical fluency

Ability to reason about data, models, RAG, agents, evals, serving, and failure. PM relevance: Explain trade-offs in plain language and ask precise questions.


### Technical judgment

Choosing among mechanisms based on evidence and constraints. PM relevance: Develop through eval reviews, architecture walkthroughs, incidents, and hands-on prototypes.


### Technical spike

Time-boxed engineering work to answer a feasibility question. PM relevance: Use for unknowns such as latency, permissions, or model capability.


### Temperature

A sampling control affecting output diversity, not factual certainty. PM relevance: Use low variation for repeatable workflows and higher variation for ideation.


### Temperature scaling

A post-hoc method for calibrating probability outputs; distinct from generation temperature.


### Tenant isolation

Preventing one customer or organizational tenant from accessing another’s data or computation.


### Test-time compute

Additional inference work used to improve a response, such as longer reasoning or multiple candidates.


### Test-time scaling

Improving results by spending more inference computation through reasoning, search, sampling, or verification.


### Text generation inference

A serving category and also the name of a Hugging Face inference server; clarify usage.


### Text-to-speech

Generating spoken audio from text with controllable voice and style. PM relevance: Design pronunciation, interruption, disclosure, and fallback.


### Throughput

Amount of work served per unit time. PM relevance: Plan capacity using realistic concurrency and sequence lengths.


### Time to first token

Delay before the first generated token reaches the user. PM relevance: Optimize perceived responsiveness for streaming interactions.


### Token

A model’s unit of text processing; words may split into several tokens. PM relevance: Budget context and output in tokens, not pages.


### Token economics

How input, output, cached, and reasoning tokens drive hosted-model cost. PM relevance: Reduce unnecessary context and outputs after protecting quality.


### Tool calling

A model selects a named function and structured arguments; application code executes it. PM relevance: Expose narrow, typed functions with explicit authorization.


### Tool result injection

Malicious instructions embedded in tool output that attempt to redirect an agent.


### Top-k sampling

Restricting generation choices to the k most probable tokens at each step.


### Top-p sampling

Restricting generation choices to the smallest set whose cumulative probability reaches p.


### Trace

A connected record of steps, spans, tool calls, retrieval, and timings for one request or task. PM relevance: Use for debugging agents and multi-stage pipelines.


### Trace-based eval

Scoring an agent’s intermediate trajectory, tool calls, evidence, and recovery in addition to its final output.


### Trade-off statement

A concise explanation of what improves, what worsens, and for whom. PM relevance: Use in every model, scope, autonomy, and launch recommendation.


### Training use

Whether customer data may improve or train provider models. PM relevance: Require explicit terms for all services and subprocessors.


### Training-serving skew

A mismatch between data or computation used during training and production inference.


### Transformer

A neural architecture built around attention, now common across language and multimodal models.


### Trust center

A maintained destination for security, privacy, governance, reliability, and AI documentation. PM relevance: Use to make evidence discoverable and current.


## U


### Unsupervised learning

Finding structure without target labels, such as clusters or anomalies. PM relevance: Use for exploration or prioritization, then validate human meaning.


### Uplift modeling

Estimating which individuals change behavior because of an intervention.


### Usage pricing

Charging by requests, tokens, minutes, images, or completed actions. PM relevance: Use when usage correlates with value and customers can predict spend.


## V


### Value sensitivity

How business outcome changes across model-quality or adoption scenarios. PM relevance: Run downside/base/upside analysis before investment.


### Vector

An ordered list of numbers representing features or learned meaning.


### Vector database

A store optimized for nearest-neighbor search over embeddings. PM relevance: Evaluate filtering, tenancy, freshness, deletion, scale, and operations.


### Vector index

A data structure supporting efficient nearest-neighbor search over vectors.


### Verifiable reward

A reward determined by an objective checker such as a unit test, compiler, solver, or exact-match rule.


### Version manifest

A record of every component affecting behavior in a release.


### Vertical slice

A thin end-to-end implementation across UI, data, model, and operations. PM relevance: Use to reveal integration and experience constraints.


### Vibe coding

Building software primarily through natural-language collaboration with coding models; speed does not remove review, testing, security, or ownership.


### Vision-language model

A model that jointly processes images and language.


## W


### Watermark

A signal embedded in generated content to support identification; robustness and coverage vary.


### Weak supervision

Combining noisy heuristics or sources to create probabilistic labels. PM relevance: Use to bootstrap when gold labels are scarce.


### Wizard-of-Oz test

Users experience an automated-looking service partly operated by humans. PM relevance: Use to validate value and interaction before expensive automation.


### Workflow

A mostly predefined sequence of steps and branches. PM relevance: Prefer for repeatable, regulated, or high-volume operations.


### Workflow change

Redesign of roles, decisions, handoffs, and incentives around the AI system. PM relevance: Plan training, policy, operations, and management behavior.


### World model

A learned representation of how an environment changes, used for prediction, planning, simulation, or control.


## Z


### Zero-shot

Performing a task from instructions without task-specific examples in context.


---SECTION---

# Appendix K. Coverage audit against recent AI-PM books and curricula


This volume uses published tables of contents and curriculum descriptions as a coverage check, not as text to reproduce. The treatment, frameworks, language, templates, and glossary here are original.


| Reference | Edition checked | Coverage signal incorporated |
|---|---|---|
| Building AI-Powered Products | Marily Nika, O’Reilly, 2025 | Role, lifecycle, AI PM profiles, probabilistic products, cross-functional execution. |
| The AI Product Manager’s Handbook | Irene Bratsis, Packt, 2023 | AI/ML foundations, infrastructure, product development, model optimization, ethics and legal considerations. |
| AI Engineering | Chip Huyen, O’Reilly, 2024 | Foundation-model applications, evaluation, prompting, RAG, agents, finetuning, inference optimization. |
| Product Management for AI | Justin Norman, Peter Skomoroch, Mike Loukides, O’Reilly, 2021 | Uncertainty, problem selection, data lifecycle, deployment and monitoring. |
| AI Meets Strategy | Anshuman Srivastava, Abhinav Garg, Anshuman Mishra, Apress, 2026 | Strategy, operating models, trustworthy AI, governance and enterprise transformation. |
| Building AI-Powered Financial Products | Abhijit Dey, Srinivasan Shanmuganathan, David Roldán Martínez, Packt, 2026 | AI-first fintech product thinking, regulatory intelligence, infrastructure, explainability and ecosystem design. |
| AI Product Management Certification curriculum | Product School, accessed 14 July 2026 | AI-specific PRDs, RAG, prompting, AI UX, evaluation and hands-on product specifications. |


## Primary current-state sources


Fast-changing claims were checked against primary or official sources on 14 July 2026. Vendor catalogs, preview labels, prices, standards, and legal timelines can change; re-check before making a production, procurement, or compliance decision.


- [European Commission — AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)

- [NIST — AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

- [NIST AI 600-1 — Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

- [ISO — ISO/IEC 42001:2023 overview](https://www.iso.org/standard/42001)

- [OWASP — Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

- [Model Context Protocol — 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)

- [A2A Protocol — official specification](https://a2a-protocol.org/latest/)

- [OpenAI — API quickstart and tool/agent overview](https://platform.openai.com/docs/quickstart)

- [Google — Gemini model catalog](https://ai.google.dev/gemini-api/docs/models)

- [Anthropic — Model Context Protocol documentation](https://docs.anthropic.com/en/docs/mcp)

- [Hugging Face — Inference Endpoints](https://huggingface.co/docs/inference-endpoints/about)

- [Hugging Face — PEFT](https://huggingface.co/docs/peft/index)


## July 2026 snapshot notes


- The foundation-model market spans proprietary hosted APIs, open-weight models, specialized reasoning, coding, image, video, speech, realtime, and small/edge models. This guide deliberately avoids declaring one permanent winner.

- MCP’s public 2026 roadmap focuses on transport scalability, agent communication, governance maturity, and enterprise readiness. A release candidate for a 28 July 2026 specification was public before this guide’s cutoff; because the final date was still in the future on 14 July, this edition treats it as forthcoming, not final.

- A2A’s official specification describes interoperability among independent agents. Use MCP and A2A as complementary patterns only where the product needs them; protocol adoption does not remove authorization, identity, evaluation, or vendor-risk work.

- The European Commission’s implementation page should be treated as the live source for AI Act timing. This guide is educational and does not substitute for legal analysis of actor role, system category, sector, or geography.

- NIST states that AI RMF 1.0 is being revised. Teams should use the current framework and GenAI profile while tracking revision status rather than freezing policy to a stale summary.


# Final desk card: the 12 questions


1. What user job or decision changes?

2. What is the current and non-AI baseline?

3. What is the minimum viable intelligence?

4. What is the operating envelope?

5. Which error matters most, to whom, and why?

6. What data and permission make the behavior possible?

7. What eval represents real frequency and consequence?

8. What can the user inspect, correct, approve, or undo?

9. What prevents one bad output from becoming a bad action?

10. What is total cost per successful task?

11. What qualifies launch, pauses ramp, and triggers rollback?

12. Who owns the product after the model changes?


> If you can answer these twelve questions with evidence, you can lead the AI product conversation in almost any room.
