-- Run directly in Athena. Read-only, no additional views required.
-- Question: did positive merchandise value grow through customer count,
-- invoice frequency, or invoice size? Unknown customers form a separate group.
-- Merchandise classification is provisional; negatives remain in the source.
WITH positive_lines AS (
 SELECT * FROM cjb_retail.retail_transactions
 WHERE regexp_like(stock_code, '^[0-9]{5}[A-Za-z]*$')
   AND quantity > 0 AND unit_price_gbp > 0
), first_seen AS (
 SELECT customer_id, MIN(invoice_month) AS first_month
 FROM positive_lines WHERE customer_id IS NOT NULL GROUP BY customer_id
), grouped AS (
 SELECT p.invoice_month,
   CASE WHEN p.customer_id IS NULL THEN 'unidentified'
        WHEN f.first_month = p.invoice_month THEN 'first_observed_this_month'
        ELSE 'previously_observed' END AS customer_group,
   COUNT(DISTINCT p.customer_id) AS customers,
   COUNT(DISTINCT p.invoice_no) AS invoices,
   SUM(p.quantity) AS units,
   SUM(p.line_value_gbp) AS positive_value_gbp
 FROM positive_lines p LEFT JOIN first_seen f ON p.customer_id=f.customer_id
 WHERE p.invoice_month IN ('2011-10','2011-11')
 GROUP BY 1,2
)
SELECT *,
 CAST(invoices AS double) / NULLIF(customers,0) AS invoices_per_customer,
 positive_value_gbp / NULLIF(invoices,0) AS value_per_invoice_gbp,
 CAST(units AS double) / NULLIF(invoices,0) AS units_per_invoice,
 positive_value_gbp / NULLIF(units,0) AS value_per_unit_gbp
FROM grouped ORDER BY invoice_month,customer_group;
