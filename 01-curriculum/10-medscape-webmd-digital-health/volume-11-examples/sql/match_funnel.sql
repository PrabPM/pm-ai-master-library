-- One row per NPI on the client's target list. npi_valid() is a small
-- check-digit function the Python runner registers with SQLite.
SELECT
  COUNT(*)                                            AS on_client_list,
  SUM(npi_valid(t.npi))                               AS valid_npi,
  SUM(p.hcp_id IS NOT NULL)                           AS matched_member,
  SUM(p.verified = 1)                                 AS verified,
  SUM(p.verified = 1 AND p.consent_state = 'granted') AS consented,
  SUM(p.verified = 1 AND p.consent_state = 'granted'
      AND p.last_seen >= '2026-08-15')                AS reachable
FROM target_list t
LEFT JOIN hcp_profile p ON p.npi = t.npi;
