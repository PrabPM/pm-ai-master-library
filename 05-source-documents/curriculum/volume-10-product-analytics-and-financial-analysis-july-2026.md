# Volume 10 — Product Analytics and Financial Analysis

## July 2026 handbook: metrics, attribution, cohorts, unit economics, dashboards, and data architecture

Edition date: 14 July 2026  
+Companion to the ML/AI PM Masterclass

This handbook converts the supplied pathway list into an original, product-manager-focused curriculum. Course counts are depth signals only. Examples use the fictional **PayFlow** product.

# How to use this volume

Read the capability chapters, complete the applied labs, use the cases for interviews and portfolio stories, and copy the operating templates into real work. Every claim should remain traceable to evidence or a primary source.

# 1. Lifetime Value (LTV)

**Coverage basis:** 4 courses in the supplied pathway. **Practice lens:** unit economics.

## Capability and decision

Lifetime Value (LTV) is revenue and cost behavior at a decision-relevant unit. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Unit:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Margin:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cac:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Ltv:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Sensitivity:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **merchant acquisition**, PayFlow uses lifetime value (ltv) to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready lifetime value (ltv) packet for merchant acquisition: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 2. SQL Analysis

**Coverage basis:** 12 courses in the supplied pathway. **Practice lens:** analysis.

## Capability and decision

SQL Analysis is reproducible transformation from question to decision. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Grain:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Population:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Measure:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Check:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Interpretation:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **payment attempts**, PayFlow uses sql analysis to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready sql analysis packet for payment attempts: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 3. Attribution Model

**Coverage basis:** 6 courses in the supplied pathway. **Practice lens:** attribution.

## Capability and decision

Attribution Model is rules or models assigning credit across touchpoints. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Scope:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Lookback:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Identity:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Counterfactual:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Limitation:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **subscription retention**, PayFlow uses attribution model to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **incremental lift, path coverage, model stability, unattributed share, sensitivity**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **credit mistaken for causality, identity gaps, lookback cherry-picking, double counting**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready attribution model packet for subscription retention: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 4. Tracking Plan

**Coverage basis:** 23 courses in the supplied pathway. **Practice lens:** instrumentation.

## Capability and decision

Tracking Plan is designed collection of reliable behavioral events. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Event:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Property:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Identity:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Quality:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Governance:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **marketplace matching**, PayFlow uses tracking plan to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **event validity, property completeness, identity match, latency, schema violations**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **tracking after launch, ambiguous events, PII leakage, silent schema drift**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready tracking plan packet for marketplace matching: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 5. Churn Analysis

**Coverage basis:** 9 courses in the supplied pathway. **Practice lens:** lifecycle analytics.

## Capability and decision

Churn Analysis is cohort-based measurement over customer time. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Cohort:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Exposure:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Retention:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Censoring:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Hazard:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **AI answer quality**, PayFlow uses churn analysis to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready churn analysis packet for AI answer quality: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 6. ROI Analysis

**Coverage basis:** 18 courses in the supplied pathway. **Practice lens:** unit economics.

## Capability and decision

ROI Analysis is revenue and cost behavior at a decision-relevant unit. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Unit:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Margin:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cac:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Ltv:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Sensitivity:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **enterprise expansion**, PayFlow uses roi analysis to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready roi analysis packet for enterprise expansion: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 7. Marketplace Liquidity

**Coverage basis:** 6 courses in the supplied pathway. **Practice lens:** marketplace analytics.

## Capability and decision

Marketplace Liquidity is measurement of matching and ecosystem health. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Fill Rate:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Time To Match:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Density:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Quality:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Balance:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **pricing economics**, PayFlow uses marketplace liquidity to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready marketplace liquidity packet for pricing economics: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 8. Marketing Attribution

**Coverage basis:** 8 courses in the supplied pathway. **Practice lens:** attribution.

## Capability and decision

Marketing Attribution is rules or models assigning credit across touchpoints. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Scope:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Lookback:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Identity:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Counterfactual:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Limitation:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **support operations**, PayFlow uses marketing attribution to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **incremental lift, path coverage, model stability, unattributed share, sensitivity**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **credit mistaken for causality, identity gaps, lookback cherry-picking, double counting**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready marketing attribution packet for support operations: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 9. ROAS Analysis

**Coverage basis:** 11 courses in the supplied pathway. **Practice lens:** unit economics.

## Capability and decision

ROAS Analysis is revenue and cost behavior at a decision-relevant unit. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Unit:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Margin:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cac:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Ltv:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Sensitivity:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **merchant acquisition**, PayFlow uses roas analysis to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready roas analysis packet for merchant acquisition: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 10. Engagement Analysis

**Coverage basis:** 26 courses in the supplied pathway. **Practice lens:** behavior analytics.

## Capability and decision

Engagement Analysis is measurement of actions and progression. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Event:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **User:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Session:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Funnel:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Segment:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **payment attempts**, PayFlow uses engagement analysis to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready engagement analysis packet for payment attempts: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 11. Metrics Dashboard

**Coverage basis:** 25 courses in the supplied pathway. **Practice lens:** measurement.

## Capability and decision

Metrics Dashboard is a governed system connecting outcomes to signals. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **North Star:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Input:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Guardrail:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Owner:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cadence:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **subscription retention**, PayFlow uses metrics dashboard to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **north-star movement, input elasticity, guardrail stability, definition consistency, freshness**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **metric proliferation, proxy gaming, no owner, incompatible definitions**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready metrics dashboard packet for subscription retention: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 12. Financial Projections

**Coverage basis:** 17 courses in the supplied pathway. **Practice lens:** finance.

## Capability and decision

Financial Projections is forward and backward view of economic performance. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Revenue:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cost:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cash:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Scenario:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Variance:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **marketplace matching**, PayFlow uses financial projections to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready financial projections packet for marketplace matching: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 13. Financial Analysis

**Coverage basis:** 31 courses in the supplied pathway. **Practice lens:** finance.

## Capability and decision

Financial Analysis is forward and backward view of economic performance. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Revenue:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cost:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cash:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Scenario:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Variance:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **AI answer quality**, PayFlow uses financial analysis to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready financial analysis packet for AI answer quality: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 14. Data Architecture

**Coverage basis:** 23 courses in the supplied pathway. **Practice lens:** data systems.

## Capability and decision

Data Architecture is architecture that makes trusted data available. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Source:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Contract:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Transform:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Lineage:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Access:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **enterprise expansion**, PayFlow uses data architecture to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **freshness, lineage coverage, test pass rate, query cost, access violations**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **undocumented transforms, semantic drift, unsafe access, warehouse-as-truth without contracts**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready data architecture packet for enterprise expansion: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 15. CAC Analysis

**Coverage basis:** 11 courses in the supplied pathway. **Practice lens:** unit economics.

## Capability and decision

CAC Analysis is revenue and cost behavior at a decision-relevant unit. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Unit:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Margin:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cac:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Ltv:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Sensitivity:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **pricing economics**, PayFlow uses cac analysis to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready cac analysis packet for pricing economics: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 16. Cohort Analysis

**Coverage basis:** 18 courses in the supplied pathway. **Practice lens:** lifecycle analytics.

## Capability and decision

Cohort Analysis is cohort-based measurement over customer time. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Cohort:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Exposure:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Retention:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Censoring:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Hazard:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **support operations**, PayFlow uses cohort analysis to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready cohort analysis packet for support operations: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 17. Correlation Analysis

**Coverage basis:** 11 courses in the supplied pathway. **Practice lens:** statistics.

## Capability and decision

Correlation Analysis is reasoning about association, uncertainty, and causality. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Variable:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Distribution:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Effect:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Confounder:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Uncertainty:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **merchant acquisition**, PayFlow uses correlation analysis to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **effect estimate, interval, power, robustness, calibration**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **multiple testing, selective reporting, leakage, model-assumption blindness**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready correlation analysis packet for merchant acquisition: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 18. Funnel Analysis

**Coverage basis:** 23 courses in the supplied pathway. **Practice lens:** behavior analytics.

## Capability and decision

Funnel Analysis is measurement of actions and progression. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Event:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **User:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Session:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Funnel:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Segment:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **payment attempts**, PayFlow uses funnel analysis to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready funnel analysis packet for payment attempts: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 19. Metrics Framework

**Coverage basis:** not specified. **Practice lens:** measurement.

## Capability and decision

Metrics Framework is a governed system connecting outcomes to signals. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **North Star:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Input:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Guardrail:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Owner:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cadence:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **subscription retention**, PayFlow uses metrics framework to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **north-star movement, input elasticity, guardrail stability, definition consistency, freshness**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **metric proliferation, proxy gaming, no owner, incompatible definitions**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready metrics framework packet for subscription retention: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 20. Product Analytics Foundations

**Coverage basis:** curriculum gap. **Practice lens:** measurement.

## Capability and decision

Product Analytics Foundations is a governed system connecting outcomes to signals. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **North Star:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Input:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Guardrail:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Owner:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cadence:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **marketplace matching**, PayFlow uses product analytics foundations to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **north-star movement, input elasticity, guardrail stability, definition consistency, freshness**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **metric proliferation, proxy gaming, no owner, incompatible definitions**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready product analytics foundations packet for marketplace matching: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 21. Metric Trees and North-Star Systems

**Coverage basis:** curriculum gap. **Practice lens:** measurement.

## Capability and decision

Metric Trees and North-Star Systems is a governed system connecting outcomes to signals. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **North Star:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Input:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Guardrail:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Owner:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cadence:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **AI answer quality**, PayFlow uses metric trees and north-star systems to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **north-star movement, input elasticity, guardrail stability, definition consistency, freshness**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **metric proliferation, proxy gaming, no owner, incompatible definitions**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready metric trees and north-star systems packet for AI answer quality: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 22. Experimentation and Statistical Power

**Coverage basis:** curriculum gap. **Practice lens:** statistics.

## Capability and decision

Experimentation and Statistical Power is reasoning about association, uncertainty, and causality. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Variable:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Distribution:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Effect:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Confounder:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Uncertainty:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **enterprise expansion**, PayFlow uses experimentation and statistical power to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **effect estimate, interval, power, robustness, calibration**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **multiple testing, selective reporting, leakage, model-assumption blindness**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready experimentation and statistical power packet for enterprise expansion: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 23. Causal Inference and Incrementality

**Coverage basis:** curriculum gap. **Practice lens:** statistics.

## Capability and decision

Causal Inference and Incrementality is reasoning about association, uncertainty, and causality. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Variable:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Distribution:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Effect:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Confounder:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Uncertainty:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **pricing economics**, PayFlow uses causal inference and incrementality to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **effect estimate, interval, power, robustness, calibration**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **multiple testing, selective reporting, leakage, model-assumption blindness**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready causal inference and incrementality packet for pricing economics: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 24. Analytics Engineering and Semantic Layers

**Coverage basis:** curriculum gap. **Practice lens:** data systems.

## Capability and decision

Analytics Engineering and Semantic Layers is architecture that makes trusted data available. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Source:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Contract:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Transform:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Lineage:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Access:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **support operations**, PayFlow uses analytics engineering and semantic layers to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **freshness, lineage coverage, test pass rate, query cost, access violations**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **undocumented transforms, semantic drift, unsafe access, warehouse-as-truth without contracts**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready analytics engineering and semantic layers packet for support operations: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 25. Data Quality, Lineage and Governance

**Coverage basis:** curriculum gap. **Practice lens:** data systems.

## Capability and decision

Data Quality, Lineage and Governance is architecture that makes trusted data available. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Source:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Contract:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Transform:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Lineage:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Access:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **merchant acquisition**, PayFlow uses data quality, lineage and governance to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **freshness, lineage coverage, test pass rate, query cost, access violations**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **undocumented transforms, semantic drift, unsafe access, warehouse-as-truth without contracts**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready data quality, lineage and governance packet for merchant acquisition: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 26. Privacy-Aware Analytics and Consent

**Coverage basis:** curriculum gap. **Practice lens:** instrumentation.

## Capability and decision

Privacy-Aware Analytics and Consent is designed collection of reliable behavioral events. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Event:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Property:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Identity:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Quality:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Governance:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **payment attempts**, PayFlow uses privacy-aware analytics and consent to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **event validity, property completeness, identity match, latency, schema violations**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **tracking after launch, ambiguous events, PII leakage, silent schema drift**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready privacy-aware analytics and consent packet for payment attempts: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 27. AI Product Analytics and Evaluation

**Coverage basis:** curriculum gap. **Practice lens:** behavior analytics.

## Capability and decision

AI Product Analytics and Evaluation is measurement of actions and progression. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Event:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **User:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Session:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Funnel:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Segment:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **subscription retention**, PayFlow uses ai product analytics and evaluation to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready ai product analytics and evaluation packet for subscription retention: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# 28. Decision Science and Sensitivity Analysis

**Coverage basis:** curriculum gap. **Practice lens:** finance.

## Capability and decision

Decision Science and Sensitivity Analysis is forward and backward view of economic performance. The skill is complete only when it changes a decision and leaves an inspectable trail from evidence to interpretation to action. Begin with the affected user or economic unit, the consequence of error, the available evidence, and the reversible decision that can be made now.

## Core concepts

- **Revenue:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cost:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Cash:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Scenario:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.
- **Variance:** Define it operationally, state what evidence establishes it, name its owner, and describe the decision it changes.

## Method

1. Write the decision, riskiest assumption, scope, population, timeframe, and exclusions.
2. Select a method whose evidence can answer the question; document why cheaper alternatives are insufficient.
3. Define the artifact, success criterion, guardrails, and stopping rule before observing results.
4. Execute with provenance, consent or permissions, accessibility, and contradictory evidence preserved.
5. Validate data quality, sampling, identity, measurement, and alternative explanations.
6. Compare at least two options and state trade-offs, residual risk, and operational burden.
7. Recommend a bounded next step with owner, rollout, rollback, and review date.

## Worked PayFlow example

For **marketplace matching**, PayFlow uses decision science and sensitivity analysis to decide whether to change the current experience. The team declares one eligible segment, a baseline, the primary outcome, diagnostic signals, and customer, financial, and operational guardrails. Findings are labeled as observation, inference, or causal evidence. The recommendation begins with a reversible cohort and identifies the evidence that would stop expansion.

## Measurement and diagnostics

Track **metric validity, control-total match, effect intervals, freshness, decision latency**. Define the unit, denominator, observation or attribution window, data source, owner, and refresh cadence. Report the distribution and relevant segments instead of relying on a blended average.

## Failure modes and controls

Watch for **grain mismatch, proxy gaming, leakage, correlation as causation**. For each material failure, specify prevention, detection, recovery, escalation, and an accountable owner. Preserve negative results and unresolved contradictions.

## AI-era practice

Separate model, system, user-outcome, and business metrics; govern generated SQL and derived fields.

## Practice assignment

Create a decision-ready decision science and sensitivity analysis packet for marketplace matching: two-page brief, working artifact, assumptions, evidence table, metric specification, risk review, and recommendation. Add a one-paragraph critique describing what the packet cannot establish.


# Applied laboratories

These laboratories integrate the capabilities under realistic ambiguity. Use fictional data unless authorized to use protected information.

# Applied Lab 01 — Lifetime Value (LTV): Marketplace Matching

## Brief

PayFlow must make a decision about marketplace matching using lifetime value (ltv). Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using unit, margin, CAC, LTV, sensitivity.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 02 — SQL Analysis: Pricing Economics

## Brief

PayFlow must make a decision about pricing economics using sql analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using grain, population, measure, check, interpretation.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 03 — Attribution Model: Payment Attempts

## Brief

PayFlow must make a decision about payment attempts using attribution model. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using scope, lookback, identity, counterfactual, limitation.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 04 — Tracking Plan: Ai Answer Quality

## Brief

PayFlow must make a decision about AI answer quality using tracking plan. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using event, property, identity, quality, governance.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 05 — Churn Analysis: Support Operations

## Brief

PayFlow must make a decision about support operations using churn analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using cohort, exposure, retention, censoring, hazard.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 06 — ROI Analysis: Subscription Retention

## Brief

PayFlow must make a decision about subscription retention using roi analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using unit, margin, CAC, LTV, sensitivity.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 07 — Marketplace Liquidity: Enterprise Expansion

## Brief

PayFlow must make a decision about enterprise expansion using marketplace liquidity. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using fill rate, time to match, density, quality, balance.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 08 — Marketing Attribution: Merchant Acquisition

## Brief

PayFlow must make a decision about merchant acquisition using marketing attribution. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using scope, lookback, identity, counterfactual, limitation.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 09 — ROAS Analysis: Marketplace Matching

## Brief

PayFlow must make a decision about marketplace matching using roas analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using unit, margin, CAC, LTV, sensitivity.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 10 — Engagement Analysis: Pricing Economics

## Brief

PayFlow must make a decision about pricing economics using engagement analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using event, user, session, funnel, segment.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 11 — Metrics Dashboard: Payment Attempts

## Brief

PayFlow must make a decision about payment attempts using metrics dashboard. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using north star, input, guardrail, owner, cadence.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 12 — Financial Projections: Ai Answer Quality

## Brief

PayFlow must make a decision about AI answer quality using financial projections. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using revenue, cost, cash, scenario, variance.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 13 — Financial Analysis: Support Operations

## Brief

PayFlow must make a decision about support operations using financial analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using revenue, cost, cash, scenario, variance.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 14 — Data Architecture: Subscription Retention

## Brief

PayFlow must make a decision about subscription retention using data architecture. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using source, contract, transform, lineage, access.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 15 — CAC Analysis: Enterprise Expansion

## Brief

PayFlow must make a decision about enterprise expansion using cac analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using unit, margin, CAC, LTV, sensitivity.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 16 — Cohort Analysis: Merchant Acquisition

## Brief

PayFlow must make a decision about merchant acquisition using cohort analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using cohort, exposure, retention, censoring, hazard.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 17 — Correlation Analysis: Marketplace Matching

## Brief

PayFlow must make a decision about marketplace matching using correlation analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using variable, distribution, effect, confounder, uncertainty.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 18 — Funnel Analysis: Pricing Economics

## Brief

PayFlow must make a decision about pricing economics using funnel analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using event, user, session, funnel, segment.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 19 — Metrics Framework: Payment Attempts

## Brief

PayFlow must make a decision about payment attempts using metrics framework. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using north star, input, guardrail, owner, cadence.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 20 — Product Analytics Foundations: Ai Answer Quality

## Brief

PayFlow must make a decision about AI answer quality using product analytics foundations. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using north star, input, guardrail, owner, cadence.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 21 — Metric Trees and North-Star Systems: Support Operations

## Brief

PayFlow must make a decision about support operations using metric trees and north-star systems. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using north star, input, guardrail, owner, cadence.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 22 — Experimentation and Statistical Power: Subscription Retention

## Brief

PayFlow must make a decision about subscription retention using experimentation and statistical power. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using variable, distribution, effect, confounder, uncertainty.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 23 — Causal Inference and Incrementality: Enterprise Expansion

## Brief

PayFlow must make a decision about enterprise expansion using causal inference and incrementality. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using variable, distribution, effect, confounder, uncertainty.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 24 — Analytics Engineering and Semantic Layers: Merchant Acquisition

## Brief

PayFlow must make a decision about merchant acquisition using analytics engineering and semantic layers. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using source, contract, transform, lineage, access.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 25 — Data Quality, Lineage and Governance: Marketplace Matching

## Brief

PayFlow must make a decision about marketplace matching using data quality, lineage and governance. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using source, contract, transform, lineage, access.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 26 — Privacy-Aware Analytics and Consent: Pricing Economics

## Brief

PayFlow must make a decision about pricing economics using privacy-aware analytics and consent. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using event, property, identity, quality, governance.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 27 — AI Product Analytics and Evaluation: Payment Attempts

## Brief

PayFlow must make a decision about payment attempts using ai product analytics and evaluation. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using event, user, session, funnel, segment.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 28 — Decision Science and Sensitivity Analysis: Ai Answer Quality

## Brief

PayFlow must make a decision about AI answer quality using decision science and sensitivity analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using revenue, cost, cash, scenario, variance.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 29 — Lifetime Value (LTV): Support Operations

## Brief

PayFlow must make a decision about support operations using lifetime value (ltv). Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using unit, margin, CAC, LTV, sensitivity.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 30 — SQL Analysis: Subscription Retention

## Brief

PayFlow must make a decision about subscription retention using sql analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using grain, population, measure, check, interpretation.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 31 — Attribution Model: Enterprise Expansion

## Brief

PayFlow must make a decision about enterprise expansion using attribution model. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using scope, lookback, identity, counterfactual, limitation.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 32 — Tracking Plan: Merchant Acquisition

## Brief

PayFlow must make a decision about merchant acquisition using tracking plan. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using event, property, identity, quality, governance.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 33 — Churn Analysis: Marketplace Matching

## Brief

PayFlow must make a decision about marketplace matching using churn analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using cohort, exposure, retention, censoring, hazard.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 34 — ROI Analysis: Pricing Economics

## Brief

PayFlow must make a decision about pricing economics using roi analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using unit, margin, CAC, LTV, sensitivity.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 35 — Marketplace Liquidity: Payment Attempts

## Brief

PayFlow must make a decision about payment attempts using marketplace liquidity. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using fill rate, time to match, density, quality, balance.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 36 — Marketing Attribution: Ai Answer Quality

## Brief

PayFlow must make a decision about AI answer quality using marketing attribution. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using scope, lookback, identity, counterfactual, limitation.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 37 — ROAS Analysis: Support Operations

## Brief

PayFlow must make a decision about support operations using roas analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using unit, margin, CAC, LTV, sensitivity.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 38 — Engagement Analysis: Subscription Retention

## Brief

PayFlow must make a decision about subscription retention using engagement analysis. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using event, user, session, funnel, segment.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 39 — Metrics Dashboard: Enterprise Expansion

## Brief

PayFlow must make a decision about enterprise expansion using metrics dashboard. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using north star, input, guardrail, owner, cadence.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# Applied Lab 40 — Financial Projections: Merchant Acquisition

## Brief

PayFlow must make a decision about merchant acquisition using financial projections. Existing evidence is incomplete and stakeholders disagree. Build the smallest rigorous analysis that can change the decision.

## Deliverables

1. Decision statement and assumption register.
2. Method or operating plan using revenue, cost, cash, scenario, variance.
3. Worked artifact with fictional, clearly labeled data.
4. Quality review covering bias, missingness, privacy, and operational feasibility.
5. Recommendation with primary measure, guardrails, rollout, and rollback.

## Model-answer standard

A strong response declares the population and timeframe, distinguishes observation from interpretation, checks an independent control, and recommends a reversible next step. It states what evidence would reverse the recommendation. A weak response selects a tool first, hides exclusions, or reports precision the evidence cannot support.


# End-to-end cases

Use these cases to integrate strategy, evidence, execution, and communication. For each case, produce an executive recommendation, a working artifact, an explicit risk review, and a measurement plan. Do not treat the provided recommendation as the only valid answer; the quality standard is traceable reasoning under stated assumptions.

# Case Study 01 — Calculate customer LTV

## Situation

The PayFlow team must calculate customer ltv in the context of marketplace matching. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Case Study 02 — Diagnose acquisition efficiency

## Situation

The PayFlow team must diagnose acquisition efficiency in the context of AI answer quality. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Case Study 03 — Design a tracking plan

## Situation

The PayFlow team must design a tracking plan in the context of enterprise expansion. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Case Study 04 — Compare attribution models

## Situation

The PayFlow team must compare attribution models in the context of pricing economics. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Case Study 05 — Analyze churn cohorts

## Situation

The PayFlow team must analyze churn cohorts in the context of support operations. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Case Study 06 — Evaluate marketplace liquidity

## Situation

The PayFlow team must evaluate marketplace liquidity in the context of merchant acquisition. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Case Study 07 — Build an executive dashboard

## Situation

The PayFlow team must build an executive dashboard in the context of payment attempts. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Case Study 08 — Forecast a new product

## Situation

The PayFlow team must forecast a new product in the context of subscription retention. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Case Study 09 — Design a governed metric layer

## Situation

The PayFlow team must design a governed metric layer in the context of marketplace matching. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Case Study 10 — Investigate misleading correlation

## Situation

The PayFlow team must investigate misleading correlation in the context of AI answer quality. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Case Study 11 — Analyze a conversion funnel

## Situation

The PayFlow team must analyze a conversion funnel in the context of enterprise expansion. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Case Study 12 — Create an analytics architecture

## Situation

The PayFlow team must create an analytics architecture in the context of pricing economics. Growth or adoption pressure is high, but instrumentation and customer evidence disagree.

## Analysis

Map actors, incentives, journey or economic flow, data lineage, and failure states. Establish the current baseline and segment the distribution. Identify the decision that can be made now versus unknowns requiring research or experimentation. For any AI-generated analysis, retain source evidence and human accountability.

## Recommendation

Choose a bounded cohort, explicit eligibility, reversible implementation, and a pre-declared review date. Pair the primary outcome with quality, customer-harm, financial, and operational guardrails. Reconcile reported results to an independent source before expansion.

## Interview debrief

Explain the trade-off, not merely the framework. Name the source of truth, causal limitation, stakeholder conflict, and evidence that would cause a stop or rollback.


# Reusable operating templates

These templates convert the curriculum into repeatable product work. Copy the structure, adapt terminology to the organization, and retain evidence links, owners, versions, and decision dates. A completed template should help a reviewer reproduce the reasoning and identify what evidence would change the decision.

# Operating Template 01 — Metric contract

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 02 — Metric tree

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 03 — Tracking plan

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 04 — Event dictionary

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 05 — Data-quality plan

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 06 — Dashboard specification

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 07 — Funnel specification

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 08 — Cohort specification

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 09 — Churn analysis

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 10 — LTV model

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 11 — CAC model

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 12 — ROI business case

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 13 — ROAS review

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 14 — Attribution comparison

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 15 — Liquidity scorecard

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 16 — Financial forecast

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 17 — Sensitivity analysis

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 18 — Data architecture decision

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 19 — Analysis readout

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Operating Template 20 — Analytics governance review

## Header

Owner; decision; audience; version; date; status; linked evidence.

## Required fields

- Purpose and decision to be made.
- Population, segment, timeframe, exclusions, and definitions.
- Evidence and provenance; assumptions and confidence.
- Method, workflow, or model; alternatives considered.
- Primary outcome, diagnostics, guardrails, and control totals.
- Risks: customer, accessibility, privacy, security, financial, and operational.
- Owners, dependencies, rollout, rollback, and review cadence.

## Completion gate

Another practitioner can reproduce the reasoning, challenge its assumptions, identify what may fail, and understand what evidence will change the decision.


# Terminology mastery checklist

**unit**, **margin**, **CAC**, **LTV**, **sensitivity**, **grain**, **population**, **measure**, **check**, **interpretation**, **scope**, **lookback**, **identity**, **counterfactual**, **limitation**, **event**, **property**, **quality**, **governance**, **cohort**, **exposure**, **retention**, **censoring**, **hazard**, **fill rate**, **time to match**, **density**, **balance**, **user**, **session**, **funnel**, **segment**, **north star**, **input**, **guardrail**, **owner**, **cadence**, **revenue**, **cost**, **cash**, **scenario**, **variance**, **source**, **contract**, **transform**, **lineage**, **access**, **variable**, **distribution**, **effect**, **confounder**, **uncertainty**

For each term, define it plainly, give an example and counterexample, connect it to a decision artifact, and name a failure caused by misunderstanding it.

# Curriculum coverage audit

This matrix checks the manuscript against major capability areas visible in the current Reforge course catalog and adjacent AI-era product practice. It is an independent curriculum, not a reproduction of proprietary course material.

| Benchmark capability | Coverage in this volume |
|---|---|
| Mastering Product Analytics | metric systems, behavioral analysis, funnels, cohorts, dashboards |
| Mastering Experimentation | power, effect estimates, guardrails, causal inference |
| Marketing Attribution | scope, lookbacks, identity, incrementality, model comparison |
| Business and Finance Foundations | LTV, CAC, ROI, projections, sensitivity, contribution margin |
| Analytics Engineering | tracking, contracts, semantic layers, lineage, quality |
| AI Product Analytics | evals, model and system metrics, human outcomes, cost and safety |
| Privacy-aware measurement | consent, minimization, retention, access and governance |

# Current primary references

- Reforge course catalog, Product Analytics, Experimentation and Marketing Attribution coverage: https://www.reforge.com/courses
- Google Analytics attribution: https://support.google.com/analytics/answer/10596866
- Google Analytics traffic-source scopes: https://support.google.com/analytics/answer/11080067
- PostgreSQL 18 documentation: https://www.postgresql.org/docs/18/
- NIST Engineering Statistics Handbook: https://www.itl.nist.gov/div898/handbook/

Verify platform behavior, law, and standards against the exact jurisdiction and product version in use.
