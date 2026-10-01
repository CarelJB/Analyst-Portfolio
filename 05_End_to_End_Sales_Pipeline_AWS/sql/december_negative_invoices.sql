-- Investigate negative lines; totals below exclude positive lines on the same invoice.
-- Do not label these as refunds without evidence of settlement or original-sale linkage.
SELECT invoice_no,
       customer_id,
       country,
       transaction_type,
       COUNT(*) AS negative_lines,
       SUM(line_value_gbp) AS negative_value_gbp
FROM cjb_retail.retail_transactions
WHERE invoice_month = '2011-12'
  AND line_value_gbp < 0
GROUP BY invoice_no, customer_id, country, transaction_type
ORDER BY negative_value_gbp ASC
LIMIT 20;
