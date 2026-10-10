-- 26 of 84 flight days have run (September 14 to October 9, 2026).
SELECT
  li.line_item,
  li.budget,
  ROUND(li.budget * 26 / 84.0, 2)                 AS planned_to_date,
  ROUND(SUM(e.impressions) * li.cpm / 1000.0, 2)  AS spend_to_date
FROM line_item li
JOIN exposure e USING (line_item)
GROUP BY li.line_item
ORDER BY li.line_item;
