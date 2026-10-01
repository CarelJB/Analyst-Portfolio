-- All product lines on the two early-November bulk invoices.
-- Include negatives and non-merchandise codes to expose adjustments/fees.
SELECT invoice_no, stock_code, MIN(description) AS example_description,
       COUNT(*) AS source_lines, SUM(quantity) AS net_units,
       MIN(unit_price_gbp) AS min_unit_price_gbp,
       MAX(unit_price_gbp) AS max_unit_price_gbp,
       SUM(line_value_gbp) AS net_line_value_gbp,
       SUM(CASE WHEN duplicate_candidate THEN 1 ELSE 0 END) AS flagged_lines
FROM cjb_retail.retail_transactions
WHERE invoice_no IN ('574941','576365')
GROUP BY invoice_no,stock_code
ORDER BY invoice_no,net_line_value_gbp DESC,stock_code;
