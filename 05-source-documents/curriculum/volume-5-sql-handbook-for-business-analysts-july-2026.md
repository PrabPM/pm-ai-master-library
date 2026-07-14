# Volume 5 — SQL for Business Analysts

## July 2026 field guide: trustworthy analytics for payments, risk, and AI products

Edition date: 14 July 2026  

This volume retains the supplied handbook's analyst mental model, payment examples, cohorts, reconciliation, hierarchy, and feature-engineering patterns. It replaces unverified company claims with the fictional **PayFlow** dataset, corrects incomplete queries, and adds current database, governance, and AI-era practice. SQL is PostgreSQL 18 style unless a dialect is named.

# 1. Translate business questions into data contracts

A strong analyst declares six things before querying: decision, population, grain, measure, time boundary, and exclusions.

“Is checkout broken?” becomes: for eligible payment attempts created in UTC yesterday, calculate terminal failure rate by method and hour; exclude tests and user-canceled attempts; classify retries separately; compare with the trailing four same weekdays.

The grain is one row per **attempt**, not order. A denominator change can reverse the conclusion. Write the metric contract beside the query and version it.

# 2. The PayFlow analytical model

Core tables:

- `customers(customer_id, signup_at, segment, country)`
- `merchants(merchant_id, parent_merchant_id, onboarded_at, category, country)`
- `payment_attempts(attempt_id, payment_id, merchant_id, customer_id, attempted_at, amount_minor, currency, method, status)`
- `payments(payment_id, merchant_id, authorized_at, captured_at, status)`
- `refunds(refund_id, payment_id, created_at, amount_minor, status, reason)`
- `ledger_entries(entry_id, account_id, payment_id, posted_at, amount_minor, currency, direction)`

Store money as integer minor units or an exact numeric type with an explicit currency. Store instants as timezone-aware timestamps and business dates separately. Event tables should be append-only. The declared grain belongs in schema documentation.

# 3. SELECT, NULL, types, and time

Logical order is `FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`. `NULL` means missing or unknown, not zero. Comparisons with `NULL` produce unknown; use `IS NULL`, `IS DISTINCT FROM`, and deliberate `COALESCE`.

```sql
SELECT attempt_id, merchant_id, amount_minor
FROM payment_attempts
WHERE attempted_at >= TIMESTAMPTZ '2026-07-13 00:00:00+00'
  AND attempted_at <  TIMESTAMPTZ '2026-07-14 00:00:00+00'
  AND status IS DISTINCT FROM 'test'
ORDER BY attempted_at, attempt_id;
```

Use half-open intervals (`>= start AND < end`) to avoid overlap. Convert to a business timezone once and document daylight-saving behavior. Never compare formatted date strings when typed dates are available.

# 4. Aggregation without lying

Always compare row counts before and after joins. Use conditional aggregation to keep one denominator visible.

```sql
SELECT method,
       COUNT(*) AS attempts,
       COUNT(*) FILTER (WHERE status = 'succeeded') AS succeeded,
       COUNT(*) FILTER (WHERE status = 'failed') AS failed,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'failed')
             / NULLIF(COUNT(*), 0), 2) AS failure_pct
FROM payment_attempts
WHERE attempted_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY method
ORDER BY failure_pct DESC NULLS LAST;
```

`COUNT(*)` counts rows; `COUNT(column)` excludes nulls; `COUNT(DISTINCT x)` counts distinct non-null values. State which one the metric uses.

# 5. Joins and cardinality

Before a join, label each side one or many. A payment with three refunds will triple payment-level columns. Aggregate the many side first or join at refund grain.

```sql
WITH refund_totals AS (
  SELECT payment_id, SUM(amount_minor) AS refunded_minor
  FROM refunds WHERE status = 'succeeded' GROUP BY payment_id
)
SELECT p.payment_id,
       COALESCE(r.refunded_minor, 0) AS refunded_minor
FROM payments p
LEFT JOIN refund_totals r USING (payment_id);
```

Use `LEFT JOIN ... WHERE right.key IS NULL` for missing matches, but distinguish late-arriving data from true absence. Keep reconciliation cutoffs explicit.

# 6. CTEs and reusable analytical steps

CTEs name transformations and make validation easier. Build a query as population → enrichment → measure → presentation. In modern PostgreSQL, CTEs may be inlined; use `MATERIALIZED` only when the execution trade-off is intentional.

```sql
WITH eligible AS (
  SELECT * FROM payment_attempts
  WHERE attempted_at >= DATE '2026-07-01'
    AND status <> 'test'
), merchant_daily AS (
  SELECT merchant_id, attempted_at::date AS day,
         COUNT(*) AS attempts,
         SUM(amount_minor) FILTER (WHERE status='succeeded') AS gmv_minor
  FROM eligible GROUP BY merchant_id, day
)
SELECT day, SUM(attempts) AS attempts, SUM(gmv_minor) AS gmv_minor
FROM merchant_daily GROUP BY day ORDER BY day;
```

# 7. Window functions

Windows preserve rows while calculating across a partition. Specify deterministic tie-breakers.

```sql
WITH monthly AS (
  SELECT date_trunc('month', attempted_at)::date AS month,
         SUM(amount_minor) FILTER (WHERE status='succeeded') AS gmv_minor
  FROM payment_attempts GROUP BY month
)
SELECT month, gmv_minor,
       LAG(gmv_minor) OVER (ORDER BY month) AS prior_month,
       ROUND(100.0 * (gmv_minor - LAG(gmv_minor) OVER (ORDER BY month))
             / NULLIF(LAG(gmv_minor) OVER (ORDER BY month), 0), 2) AS growth_pct,
       SUM(gmv_minor) OVER (ORDER BY month) AS cumulative_minor
FROM monthly ORDER BY month;
```

Learn `ROW_NUMBER`, `RANK`, `LAG/LEAD`, cumulative frames, rolling windows, and `NTILE`. Write frame clauses explicitly when duplicate sort keys could surprise you.

# 8. Funnels, cohorts, and retention

Define each stage and eligibility. For onboarding, use one row per entity per first stage time, then enforce ordering.

```sql
WITH firsts AS (
  SELECT merchant_id,
    MIN(event_at) FILTER (WHERE event_name='started') AS started_at,
    MIN(event_at) FILTER (WHERE event_name='kyb_approved') AS approved_at,
    MIN(event_at) FILTER (WHERE event_name='first_payment') AS paid_at
  FROM merchant_events GROUP BY merchant_id
)
SELECT COUNT(*) AS started,
       COUNT(*) FILTER (WHERE approved_at >= started_at) AS approved,
       COUNT(*) FILTER (WHERE paid_at >= approved_at) AS activated
FROM firsts WHERE started_at >= DATE '2026-06-01';
```

For retention, define cohort event, return event, interval, observation window, and censoring. Do not compare a young cohort's month-six retention before six months have elapsed.

# 9. Hierarchies and recursive CTEs

```sql
WITH RECURSIVE tree AS (
  SELECT merchant_id, parent_merchant_id, merchant_id AS root_id,
         ARRAY[merchant_id] AS path, 0 AS depth
  FROM merchants WHERE parent_merchant_id IS NULL
  UNION ALL
  SELECT m.merchant_id, m.parent_merchant_id, t.root_id,
         t.path || m.merchant_id, t.depth + 1
  FROM merchants m JOIN tree t ON m.parent_merchant_id=t.merchant_id
  WHERE NOT m.merchant_id = ANY(t.path) AND t.depth < 20
)
SELECT * FROM tree;
```

The path prevents cycles and the depth cap limits damage. Validate orphans, duplicate parents, and effective dates before financial rollups.

# 10. Ledgers and reconciliation

Payments are workflows; ledgers are accounting records. A balanced double-entry posting sums to zero per transaction and currency.

```sql
SELECT payment_id, currency,
       SUM(CASE direction WHEN 'debit' THEN amount_minor
                          WHEN 'credit' THEN -amount_minor END) AS imbalance_minor
FROM ledger_entries
WHERE posted_at < TIMESTAMPTZ '2026-07-14 00:00:00+00'
GROUP BY payment_id, currency
HAVING SUM(CASE direction WHEN 'debit' THEN amount_minor
                          WHEN 'credit' THEN -amount_minor END) <> 0;
```

A reconciliation query needs independent sources, cutoffs, tolerated timing differences, and categories such as missing-left, missing-right, amount mismatch, duplicate, and late. Never “fix” a mismatch by deleting evidence; create an adjustment with reason and approver.

# 11. Risk, fraud, and point-in-time features

Features must use only information available at the prediction timestamp. Otherwise leakage makes offline results fiction.

```sql
SELECT a.attempt_id,
       COUNT(*) FILTER (WHERE x.attempted_at >= a.attempted_at-INTERVAL '1 hour') AS device_attempts_1h,
       COUNT(DISTINCT x.merchant_id) AS device_merchants_24h,
       AVG(x.amount_minor) AS device_avg_minor_24h
FROM payment_attempts a
LEFT JOIN payment_attempts x
  ON x.device_id=a.device_id
 AND x.attempted_at < a.attempted_at
 AND x.attempted_at >= a.attempted_at-INTERVAL '24 hours'
GROUP BY a.attempt_id;
```

Freeze training snapshots, version feature logic, and monitor nulls and distributions. Restrict sensitive attributes by purpose and access policy. A SQL view is not automatically a safe feature store.

# 12. JSON, arrays, and vector data

Semi-structured columns are useful for evolving payloads, but promote stable, queried fields into typed columns. Validate schema version and retain raw event provenance.

```sql
SELECT event_id,
       payload->>'model' AS model,
       (payload->>'latency_ms')::integer AS latency_ms
FROM ai_events
WHERE payload ? 'model'
  AND jsonb_typeof(payload->'latency_ms') = 'number';
```

Vector similarity retrieves candidates; it does not prove truth. Keep document ID, chunk offsets, embedding model/version, tenant boundary, and access policy beside each vector. Evaluate recall and downstream answer support, not only nearest-neighbor speed.

# 13. Transactions, isolation, and concurrency

ACID does not mean every multi-step workflow is magically exactly once. Understand read committed, repeatable read, and serializable behavior in your engine. Use unique constraints as correctness mechanisms.

```sql
CREATE UNIQUE INDEX uq_idempotency
ON payment_commands(merchant_id, idempotency_key);

INSERT INTO payment_commands(merchant_id,idempotency_key,payload_hash,status)
VALUES ($1,$2,$3,'received')
ON CONFLICT (merchant_id,idempotency_key)
DO UPDATE SET last_seen_at = CURRENT_TIMESTAMP
RETURNING command_id,status,payload_hash;
```

Compare the stored payload hash on retry. An identical key with different content is a client error, not a new payment.

# 14. Performance and modern engines

PostgreSQL 18, released in September 2025, adds asynchronous I/O infrastructure and skip-scan support among other features. MySQL 8.4 remains an LTS line, with 8.4.10 released in June 2026. SQL Server 2025 is in support. Cloud warehouses and local analytical engines differ from row stores; write to the target dialect and cost model.

Performance method:

1. Bound time and partition keys.
2. Project only needed columns.
3. Reduce the large side before joining.
4. Inspect `EXPLAIN (ANALYZE, BUFFERS)` on safe representative data.
5. Check estimates versus actual rows.
6. Add an index only for a demonstrated access pattern.
7. Re-test write cost and production-like skew.

Approximate distinct counts can be useful for exploration, but label them. Materialized aggregates require freshness and backfill contracts.

# 15. Security, governance, and quality

Use least privilege, separate human and service identities, parameterized queries, row/column policies where appropriate, encryption, secret rotation, and auditable access. Masking a value in a dashboard does not remove it from query logs or exports.

Data tests should cover uniqueness, not-null, accepted values, relationships, freshness, volume anomalies, and business invariants. Reconcile dashboard totals to an independent control total. Version metric definitions and publish owners.

Never paste customer data or credentials into an AI assistant. A text-to-SQL system needs schema-scoped retrieval, read-only credentials, query parsing, cost/time limits, row limits, PII controls, audit logs, and user confirmation for exports.

# 16. Dialect notes and current SQL

ISO/IEC 9075:2023 is the current published SQL standard family, but vendors implement different subsets and extensions. Examples to watch:

- `FILTER` is PostgreSQL-style; use conditional `SUM(CASE...)` where absent.
- Date arithmetic and truncation vary widely.
- `QUALIFY` is available in several analytical engines but not PostgreSQL.
- `MERGE` semantics and concurrency behavior differ by product.
- Identifier case, `NULL` sorting, JSON, arrays, and approximate functions vary.

Keep a tested dialect layer rather than assuming syntax portability.

# 17. Interview and on-the-job framework

Use **G-R-A-I-N**:

1. **Goal:** decision and metric.
2. **Rows:** target grain and population.
3. **Associations:** tables, cardinality, keys.
4. **Intervals:** time, timezone, cutoff, censoring.
5. **Numbers:** query, checks, interpretation, action.

Practice: terminal failure rate with retries; top merchant per category; retention cohort; hierarchy rollup; balanced ledger; refund liability; point-in-time fraud features; duplicate webhook detection; slow-query rewrite; safe natural-language analytics.

For every answer, give a sanity check: row counts, null rate, duplicate keys, control total, known example, and expected range.

# 18. Compact practice lab

```sql
CREATE TABLE payment_attempts(
  attempt_id text PRIMARY KEY, payment_id text NOT NULL,
  merchant_id text NOT NULL, customer_id text NOT NULL,
  attempted_at timestamptz NOT NULL, amount_minor bigint NOT NULL CHECK(amount_minor>=0),
  currency char(3) NOT NULL, method text NOT NULL,
  status text NOT NULL CHECK(status IN ('succeeded','failed','pending','canceled'))
);
```

Exercises:

1. Compute daily success and terminal-failure rates.
2. Find payments with multiple successful attempts.
3. Build merchant activation by signup cohort.
4. Reconcile payment captures to ledger credits at a cutoff.
5. Create a point-in-time 24-hour velocity feature.
6. Explain and optimize a one-month merchant aggregate.

Definition of done: query runs in the named dialect; grain is stated; edge cases are covered; totals reconcile; performance is bounded; sensitive data is protected; result is translated into a decision.

# Current primary references

- PostgreSQL 18 documentation and release notes: https://www.postgresql.org/docs/18/release.html
- MySQL 8.4 Reference Manual and release notes: https://dev.mysql.com/doc/refman/8.4/en/ and https://dev.mysql.com/doc/relnotes/mysql/8.4/en/
- Microsoft SQL Server 2025 lifecycle: https://learn.microsoft.com/en-us/lifecycle/products/sql-server-2025
- ISO/IEC 9075-1:2023 SQL framework: https://www.iso.org/standard/76583.html

Always verify behavior against the exact engine version and execution plan used by your organization.


<!-- COMPREHENSIVE-EDITION -->


# Applied curriculum and mastery labs

These labs turn the core chapters into portfolio-ready practice. Complete them with explicit assumptions and retain both the artifact and its review notes.

# Lab 01 — Metric Contract: Checkout Attempts

## Objective

Produce a reviewable metric contract for checkout attempts. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its checkout attempts experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the metric contract; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: half-open time boundaries; null behavior documented; and bounded scans and timeouts.
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


# Lab 02 — Grain Declaration: Interchange Cost

## Objective

Produce a reviewable grain declaration for interchange cost. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its interchange cost experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the grain declaration; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: join-cardinality validation; point-in-time correctness; and least-privilege access and masked output.
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


# Lab 03 — Profiling Query: Ai Assistant Telemetry

## Objective

Produce a reviewable profiling query for AI assistant telemetry. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its AI assistant telemetry experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the profiling query; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: null behavior documented; independent control totals; and explicit grain and denominator.
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


# Lab 04 — Join Audit: Payout Settlement

## Objective

Produce a reviewable join audit for payout settlement. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payout settlement experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the join audit; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: point-in-time correctness; bounded scans and timeouts; and half-open time boundaries.
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


# Lab 05 — Conditional Aggregate: Fraud Velocity

## Objective

Produce a reviewable conditional aggregate for fraud velocity. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its fraud velocity experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the conditional aggregate; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: independent control totals; least-privilege access and masked output; and join-cardinality validation.
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


# Lab 06 — Window Analysis: Merchant Activation

## Objective

Produce a reviewable window analysis for merchant activation. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its merchant activation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the window analysis; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: bounded scans and timeouts; explicit grain and denominator; and null behavior documented.
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


# Lab 07 — Cohort Table: Subscription Billing

## Objective

Produce a reviewable cohort table for subscription billing. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its subscription billing experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the cohort table; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege access and masked output; half-open time boundaries; and point-in-time correctness.
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


# Lab 08 — Funnel Query: Support Operations

## Objective

Produce a reviewable funnel query for support operations. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its support operations experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the funnel query; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit grain and denominator; join-cardinality validation; and independent control totals.
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


# Lab 09 — Hierarchy Rollup: Card Disputes

## Objective

Produce a reviewable hierarchy rollup for card disputes. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its card disputes experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the hierarchy rollup; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: half-open time boundaries; null behavior documented; and bounded scans and timeouts.
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


# Lab 10 — Ledger Control: Enterprise Hierarchy

## Objective

Produce a reviewable ledger control for enterprise hierarchy. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its enterprise hierarchy experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the ledger control; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: join-cardinality validation; point-in-time correctness; and least-privilege access and masked output.
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


# Lab 11 — Reconciliation Report: Refund Liability

## Objective

Produce a reviewable reconciliation report for refund liability. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its refund liability experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the reconciliation report; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: null behavior documented; independent control totals; and explicit grain and denominator.
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


# Lab 12 — Point-In-Time Feature: Kyb Applications

## Objective

Produce a reviewable point-in-time feature for KYB applications. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its KYB applications experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the point-in-time feature; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: point-in-time correctness; bounded scans and timeouts; and half-open time boundaries.
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


# Lab 13 — Json Extraction: Checkout Attempts

## Objective

Produce a reviewable JSON extraction for checkout attempts. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its checkout attempts experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the JSON extraction; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: independent control totals; least-privilege access and masked output; and join-cardinality validation.
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


# Lab 14 — Vector Retrieval Audit: Interchange Cost

## Objective

Produce a reviewable vector retrieval audit for interchange cost. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its interchange cost experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the vector retrieval audit; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: bounded scans and timeouts; explicit grain and denominator; and null behavior documented.
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


# Lab 15 — Transaction Test: Ai Assistant Telemetry

## Objective

Produce a reviewable transaction test for AI assistant telemetry. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its AI assistant telemetry experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the transaction test; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege access and masked output; half-open time boundaries; and point-in-time correctness.
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


# Lab 16 — Execution-Plan Review: Payout Settlement

## Objective

Produce a reviewable execution-plan review for payout settlement. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payout settlement experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the execution-plan review; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit grain and denominator; join-cardinality validation; and independent control totals.
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


# Lab 17 — Index Proposal: Fraud Velocity

## Objective

Produce a reviewable index proposal for fraud velocity. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its fraud velocity experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the index proposal; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: half-open time boundaries; null behavior documented; and bounded scans and timeouts.
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


# Lab 18 — Partition Strategy: Merchant Activation

## Objective

Produce a reviewable partition strategy for merchant activation. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its merchant activation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the partition strategy; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: join-cardinality validation; point-in-time correctness; and least-privilege access and masked output.
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


# Lab 19 — Data-Quality Test: Subscription Billing

## Objective

Produce a reviewable data-quality test for subscription billing. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its subscription billing experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the data-quality test; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: null behavior documented; independent control totals; and explicit grain and denominator.
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


# Lab 20 — Text-To-Sql Safety Review: Support Operations

## Objective

Produce a reviewable text-to-SQL safety review for support operations. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its support operations experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the text-to-SQL safety review; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: point-in-time correctness; bounded scans and timeouts; and half-open time boundaries.
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


# Lab 21 — Metric Contract: Interchange Cost

## Objective

Produce a reviewable metric contract for interchange cost. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its interchange cost experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the metric contract; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: independent control totals; least-privilege access and masked output; and join-cardinality validation.
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


# Lab 22 — Grain Declaration: Ai Assistant Telemetry

## Objective

Produce a reviewable grain declaration for AI assistant telemetry. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its AI assistant telemetry experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the grain declaration; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: bounded scans and timeouts; explicit grain and denominator; and null behavior documented.
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


# Lab 23 — Profiling Query: Payout Settlement

## Objective

Produce a reviewable profiling query for payout settlement. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payout settlement experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the profiling query; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege access and masked output; half-open time boundaries; and point-in-time correctness.
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


# Lab 24 — Join Audit: Fraud Velocity

## Objective

Produce a reviewable join audit for fraud velocity. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its fraud velocity experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the join audit; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit grain and denominator; join-cardinality validation; and independent control totals.
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


# Lab 25 — Conditional Aggregate: Merchant Activation

## Objective

Produce a reviewable conditional aggregate for merchant activation. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its merchant activation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the conditional aggregate; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: half-open time boundaries; null behavior documented; and bounded scans and timeouts.
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


# Lab 26 — Window Analysis: Subscription Billing

## Objective

Produce a reviewable window analysis for subscription billing. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its subscription billing experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the window analysis; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: join-cardinality validation; point-in-time correctness; and least-privilege access and masked output.
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


# Lab 27 — Cohort Table: Support Operations

## Objective

Produce a reviewable cohort table for support operations. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its support operations experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the cohort table; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: null behavior documented; independent control totals; and explicit grain and denominator.
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


# Lab 28 — Funnel Query: Card Disputes

## Objective

Produce a reviewable funnel query for card disputes. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its card disputes experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the funnel query; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: point-in-time correctness; bounded scans and timeouts; and half-open time boundaries.
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


# Lab 29 — Hierarchy Rollup: Enterprise Hierarchy

## Objective

Produce a reviewable hierarchy rollup for enterprise hierarchy. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its enterprise hierarchy experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the hierarchy rollup; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: independent control totals; least-privilege access and masked output; and join-cardinality validation.
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


# Lab 30 — Ledger Control: Refund Liability

## Objective

Produce a reviewable ledger control for refund liability. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its refund liability experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the ledger control; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: bounded scans and timeouts; explicit grain and denominator; and null behavior documented.
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


# Lab 31 — Reconciliation Report: Kyb Applications

## Objective

Produce a reviewable reconciliation report for KYB applications. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its KYB applications experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the reconciliation report; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege access and masked output; half-open time boundaries; and point-in-time correctness.
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


# Lab 32 — Point-In-Time Feature: Checkout Attempts

## Objective

Produce a reviewable point-in-time feature for checkout attempts. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its checkout attempts experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the point-in-time feature; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit grain and denominator; join-cardinality validation; and independent control totals.
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


# Lab 33 — Json Extraction: Interchange Cost

## Objective

Produce a reviewable JSON extraction for interchange cost. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its interchange cost experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the JSON extraction; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: half-open time boundaries; null behavior documented; and bounded scans and timeouts.
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


# Lab 34 — Vector Retrieval Audit: Ai Assistant Telemetry

## Objective

Produce a reviewable vector retrieval audit for AI assistant telemetry. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its AI assistant telemetry experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the vector retrieval audit; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: join-cardinality validation; point-in-time correctness; and least-privilege access and masked output.
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


# Lab 35 — Transaction Test: Payout Settlement

## Objective

Produce a reviewable transaction test for payout settlement. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payout settlement experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the transaction test; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: null behavior documented; independent control totals; and explicit grain and denominator.
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


# Lab 36 — Execution-Plan Review: Fraud Velocity

## Objective

Produce a reviewable execution-plan review for fraud velocity. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its fraud velocity experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the execution-plan review; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: point-in-time correctness; bounded scans and timeouts; and half-open time boundaries.
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


# Lab 37 — Index Proposal: Merchant Activation

## Objective

Produce a reviewable index proposal for merchant activation. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its merchant activation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the index proposal; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: independent control totals; least-privilege access and masked output; and join-cardinality validation.
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


# Lab 38 — Partition Strategy: Subscription Billing

## Objective

Produce a reviewable partition strategy for subscription billing. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its subscription billing experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the partition strategy; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: bounded scans and timeouts; explicit grain and denominator; and null behavior documented.
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


# Lab 39 — Data-Quality Test: Support Operations

## Objective

Produce a reviewable data-quality test for support operations. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its support operations experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the data-quality test; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege access and masked output; half-open time boundaries; and point-in-time correctness.
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


# Lab 40 — Text-To-Sql Safety Review: Card Disputes

## Objective

Produce a reviewable text-to-SQL safety review for card disputes. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its card disputes experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the text-to-SQL safety review; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit grain and denominator; join-cardinality validation; and independent control totals.
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


# Lab 41 — Metric Contract: Ai Assistant Telemetry

## Objective

Produce a reviewable metric contract for AI assistant telemetry. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its AI assistant telemetry experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the metric contract; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: half-open time boundaries; null behavior documented; and bounded scans and timeouts.
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


# Lab 42 — Grain Declaration: Payout Settlement

## Objective

Produce a reviewable grain declaration for payout settlement. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its payout settlement experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the grain declaration; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: join-cardinality validation; point-in-time correctness; and least-privilege access and masked output.
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


# Lab 43 — Profiling Query: Fraud Velocity

## Objective

Produce a reviewable profiling query for fraud velocity. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its fraud velocity experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the profiling query; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: null behavior documented; independent control totals; and explicit grain and denominator.
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


# Lab 44 — Join Audit: Merchant Activation

## Objective

Produce a reviewable join audit for merchant activation. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its merchant activation experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the join audit; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: point-in-time correctness; bounded scans and timeouts; and half-open time boundaries.
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


# Lab 45 — Conditional Aggregate: Subscription Billing

## Objective

Produce a reviewable conditional aggregate for subscription billing. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its subscription billing experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the conditional aggregate; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: independent control totals; least-privilege access and masked output; and join-cardinality validation.
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


# Lab 46 — Window Analysis: Support Operations

## Objective

Produce a reviewable window analysis for support operations. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its support operations experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the window analysis; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: bounded scans and timeouts; explicit grain and denominator; and null behavior documented.
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


# Lab 47 — Cohort Table: Card Disputes

## Objective

Produce a reviewable cohort table for card disputes. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its card disputes experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the cohort table; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: least-privilege access and masked output; half-open time boundaries; and point-in-time correctness.
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


# Lab 48 — Funnel Query: Enterprise Hierarchy

## Objective

Produce a reviewable funnel query for enterprise hierarchy. The exercise tests whether a business analyst can connect a user or business decision to evidence, system behavior, correctness controls, and a measurable outcome.

## Scenario

PayFlow is changing its enterprise hierarchy experience. Volume has grown, teams use inconsistent definitions, and a recent incident exposed an unhandled edge case. You have one week to propose the smallest safe improvement and an evidence plan. State assumptions instead of inventing facts.

## Assignment

1. Declare the actor, goal, trigger, scope, and unit of analysis.
2. Draw or describe the happy path plus at least four failure or boundary states.
3. Produce the funnel query; include owner, inputs, outputs, decision rule, and version date.
4. Apply these controls: explicit grain and denominator; join-cardinality validation; and independent control totals.
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

# Case Study 01 — Diagnose checkout failure

## Executive brief

PayFlow must diagnose checkout failure while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce half-open time boundaries, point-in-time correctness, and least-privilege access and masked output. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 02 — Measure merchant activation

## Executive brief

PayFlow must measure merchant activation while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce join-cardinality validation, independent control totals, and explicit grain and denominator. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 03 — Calculate refund exposure

## Executive brief

PayFlow must calculate refund exposure while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce null behavior documented, bounded scans and timeouts, and half-open time boundaries. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 04 — Reconcile payouts to ledger

## Executive brief

PayFlow must reconcile payouts to ledger while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce point-in-time correctness, least-privilege access and masked output, and join-cardinality validation. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 05 — Find systemic interchange leakage

## Executive brief

PayFlow must find systemic interchange leakage while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce independent control totals, explicit grain and denominator, and null behavior documented. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 06 — Analyze subscription retention

## Executive brief

PayFlow must analyze subscription retention while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce bounded scans and timeouts, half-open time boundaries, and point-in-time correctness. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 07 — Roll up enterprise merchants

## Executive brief

PayFlow must roll up enterprise merchants while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce least-privilege access and masked output, join-cardinality validation, and independent control totals. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 08 — Build fraud velocity features

## Executive brief

PayFlow must build fraud velocity features while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce explicit grain and denominator, null behavior documented, and bounded scans and timeouts. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 09 — Detect late-arriving data

## Executive brief

PayFlow must detect late-arriving data while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce half-open time boundaries, point-in-time correctness, and least-privilege access and masked output. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 10 — Optimize a monthly aggregate

## Executive brief

PayFlow must optimize a monthly aggregate while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce join-cardinality validation, independent control totals, and explicit grain and denominator. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 11 — Audit an AI analytics assistant

## Executive brief

PayFlow must audit an ai analytics assistant while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce null behavior documented, bounded scans and timeouts, and half-open time boundaries. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Case Study 12 — Define a governed executive metric

## Executive brief

PayFlow must define a governed executive metric while protecting financial correctness, customer trust, and operational recoverability. The team has incomplete evidence and cannot redesign every dependency at once. The PM must choose a bounded intervention, make its assumptions inspectable, and define how the organization will know whether it worked.

## Analysis

Map the current system before proposing the future one: actors, state transitions, data sources, permissions, asynchronous dependencies, and manual workarounds. Establish a baseline by outcome and segment. Inspect the tail, not only the average. Reconcile product telemetry to an independent operational or financial control so that a tracking defect cannot masquerade as improvement.

The design must enforce point-in-time correctness, least-privilege access and masked output, and join-cardinality validation. Treat missing, delayed, duplicated, unauthorized, and contradictory inputs as first-class cases. Where a model or heuristic is involved, record the version, evidence available at decision time, confidence behavior, and escalation path.

## Recommended release

Ship to one observable cohort with a written eligibility rule. Keep the prior path available, document migration and rollback, and assign incident ownership. Review the primary outcome, correctness, latency, support demand, and disparate failure rates. Expand only after the result is stable across at least one complete business cycle and the control totals reconcile.

## Interview debrief

A strong answer declares the invariant before the interface or query, distinguishes correlation from causation, names the source of truth, and discusses failure recovery. A weak answer jumps to technology, quotes an average without a distribution, or invokes “human review” without specifying authority, context, workload, and auditability.


# Reusable operating templates

Copy these structures into briefs, reviews, and launch packets. Remove fields only when they are demonstrably irrelevant.

# Operating Template 01 — Business-question translation

Use this template when preparing a business-question translation for analytical SQL work.

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


# Operating Template 02 — Metric contract

Use this template when preparing a metric contract for analytical SQL work.

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


# Operating Template 03 — Dataset profile

Use this template when preparing a dataset profile for analytical SQL work.

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


# Operating Template 04 — Join cardinality worksheet

Use this template when preparing a join cardinality worksheet for analytical SQL work.

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


# Operating Template 05 — Query review

Use this template when preparing a query review for analytical SQL work.

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


# Operating Template 06 — Cohort specification

Use this template when preparing a cohort specification for analytical SQL work.

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


# Operating Template 07 — Funnel specification

Use this template when preparing a funnel specification for analytical SQL work.

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


# Operating Template 08 — Reconciliation control

Use this template when preparing a reconciliation control for analytical SQL work.

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


# Operating Template 09 — Feature definition

Use this template when preparing a feature definition for analytical SQL work.

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


# Operating Template 10 — Point-in-time review

Use this template when preparing a point-in-time review for analytical SQL work.

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


# Operating Template 11 — Data-quality test plan

Use this template when preparing a data-quality test plan for analytical SQL work.

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


# Operating Template 12 — Dashboard contract

Use this template when preparing a dashboard contract for analytical SQL work.

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


# Operating Template 13 — Performance investigation

Use this template when preparing a performance investigation for analytical SQL work.

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


# Operating Template 14 — Index decision record

Use this template when preparing a index decision record for analytical SQL work.

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


# Operating Template 15 — Backfill plan

Use this template when preparing a backfill plan for analytical SQL work.

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


# Operating Template 16 — Data incident brief

Use this template when preparing a data incident brief for analytical SQL work.

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


# Operating Template 17 — Access review

Use this template when preparing a access review for analytical SQL work.

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


# Operating Template 18 — Text-to-SQL threat model

Use this template when preparing a text-to-sql threat model for analytical SQL work.

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


# Operating Template 19 — SQL interview worksheet

Use this template when preparing a sql interview worksheet for analytical SQL work.

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


# Operating Template 20 — Analysis readout

Use this template when preparing a analysis readout for analytical SQL work.

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

**grain**, **population**, **denominator**, **fact table**, **dimension**, **surrogate key**, **natural key**, **primary key**, **foreign key**, **cardinality**, **selectivity**, **null**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.

## Mastery set 2

**three-valued logic**, **coalesce**, **half-open interval**, **timezone**, **aggregation**, **conditional aggregation**, **distinct count**, **inner join**, **left join**, **anti-join**, **semi-join**, **CTE**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.

## Mastery set 3

**recursive CTE**, **window function**, **partition by**, **window frame**, **row number**, **rank**, **lag**, **lead**, **cohort**, **retention**, **censoring**, **funnel**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.

## Mastery set 4

**ledger**, **journal entry**, **reconciliation**, **control total**, **cutoff**, **late-arriving data**, **idempotency key**, **transaction**, **isolation**, **serializable**, **deadlock**, **JSON**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.

## Mastery set 5

**array**, **vector embedding**, **cosine similarity**, **point-in-time join**, **feature leakage**, **query plan**, **sequential scan**, **index scan**, **skip scan**, **partition pruning**, **materialized view**, **approximate count**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.

## Mastery set 6

**row-level security**, **masking**, **lineage**, **freshness**, **data contract**, **schema drift**, **backfill**, **text to SQL**, **parameterized query**

Mastery check: define each term plainly, give an example and counterexample, connect it to an artifact or failure, and identify its governing contract.
