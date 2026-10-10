-- ============================================================================
-- PayFlow practice database
-- Companion to "SQL Handbook for Business Analysts", Version 2 (October 2026)
--
-- PayFlow is a fictional payments company. Every row here is invented.
-- The data covers 1 June - 13 July 2026 (onboarding events go back to April).
-- All timestamps are fixed, so every query in the book returns the same result
-- for you as it does on the printed page.
--
-- Load it (PostgreSQL 16, 17 or 18):
--     createdb payflow_book
--     psql -d payflow_book -v ON_ERROR_STOP=1 -f payflow_practice.sql
-- Then, at the start of each session:
--     SET search_path = payflow;
--
-- The script is safe to re-run: it drops and rebuilds the payflow schema.
-- It also makes UTC and the payflow schema the defaults for THIS database
-- (ALTER DATABASE), so new sessions print the same output as the book. Use a
-- scratch database, not one that holds anything you care about.
-- ============================================================================

DROP SCHEMA IF EXISTS payflow CASCADE;
CREATE SCHEMA payflow;
SET search_path = payflow;

SET timezone = 'UTC';
DO $$
BEGIN
  EXECUTE format('ALTER DATABASE %I SET timezone = %L', current_database(), 'UTC');
  EXECUTE format('ALTER DATABASE %I SET search_path = payflow, public',
                 current_database());
EXCEPTION WHEN insufficient_privilege THEN
  RAISE NOTICE 'Could not change database defaults; run SET timezone = ''UTC'' and SET search_path = payflow in each session.';
END
$$;

-- ----------------------------------------------------------------------------
-- Tables
-- ----------------------------------------------------------------------------

CREATE TABLE merchants (
  merchant_id        text PRIMARY KEY,
  merchant_name      text NOT NULL,
  parent_merchant_id text REFERENCES merchants (merchant_id),
  category           text NOT NULL,
  country            char(2) NOT NULL,
  onboarded_at       timestamptz
);
COMMENT ON TABLE merchants IS
  'One row per merchant account.';
COMMENT ON COLUMN merchants.parent_merchant_id IS
  'The merchant this account rolls up to. NULL for a top-level merchant.';
COMMENT ON COLUMN merchants.onboarded_at IS
  'When identity checks (KYB) were approved. NULL while onboarding is unfinished.';

CREATE TABLE customers (
  customer_id   text PRIMARY KEY,
  customer_name text NOT NULL,
  signup_at     timestamptz NOT NULL,
  segment       text NOT NULL CHECK (segment IN ('consumer', 'business')),
  country       char(2) NOT NULL
);
COMMENT ON TABLE customers IS
  'One row per registered payer (guests have no row).';

CREATE TABLE payments (
  payment_id    text PRIMARY KEY,
  merchant_id   text NOT NULL REFERENCES merchants (merchant_id),
  customer_id   text REFERENCES customers (customer_id),
  created_at    timestamptz NOT NULL,
  amount_minor  bigint NOT NULL CHECK (amount_minor > 0),
  currency      char(3) NOT NULL,
  status        text NOT NULL
                CHECK (status IN ('captured', 'authorized', 'failed', 'canceled', 'pending')),
  authorized_at timestamptz,
  captured_at   timestamptz,
  is_test       boolean NOT NULL DEFAULT false
);
COMMENT ON TABLE payments IS
  'One row per payment: one intent to pay for one order.';
COMMENT ON COLUMN payments.amount_minor IS
  'Amount in minor units of the currency: cents for USD, pence for GBP.';
COMMENT ON COLUMN payments.customer_id IS
  'NULL for guest checkouts and for internal test traffic.';
COMMENT ON COLUMN payments.status IS
  'Final state: captured (money taken), authorized (held, not yet taken), failed, canceled, pending.';
COMMENT ON COLUMN payments.is_test IS
  'True for PayFlow''s own monitoring probes. Exclude from business metrics.';

CREATE TABLE payment_attempts (
  attempt_id   text PRIMARY KEY,
  payment_id   text NOT NULL REFERENCES payments (payment_id),
  merchant_id  text NOT NULL REFERENCES merchants (merchant_id),
  customer_id  text REFERENCES customers (customer_id),
  attempted_at timestamptz NOT NULL,
  amount_minor bigint NOT NULL CHECK (amount_minor > 0),
  currency     char(3) NOT NULL,
  method       text NOT NULL CHECK (method IN ('card', 'wallet', 'bank_transfer')),
  status       text NOT NULL
               CHECK (status IN ('succeeded', 'failed', 'pending', 'canceled')),
  failure_code text,
  device_id    text,
  is_test      boolean NOT NULL DEFAULT false,
  CHECK ((status = 'failed') = (failure_code IS NOT NULL))
);
COMMENT ON TABLE payment_attempts IS
  'One row per attempt: one try at charging a payment.';
COMMENT ON COLUMN payment_attempts.failure_code IS
  'Why a failed attempt failed. NULL unless status = failed.';
COMMENT ON COLUMN payment_attempts.device_id IS
  'Fingerprint of the browser or phone. NULL for bank transfers.';
COMMENT ON COLUMN payment_attempts.is_test IS
  'True for PayFlow''s own monitoring probes. Exclude from business metrics.';

CREATE TABLE refunds (
  refund_id    text PRIMARY KEY,
  payment_id   text NOT NULL REFERENCES payments (payment_id),
  created_at   timestamptz NOT NULL,
  amount_minor bigint NOT NULL CHECK (amount_minor > 0),
  status       text NOT NULL CHECK (status IN ('succeeded', 'failed', 'pending')),
  reason       text NOT NULL
);
COMMENT ON TABLE refunds IS
  'One row per refund request (a payment can have several).';

CREATE TABLE disputes (
  dispute_id   text PRIMARY KEY,
  payment_id   text NOT NULL REFERENCES payments (payment_id),
  opened_at    timestamptz NOT NULL,
  amount_minor bigint NOT NULL CHECK (amount_minor > 0),
  reason       text NOT NULL,
  status       text NOT NULL CHECK (status IN ('open', 'won', 'lost'))
);
COMMENT ON TABLE disputes IS
  'One row per chargeback raised by a cardholder.';

CREATE TABLE ledger_entries (
  entry_id     integer PRIMARY KEY,
  journal_id   text NOT NULL,
  payment_id   text NOT NULL REFERENCES payments (payment_id),
  account      text NOT NULL
               CHECK (account IN ('processor_receivable', 'merchant_payable', 'fee_revenue')),
  direction    text NOT NULL CHECK (direction IN ('debit', 'credit')),
  amount_minor bigint NOT NULL CHECK (amount_minor > 0),
  currency     char(3) NOT NULL,
  posted_at    timestamptz NOT NULL
);
COMMENT ON TABLE ledger_entries IS
  'One row per ledger line; a journal_id groups one posting.';
COMMENT ON COLUMN ledger_entries.journal_id IS
  'Groups the debit and credit lines of one accounting event (a capture or a refund).';

CREATE TABLE settlement_lines (
  line_id      text PRIMARY KEY,
  file_date    date NOT NULL,
  payment_id   text NOT NULL,
  gross_minor  bigint NOT NULL,
  currency     char(3) NOT NULL
);
COMMENT ON TABLE settlement_lines IS
  'One row per line of the provider''s daily settlement file.';
COMMENT ON COLUMN settlement_lines.file_date IS
  'Date of the file the line arrived in. A capture is expected in the next day''s file.';
COMMENT ON COLUMN settlement_lines.payment_id IS
  'PayFlow''s payment reference as the provider reports it. External data, so no foreign key.';

CREATE TABLE merchant_events (
  event_id    text PRIMARY KEY,
  merchant_id text NOT NULL REFERENCES merchants (merchant_id),
  event_name  text NOT NULL
              CHECK (event_name IN ('started', 'kyb_submitted', 'kyb_approved', 'first_payment')),
  event_at    timestamptz NOT NULL
);
COMMENT ON TABLE merchant_events IS
  'One row per onboarding event delivered (can repeat).';

CREATE TABLE experiment_assignments (
  experiment_key text NOT NULL,
  payment_id     text NOT NULL REFERENCES payments (payment_id),
  variant        text NOT NULL CHECK (variant IN ('control', 'treatment')),
  assigned_at    timestamptz NOT NULL
);
COMMENT ON TABLE experiment_assignments IS
  'One row per payment-to-arm assignment.';

CREATE TABLE ai_events (
  event_id    text PRIMARY KEY,
  occurred_at timestamptz NOT NULL,
  payload     jsonb NOT NULL
);
COMMENT ON TABLE ai_events IS
  'One row per question asked of the Ask PayFlow assistant.';

CREATE TABLE payment_commands (
  command_id      text PRIMARY KEY,
  merchant_id     text NOT NULL REFERENCES merchants (merchant_id),
  idempotency_key text NOT NULL,
  payload_hash    text NOT NULL,
  status          text NOT NULL,
  created_at      timestamptz NOT NULL,
  last_seen_at    timestamptz NOT NULL,
  CONSTRAINT uq_idempotency UNIQUE (merchant_id, idempotency_key)
);
COMMENT ON TABLE payment_commands IS
  'One row per charge request (merchant + idempotency key).';

CREATE TABLE attempts_big (
  attempt_id   integer PRIMARY KEY,
  merchant_id  text NOT NULL,
  attempted_at timestamptz NOT NULL,
  amount_minor integer NOT NULL,
  method       text NOT NULL,
  status       text NOT NULL
);
COMMENT ON TABLE attempts_big IS
  'Synthetic: 20,000 attempts for the performance chapter.';

-- ----------------------------------------------------------------------------
-- Data
-- ----------------------------------------------------------------------------

INSERT INTO merchants
  (merchant_id, merchant_name, parent_merchant_id, category, country, onboarded_at)
VALUES
  ('M01', 'Northwind Group', NULL, 'wholesale', 'US', '2026-04-08 15:00:00+00'),
  ('M02', 'Northwind Retail', 'M01', 'retail', 'US', '2026-04-10 14:00:00+00'),
  ('M03', 'Northwind Outlet', 'M02', 'retail', 'US', '2026-05-06 16:30:00+00'),
  ('M04', 'Northwind Travel', 'M01', 'travel', 'US', '2026-05-15 13:00:00+00'),
  ('M05', 'Bluebird Coffee', NULL, 'food_beverage', 'US', '2026-04-14 17:00:00+00'),
  ('M06', 'Cedar Books', NULL, 'retail', 'US', '2026-05-20 15:00:00+00'),
  ('M07', 'Lumen Fitness', NULL, 'fitness', 'US', '2026-04-27 18:00:00+00'),
  ('M08', 'Thames Tea', NULL, 'food_beverage', 'GB', '2026-06-03 10:00:00+00'),
  ('M09', 'Harbor Games', NULL, 'gaming', 'US', '2026-05-27 19:00:00+00'),
  ('M10', 'Quill Stationery', NULL, 'retail', 'US', '2026-06-18 14:00:00+00'),
  ('M11', 'Pioneer Pets', NULL, 'retail', 'US', '2026-07-08 16:00:00+00'),
  ('M12', 'Juniper Bikes', NULL, 'retail', 'CA', NULL);

INSERT INTO customers
  (customer_id, customer_name, signup_at, segment, country)
VALUES
  ('C01', 'Ava Chen', '2026-04-12 14:20:00+00', 'consumer', 'US'),
  ('C02', 'Ben Okafor', '2026-04-28 22:10:00+00', 'consumer', 'US'),
  ('C03', 'Carla Delgado', '2026-05-05 15:00:00+00', 'business', 'US'),
  ('C04', 'Dev Patel', '2026-05-19 19:45:00+00', 'consumer', 'US'),
  ('C05', 'Emma Novak', '2026-06-01 13:02:00+00', 'consumer', 'US'),
  ('C06', 'Farid Haddad', '2026-06-02 18:30:00+00', 'consumer', 'US'),
  ('C07', 'Grace Kim', '2026-06-04 19:10:00+00', 'consumer', 'US'),
  ('C08', 'Isla Brown', '2026-06-08 09:10:00+00', 'consumer', 'GB'),
  ('C09', 'Hugo Martin', '2026-06-09 17:05:00+00', 'consumer', 'CA'),
  ('C10', 'Jonas Weber', '2026-06-12 15:55:00+00', 'business', 'US'),
  ('C11', 'Kira Sato', '2026-06-15 14:00:00+00', 'consumer', 'US'),
  ('C12', 'Liam Murphy', '2026-06-18 13:15:00+00', 'consumer', 'US'),
  ('C13', 'Maya Singh', '2026-06-22 13:00:00+00', 'consumer', 'US'),
  ('C14', 'Noah Rossi', '2026-06-25 14:25:00+00', 'consumer', 'US'),
  ('C15', 'Olivia Park', '2026-07-01 02:05:00+00', 'consumer', 'US'),
  ('C16', 'Priya Nair', '2026-07-07 15:05:00+00', 'consumer', 'US');

INSERT INTO payments
  (payment_id, merchant_id, customer_id, created_at, amount_minor, currency, status, authorized_at, captured_at, is_test)
VALUES
  ('P0001', 'M05', 'C01', '2026-06-01 12:05:10+00', 600, 'USD', 'captured', '2026-06-01 12:05:10+00', '2026-06-01 12:05:13+00', false),
  ('P0002', 'M09', 'C05', '2026-06-01 13:20:05+00', 2000, 'USD', 'captured', '2026-06-01 13:20:05+00', '2026-06-01 13:20:08+00', false),
  ('P0003', 'M01', 'C03', '2026-06-01 15:40:00+00', 240000, 'USD', 'captured', '2026-06-01 15:40:00+00', '2026-06-01 15:40:03+00', false),
  ('P0004', 'M07', 'C02', '2026-06-01 23:10:12+00', 2500, 'USD', 'captured', '2026-06-01 23:12:40+00', '2026-06-01 23:12:43+00', false),
  ('P0005', 'M05', 'C01', '2026-06-02 12:10:33+00', 600, 'USD', 'captured', '2026-06-02 12:10:33+00', '2026-06-02 12:10:36+00', false),
  ('P0006', 'M06', 'C04', '2026-06-02 16:30:00+00', 3200, 'USD', 'captured', '2026-06-02 16:30:00+00', '2026-06-02 16:30:03+00', false),
  ('P0007', 'M02', 'C06', '2026-06-02 18:45:21+00', 9000, 'USD', 'captured', '2026-06-02 18:45:21+00', '2026-06-02 18:45:24+00', false),
  ('P0008', 'M05', NULL, '2026-06-02 20:00:00+00', 500, 'USD', 'failed', NULL, NULL, true),
  ('P0009', 'M05', 'C01', '2026-06-03 12:02:47+00', 800, 'USD', 'captured', '2026-06-03 12:02:47+00', '2026-06-03 12:02:50+00', false),
  ('P0010', 'M03', NULL, '2026-06-03 22:40:15+00', 4000, 'USD', 'captured', '2026-06-03 22:40:15+00', '2026-06-03 22:40:18+00', false),
  ('P0011', 'M05', 'C01', '2026-06-04 12:15:02+00', 600, 'USD', 'captured', '2026-06-04 12:15:02+00', '2026-06-04 12:15:05+00', false),
  ('P0012', 'M06', 'C07', '2026-06-04 19:30:44+00', 2700, 'USD', 'captured', '2026-06-04 19:30:44+00', '2026-06-04 19:30:47+00', false),
  ('P0013', 'M02', 'C04', '2026-06-04 21:05:30+00', 12000, 'USD', 'failed', NULL, NULL, false),
  ('P0014', 'M04', 'C03', '2026-06-05 14:00:00+00', 90000, 'USD', 'captured', '2026-06-05 14:00:00+00', '2026-06-08 10:00:00+00', false),
  ('P0015', 'M09', 'C02', '2026-06-05 23:30:18+00', 1000, 'USD', 'captured', '2026-06-05 23:30:18+00', '2026-06-05 23:30:21+00', false),
  ('P0016', 'M05', 'C05', '2026-06-06 15:20:00+00', 1200, 'USD', 'captured', '2026-06-06 15:20:00+00', '2026-06-06 15:20:03+00', false),
  ('P0017', 'M08', 'C08', '2026-06-08 09:30:00+00', 1800, 'GBP', 'captured', '2026-06-08 09:30:00+00', '2026-06-08 09:30:03+00', false),
  ('P0018', 'M05', 'C01', '2026-06-08 12:08:19+00', 600, 'USD', 'captured', '2026-06-08 12:08:19+00', '2026-06-08 12:08:22+00', false),
  ('P0019', 'M07', 'C02', '2026-06-08 23:05:00+00', 2500, 'USD', 'captured', '2026-06-08 23:05:00+00', '2026-06-08 23:05:03+00', false),
  ('P0020', 'M02', 'C05', '2026-06-08 23:50:41+00', 6500, 'USD', 'captured', '2026-06-08 23:50:41+00', '2026-06-08 23:50:44+00', false),
  ('P0021', 'M05', 'C01', '2026-06-09 12:11:05+00', 600, 'USD', 'captured', '2026-06-09 12:11:05+00', '2026-06-09 12:11:08+00', false),
  ('P0022', 'M03', 'C09', '2026-06-09 17:25:10+00', 3500, 'USD', 'captured', '2026-06-09 17:31:02+00', '2026-06-09 17:31:05+00', false),
  ('P0023', 'M05', NULL, '2026-06-09 19:00:00+00', 500, 'USD', 'failed', NULL, NULL, true),
  ('P0024', 'M06', 'C06', '2026-06-10 14:45:30+00', 1900, 'USD', 'captured', '2026-06-10 14:45:30+00', '2026-06-10 14:45:33+00', false),
  ('P0025', 'M01', 'C03', '2026-06-10 20:15:00+00', 180000, 'USD', 'captured', '2026-06-10 20:15:00+00', '2026-06-10 20:15:03+00', false),
  ('P0026', 'M09', 'C04', '2026-06-11 02:20:50+00', 5000, 'USD', 'captured', '2026-06-11 02:20:50+00', '2026-06-11 02:20:53+00', false),
  ('P0027', 'M05', NULL, '2026-06-11 13:00:25+00', 900, 'USD', 'captured', '2026-06-11 13:00:25+00', '2026-06-11 13:00:28+00', false),
  ('P0028', 'M02', 'C10', '2026-06-12 16:10:00+00', 15000, 'USD', 'captured', '2026-06-12 16:10:00+00', '2026-06-12 16:10:03+00', false),
  ('P0029', 'M08', 'C08', '2026-06-12 18:30:12+00', 2400, 'GBP', 'captured', '2026-06-12 18:30:12+00', '2026-06-12 18:30:15+00', false),
  ('P0030', 'M05', 'C02', '2026-06-13 15:00:09+00', 1500, 'USD', 'captured', '2026-06-13 15:00:09+00', '2026-06-13 15:00:12+00', false),
  ('P0031', 'M05', 'C01', '2026-06-15 12:04:44+00', 600, 'USD', 'captured', '2026-06-15 12:04:44+00', '2026-06-15 12:04:47+00', false),
  ('P0032', 'M06', 'C11', '2026-06-15 14:10:00+00', 5200, 'USD', 'captured', '2026-06-15 14:10:00+00', '2026-06-15 14:10:03+00', false),
  ('P0033', 'M09', 'C05', '2026-06-15 15:30:20+00', 2000, 'USD', 'captured', '2026-06-15 15:34:05+00', '2026-06-15 15:34:08+00', false),
  ('P0034', 'M07', 'C02', '2026-06-15 23:08:00+00', 2500, 'USD', 'captured', '2026-06-15 23:08:00+00', '2026-06-15 23:08:03+00', false),
  ('P0035', 'M05', 'C01', '2026-06-16 12:06:31+00', 800, 'USD', 'captured', '2026-06-16 12:06:31+00', '2026-06-16 12:06:34+00', false),
  ('P0036', 'M03', 'C07', '2026-06-16 19:45:00+00', 6000, 'USD', 'captured', '2026-06-16 19:45:00+00', '2026-06-16 19:45:03+00', false),
  ('P0037', 'M09', NULL, '2026-06-16 20:00:00+00', 1000, 'USD', 'captured', '2026-06-16 20:00:00+00', '2026-06-16 20:00:03+00', true),
  ('P0038', 'M05', 'C01', '2026-06-17 12:09:12+00', 600, 'USD', 'captured', '2026-06-17 12:09:12+00', '2026-06-17 12:09:15+00', false),
  ('P0039', 'M06', 'C09', '2026-06-17 16:20:35+00', 2300, 'USD', 'captured', '2026-06-17 16:20:35+00', '2026-06-17 16:20:38+00', false),
  ('P0040', 'M04', 'C04', '2026-06-17 21:40:00+00', 45000, 'USD', 'captured', '2026-06-17 21:40:00+00', '2026-06-19 09:00:00+00', false),
  ('P0041', 'M05', 'C12', '2026-06-18 13:30:00+00', 1100, 'USD', 'captured', '2026-06-18 13:30:00+00', '2026-06-18 13:30:03+00', false),
  ('P0042', 'M08', 'C08', '2026-06-18 17:00:48+00', 1200, 'GBP', 'captured', '2026-06-18 17:00:48+00', '2026-06-18 17:00:51+00', false),
  ('P0043', 'M02', 'C03', '2026-06-19 22:15:07+00', 7800, 'USD', 'canceled', NULL, NULL, false),
  ('P0044', 'M09', 'C06', '2026-06-19 23:45:55+00', 1000, 'USD', 'failed', NULL, NULL, false),
  ('P0045', 'M09', 'C02', '2026-06-20 14:30:00+00', 2000, 'USD', 'captured', '2026-06-20 14:30:00+00', '2026-06-20 14:30:03+00', false),
  ('P0046', 'M03', NULL, '2026-06-20 16:00:26+00', 2500, 'USD', 'failed', NULL, NULL, false),
  ('P0047', 'M05', 'C01', '2026-06-22 12:03:58+00', 600, 'USD', 'captured', '2026-06-22 12:03:58+00', '2026-06-22 12:04:01+00', false),
  ('P0048', 'M02', 'C13', '2026-06-22 13:15:00+00', 9900, 'USD', 'captured', '2026-06-22 13:15:00+00', '2026-06-22 13:15:03+00', false),
  ('P0049', 'M08', 'C08', '2026-06-22 18:20:14+00', 3600, 'GBP', 'captured', '2026-06-22 18:26:39+00', '2026-06-22 18:26:42+00', false),
  ('P0050', 'M07', 'C02', '2026-06-22 23:02:00+00', 2500, 'USD', 'captured', '2026-06-22 23:02:00+00', '2026-06-22 23:02:03+00', false),
  ('P0051', 'M05', 'C01', '2026-06-23 12:12:20+00', 600, 'USD', 'captured', '2026-06-23 12:12:20+00', '2026-06-23 12:12:23+00', false),
  ('P0052', 'M03', 'C11', '2026-06-23 15:50:00+00', 4400, 'USD', 'captured', '2026-06-23 15:50:00+00', '2026-06-23 15:50:03+00', false),
  ('P0053', 'M05', NULL, '2026-06-23 19:00:00+00', 500, 'USD', 'failed', NULL, NULL, true),
  ('P0054', 'M05', 'C01', '2026-06-24 12:07:03+00', 800, 'USD', 'captured', '2026-06-24 12:07:03+00', '2026-06-24 12:07:06+00', false),
  ('P0055', 'M06', 'C05', '2026-06-24 17:35:42+00', 2100, 'USD', 'captured', '2026-06-24 17:35:42+00', '2026-06-24 17:35:45+00', false),
  ('P0056', 'M01', 'C03', '2026-06-24 20:10:00+00', 500000, 'USD', 'captured', '2026-06-24 20:10:00+00', '2026-06-24 20:10:03+00', false),
  ('P0057', 'M09', 'C14', '2026-06-25 14:40:00+00', 5000, 'USD', 'captured', '2026-06-25 14:40:00+00', '2026-06-25 14:40:03+00', false),
  ('P0058', 'M02', 'C04', '2026-06-25 16:05:10+00', 13500, 'USD', 'captured', '2026-06-25 16:05:10+00', '2026-06-25 16:05:13+00', false),
  ('P0059', 'M05', 'C12', '2026-06-26 13:10:00+00', 700, 'USD', 'failed', NULL, NULL, false),
  ('P0060', 'M04', 'C03', '2026-06-26 21:30:00+00', 120000, 'USD', 'captured', '2026-06-26 21:30:00+00', '2026-06-27 09:00:00+00', false),
  ('P0061', 'M05', 'C02', '2026-06-27 15:15:22+00', 1500, 'USD', 'captured', '2026-06-27 15:15:22+00', '2026-06-27 15:15:25+00', false),
  ('P0062', 'M06', NULL, '2026-06-27 18:00:00+00', 1800, 'USD', 'captured', '2026-06-27 18:00:00+00', '2026-06-27 18:00:03+00', false),
  ('P0063', 'M06', 'C01', '2026-06-28 23:55:10+00', 3400, 'USD', 'captured', '2026-06-28 23:55:10+00', '2026-06-28 23:55:13+00', false),
  ('P0064', 'M05', 'C01', '2026-06-29 12:05:00+00', 600, 'USD', 'captured', '2026-06-29 12:05:00+00', '2026-06-29 12:05:03+00', false),
  ('P0065', 'M03', 'C13', '2026-06-29 14:20:30+00', 3800, 'USD', 'captured', '2026-06-29 14:20:30+00', '2026-06-29 14:20:33+00', false),
  ('P0066', 'M08', 'C08', '2026-06-29 16:45:00+00', 2000, 'GBP', 'captured', '2026-06-29 16:45:00+00', '2026-06-29 16:45:03+00', false),
  ('P0067', 'M06', 'C04', '2026-06-29 19:30:11+00', 2600, 'USD', 'captured', '2026-06-29 19:38:52+00', '2026-06-29 19:38:55+00', false),
  ('P0068', 'M07', 'C02', '2026-06-29 23:04:00+00', 2500, 'USD', 'captured', '2026-06-29 23:04:00+00', '2026-06-29 23:04:03+00', false),
  ('P0069', 'M05', 'C01', '2026-06-30 12:10:15+00', 600, 'USD', 'captured', '2026-06-30 12:10:15+00', '2026-06-30 12:10:18+00', false),
  ('P0070', 'M02', 'C11', '2026-06-30 17:20:00+00', 7200, 'USD', 'captured', '2026-06-30 17:20:00+00', '2026-06-30 17:20:03+00', false),
  ('P0071', 'M09', NULL, '2026-06-30 20:00:00+00', 1000, 'USD', 'failed', NULL, NULL, true),
  ('P0072', 'M02', 'C05', '2026-07-01 00:00:00+00', 15000, 'USD', 'captured', '2026-07-01 00:00:00+00', '2026-07-01 00:00:03+00', false),
  ('P0073', 'M03', 'C04', '2026-07-01 01:10:45+00', 4500, 'USD', 'captured', '2026-07-01 01:10:45+00', '2026-07-01 01:10:48+00', false),
  ('P0074', 'M09', 'C15', '2026-07-01 02:15:00+00', 6000, 'USD', 'captured', '2026-07-01 02:15:00+00', '2026-07-01 02:15:03+00', false),
  ('P0075', 'M05', 'C01', '2026-07-01 12:08:30+00', 800, 'USD', 'captured', '2026-07-01 12:08:30+00', '2026-07-01 12:08:33+00', false),
  ('P0076', 'M04', 'C03', '2026-07-01 15:00:00+00', 60000, 'USD', 'captured', '2026-07-01 15:00:00+00', '2026-07-03 09:00:00+00', false),
  ('P0077', 'M10', 'C01', '2026-07-02 14:15:00+00', 1800, 'USD', 'captured', '2026-07-02 14:15:00+00', '2026-07-02 14:15:03+00', false),
  ('P0078', 'M02', NULL, '2026-07-02 16:40:12+00', 5500, 'USD', 'captured', '2026-07-02 16:40:12+00', '2026-07-02 16:40:15+00', false),
  ('P0079', 'M09', 'C02', '2026-07-02 23:20:00+00', 2000, 'USD', 'captured', '2026-07-02 23:20:00+00', '2026-07-02 23:20:03+00', false),
  ('P0080', 'M05', 'C01', '2026-07-03 13:05:44+00', 600, 'USD', 'captured', '2026-07-03 13:05:44+00', '2026-07-03 13:05:47+00', false),
  ('P0081', 'M06', 'C14', '2026-07-03 18:50:00+00', 2900, 'USD', 'failed', NULL, NULL, false),
  ('P0082', 'M10', 'C04', '2026-07-05 16:30:00+00', 3400, 'USD', 'captured', '2026-07-05 16:30:00+00', '2026-07-05 16:30:03+00', false),
  ('P0083', 'M05', 'C01', '2026-07-06 12:06:09+00', 600, 'USD', 'captured', '2026-07-06 12:06:09+00', '2026-07-06 12:06:12+00', false),
  ('P0084', 'M02', 'C04', '2026-07-06 13:40:00+00', 8800, 'USD', 'captured', '2026-07-06 13:40:00+00', '2026-07-06 13:40:03+00', false),
  ('P0085', 'M06', 'C11', '2026-07-06 17:10:25+00', 3100, 'USD', 'captured', '2026-07-06 17:25:40+00', '2026-07-06 17:25:43+00', false),
  ('P0086', 'M07', 'C02', '2026-07-06 23:03:00+00', 2500, 'USD', 'captured', '2026-07-06 23:03:00+00', '2026-07-06 23:03:03+00', false),
  ('P0087', 'M05', 'C01', '2026-07-07 12:09:00+00', 800, 'USD', 'captured', '2026-07-07 12:09:00+00', '2026-07-07 12:09:03+00', false),
  ('P0088', 'M03', 'C16', '2026-07-07 15:20:00+00', 5600, 'USD', 'captured', '2026-07-07 15:20:00+00', '2026-07-07 15:20:03+00', false),
  ('P0089', 'M05', NULL, '2026-07-07 19:00:00+00', 500, 'USD', 'failed', NULL, NULL, true),
  ('P0090', 'M05', 'C01', '2026-07-08 12:04:36+00', 600, 'USD', 'captured', '2026-07-08 12:04:36+00', '2026-07-08 12:04:39+00', false),
  ('P0091', 'M04', 'C05', '2026-07-08 14:30:00+00', 38000, 'USD', 'captured', '2026-07-08 14:30:00+00', '2026-07-09 09:00:00+00', false),
  ('P0092', 'M01', 'C03', '2026-07-08 20:45:00+00', 320000, 'USD', 'captured', '2026-07-08 20:45:00+00', '2026-07-08 20:45:03+00', false),
  ('P0093', 'M09', NULL, '2026-07-09 03:02:10+00', 5000, 'USD', 'failed', NULL, NULL, false),
  ('P0094', 'M09', NULL, '2026-07-09 03:05:44+00', 5000, 'USD', 'failed', NULL, NULL, false),
  ('P0095', 'M09', NULL, '2026-07-09 03:09:02+00', 2000, 'USD', 'captured', '2026-07-09 03:09:02+00', '2026-07-09 03:09:05+00', false),
  ('P0096', 'M09', NULL, '2026-07-09 03:14:30+00', 5000, 'USD', 'failed', NULL, NULL, false),
  ('P0097', 'M09', NULL, '2026-07-09 03:21:15+00', 2000, 'USD', 'captured', '2026-07-09 03:21:15+00', '2026-07-09 03:21:18+00', false),
  ('P0098', 'M09', NULL, '2026-07-09 03:40:00+00', 10000, 'USD', 'failed', NULL, NULL, false),
  ('P0099', 'M05', 'C01', '2026-07-09 12:10:00+00', 600, 'USD', 'captured', '2026-07-09 12:10:00+00', '2026-07-09 12:10:03+00', false),
  ('P0100', 'M02', 'C15', '2026-07-09 16:15:00+00', 4800, 'USD', 'captured', '2026-07-09 16:15:00+00', '2026-07-09 16:15:03+00', false),
  ('P0101', 'M08', 'C08', '2026-07-10 13:20:00+00', 2800, 'GBP', 'captured', '2026-07-10 13:20:00+00', '2026-07-10 13:20:03+00', false),
  ('P0102', 'M06', 'C04', '2026-07-10 18:30:00+00', 4100, 'USD', 'captured', '2026-07-10 18:30:00+00', '2026-07-10 18:30:03+00', false),
  ('P0103', 'M02', 'C06', '2026-07-10 21:00:00+00', 9500, 'USD', 'pending', NULL, NULL, false),
  ('P0104', 'M09', 'C02', '2026-07-11 02:40:00+00', 1000, 'USD', 'captured', '2026-07-11 02:40:00+00', '2026-07-11 02:40:03+00', false),
  ('P0105', 'M04', 'C03', '2026-07-11 15:10:00+00', 75000, 'USD', 'authorized', '2026-07-11 15:10:00+00', NULL, false),
  ('P0106', 'M06', 'C01', '2026-07-11 23:52:00+00', 2200, 'USD', 'captured', '2026-07-11 23:52:00+00', '2026-07-11 23:52:03+00', false),
  ('P0107', 'M05', 'C04', '2026-07-12 14:00:00+00', 1300, 'USD', 'captured', '2026-07-12 14:00:00+00', '2026-07-12 14:00:03+00', false),
  ('P0108', 'M10', NULL, '2026-07-12 19:20:00+00', 1200, 'USD', 'canceled', NULL, NULL, false),
  ('P0109', 'M05', 'C01', '2026-07-13 12:05:00+00', 600, 'USD', 'captured', '2026-07-13 12:05:00+00', '2026-07-13 12:05:03+00', false),
  ('P0110', 'M08', 'C08', '2026-07-13 13:10:00+00', 1500, 'GBP', 'captured', '2026-07-13 13:10:00+00', '2026-07-13 13:10:03+00', false),
  ('P0111', 'M02', 'C04', '2026-07-13 14:05:12+00', 6400, 'USD', 'captured', '2026-07-13 14:12:05+00', '2026-07-13 14:12:08+00', false),
  ('P0112', 'M03', 'C16', '2026-07-13 14:20:00+00', 3000, 'USD', 'failed', NULL, NULL, false),
  ('P0113', 'M05', NULL, '2026-07-13 14:30:00+00', 500, 'USD', 'failed', NULL, NULL, true),
  ('P0114', 'M06', 'C11', '2026-07-13 14:35:00+00', 2800, 'USD', 'captured', '2026-07-13 16:10:27+00', '2026-07-13 16:10:30+00', false),
  ('P0115', 'M09', 'C15', '2026-07-13 14:50:00+00', 2000, 'USD', 'failed', NULL, NULL, false),
  ('P0116', 'M05', NULL, '2026-07-13 15:00:00+00', 500, 'USD', 'failed', NULL, NULL, true),
  ('P0117', 'M05', 'C02', '2026-07-13 15:05:00+00', 900, 'USD', 'captured', '2026-07-13 15:05:00+00', '2026-07-13 15:05:03+00', false),
  ('P0118', 'M10', NULL, '2026-07-13 15:15:00+00', 2600, 'USD', 'failed', NULL, NULL, false),
  ('P0119', 'M02', 'C05', '2026-07-13 15:30:00+00', 11000, 'USD', 'canceled', NULL, NULL, false),
  ('P0120', 'M01', 'C03', '2026-07-13 15:45:00+00', 260000, 'USD', 'pending', NULL, NULL, false),
  ('P0121', 'M06', 'C14', '2026-07-13 15:50:00+00', 1700, 'USD', 'captured', '2026-07-13 16:20:00+00', '2026-07-13 16:20:03+00', false),
  ('P0122', 'M10', 'C01', '2026-07-13 17:30:00+00', 2100, 'USD', 'captured', '2026-07-13 17:30:00+00', '2026-07-13 17:30:03+00', false),
  ('P0123', 'M07', 'C02', '2026-07-13 23:05:00+00', 2500, 'USD', 'captured', '2026-07-13 23:05:00+00', '2026-07-13 23:05:03+00', false);

INSERT INTO payment_attempts
  (attempt_id, payment_id, merchant_id, customer_id, attempted_at, amount_minor, currency, method, status, failure_code, device_id, is_test)
VALUES
  ('A0001', 'P0001', 'M05', 'C01', '2026-06-01 12:05:10+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0002', 'P0002', 'M09', 'C05', '2026-06-01 13:20:05+00', 2000, 'USD', 'card', 'succeeded', NULL, 'dev-05', false),
  ('A0003', 'P0003', 'M01', 'C03', '2026-06-01 15:40:00+00', 240000, 'USD', 'bank_transfer', 'succeeded', NULL, NULL, false),
  ('A0004', 'P0004', 'M07', 'C02', '2026-06-01 23:10:12+00', 2500, 'USD', 'card', 'failed', 'authentication_failed', 'dev-02', false),
  ('A0005', 'P0004', 'M07', 'C02', '2026-06-01 23:12:40+00', 2500, 'USD', 'card', 'succeeded', NULL, 'dev-02', false),
  ('A0006', 'P0005', 'M05', 'C01', '2026-06-02 12:10:33+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0007', 'P0006', 'M06', 'C04', '2026-06-02 16:30:00+00', 3200, 'USD', 'card', 'succeeded', NULL, 'dev-04', false),
  ('A0008', 'P0007', 'M02', 'C06', '2026-06-02 18:45:21+00', 9000, 'USD', 'wallet', 'succeeded', NULL, 'dev-06', false),
  ('A0009', 'P0008', 'M05', NULL, '2026-06-02 20:00:00+00', 500, 'USD', 'card', 'failed', 'do_not_honor', 'dev-qa', true),
  ('A0010', 'P0009', 'M05', 'C01', '2026-06-03 12:02:47+00', 800, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0011', 'P0010', 'M03', NULL, '2026-06-03 22:40:15+00', 4000, 'USD', 'card', 'succeeded', NULL, 'dev-g1', false),
  ('A0012', 'P0011', 'M05', 'C01', '2026-06-04 12:15:02+00', 600, 'USD', 'wallet', 'succeeded', NULL, 'dev-01', false),
  ('A0013', 'P0012', 'M06', 'C07', '2026-06-04 19:30:44+00', 2700, 'USD', 'card', 'succeeded', NULL, 'dev-07', false),
  ('A0014', 'P0013', 'M02', 'C04', '2026-06-04 21:05:30+00', 12000, 'USD', 'card', 'failed', 'insufficient_funds', 'dev-04', false),
  ('A0015', 'P0014', 'M04', 'C03', '2026-06-05 14:00:00+00', 90000, 'USD', 'card', 'succeeded', NULL, 'dev-03', false),
  ('A0016', 'P0015', 'M09', 'C02', '2026-06-05 23:30:18+00', 1000, 'USD', 'wallet', 'succeeded', NULL, 'dev-02', false),
  ('A0017', 'P0016', 'M05', 'C05', '2026-06-06 15:20:00+00', 1200, 'USD', 'card', 'succeeded', NULL, 'dev-05', false),
  ('A0018', 'P0017', 'M08', 'C08', '2026-06-08 09:30:00+00', 1800, 'GBP', 'card', 'succeeded', NULL, 'dev-08', false),
  ('A0019', 'P0018', 'M05', 'C01', '2026-06-08 12:08:19+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0020', 'P0019', 'M07', 'C02', '2026-06-08 23:05:00+00', 2500, 'USD', 'card', 'succeeded', NULL, 'dev-02', false),
  ('A0021', 'P0020', 'M02', 'C05', '2026-06-08 23:50:41+00', 6500, 'USD', 'card', 'succeeded', NULL, 'dev-05', false),
  ('A0022', 'P0021', 'M05', 'C01', '2026-06-09 12:11:05+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0023', 'P0022', 'M03', 'C09', '2026-06-09 17:25:10+00', 3500, 'USD', 'card', 'failed', 'expired_card', 'dev-09', false),
  ('A0024', 'P0022', 'M03', 'C09', '2026-06-09 17:31:02+00', 3500, 'USD', 'wallet', 'succeeded', NULL, 'dev-09', false),
  ('A0025', 'P0023', 'M05', NULL, '2026-06-09 19:00:00+00', 500, 'USD', 'card', 'failed', 'do_not_honor', 'dev-qa', true),
  ('A0026', 'P0024', 'M06', 'C06', '2026-06-10 14:45:30+00', 1900, 'USD', 'card', 'succeeded', NULL, 'dev-06', false),
  ('A0027', 'P0025', 'M01', 'C03', '2026-06-10 20:15:00+00', 180000, 'USD', 'bank_transfer', 'succeeded', NULL, NULL, false),
  ('A0028', 'P0026', 'M09', 'C04', '2026-06-11 02:20:50+00', 5000, 'USD', 'card', 'succeeded', NULL, 'dev-04', false),
  ('A0029', 'P0027', 'M05', NULL, '2026-06-11 13:00:25+00', 900, 'USD', 'card', 'succeeded', NULL, 'dev-g2', false),
  ('A0030', 'P0028', 'M02', 'C10', '2026-06-12 16:10:00+00', 15000, 'USD', 'card', 'succeeded', NULL, 'dev-10', false),
  ('A0031', 'P0029', 'M08', 'C08', '2026-06-12 18:30:12+00', 2400, 'GBP', 'card', 'succeeded', NULL, 'dev-08', false),
  ('A0032', 'P0030', 'M05', 'C02', '2026-06-13 15:00:09+00', 1500, 'USD', 'wallet', 'succeeded', NULL, 'dev-02', false),
  ('A0033', 'P0031', 'M05', 'C01', '2026-06-15 12:04:44+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0034', 'P0032', 'M06', 'C11', '2026-06-15 14:10:00+00', 5200, 'USD', 'card', 'succeeded', NULL, 'dev-11', false),
  ('A0035', 'P0033', 'M09', 'C05', '2026-06-15 15:30:20+00', 2000, 'USD', 'card', 'failed', 'do_not_honor', 'dev-05', false),
  ('A0036', 'P0033', 'M09', 'C05', '2026-06-15 15:34:05+00', 2000, 'USD', 'card', 'succeeded', NULL, 'dev-05', false),
  ('A0037', 'P0034', 'M07', 'C02', '2026-06-15 23:08:00+00', 2500, 'USD', 'card', 'succeeded', NULL, 'dev-02', false),
  ('A0038', 'P0035', 'M05', 'C01', '2026-06-16 12:06:31+00', 800, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0039', 'P0036', 'M03', 'C07', '2026-06-16 19:45:00+00', 6000, 'USD', 'wallet', 'succeeded', NULL, 'dev-07', false),
  ('A0040', 'P0037', 'M09', NULL, '2026-06-16 20:00:00+00', 1000, 'USD', 'card', 'succeeded', NULL, 'dev-qa', true),
  ('A0041', 'P0038', 'M05', 'C01', '2026-06-17 12:09:12+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0042', 'P0039', 'M06', 'C09', '2026-06-17 16:20:35+00', 2300, 'USD', 'card', 'succeeded', NULL, 'dev-09', false),
  ('A0043', 'P0040', 'M04', 'C04', '2026-06-17 21:40:00+00', 45000, 'USD', 'card', 'succeeded', NULL, 'dev-04', false),
  ('A0044', 'P0041', 'M05', 'C12', '2026-06-18 13:30:00+00', 1100, 'USD', 'card', 'succeeded', NULL, 'dev-12', false),
  ('A0045', 'P0042', 'M08', 'C08', '2026-06-18 17:00:48+00', 1200, 'GBP', 'wallet', 'succeeded', NULL, 'dev-08', false),
  ('A0046', 'P0043', 'M02', 'C03', '2026-06-19 22:15:07+00', 7800, 'USD', 'card', 'canceled', NULL, 'dev-03', false),
  ('A0047', 'P0044', 'M09', 'C06', '2026-06-19 23:45:55+00', 1000, 'USD', 'wallet', 'failed', 'insufficient_funds', 'dev-06', false),
  ('A0048', 'P0045', 'M09', 'C02', '2026-06-20 14:30:00+00', 2000, 'USD', 'wallet', 'succeeded', NULL, 'dev-02', false),
  ('A0049', 'P0046', 'M03', NULL, '2026-06-20 16:00:26+00', 2500, 'USD', 'card', 'failed', 'do_not_honor', 'dev-g3', false),
  ('A0050', 'P0047', 'M05', 'C01', '2026-06-22 12:03:58+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0051', 'P0048', 'M02', 'C13', '2026-06-22 13:15:00+00', 9900, 'USD', 'wallet', 'succeeded', NULL, 'dev-13', false),
  ('A0052', 'P0049', 'M08', 'C08', '2026-06-22 18:20:14+00', 3600, 'GBP', 'card', 'failed', 'authentication_failed', 'dev-08', false),
  ('A0053', 'P0049', 'M08', 'C08', '2026-06-22 18:26:39+00', 3600, 'GBP', 'card', 'succeeded', NULL, 'dev-08', false),
  ('A0054', 'P0050', 'M07', 'C02', '2026-06-22 23:02:00+00', 2500, 'USD', 'card', 'succeeded', NULL, 'dev-02', false),
  ('A0055', 'P0051', 'M05', 'C01', '2026-06-23 12:12:20+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0056', 'P0052', 'M03', 'C11', '2026-06-23 15:50:00+00', 4400, 'USD', 'card', 'succeeded', NULL, 'dev-11', false),
  ('A0057', 'P0053', 'M05', NULL, '2026-06-23 19:00:00+00', 500, 'USD', 'card', 'failed', 'processor_timeout', 'dev-qa', true),
  ('A0058', 'P0054', 'M05', 'C01', '2026-06-24 12:07:03+00', 800, 'USD', 'wallet', 'succeeded', NULL, 'dev-01', false),
  ('A0059', 'P0055', 'M06', 'C05', '2026-06-24 17:35:42+00', 2100, 'USD', 'card', 'succeeded', NULL, 'dev-05', false),
  ('A0060', 'P0056', 'M01', 'C03', '2026-06-24 20:10:00+00', 500000, 'USD', 'bank_transfer', 'succeeded', NULL, NULL, false),
  ('A0061', 'P0057', 'M09', 'C14', '2026-06-25 14:40:00+00', 5000, 'USD', 'card', 'succeeded', NULL, 'dev-14', false),
  ('A0062', 'P0058', 'M02', 'C04', '2026-06-25 16:05:10+00', 13500, 'USD', 'card', 'succeeded', NULL, 'dev-04', false),
  ('A0063', 'P0058', 'M02', 'C04', '2026-06-25 16:05:31+00', 13500, 'USD', 'card', 'succeeded', NULL, 'dev-04', false),
  ('A0064', 'P0059', 'M05', 'C12', '2026-06-26 13:10:00+00', 700, 'USD', 'card', 'failed', 'insufficient_funds', 'dev-12', false),
  ('A0065', 'P0060', 'M04', 'C03', '2026-06-26 21:30:00+00', 120000, 'USD', 'card', 'succeeded', NULL, 'dev-03', false),
  ('A0066', 'P0061', 'M05', 'C02', '2026-06-27 15:15:22+00', 1500, 'USD', 'card', 'succeeded', NULL, 'dev-02', false),
  ('A0067', 'P0062', 'M06', NULL, '2026-06-27 18:00:00+00', 1800, 'USD', 'wallet', 'succeeded', NULL, 'dev-g4', false),
  ('A0068', 'P0063', 'M06', 'C01', '2026-06-28 23:55:10+00', 3400, 'USD', 'card', 'succeeded', NULL, 'dev-01b', false),
  ('A0069', 'P0064', 'M05', 'C01', '2026-06-29 12:05:00+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0070', 'P0065', 'M03', 'C13', '2026-06-29 14:20:30+00', 3800, 'USD', 'card', 'succeeded', NULL, 'dev-13', false),
  ('A0071', 'P0066', 'M08', 'C08', '2026-06-29 16:45:00+00', 2000, 'GBP', 'card', 'succeeded', NULL, 'dev-08', false),
  ('A0072', 'P0067', 'M06', 'C04', '2026-06-29 19:30:11+00', 2600, 'USD', 'card', 'failed', 'expired_card', 'dev-04', false),
  ('A0073', 'P0067', 'M06', 'C04', '2026-06-29 19:38:52+00', 2600, 'USD', 'card', 'succeeded', NULL, 'dev-04', false),
  ('A0074', 'P0068', 'M07', 'C02', '2026-06-29 23:04:00+00', 2500, 'USD', 'card', 'succeeded', NULL, 'dev-02', false),
  ('A0075', 'P0069', 'M05', 'C01', '2026-06-30 12:10:15+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0076', 'P0070', 'M02', 'C11', '2026-06-30 17:20:00+00', 7200, 'USD', 'card', 'succeeded', NULL, 'dev-11', false),
  ('A0077', 'P0071', 'M09', NULL, '2026-06-30 20:00:00+00', 1000, 'USD', 'card', 'failed', 'do_not_honor', 'dev-qa', true),
  ('A0078', 'P0072', 'M02', 'C05', '2026-07-01 00:00:00+00', 15000, 'USD', 'card', 'succeeded', NULL, 'dev-05', false),
  ('A0079', 'P0073', 'M03', 'C04', '2026-07-01 01:10:45+00', 4500, 'USD', 'wallet', 'succeeded', NULL, 'dev-04', false),
  ('A0080', 'P0074', 'M09', 'C15', '2026-07-01 02:15:00+00', 6000, 'USD', 'card', 'succeeded', NULL, 'dev-15', false),
  ('A0081', 'P0075', 'M05', 'C01', '2026-07-01 12:08:30+00', 800, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0082', 'P0076', 'M04', 'C03', '2026-07-01 15:00:00+00', 60000, 'USD', 'card', 'succeeded', NULL, 'dev-03', false),
  ('A0083', 'P0077', 'M10', 'C01', '2026-07-02 14:15:00+00', 1800, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0084', 'P0078', 'M02', NULL, '2026-07-02 16:40:12+00', 5500, 'USD', 'card', 'succeeded', NULL, 'dev-g5', false),
  ('A0085', 'P0079', 'M09', 'C02', '2026-07-02 23:20:00+00', 2000, 'USD', 'card', 'succeeded', NULL, 'dev-02', false),
  ('A0086', 'P0080', 'M05', 'C01', '2026-07-03 13:05:44+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0087', 'P0081', 'M06', 'C14', '2026-07-03 18:50:00+00', 2900, 'USD', 'card', 'failed', 'do_not_honor', 'dev-12', false),
  ('A0088', 'P0082', 'M10', 'C04', '2026-07-05 16:30:00+00', 3400, 'USD', 'wallet', 'succeeded', NULL, 'dev-04', false),
  ('A0089', 'P0083', 'M05', 'C01', '2026-07-06 12:06:09+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0090', 'P0084', 'M02', 'C04', '2026-07-06 13:40:00+00', 8800, 'USD', 'card', 'succeeded', NULL, 'dev-04', false),
  ('A0091', 'P0085', 'M06', 'C11', '2026-07-06 17:10:25+00', 3100, 'USD', 'card', 'failed', 'insufficient_funds', 'dev-11', false),
  ('A0092', 'P0085', 'M06', 'C11', '2026-07-06 17:25:40+00', 3100, 'USD', 'wallet', 'succeeded', NULL, 'dev-11', false),
  ('A0093', 'P0086', 'M07', 'C02', '2026-07-06 23:03:00+00', 2500, 'USD', 'card', 'succeeded', NULL, 'dev-02', false),
  ('A0094', 'P0087', 'M05', 'C01', '2026-07-07 12:09:00+00', 800, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0095', 'P0088', 'M03', 'C16', '2026-07-07 15:20:00+00', 5600, 'USD', 'card', 'succeeded', NULL, 'dev-16', false),
  ('A0096', 'P0089', 'M05', NULL, '2026-07-07 19:00:00+00', 500, 'USD', 'card', 'failed', 'do_not_honor', 'dev-qa', true),
  ('A0097', 'P0090', 'M05', 'C01', '2026-07-08 12:04:36+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0098', 'P0091', 'M04', 'C05', '2026-07-08 14:30:00+00', 38000, 'USD', 'card', 'succeeded', NULL, 'dev-05', false),
  ('A0099', 'P0092', 'M01', 'C03', '2026-07-08 20:45:00+00', 320000, 'USD', 'bank_transfer', 'succeeded', NULL, NULL, false),
  ('A0100', 'P0093', 'M09', NULL, '2026-07-09 03:02:10+00', 5000, 'USD', 'card', 'failed', 'suspected_fraud', 'dev-x9', false),
  ('A0101', 'P0094', 'M09', NULL, '2026-07-09 03:05:44+00', 5000, 'USD', 'card', 'failed', 'do_not_honor', 'dev-x9', false),
  ('A0102', 'P0095', 'M09', NULL, '2026-07-09 03:09:02+00', 2000, 'USD', 'card', 'succeeded', NULL, 'dev-x9', false),
  ('A0103', 'P0096', 'M09', NULL, '2026-07-09 03:14:30+00', 5000, 'USD', 'card', 'failed', 'suspected_fraud', 'dev-x9', false),
  ('A0104', 'P0097', 'M09', NULL, '2026-07-09 03:21:15+00', 2000, 'USD', 'card', 'succeeded', NULL, 'dev-x9', false),
  ('A0105', 'P0098', 'M09', NULL, '2026-07-09 03:40:00+00', 10000, 'USD', 'card', 'failed', 'suspected_fraud', 'dev-x9', false),
  ('A0106', 'P0099', 'M05', 'C01', '2026-07-09 12:10:00+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0107', 'P0100', 'M02', 'C15', '2026-07-09 16:15:00+00', 4800, 'USD', 'card', 'succeeded', NULL, 'dev-15', false),
  ('A0108', 'P0101', 'M08', 'C08', '2026-07-10 13:20:00+00', 2800, 'GBP', 'card', 'succeeded', NULL, 'dev-08', false),
  ('A0109', 'P0102', 'M06', 'C04', '2026-07-10 18:30:00+00', 4100, 'USD', 'card', 'succeeded', NULL, 'dev-04', false),
  ('A0110', 'P0103', 'M02', 'C06', '2026-07-10 21:00:00+00', 9500, 'USD', 'bank_transfer', 'pending', NULL, NULL, false),
  ('A0111', 'P0104', 'M09', 'C02', '2026-07-11 02:40:00+00', 1000, 'USD', 'wallet', 'succeeded', NULL, 'dev-02', false),
  ('A0112', 'P0105', 'M04', 'C03', '2026-07-11 15:10:00+00', 75000, 'USD', 'card', 'succeeded', NULL, 'dev-03', false),
  ('A0113', 'P0106', 'M06', 'C01', '2026-07-11 23:52:00+00', 2200, 'USD', 'card', 'succeeded', NULL, 'dev-01b', false),
  ('A0114', 'P0107', 'M05', 'C04', '2026-07-12 14:00:00+00', 1300, 'USD', 'card', 'succeeded', NULL, 'dev-04', false),
  ('A0115', 'P0108', 'M10', NULL, '2026-07-12 19:20:00+00', 1200, 'USD', 'card', 'canceled', NULL, 'dev-g6', false),
  ('A0116', 'P0109', 'M05', 'C01', '2026-07-13 12:05:00+00', 600, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0117', 'P0110', 'M08', 'C08', '2026-07-13 13:10:00+00', 1500, 'GBP', 'card', 'succeeded', NULL, 'dev-08', false),
  ('A0118', 'P0111', 'M02', 'C04', '2026-07-13 14:05:12+00', 6400, 'USD', 'card', 'failed', 'processor_timeout', 'dev-04', false),
  ('A0119', 'P0111', 'M02', 'C04', '2026-07-13 14:07:30+00', 6400, 'USD', 'card', 'failed', 'processor_timeout', 'dev-04', false),
  ('A0120', 'P0111', 'M02', 'C04', '2026-07-13 14:12:05+00', 6400, 'USD', 'wallet', 'succeeded', NULL, 'dev-04', false),
  ('A0121', 'P0112', 'M03', 'C16', '2026-07-13 14:20:00+00', 3000, 'USD', 'card', 'failed', 'processor_timeout', 'dev-16', false),
  ('A0122', 'P0112', 'M03', 'C16', '2026-07-13 14:22:18+00', 3000, 'USD', 'card', 'failed', 'processor_timeout', 'dev-16', false),
  ('A0123', 'P0113', 'M05', NULL, '2026-07-13 14:30:00+00', 500, 'USD', 'card', 'failed', 'processor_timeout', 'dev-qa', true),
  ('A0124', 'P0114', 'M06', 'C11', '2026-07-13 14:35:00+00', 2800, 'USD', 'card', 'failed', 'processor_timeout', 'dev-11', false),
  ('A0125', 'P0115', 'M09', 'C15', '2026-07-13 14:50:00+00', 2000, 'USD', 'card', 'failed', 'processor_timeout', 'dev-15', false),
  ('A0126', 'P0115', 'M09', 'C15', '2026-07-13 14:52:10+00', 2000, 'USD', 'card', 'failed', 'processor_timeout', 'dev-15', false),
  ('A0127', 'P0115', 'M09', 'C15', '2026-07-13 14:58:45+00', 2000, 'USD', 'card', 'failed', 'processor_timeout', 'dev-15', false),
  ('A0128', 'P0116', 'M05', NULL, '2026-07-13 15:00:00+00', 500, 'USD', 'card', 'failed', 'processor_timeout', 'dev-qa', true),
  ('A0129', 'P0117', 'M05', 'C02', '2026-07-13 15:05:00+00', 900, 'USD', 'wallet', 'succeeded', NULL, 'dev-02', false),
  ('A0130', 'P0118', 'M10', NULL, '2026-07-13 15:15:00+00', 2600, 'USD', 'card', 'failed', 'processor_timeout', 'dev-g7', false),
  ('A0131', 'P0119', 'M02', 'C05', '2026-07-13 15:30:00+00', 11000, 'USD', 'card', 'failed', 'processor_timeout', 'dev-05', false),
  ('A0132', 'P0119', 'M02', 'C05', '2026-07-13 15:33:20+00', 11000, 'USD', 'card', 'canceled', NULL, 'dev-05', false),
  ('A0133', 'P0120', 'M01', 'C03', '2026-07-13 15:45:00+00', 260000, 'USD', 'bank_transfer', 'pending', NULL, NULL, false),
  ('A0134', 'P0121', 'M06', 'C14', '2026-07-13 15:50:00+00', 1700, 'USD', 'card', 'failed', 'processor_timeout', 'dev-14', false),
  ('A0135', 'P0114', 'M06', 'C11', '2026-07-13 16:10:27+00', 2800, 'USD', 'card', 'succeeded', NULL, 'dev-11', false),
  ('A0136', 'P0121', 'M06', 'C14', '2026-07-13 16:20:00+00', 1700, 'USD', 'card', 'succeeded', NULL, 'dev-14', false),
  ('A0137', 'P0122', 'M10', 'C01', '2026-07-13 17:30:00+00', 2100, 'USD', 'card', 'succeeded', NULL, 'dev-01', false),
  ('A0138', 'P0123', 'M07', 'C02', '2026-07-13 23:05:00+00', 2500, 'USD', 'card', 'succeeded', NULL, 'dev-02', false);

INSERT INTO refunds
  (refund_id, payment_id, created_at, amount_minor, status, reason)
VALUES
  ('R01', 'P0007', '2026-06-05 16:00:00+00', 9000, 'succeeded', 'customer_request'),
  ('R02', 'P0036', '2026-06-18 11:00:00+00', 1500, 'failed', 'product_issue'),
  ('R03', 'P0036', '2026-06-19 11:30:00+00', 1500, 'succeeded', 'product_issue'),
  ('R04', 'P0058', '2026-06-26 14:00:00+00', 13500, 'succeeded', 'duplicate'),
  ('R05', 'P0060', '2026-06-29 15:00:00+00', 20000, 'succeeded', 'product_issue'),
  ('R06', 'P0060', '2026-07-02 15:30:00+00', 30000, 'succeeded', 'customer_request'),
  ('R07', 'P0060', '2026-07-06 10:15:00+00', 10000, 'succeeded', 'product_issue'),
  ('R08', 'P0095', '2026-07-10 09:00:00+00', 2000, 'succeeded', 'fraud'),
  ('R09', 'P0102', '2026-07-13 10:00:00+00', 4100, 'pending', 'customer request');

INSERT INTO disputes
  (dispute_id, payment_id, opened_at, amount_minor, reason, status)
VALUES
  ('D01', 'P0014', '2026-06-20 10:00:00+00', 90000, 'service_not_provided', 'won'),
  ('D02', 'P0026', '2026-06-24 12:30:00+00', 5000, 'unrecognized', 'lost'),
  ('D03', 'P0057', '2026-07-08 09:45:00+00', 5000, 'fraudulent', 'open'),
  ('D04', 'P0097', '2026-07-12 08:20:00+00', 2000, 'fraudulent', 'open');

INSERT INTO ledger_entries
  (entry_id, journal_id, payment_id, account, direction, amount_minor, currency, posted_at)
VALUES
  (1, 'J0001', 'P0001', 'processor_receivable', 'debit', 600, 'USD', '2026-06-01 12:05:13+00'),
  (2, 'J0001', 'P0001', 'merchant_payable', 'credit', 582, 'USD', '2026-06-01 12:05:13+00'),
  (3, 'J0001', 'P0001', 'fee_revenue', 'credit', 18, 'USD', '2026-06-01 12:05:13+00'),
  (4, 'J0002', 'P0002', 'processor_receivable', 'debit', 2000, 'USD', '2026-06-01 13:20:08+00'),
  (5, 'J0002', 'P0002', 'merchant_payable', 'credit', 1940, 'USD', '2026-06-01 13:20:08+00'),
  (6, 'J0002', 'P0002', 'fee_revenue', 'credit', 60, 'USD', '2026-06-01 13:20:08+00'),
  (7, 'J0003', 'P0003', 'processor_receivable', 'debit', 240000, 'USD', '2026-06-01 15:40:03+00'),
  (8, 'J0003', 'P0003', 'merchant_payable', 'credit', 232800, 'USD', '2026-06-01 15:40:03+00'),
  (9, 'J0003', 'P0003', 'fee_revenue', 'credit', 7200, 'USD', '2026-06-01 15:40:03+00'),
  (10, 'J0004', 'P0004', 'processor_receivable', 'debit', 2500, 'USD', '2026-06-01 23:12:43+00'),
  (11, 'J0004', 'P0004', 'merchant_payable', 'credit', 2425, 'USD', '2026-06-01 23:12:43+00'),
  (12, 'J0004', 'P0004', 'fee_revenue', 'credit', 75, 'USD', '2026-06-01 23:12:43+00'),
  (13, 'J0005', 'P0005', 'processor_receivable', 'debit', 600, 'USD', '2026-06-02 12:10:36+00'),
  (14, 'J0005', 'P0005', 'merchant_payable', 'credit', 582, 'USD', '2026-06-02 12:10:36+00'),
  (15, 'J0005', 'P0005', 'fee_revenue', 'credit', 18, 'USD', '2026-06-02 12:10:36+00'),
  (16, 'J0006', 'P0006', 'processor_receivable', 'debit', 3200, 'USD', '2026-06-02 16:30:03+00'),
  (17, 'J0006', 'P0006', 'merchant_payable', 'credit', 3104, 'USD', '2026-06-02 16:30:03+00'),
  (18, 'J0006', 'P0006', 'fee_revenue', 'credit', 96, 'USD', '2026-06-02 16:30:03+00'),
  (19, 'J0007', 'P0007', 'processor_receivable', 'debit', 9000, 'USD', '2026-06-02 18:45:24+00'),
  (20, 'J0007', 'P0007', 'merchant_payable', 'credit', 8730, 'USD', '2026-06-02 18:45:24+00'),
  (21, 'J0007', 'P0007', 'fee_revenue', 'credit', 270, 'USD', '2026-06-02 18:45:24+00'),
  (22, 'J0008', 'P0009', 'processor_receivable', 'debit', 800, 'USD', '2026-06-03 12:02:50+00'),
  (23, 'J0008', 'P0009', 'merchant_payable', 'credit', 776, 'USD', '2026-06-03 12:02:50+00'),
  (24, 'J0008', 'P0009', 'fee_revenue', 'credit', 24, 'USD', '2026-06-03 12:02:50+00'),
  (25, 'J0009', 'P0010', 'processor_receivable', 'debit', 4000, 'USD', '2026-06-03 22:40:18+00'),
  (26, 'J0009', 'P0010', 'merchant_payable', 'credit', 3880, 'USD', '2026-06-03 22:40:18+00'),
  (27, 'J0009', 'P0010', 'fee_revenue', 'credit', 120, 'USD', '2026-06-03 22:40:18+00'),
  (28, 'J0010', 'P0011', 'processor_receivable', 'debit', 600, 'USD', '2026-06-04 12:15:05+00'),
  (29, 'J0010', 'P0011', 'merchant_payable', 'credit', 582, 'USD', '2026-06-04 12:15:05+00'),
  (30, 'J0010', 'P0011', 'fee_revenue', 'credit', 18, 'USD', '2026-06-04 12:15:05+00'),
  (31, 'J0011', 'P0012', 'processor_receivable', 'debit', 2700, 'USD', '2026-06-04 19:30:47+00'),
  (32, 'J0011', 'P0012', 'merchant_payable', 'credit', 2619, 'USD', '2026-06-04 19:30:47+00'),
  (33, 'J0011', 'P0012', 'fee_revenue', 'credit', 81, 'USD', '2026-06-04 19:30:47+00'),
  (34, 'J0012', 'P0007', 'merchant_payable', 'debit', 9000, 'USD', '2026-06-05 16:00:00+00'),
  (35, 'J0012', 'P0007', 'processor_receivable', 'credit', 9000, 'USD', '2026-06-05 16:00:00+00'),
  (36, 'J0013', 'P0015', 'processor_receivable', 'debit', 1000, 'USD', '2026-06-05 23:30:21+00'),
  (37, 'J0013', 'P0015', 'merchant_payable', 'credit', 970, 'USD', '2026-06-05 23:30:21+00'),
  (38, 'J0013', 'P0015', 'fee_revenue', 'credit', 30, 'USD', '2026-06-05 23:30:21+00'),
  (39, 'J0014', 'P0016', 'processor_receivable', 'debit', 1200, 'USD', '2026-06-06 15:20:03+00'),
  (40, 'J0014', 'P0016', 'merchant_payable', 'credit', 1164, 'USD', '2026-06-06 15:20:03+00'),
  (41, 'J0014', 'P0016', 'fee_revenue', 'credit', 36, 'USD', '2026-06-06 15:20:03+00'),
  (42, 'J0015', 'P0017', 'processor_receivable', 'debit', 1800, 'GBP', '2026-06-08 09:30:03+00'),
  (43, 'J0015', 'P0017', 'merchant_payable', 'credit', 1746, 'GBP', '2026-06-08 09:30:03+00'),
  (44, 'J0015', 'P0017', 'fee_revenue', 'credit', 54, 'GBP', '2026-06-08 09:30:03+00'),
  (45, 'J0016', 'P0014', 'processor_receivable', 'debit', 90000, 'USD', '2026-06-08 10:00:00+00'),
  (46, 'J0016', 'P0014', 'merchant_payable', 'credit', 87300, 'USD', '2026-06-08 10:00:00+00'),
  (47, 'J0016', 'P0014', 'fee_revenue', 'credit', 2700, 'USD', '2026-06-08 10:00:00+00'),
  (48, 'J0017', 'P0018', 'processor_receivable', 'debit', 600, 'USD', '2026-06-08 12:08:22+00'),
  (49, 'J0017', 'P0018', 'merchant_payable', 'credit', 582, 'USD', '2026-06-08 12:08:22+00'),
  (50, 'J0017', 'P0018', 'fee_revenue', 'credit', 18, 'USD', '2026-06-08 12:08:22+00'),
  (51, 'J0018', 'P0019', 'processor_receivable', 'debit', 2500, 'USD', '2026-06-08 23:05:03+00'),
  (52, 'J0018', 'P0019', 'merchant_payable', 'credit', 2425, 'USD', '2026-06-08 23:05:03+00'),
  (53, 'J0018', 'P0019', 'fee_revenue', 'credit', 75, 'USD', '2026-06-08 23:05:03+00'),
  (54, 'J0019', 'P0020', 'processor_receivable', 'debit', 6500, 'USD', '2026-06-08 23:50:44+00'),
  (55, 'J0019', 'P0020', 'merchant_payable', 'credit', 6305, 'USD', '2026-06-08 23:50:44+00'),
  (56, 'J0019', 'P0020', 'fee_revenue', 'credit', 195, 'USD', '2026-06-08 23:50:44+00'),
  (57, 'J0020', 'P0021', 'processor_receivable', 'debit', 600, 'USD', '2026-06-09 12:11:08+00'),
  (58, 'J0020', 'P0021', 'merchant_payable', 'credit', 582, 'USD', '2026-06-09 12:11:08+00'),
  (59, 'J0020', 'P0021', 'fee_revenue', 'credit', 18, 'USD', '2026-06-09 12:11:08+00'),
  (60, 'J0021', 'P0022', 'processor_receivable', 'debit', 3500, 'USD', '2026-06-09 17:31:05+00'),
  (61, 'J0021', 'P0022', 'merchant_payable', 'credit', 3395, 'USD', '2026-06-09 17:31:05+00'),
  (62, 'J0021', 'P0022', 'fee_revenue', 'credit', 105, 'USD', '2026-06-09 17:31:05+00'),
  (63, 'J0022', 'P0024', 'processor_receivable', 'debit', 1900, 'USD', '2026-06-10 14:45:33+00'),
  (64, 'J0022', 'P0024', 'merchant_payable', 'credit', 1843, 'USD', '2026-06-10 14:45:33+00'),
  (65, 'J0022', 'P0024', 'fee_revenue', 'credit', 57, 'USD', '2026-06-10 14:45:33+00'),
  (66, 'J0023', 'P0025', 'processor_receivable', 'debit', 180000, 'USD', '2026-06-10 20:15:03+00'),
  (67, 'J0023', 'P0025', 'merchant_payable', 'credit', 174600, 'USD', '2026-06-10 20:15:03+00'),
  (68, 'J0023', 'P0025', 'fee_revenue', 'credit', 5400, 'USD', '2026-06-10 20:15:03+00'),
  (69, 'J0024', 'P0026', 'processor_receivable', 'debit', 5000, 'USD', '2026-06-11 02:20:53+00'),
  (70, 'J0024', 'P0026', 'merchant_payable', 'credit', 4850, 'USD', '2026-06-11 02:20:53+00'),
  (71, 'J0024', 'P0026', 'fee_revenue', 'credit', 150, 'USD', '2026-06-11 02:20:53+00'),
  (72, 'J0025', 'P0027', 'processor_receivable', 'debit', 900, 'USD', '2026-06-11 13:00:28+00'),
  (73, 'J0025', 'P0027', 'merchant_payable', 'credit', 873, 'USD', '2026-06-11 13:00:28+00'),
  (74, 'J0025', 'P0027', 'fee_revenue', 'credit', 27, 'USD', '2026-06-11 13:00:28+00'),
  (75, 'J0026', 'P0028', 'processor_receivable', 'debit', 15000, 'USD', '2026-06-12 16:10:03+00'),
  (76, 'J0026', 'P0028', 'merchant_payable', 'credit', 14550, 'USD', '2026-06-12 16:10:03+00'),
  (77, 'J0026', 'P0028', 'fee_revenue', 'credit', 450, 'USD', '2026-06-12 16:10:03+00'),
  (78, 'J0027', 'P0029', 'processor_receivable', 'debit', 2400, 'GBP', '2026-06-12 18:30:15+00'),
  (79, 'J0027', 'P0029', 'merchant_payable', 'credit', 2328, 'GBP', '2026-06-12 18:30:15+00'),
  (80, 'J0027', 'P0029', 'fee_revenue', 'credit', 72, 'GBP', '2026-06-12 18:30:15+00'),
  (81, 'J0028', 'P0030', 'processor_receivable', 'debit', 1500, 'USD', '2026-06-13 15:00:12+00'),
  (82, 'J0028', 'P0030', 'merchant_payable', 'credit', 1455, 'USD', '2026-06-13 15:00:12+00'),
  (83, 'J0028', 'P0030', 'fee_revenue', 'credit', 45, 'USD', '2026-06-13 15:00:12+00'),
  (84, 'J0029', 'P0031', 'processor_receivable', 'debit', 600, 'USD', '2026-06-15 12:04:47+00'),
  (85, 'J0029', 'P0031', 'merchant_payable', 'credit', 582, 'USD', '2026-06-15 12:04:47+00'),
  (86, 'J0029', 'P0031', 'fee_revenue', 'credit', 18, 'USD', '2026-06-15 12:04:47+00'),
  (87, 'J0030', 'P0032', 'processor_receivable', 'debit', 5200, 'USD', '2026-06-15 14:10:03+00'),
  (88, 'J0030', 'P0032', 'merchant_payable', 'credit', 5044, 'USD', '2026-06-15 14:10:03+00'),
  (89, 'J0030', 'P0032', 'fee_revenue', 'credit', 156, 'USD', '2026-06-15 14:10:03+00'),
  (90, 'J0031', 'P0033', 'processor_receivable', 'debit', 2000, 'USD', '2026-06-15 15:34:08+00'),
  (91, 'J0031', 'P0033', 'merchant_payable', 'credit', 1940, 'USD', '2026-06-15 15:34:08+00'),
  (92, 'J0031', 'P0033', 'fee_revenue', 'credit', 60, 'USD', '2026-06-15 15:34:08+00'),
  (93, 'J0032', 'P0034', 'processor_receivable', 'debit', 2500, 'USD', '2026-06-15 23:08:03+00'),
  (94, 'J0032', 'P0034', 'merchant_payable', 'credit', 2425, 'USD', '2026-06-15 23:08:03+00'),
  (95, 'J0032', 'P0034', 'fee_revenue', 'credit', 75, 'USD', '2026-06-15 23:08:03+00'),
  (96, 'J0033', 'P0035', 'processor_receivable', 'debit', 800, 'USD', '2026-06-16 12:06:34+00'),
  (97, 'J0033', 'P0035', 'merchant_payable', 'credit', 776, 'USD', '2026-06-16 12:06:34+00'),
  (98, 'J0033', 'P0035', 'fee_revenue', 'credit', 24, 'USD', '2026-06-16 12:06:34+00'),
  (99, 'J0034', 'P0036', 'processor_receivable', 'debit', 6000, 'USD', '2026-06-16 19:45:03+00'),
  (100, 'J0034', 'P0036', 'merchant_payable', 'credit', 5820, 'USD', '2026-06-16 19:45:03+00'),
  (101, 'J0034', 'P0036', 'fee_revenue', 'credit', 180, 'USD', '2026-06-16 19:45:03+00'),
  (102, 'J0035', 'P0038', 'processor_receivable', 'debit', 600, 'USD', '2026-06-17 12:09:15+00'),
  (103, 'J0035', 'P0038', 'merchant_payable', 'credit', 582, 'USD', '2026-06-17 12:09:15+00'),
  (104, 'J0035', 'P0038', 'fee_revenue', 'credit', 18, 'USD', '2026-06-17 12:09:15+00'),
  (105, 'J0036', 'P0039', 'processor_receivable', 'debit', 2300, 'USD', '2026-06-17 16:20:38+00'),
  (106, 'J0036', 'P0039', 'merchant_payable', 'credit', 2231, 'USD', '2026-06-17 16:20:38+00'),
  (107, 'J0036', 'P0039', 'fee_revenue', 'credit', 69, 'USD', '2026-06-17 16:20:38+00'),
  (108, 'J0037', 'P0041', 'processor_receivable', 'debit', 1100, 'USD', '2026-06-18 13:30:03+00'),
  (109, 'J0037', 'P0041', 'merchant_payable', 'credit', 1067, 'USD', '2026-06-18 13:30:03+00'),
  (110, 'J0037', 'P0041', 'fee_revenue', 'credit', 33, 'USD', '2026-06-18 13:30:03+00'),
  (111, 'J0038', 'P0042', 'processor_receivable', 'debit', 1200, 'GBP', '2026-06-18 17:00:51+00'),
  (112, 'J0038', 'P0042', 'merchant_payable', 'credit', 1164, 'GBP', '2026-06-18 17:00:51+00'),
  (113, 'J0038', 'P0042', 'fee_revenue', 'credit', 36, 'GBP', '2026-06-18 17:00:51+00'),
  (114, 'J0039', 'P0040', 'processor_receivable', 'debit', 45000, 'USD', '2026-06-19 09:00:00+00'),
  (115, 'J0039', 'P0040', 'merchant_payable', 'credit', 43650, 'USD', '2026-06-19 09:00:00+00'),
  (116, 'J0039', 'P0040', 'fee_revenue', 'credit', 1350, 'USD', '2026-06-19 09:00:00+00'),
  (117, 'J0040', 'P0036', 'merchant_payable', 'debit', 1500, 'USD', '2026-06-19 11:30:00+00'),
  (118, 'J0040', 'P0036', 'processor_receivable', 'credit', 1500, 'USD', '2026-06-19 11:30:00+00'),
  (119, 'J0041', 'P0045', 'processor_receivable', 'debit', 2000, 'USD', '2026-06-20 14:30:03+00'),
  (120, 'J0041', 'P0045', 'merchant_payable', 'credit', 1940, 'USD', '2026-06-20 14:30:03+00'),
  (121, 'J0041', 'P0045', 'fee_revenue', 'credit', 60, 'USD', '2026-06-20 14:30:03+00'),
  (122, 'J0042', 'P0047', 'processor_receivable', 'debit', 600, 'USD', '2026-06-22 12:04:01+00'),
  (123, 'J0042', 'P0047', 'merchant_payable', 'credit', 582, 'USD', '2026-06-22 12:04:01+00'),
  (124, 'J0042', 'P0047', 'fee_revenue', 'credit', 18, 'USD', '2026-06-22 12:04:01+00'),
  (125, 'J0043', 'P0048', 'processor_receivable', 'debit', 9900, 'USD', '2026-06-22 13:15:03+00'),
  (126, 'J0043', 'P0048', 'merchant_payable', 'credit', 9603, 'USD', '2026-06-22 13:15:03+00'),
  (127, 'J0043', 'P0048', 'fee_revenue', 'credit', 297, 'USD', '2026-06-22 13:15:03+00'),
  (128, 'J0044', 'P0049', 'processor_receivable', 'debit', 3600, 'GBP', '2026-06-22 18:26:42+00'),
  (129, 'J0044', 'P0049', 'merchant_payable', 'credit', 3492, 'GBP', '2026-06-22 18:26:42+00'),
  (130, 'J0044', 'P0049', 'fee_revenue', 'credit', 108, 'GBP', '2026-06-22 18:26:42+00'),
  (131, 'J0045', 'P0050', 'processor_receivable', 'debit', 2500, 'USD', '2026-06-22 23:02:03+00'),
  (132, 'J0045', 'P0050', 'merchant_payable', 'credit', 2425, 'USD', '2026-06-22 23:02:03+00'),
  (133, 'J0045', 'P0050', 'fee_revenue', 'credit', 75, 'USD', '2026-06-22 23:02:03+00'),
  (134, 'J0046', 'P0051', 'processor_receivable', 'debit', 600, 'USD', '2026-06-23 12:12:23+00'),
  (135, 'J0046', 'P0051', 'merchant_payable', 'credit', 582, 'USD', '2026-06-23 12:12:23+00'),
  (136, 'J0046', 'P0051', 'fee_revenue', 'credit', 18, 'USD', '2026-06-23 12:12:23+00'),
  (137, 'J0047', 'P0052', 'processor_receivable', 'debit', 4400, 'USD', '2026-06-23 15:50:03+00'),
  (138, 'J0047', 'P0052', 'merchant_payable', 'credit', 4268, 'USD', '2026-06-23 15:50:03+00'),
  (139, 'J0047', 'P0052', 'fee_revenue', 'credit', 132, 'USD', '2026-06-23 15:50:03+00'),
  (140, 'J0048', 'P0054', 'processor_receivable', 'debit', 800, 'USD', '2026-06-24 12:07:06+00'),
  (141, 'J0048', 'P0054', 'merchant_payable', 'credit', 776, 'USD', '2026-06-24 12:07:06+00'),
  (142, 'J0048', 'P0054', 'fee_revenue', 'credit', 24, 'USD', '2026-06-24 12:07:06+00'),
  (143, 'J0049', 'P0055', 'processor_receivable', 'debit', 2100, 'USD', '2026-06-24 17:35:45+00'),
  (144, 'J0049', 'P0055', 'merchant_payable', 'credit', 2037, 'USD', '2026-06-24 17:35:45+00'),
  (145, 'J0049', 'P0055', 'fee_revenue', 'credit', 63, 'USD', '2026-06-24 17:35:45+00'),
  (146, 'J0050', 'P0056', 'processor_receivable', 'debit', 500000, 'USD', '2026-06-24 20:10:03+00'),
  (147, 'J0050', 'P0056', 'merchant_payable', 'credit', 485000, 'USD', '2026-06-24 20:10:03+00'),
  (148, 'J0050', 'P0056', 'fee_revenue', 'credit', 15000, 'USD', '2026-06-24 20:10:03+00'),
  (149, 'J0051', 'P0057', 'processor_receivable', 'debit', 5000, 'USD', '2026-06-25 14:40:03+00'),
  (150, 'J0051', 'P0057', 'merchant_payable', 'credit', 4850, 'USD', '2026-06-25 14:40:03+00'),
  (151, 'J0051', 'P0057', 'fee_revenue', 'credit', 150, 'USD', '2026-06-25 14:40:03+00'),
  (152, 'J0052', 'P0058', 'processor_receivable', 'debit', 13500, 'USD', '2026-06-25 16:05:13+00'),
  (153, 'J0052', 'P0058', 'merchant_payable', 'credit', 13095, 'USD', '2026-06-25 16:05:13+00'),
  (154, 'J0052', 'P0058', 'fee_revenue', 'credit', 405, 'USD', '2026-06-25 16:05:13+00'),
  (155, 'J0053', 'P0058', 'processor_receivable', 'debit', 13500, 'USD', '2026-06-25 16:05:34+00'),
  (156, 'J0053', 'P0058', 'merchant_payable', 'credit', 13095, 'USD', '2026-06-25 16:05:34+00'),
  (157, 'J0053', 'P0058', 'fee_revenue', 'credit', 405, 'USD', '2026-06-25 16:05:34+00'),
  (158, 'J0054', 'P0058', 'merchant_payable', 'debit', 13500, 'USD', '2026-06-26 14:00:00+00'),
  (159, 'J0054', 'P0058', 'processor_receivable', 'credit', 13500, 'USD', '2026-06-26 14:00:00+00'),
  (160, 'J0055', 'P0060', 'processor_receivable', 'debit', 120000, 'USD', '2026-06-27 09:00:00+00'),
  (161, 'J0055', 'P0060', 'merchant_payable', 'credit', 116400, 'USD', '2026-06-27 09:00:00+00'),
  (162, 'J0055', 'P0060', 'fee_revenue', 'credit', 3600, 'USD', '2026-06-27 09:00:00+00'),
  (163, 'J0056', 'P0061', 'processor_receivable', 'debit', 1500, 'USD', '2026-06-27 15:15:25+00'),
  (164, 'J0056', 'P0061', 'merchant_payable', 'credit', 1455, 'USD', '2026-06-27 15:15:25+00'),
  (165, 'J0056', 'P0061', 'fee_revenue', 'credit', 45, 'USD', '2026-06-27 15:15:25+00'),
  (166, 'J0057', 'P0062', 'processor_receivable', 'debit', 1800, 'USD', '2026-06-27 18:00:03+00'),
  (167, 'J0057', 'P0062', 'merchant_payable', 'credit', 1746, 'USD', '2026-06-27 18:00:03+00'),
  (168, 'J0057', 'P0062', 'fee_revenue', 'credit', 54, 'USD', '2026-06-27 18:00:03+00'),
  (169, 'J0058', 'P0063', 'processor_receivable', 'debit', 3400, 'USD', '2026-06-28 23:55:13+00'),
  (170, 'J0058', 'P0063', 'merchant_payable', 'credit', 3298, 'USD', '2026-06-28 23:55:13+00'),
  (171, 'J0058', 'P0063', 'fee_revenue', 'credit', 102, 'USD', '2026-06-28 23:55:13+00'),
  (172, 'J0059', 'P0064', 'processor_receivable', 'debit', 600, 'USD', '2026-06-29 12:05:03+00'),
  (173, 'J0059', 'P0064', 'merchant_payable', 'credit', 582, 'USD', '2026-06-29 12:05:03+00'),
  (174, 'J0059', 'P0064', 'fee_revenue', 'credit', 18, 'USD', '2026-06-29 12:05:03+00'),
  (175, 'J0060', 'P0065', 'processor_receivable', 'debit', 3800, 'USD', '2026-06-29 14:20:33+00'),
  (176, 'J0060', 'P0065', 'merchant_payable', 'credit', 3686, 'USD', '2026-06-29 14:20:33+00'),
  (177, 'J0060', 'P0065', 'fee_revenue', 'credit', 114, 'USD', '2026-06-29 14:20:33+00'),
  (178, 'J0061', 'P0060', 'merchant_payable', 'debit', 20000, 'USD', '2026-06-29 15:00:00+00'),
  (179, 'J0061', 'P0060', 'processor_receivable', 'credit', 20000, 'USD', '2026-06-29 15:00:00+00'),
  (180, 'J0062', 'P0066', 'processor_receivable', 'debit', 2000, 'GBP', '2026-06-29 16:45:03+00'),
  (181, 'J0062', 'P0066', 'merchant_payable', 'credit', 1940, 'GBP', '2026-06-29 16:45:03+00'),
  (182, 'J0062', 'P0066', 'fee_revenue', 'credit', 60, 'GBP', '2026-06-29 16:45:03+00'),
  (183, 'J0063', 'P0067', 'processor_receivable', 'debit', 2600, 'USD', '2026-06-29 19:38:55+00'),
  (184, 'J0063', 'P0067', 'merchant_payable', 'credit', 2522, 'USD', '2026-06-29 19:38:55+00'),
  (185, 'J0063', 'P0067', 'fee_revenue', 'credit', 78, 'USD', '2026-06-29 19:38:55+00'),
  (186, 'J0064', 'P0068', 'processor_receivable', 'debit', 2500, 'USD', '2026-06-29 23:04:03+00'),
  (187, 'J0064', 'P0068', 'merchant_payable', 'credit', 2425, 'USD', '2026-06-29 23:04:03+00'),
  (188, 'J0064', 'P0068', 'fee_revenue', 'credit', 75, 'USD', '2026-06-29 23:04:03+00'),
  (189, 'J0065', 'P0069', 'processor_receivable', 'debit', 600, 'USD', '2026-06-30 12:10:18+00'),
  (190, 'J0065', 'P0069', 'merchant_payable', 'credit', 582, 'USD', '2026-06-30 12:10:18+00'),
  (191, 'J0065', 'P0069', 'fee_revenue', 'credit', 18, 'USD', '2026-06-30 12:10:18+00'),
  (192, 'J0066', 'P0070', 'processor_receivable', 'debit', 7200, 'USD', '2026-06-30 17:20:03+00'),
  (193, 'J0066', 'P0070', 'merchant_payable', 'credit', 6984, 'USD', '2026-06-30 17:20:03+00'),
  (194, 'J0067', 'P0072', 'processor_receivable', 'debit', 15000, 'USD', '2026-07-01 00:00:03+00'),
  (195, 'J0067', 'P0072', 'merchant_payable', 'credit', 14550, 'USD', '2026-07-01 00:00:03+00'),
  (196, 'J0067', 'P0072', 'fee_revenue', 'credit', 450, 'USD', '2026-07-01 00:00:03+00'),
  (197, 'J0068', 'P0073', 'processor_receivable', 'debit', 4500, 'USD', '2026-07-01 01:10:48+00'),
  (198, 'J0068', 'P0073', 'merchant_payable', 'credit', 4365, 'USD', '2026-07-01 01:10:48+00'),
  (199, 'J0068', 'P0073', 'fee_revenue', 'credit', 135, 'USD', '2026-07-01 01:10:48+00'),
  (200, 'J0069', 'P0074', 'processor_receivable', 'debit', 6000, 'USD', '2026-07-01 02:15:03+00'),
  (201, 'J0069', 'P0074', 'merchant_payable', 'credit', 5820, 'USD', '2026-07-01 02:15:03+00'),
  (202, 'J0069', 'P0074', 'fee_revenue', 'credit', 180, 'USD', '2026-07-01 02:15:03+00'),
  (203, 'J0070', 'P0075', 'processor_receivable', 'debit', 800, 'USD', '2026-07-01 12:08:33+00'),
  (204, 'J0070', 'P0075', 'merchant_payable', 'credit', 776, 'USD', '2026-07-01 12:08:33+00'),
  (205, 'J0070', 'P0075', 'fee_revenue', 'credit', 24, 'USD', '2026-07-01 12:08:33+00'),
  (206, 'J0071', 'P0077', 'processor_receivable', 'debit', 1800, 'USD', '2026-07-02 14:15:03+00'),
  (207, 'J0071', 'P0077', 'merchant_payable', 'credit', 1746, 'USD', '2026-07-02 14:15:03+00'),
  (208, 'J0071', 'P0077', 'fee_revenue', 'credit', 54, 'USD', '2026-07-02 14:15:03+00'),
  (209, 'J0072', 'P0060', 'merchant_payable', 'debit', 30000, 'USD', '2026-07-02 15:30:00+00'),
  (210, 'J0072', 'P0060', 'processor_receivable', 'credit', 30000, 'USD', '2026-07-02 15:30:00+00'),
  (211, 'J0073', 'P0078', 'processor_receivable', 'debit', 5500, 'USD', '2026-07-02 16:40:15+00'),
  (212, 'J0073', 'P0078', 'merchant_payable', 'credit', 5335, 'USD', '2026-07-02 16:40:15+00'),
  (213, 'J0073', 'P0078', 'fee_revenue', 'credit', 165, 'USD', '2026-07-02 16:40:15+00'),
  (214, 'J0074', 'P0079', 'processor_receivable', 'debit', 2000, 'USD', '2026-07-02 23:20:03+00'),
  (215, 'J0074', 'P0079', 'merchant_payable', 'credit', 1940, 'USD', '2026-07-02 23:20:03+00'),
  (216, 'J0074', 'P0079', 'fee_revenue', 'credit', 60, 'USD', '2026-07-02 23:20:03+00'),
  (217, 'J0075', 'P0076', 'processor_receivable', 'debit', 60000, 'USD', '2026-07-03 09:00:00+00'),
  (218, 'J0075', 'P0076', 'merchant_payable', 'credit', 58200, 'USD', '2026-07-03 09:00:00+00'),
  (219, 'J0075', 'P0076', 'fee_revenue', 'credit', 1800, 'USD', '2026-07-03 09:00:00+00'),
  (220, 'J0076', 'P0080', 'processor_receivable', 'debit', 600, 'USD', '2026-07-03 13:05:47+00'),
  (221, 'J0076', 'P0080', 'merchant_payable', 'credit', 582, 'USD', '2026-07-03 13:05:47+00'),
  (222, 'J0076', 'P0080', 'fee_revenue', 'credit', 18, 'USD', '2026-07-03 13:05:47+00'),
  (223, 'J0077', 'P0082', 'processor_receivable', 'debit', 3400, 'USD', '2026-07-05 16:30:03+00'),
  (224, 'J0077', 'P0082', 'merchant_payable', 'credit', 3298, 'USD', '2026-07-05 16:30:03+00'),
  (225, 'J0077', 'P0082', 'fee_revenue', 'credit', 102, 'USD', '2026-07-05 16:30:03+00'),
  (226, 'J0078', 'P0060', 'merchant_payable', 'debit', 10000, 'USD', '2026-07-06 10:15:00+00'),
  (227, 'J0078', 'P0060', 'processor_receivable', 'credit', 10000, 'USD', '2026-07-06 10:15:00+00'),
  (228, 'J0079', 'P0083', 'processor_receivable', 'debit', 600, 'USD', '2026-07-06 12:06:12+00'),
  (229, 'J0079', 'P0083', 'merchant_payable', 'credit', 582, 'USD', '2026-07-06 12:06:12+00'),
  (230, 'J0079', 'P0083', 'fee_revenue', 'credit', 18, 'USD', '2026-07-06 12:06:12+00'),
  (231, 'J0080', 'P0084', 'processor_receivable', 'debit', 8800, 'USD', '2026-07-06 13:40:03+00'),
  (232, 'J0080', 'P0084', 'merchant_payable', 'credit', 8536, 'USD', '2026-07-06 13:40:03+00'),
  (233, 'J0080', 'P0084', 'fee_revenue', 'credit', 264, 'USD', '2026-07-06 13:40:03+00'),
  (234, 'J0081', 'P0085', 'processor_receivable', 'debit', 3100, 'USD', '2026-07-06 17:25:43+00'),
  (235, 'J0081', 'P0085', 'merchant_payable', 'credit', 3007, 'USD', '2026-07-06 17:25:43+00'),
  (236, 'J0081', 'P0085', 'fee_revenue', 'credit', 93, 'USD', '2026-07-06 17:25:43+00'),
  (237, 'J0082', 'P0086', 'processor_receivable', 'debit', 2500, 'USD', '2026-07-06 23:03:03+00'),
  (238, 'J0082', 'P0086', 'merchant_payable', 'credit', 2425, 'USD', '2026-07-06 23:03:03+00'),
  (239, 'J0082', 'P0086', 'fee_revenue', 'credit', 75, 'USD', '2026-07-06 23:03:03+00'),
  (240, 'J0083', 'P0087', 'processor_receivable', 'debit', 800, 'USD', '2026-07-07 12:09:03+00'),
  (241, 'J0083', 'P0087', 'merchant_payable', 'credit', 776, 'USD', '2026-07-07 12:09:03+00'),
  (242, 'J0083', 'P0087', 'fee_revenue', 'credit', 24, 'USD', '2026-07-07 12:09:03+00'),
  (243, 'J0084', 'P0088', 'processor_receivable', 'debit', 5600, 'USD', '2026-07-07 15:20:03+00'),
  (244, 'J0084', 'P0088', 'merchant_payable', 'credit', 5432, 'USD', '2026-07-07 15:20:03+00'),
  (245, 'J0084', 'P0088', 'fee_revenue', 'credit', 168, 'USD', '2026-07-07 15:20:03+00'),
  (246, 'J0085', 'P0090', 'processor_receivable', 'debit', 600, 'USD', '2026-07-08 12:04:39+00'),
  (247, 'J0085', 'P0090', 'merchant_payable', 'credit', 582, 'USD', '2026-07-08 12:04:39+00'),
  (248, 'J0085', 'P0090', 'fee_revenue', 'credit', 18, 'USD', '2026-07-08 12:04:39+00'),
  (249, 'J0086', 'P0092', 'processor_receivable', 'debit', 320000, 'USD', '2026-07-08 20:45:03+00'),
  (250, 'J0086', 'P0092', 'merchant_payable', 'credit', 310400, 'USD', '2026-07-08 20:45:03+00'),
  (251, 'J0086', 'P0092', 'fee_revenue', 'credit', 9600, 'USD', '2026-07-08 20:45:03+00'),
  (252, 'J0087', 'P0095', 'processor_receivable', 'debit', 2000, 'USD', '2026-07-09 03:09:05+00'),
  (253, 'J0087', 'P0095', 'merchant_payable', 'credit', 1940, 'USD', '2026-07-09 03:09:05+00'),
  (254, 'J0087', 'P0095', 'fee_revenue', 'credit', 60, 'USD', '2026-07-09 03:09:05+00'),
  (255, 'J0088', 'P0097', 'processor_receivable', 'debit', 2000, 'USD', '2026-07-09 03:21:18+00'),
  (256, 'J0088', 'P0097', 'merchant_payable', 'credit', 1940, 'USD', '2026-07-09 03:21:18+00'),
  (257, 'J0088', 'P0097', 'fee_revenue', 'credit', 60, 'USD', '2026-07-09 03:21:18+00'),
  (258, 'J0089', 'P0091', 'processor_receivable', 'debit', 38000, 'USD', '2026-07-09 09:00:00+00'),
  (259, 'J0089', 'P0091', 'merchant_payable', 'credit', 36860, 'USD', '2026-07-09 09:00:00+00'),
  (260, 'J0089', 'P0091', 'fee_revenue', 'credit', 1140, 'USD', '2026-07-09 09:00:00+00'),
  (261, 'J0090', 'P0099', 'processor_receivable', 'debit', 600, 'USD', '2026-07-09 12:10:03+00'),
  (262, 'J0090', 'P0099', 'merchant_payable', 'credit', 582, 'USD', '2026-07-09 12:10:03+00'),
  (263, 'J0090', 'P0099', 'fee_revenue', 'credit', 18, 'USD', '2026-07-09 12:10:03+00'),
  (264, 'J0091', 'P0100', 'processor_receivable', 'debit', 4800, 'USD', '2026-07-09 16:15:03+00'),
  (265, 'J0091', 'P0100', 'merchant_payable', 'credit', 4656, 'USD', '2026-07-09 16:15:03+00'),
  (266, 'J0091', 'P0100', 'fee_revenue', 'credit', 144, 'USD', '2026-07-09 16:15:03+00'),
  (267, 'J0092', 'P0095', 'merchant_payable', 'debit', 2000, 'USD', '2026-07-10 09:00:00+00'),
  (268, 'J0092', 'P0095', 'processor_receivable', 'credit', 2000, 'USD', '2026-07-10 09:00:00+00'),
  (269, 'J0093', 'P0101', 'processor_receivable', 'debit', 2800, 'GBP', '2026-07-10 13:20:03+00'),
  (270, 'J0093', 'P0101', 'merchant_payable', 'credit', 2716, 'GBP', '2026-07-10 13:20:03+00'),
  (271, 'J0093', 'P0101', 'fee_revenue', 'credit', 84, 'GBP', '2026-07-10 13:20:03+00'),
  (272, 'J0094', 'P0102', 'processor_receivable', 'debit', 4100, 'USD', '2026-07-10 18:30:03+00'),
  (273, 'J0094', 'P0102', 'merchant_payable', 'credit', 3977, 'USD', '2026-07-10 18:30:03+00'),
  (274, 'J0094', 'P0102', 'fee_revenue', 'credit', 123, 'USD', '2026-07-10 18:30:03+00'),
  (275, 'J0095', 'P0104', 'processor_receivable', 'debit', 1000, 'USD', '2026-07-11 02:40:03+00'),
  (276, 'J0095', 'P0104', 'merchant_payable', 'credit', 970, 'USD', '2026-07-11 02:40:03+00'),
  (277, 'J0095', 'P0104', 'fee_revenue', 'credit', 30, 'USD', '2026-07-11 02:40:03+00'),
  (278, 'J0096', 'P0106', 'processor_receivable', 'debit', 2200, 'USD', '2026-07-11 23:52:03+00'),
  (279, 'J0096', 'P0106', 'merchant_payable', 'credit', 2134, 'USD', '2026-07-11 23:52:03+00'),
  (280, 'J0096', 'P0106', 'fee_revenue', 'credit', 66, 'USD', '2026-07-11 23:52:03+00'),
  (281, 'J0097', 'P0107', 'processor_receivable', 'debit', 1300, 'USD', '2026-07-12 14:00:03+00'),
  (282, 'J0097', 'P0107', 'merchant_payable', 'credit', 1261, 'USD', '2026-07-12 14:00:03+00'),
  (283, 'J0097', 'P0107', 'fee_revenue', 'credit', 39, 'USD', '2026-07-12 14:00:03+00'),
  (284, 'J0098', 'P0109', 'processor_receivable', 'debit', 600, 'USD', '2026-07-13 12:05:03+00'),
  (285, 'J0098', 'P0109', 'merchant_payable', 'credit', 582, 'USD', '2026-07-13 12:05:03+00'),
  (286, 'J0098', 'P0109', 'fee_revenue', 'credit', 18, 'USD', '2026-07-13 12:05:03+00'),
  (287, 'J0099', 'P0110', 'processor_receivable', 'debit', 1500, 'GBP', '2026-07-13 13:10:03+00'),
  (288, 'J0099', 'P0110', 'merchant_payable', 'credit', 1455, 'GBP', '2026-07-13 13:10:03+00'),
  (289, 'J0099', 'P0110', 'fee_revenue', 'credit', 45, 'GBP', '2026-07-13 13:10:03+00'),
  (290, 'J0100', 'P0111', 'processor_receivable', 'debit', 6400, 'USD', '2026-07-13 14:12:08+00'),
  (291, 'J0100', 'P0111', 'merchant_payable', 'credit', 6208, 'USD', '2026-07-13 14:12:08+00'),
  (292, 'J0100', 'P0111', 'fee_revenue', 'credit', 192, 'USD', '2026-07-13 14:12:08+00'),
  (293, 'J0101', 'P0117', 'processor_receivable', 'debit', 900, 'USD', '2026-07-13 15:05:03+00'),
  (294, 'J0101', 'P0117', 'merchant_payable', 'credit', 873, 'USD', '2026-07-13 15:05:03+00'),
  (295, 'J0101', 'P0117', 'fee_revenue', 'credit', 27, 'USD', '2026-07-13 15:05:03+00'),
  (296, 'J0102', 'P0114', 'processor_receivable', 'debit', 2800, 'USD', '2026-07-13 16:10:30+00'),
  (297, 'J0102', 'P0114', 'merchant_payable', 'credit', 2716, 'USD', '2026-07-13 16:10:30+00'),
  (298, 'J0102', 'P0114', 'fee_revenue', 'credit', 84, 'USD', '2026-07-13 16:10:30+00'),
  (299, 'J0103', 'P0121', 'processor_receivable', 'debit', 1700, 'USD', '2026-07-13 16:20:03+00'),
  (300, 'J0103', 'P0121', 'merchant_payable', 'credit', 1649, 'USD', '2026-07-13 16:20:03+00'),
  (301, 'J0103', 'P0121', 'fee_revenue', 'credit', 51, 'USD', '2026-07-13 16:20:03+00'),
  (302, 'J0104', 'P0122', 'processor_receivable', 'debit', 2100, 'USD', '2026-07-13 17:30:03+00'),
  (303, 'J0104', 'P0122', 'merchant_payable', 'credit', 2037, 'USD', '2026-07-13 17:30:03+00'),
  (304, 'J0104', 'P0122', 'fee_revenue', 'credit', 63, 'USD', '2026-07-13 17:30:03+00'),
  (305, 'J0105', 'P0123', 'processor_receivable', 'debit', 2500, 'USD', '2026-07-13 23:05:03+00'),
  (306, 'J0105', 'P0123', 'merchant_payable', 'credit', 2425, 'USD', '2026-07-13 23:05:03+00'),
  (307, 'J0105', 'P0123', 'fee_revenue', 'credit', 75, 'USD', '2026-07-13 23:05:03+00');

INSERT INTO settlement_lines
  (line_id, file_date, payment_id, gross_minor, currency)
VALUES
  ('S001', '2026-07-02', 'P0072', 15000, 'USD'),
  ('S002', '2026-07-02', 'P0073', 4500, 'USD'),
  ('S003', '2026-07-02', 'P0074', 6000, 'USD'),
  ('S004', '2026-07-02', 'P0075', 800, 'USD'),
  ('S005', '2026-07-03', 'P0077', 1800, 'USD'),
  ('S006', '2026-07-03', 'P0078', 5500, 'USD'),
  ('S007', '2026-07-03', 'P0079', 2000, 'USD'),
  ('S008', '2026-07-04', 'P0076', 60000, 'USD'),
  ('S009', '2026-07-04', 'P0080', 600, 'USD'),
  ('S010', '2026-07-06', 'P0082', 3400, 'USD'),
  ('S011', '2026-07-07', 'P0083', 600, 'USD'),
  ('S012', '2026-07-07', 'P0084', 8080, 'USD'),
  ('S013', '2026-07-07', 'P0085', 3100, 'USD'),
  ('S014', '2026-07-07', 'P0086', 2500, 'USD'),
  ('S015', '2026-07-08', 'P0087', 800, 'USD'),
  ('S016', '2026-07-09', 'P0090', 600, 'USD'),
  ('S017', '2026-07-09', 'P0092', 320000, 'USD'),
  ('S018', '2026-07-10', 'P0091', 38000, 'USD'),
  ('S019', '2026-07-10', 'P0095', 2000, 'USD'),
  ('S020', '2026-07-10', 'P0097', 2000, 'USD'),
  ('S021', '2026-07-10', 'P0099', 600, 'USD'),
  ('S022', '2026-07-10', 'P0100', 4800, 'USD'),
  ('S023', '2026-07-10', 'P0100', 4800, 'USD'),
  ('S024', '2026-07-11', 'P0101', 2800, 'GBP'),
  ('S025', '2026-07-11', 'P0102', 4100, 'USD'),
  ('S026', '2026-07-11', 'P0103', 9500, 'USD'),
  ('S027', '2026-07-12', 'P0104', 1000, 'USD'),
  ('S028', '2026-07-13', 'P0106', 2200, 'USD'),
  ('S029', '2026-07-13', 'P0107', 1300, 'USD');

INSERT INTO merchant_events
  (event_id, merchant_id, event_name, event_at)
VALUES
  ('E001', 'M07', 'kyb_approved', '2026-03-30 12:00:00+00'),
  ('E002', 'M01', 'started', '2026-04-06 14:00:00+00'),
  ('E003', 'M01', 'kyb_submitted', '2026-04-07 10:00:00+00'),
  ('E004', 'M02', 'started', '2026-04-07 15:30:00+00'),
  ('E005', 'M02', 'kyb_submitted', '2026-04-08 11:00:00+00'),
  ('E006', 'M01', 'kyb_approved', '2026-04-08 15:00:00+00'),
  ('E007', 'M02', 'kyb_approved', '2026-04-10 14:00:00+00'),
  ('E008', 'M05', 'started', '2026-04-13 16:00:00+00'),
  ('E009', 'M05', 'started', '2026-04-13 16:00:00+00'),
  ('E010', 'M05', 'kyb_submitted', '2026-04-13 18:00:00+00'),
  ('E011', 'M05', 'kyb_approved', '2026-04-14 17:00:00+00'),
  ('E012', 'M01', 'first_payment', '2026-04-15 16:20:00+00'),
  ('E013', 'M05', 'first_payment', '2026-04-16 12:30:00+00'),
  ('E014', 'M07', 'started', '2026-04-20 15:00:00+00'),
  ('E015', 'M02', 'first_payment', '2026-04-20 18:05:00+00'),
  ('E016', 'M07', 'kyb_submitted', '2026-04-22 09:00:00+00'),
  ('E017', 'M07', 'kyb_approved', '2026-04-27 18:00:00+00'),
  ('E018', 'M03', 'started', '2026-05-04 13:00:00+00'),
  ('E019', 'M03', 'kyb_submitted', '2026-05-05 09:30:00+00'),
  ('E020', 'M03', 'kyb_approved', '2026-05-06 16:30:00+00'),
  ('E021', 'M04', 'started', '2026-05-11 14:45:00+00'),
  ('E022', 'M03', 'first_payment', '2026-05-12 20:10:00+00'),
  ('E023', 'M04', 'kyb_submitted', '2026-05-13 10:00:00+00'),
  ('E024', 'M04', 'kyb_approved', '2026-05-15 13:00:00+00'),
  ('E025', 'M06', 'started', '2026-05-18 13:20:00+00'),
  ('E026', 'M06', 'kyb_submitted', '2026-05-19 15:00:00+00'),
  ('E027', 'M06', 'kyb_approved', '2026-05-20 15:00:00+00'),
  ('E028', 'M09', 'started', '2026-05-26 17:00:00+00'),
  ('E029', 'M09', 'kyb_submitted', '2026-05-26 19:30:00+00'),
  ('E030', 'M09', 'kyb_approved', '2026-05-27 19:00:00+00'),
  ('E031', 'M07', 'first_payment', '2026-05-28 23:05:00+00'),
  ('E032', 'M04', 'first_payment', '2026-05-30 15:00:00+00'),
  ('E033', 'M08', 'started', '2026-06-01 09:00:00+00'),
  ('E034', 'M09', 'first_payment', '2026-06-01 13:20:05+00'),
  ('E035', 'M08', 'kyb_submitted', '2026-06-02 11:00:00+00'),
  ('E036', 'M06', 'first_payment', '2026-06-02 16:30:00+00'),
  ('E037', 'M08', 'kyb_approved', '2026-06-03 10:00:00+00'),
  ('E038', 'M08', 'first_payment', '2026-06-08 09:30:00+00'),
  ('E039', 'M10', 'started', '2026-06-15 14:00:00+00'),
  ('E040', 'M10', 'kyb_submitted', '2026-06-16 10:00:00+00'),
  ('E041', 'M10', 'kyb_approved', '2026-06-18 14:00:00+00'),
  ('E042', 'M10', 'first_payment', '2026-07-02 14:15:00+00'),
  ('E043', 'M11', 'started', '2026-07-06 15:00:00+00'),
  ('E044', 'M11', 'kyb_submitted', '2026-07-07 09:00:00+00'),
  ('E045', 'M11', 'kyb_approved', '2026-07-08 16:00:00+00'),
  ('E046', 'M12', 'started', '2026-07-09 13:30:00+00'),
  ('E047', 'M12', 'kyb_submitted', '2026-07-10 11:00:00+00');

INSERT INTO experiment_assignments
  (experiment_key, payment_id, variant, assigned_at)
VALUES
  ('checkout_v2', 'P0047', 'control', '2026-06-22 12:03:58+00'),
  ('checkout_v2', 'P0048', 'treatment', '2026-06-22 13:15:00+00'),
  ('checkout_v2', 'P0049', 'treatment', '2026-06-22 18:20:14+00'),
  ('checkout_v2', 'P0050', 'control', '2026-06-22 23:02:00+00'),
  ('checkout_v2', 'P0051', 'control', '2026-06-23 12:12:20+00'),
  ('checkout_v2', 'P0052', 'treatment', '2026-06-23 15:50:00+00'),
  ('checkout_v2', 'P0053', 'treatment', '2026-06-23 19:00:00+00'),
  ('checkout_v2', 'P0054', 'control', '2026-06-24 12:07:03+00'),
  ('checkout_v2', 'P0055', 'control', '2026-06-24 17:35:42+00'),
  ('checkout_v2', 'P0056', 'treatment', '2026-06-24 20:10:00+00'),
  ('checkout_v2', 'P0057', 'treatment', '2026-06-25 14:40:00+00'),
  ('checkout_v2', 'P0058', 'control', '2026-06-25 16:05:10+00'),
  ('checkout_v2', 'P0059', 'control', '2026-06-26 13:10:00+00'),
  ('checkout_v2', 'P0060', 'treatment', '2026-06-26 21:30:00+00'),
  ('checkout_v2', 'P0061', 'treatment', '2026-06-27 15:15:22+00'),
  ('checkout_v2', 'P0062', 'control', '2026-06-27 18:00:00+00'),
  ('checkout_v2', 'P0063', 'control', '2026-06-28 23:55:10+00'),
  ('checkout_v2', 'P0064', 'treatment', '2026-06-29 12:05:00+00'),
  ('checkout_v2', 'P0065', 'treatment', '2026-06-29 14:20:30+00'),
  ('checkout_v2', 'P0066', 'control', '2026-06-29 16:45:00+00'),
  ('checkout_v2', 'P0067', 'control', '2026-06-29 19:30:11+00'),
  ('checkout_v2', 'P0068', 'treatment', '2026-06-29 23:04:00+00'),
  ('checkout_v2', 'P0069', 'treatment', '2026-06-30 12:10:15+00'),
  ('checkout_v2', 'P0070', 'control', '2026-06-30 17:20:00+00'),
  ('checkout_v2', 'P0071', 'control', '2026-06-30 20:00:00+00'),
  ('checkout_v2', 'P0072', 'treatment', '2026-07-01 00:00:00+00'),
  ('checkout_v2', 'P0073', 'treatment', '2026-07-01 01:10:45+00'),
  ('checkout_v2', 'P0074', 'control', '2026-07-01 02:15:00+00'),
  ('checkout_v2', 'P0075', 'control', '2026-07-01 12:08:30+00'),
  ('checkout_v2', 'P0076', 'treatment', '2026-07-01 15:00:00+00'),
  ('checkout_v2', 'P0077', 'treatment', '2026-07-02 14:15:00+00'),
  ('checkout_v2', 'P0078', 'control', '2026-07-02 16:40:12+00'),
  ('checkout_v2', 'P0079', 'control', '2026-07-02 23:20:00+00'),
  ('checkout_v2', 'P0080', 'treatment', '2026-07-03 13:05:44+00'),
  ('checkout_v2', 'P0081', 'treatment', '2026-07-03 18:50:00+00'),
  ('checkout_v2', 'P0082', 'control', '2026-07-05 16:30:00+00'),
  ('checkout_v2', 'P0083', 'control', '2026-07-06 12:06:09+00'),
  ('checkout_v2', 'P0084', 'treatment', '2026-07-06 13:40:00+00'),
  ('checkout_v2', 'P0084', 'control', '2026-07-06 13:40:02+00'),
  ('checkout_v2', 'P0085', 'treatment', '2026-07-06 17:10:25+00'),
  ('checkout_v2', 'P0086', 'control', '2026-07-06 23:03:00+00'),
  ('checkout_v2', 'P0087', 'control', '2026-07-07 12:09:00+00'),
  ('checkout_v2', 'P0088', 'treatment', '2026-07-07 15:20:00+00'),
  ('checkout_v2', 'P0089', 'treatment', '2026-07-07 19:00:00+00'),
  ('checkout_v2', 'P0090', 'control', '2026-07-08 12:04:36+00'),
  ('checkout_v2', 'P0091', 'control', '2026-07-08 14:30:00+00'),
  ('checkout_v2', 'P0092', 'treatment', '2026-07-08 20:45:00+00'),
  ('checkout_v2', 'P0093', 'control', '2026-07-09 03:02:10+00'),
  ('checkout_v2', 'P0094', 'control', '2026-07-09 03:05:44+00'),
  ('checkout_v2', 'P0095', 'treatment', '2026-07-09 03:09:02+00'),
  ('checkout_v2', 'P0096', 'control', '2026-07-09 03:14:30+00'),
  ('checkout_v2', 'P0097', 'treatment', '2026-07-09 03:21:15+00'),
  ('checkout_v2', 'P0098', 'control', '2026-07-09 03:40:00+00'),
  ('checkout_v2', 'P0099', 'treatment', '2026-07-09 12:10:00+00'),
  ('checkout_v2', 'P0100', 'control', '2026-07-09 16:15:00+00'),
  ('checkout_v2', 'P0101', 'control', '2026-07-10 13:20:00+00'),
  ('checkout_v2', 'P0102', 'treatment', '2026-07-10 18:30:00+00'),
  ('checkout_v2', 'P0103', 'treatment', '2026-07-10 21:00:00+00'),
  ('checkout_v2', 'P0104', 'control', '2026-07-11 02:40:00+00'),
  ('checkout_v2', 'P0105', 'control', '2026-07-11 15:10:00+00'),
  ('checkout_v2', 'P0106', 'treatment', '2026-07-11 23:52:00+00'),
  ('checkout_v2', 'P0107', 'treatment', '2026-07-12 14:00:00+00'),
  ('checkout_v2', 'P0108', 'control', '2026-07-12 19:20:00+00');

INSERT INTO ai_events
  (event_id, occurred_at, payload)
VALUES
  ('AE01', '2026-07-06 14:02:00+00',
   '{"schema_version": 1, "model": "pf-analyst-small", "latency_ms": 820, "prompt_tokens": 410, "completion_tokens": 62, "user_role": "analyst", "question": "Daily captured revenue last week", "tags": ["revenue", "daily"], "rows_returned": 7}'),
  ('AE02', '2026-07-06 14:10:00+00',
   '{"schema_version": 1, "model": "pf-analyst-small", "latency_ms": 640, "prompt_tokens": 388, "completion_tokens": 51, "user_role": "analyst", "question": "List refunds in June", "tags": ["refunds"], "rows_returned": 5}'),
  ('AE03', '2026-07-07 09:30:00+00',
   '{"schema_version": 1, "model": "pf-analyst-large", "latency_ms": 2310, "prompt_tokens": 905, "completion_tokens": 188, "user_role": "pm", "question": "Weekly retention by signup cohort", "tags": ["cohort", "retention"], "rows_returned": 6}'),
  ('AE04', '2026-07-07 16:45:00+00',
   '{"schema_version": 1, "model": "pf-analyst-small", "latency_ms": "1200", "prompt_tokens": 402, "completion_tokens": 70, "user_role": "analyst", "question": "Top merchants by volume", "tags": ["revenue", "merchants"], "rows_returned": 10}'),
  ('AE05', '2026-07-08 11:20:00+00',
   '{"schema_version": 1, "latency_ms": 700, "prompt_tokens": 350, "completion_tokens": 44, "user_role": "support", "question": "Status of payment P0101", "tags": ["lookup"], "rows_returned": 1}'),
  ('AE06', '2026-07-08 15:05:00+00',
   '{"schema_version": 1, "model": "pf-analyst-large", "latency_ms": 3100, "prompt_tokens": 620, "completion_tokens": 95, "user_role": "support", "question": "Delete the test payments", "tags": ["admin"], "blocked": true, "block_reason": "write_statement", "rows_returned": 0}'),
  ('AE07', '2026-07-09 10:00:00+00',
   '{"schema_version": 2, "model": "pf-analyst-large", "latency_ms": 1850, "usage": {"input_tokens": 980, "output_tokens": 140}, "user_role": "risk", "question": "Attempts per device in the last hour", "tags": ["fraud", "velocity"], "rows_returned": 6}'),
  ('AE08', '2026-07-10 13:15:00+00',
   '{"schema_version": 2, "model": "pf-analyst-small", "latency_ms": 540, "usage": {"input_tokens": 455, "output_tokens": 88}, "user_role": "pm", "question": "Net revenue by merchant for June", "tags": ["revenue", "refunds"], "rows_returned": 9, "sql": "SELECT m.merchant_name, SUM(p.amount_minor) - SUM(r.amount_minor) AS net_revenue FROM payments p JOIN merchants m ON m.merchant_id = p.merchant_id LEFT JOIN refunds r ON r.payment_id = p.payment_id WHERE p.created_at BETWEEN ''2026-06-01'' AND ''2026-06-30'' GROUP BY m.merchant_name ORDER BY net_revenue DESC, m.merchant_name"}'),
  ('AE09', '2026-07-10 17:40:00+00',
   '{"schema_version": 2, "model": "pf-analyst-large", "latency_ms": 2750, "usage": {"input_tokens": 1210, "output_tokens": 230}, "user_role": "finance", "question": "Settlement lines without a captured payment", "tags": ["reconciliation", "settlement"], "rows_returned": 1}'),
  ('AE10', '2026-07-13 14:20:00+00',
   '{"schema_version": 2, "model": "pf-analyst-small", "latency_ms": 610, "usage": {"input_tokens": 430, "output_tokens": 75}, "user_role": "pm", "question": "Failure rate by method today", "tags": ["failures", "incident"], "rows_returned": 3}'),
  ('AE11', '2026-07-13 14:41:00+00',
   '{"schema_version": 2, "model": "pf-analyst-large", "latency_ms": 4200, "usage": {"input_tokens": 1500, "output_tokens": 310}, "user_role": "pm", "question": "Card failures by hour and failure code today", "tags": ["failures", "incident", "hourly"], "rows_returned": 8}'),
  ('AE12', '2026-07-13 15:02:00+00',
   '{"schema_version": 2, "model": "pf-analyst-small", "latency_ms": 580, "usage": {"input_tokens": 410, "output_tokens": 66}, "user_role": "support", "question": "Is checkout down?", "tags": ["failures"], "rows_returned": null}');

INSERT INTO payment_commands
  (command_id, merchant_id, idempotency_key, payload_hash, status, created_at, last_seen_at)
VALUES
  ('CMD-0001', 'M02', 'ord-88121', md5('amount=6400&currency=USD&customer=C04'), 'completed',
   '2026-07-13 14:05:12+00', '2026-07-13 14:12:05+00'),
  ('CMD-0002', 'M03', 'ord-55310', md5('amount=3000&currency=USD&customer=C16'), 'failed',
   '2026-07-13 14:20:00+00', '2026-07-13 14:22:18+00'),
  ('CMD-0003', 'M06', 'ord-20977', md5('amount=2800&currency=USD&customer=C11'), 'completed',
   '2026-07-13 14:35:00+00', '2026-07-13 16:10:27+00'),
  ('CMD-0004', 'M06', 'ord-88121', md5('amount=1700&currency=USD&customer=C14'), 'completed',
   '2026-07-13 15:50:00+00', '2026-07-13 16:20:00+00');

-- 20,000 synthetic attempts, one every three minutes, spread over 200 merchants.
-- Built with arithmetic only (no random()), so it is identical on every load.
INSERT INTO attempts_big (attempt_id, merchant_id, attempted_at, amount_minor, method, status)
SELECT g,
       'B' || lpad(((g * 7) % 200 + 1)::text, 3, '0'),
       TIMESTAMPTZ '2026-06-01 00:00:00+00' + g * INTERVAL '3 minutes',
       500 + (g * 37) % 9500,
       CASE WHEN g % 5 = 0 THEN 'wallet' ELSE 'card' END,
       CASE WHEN g % 10 = 3 THEN 'failed' ELSE 'succeeded' END
FROM generate_series(1, 20000) AS g;

ANALYZE;

-- Quick confirmation: row counts per table.
SELECT 'merchants' AS table_name, COUNT(*) AS row_count FROM merchants
UNION ALL SELECT 'customers', COUNT(*) FROM customers
UNION ALL SELECT 'payments', COUNT(*) FROM payments
UNION ALL SELECT 'payment_attempts', COUNT(*) FROM payment_attempts
UNION ALL SELECT 'refunds', COUNT(*) FROM refunds
UNION ALL SELECT 'disputes', COUNT(*) FROM disputes
UNION ALL SELECT 'ledger_entries', COUNT(*) FROM ledger_entries
UNION ALL SELECT 'settlement_lines', COUNT(*) FROM settlement_lines
UNION ALL SELECT 'merchant_events', COUNT(*) FROM merchant_events
UNION ALL SELECT 'experiment_assignments', COUNT(*) FROM experiment_assignments
UNION ALL SELECT 'ai_events', COUNT(*) FROM ai_events
UNION ALL SELECT 'payment_commands', COUNT(*) FROM payment_commands
UNION ALL SELECT 'attempts_big', COUNT(*) FROM attempts_big;
