-- Run setup SQL first. Values are GBP, not ZAR. No profit/cost data is available.
-- 1. Reconcile these results to quality_report.json before interpreting the data.
SELECT COUNT(*) AS accepted_rows,
       SUM(line_value_gbp) AS net_line_value_gbp,
       SUM(CASE WHEN line_value_gbp > 0 THEN line_value_gbp ELSE 0 END) AS positive_value_gbp,
       SUM(CASE WHEN line_value_gbp < 0 THEN line_value_gbp ELSE 0 END) AS negative_value_gbp,
       COUNT(DISTINCT customer_id) AS known_customers
FROM cjb_retail.retail_transactions;

-- 2. Monthly trend. December 2011 is incomplete; do not compare it as a full month.
SELECT invoice_month, COUNT(*) AS line_count,
       SUM(line_value_gbp) AS net_line_value_gbp,
       SUM(CASE WHEN transaction_type = 'cancellation' THEN line_value_gbp ELSE 0 END) AS cancellation_value_gbp
FROM cjb_retail.retail_transactions GROUP BY 1 ORDER BY 1;

-- 3. Country contribution including unknown customers.
SELECT country, SUM(line_value_gbp) AS net_line_value_gbp,
       COUNT(DISTINCT customer_id) AS known_customers
FROM cjb_retail.retail_transactions GROUP BY 1 ORDER BY 2 DESC;

-- 4. Customer concentration applies only to identified customers.
SELECT customer_id, SUM(line_value_gbp) AS net_line_value_gbp
FROM cjb_retail.retail_transactions WHERE customer_id IS NOT NULL
GROUP BY 1 ORDER BY 2 DESC LIMIT 10;

-- 5. Sensitivity to duplicate candidates (not proof of duplicate errors).
SELECT duplicate_candidate, COUNT(*) AS rows, SUM(line_value_gbp) AS value_gbp
FROM cjb_retail.retail_transactions GROUP BY 1;

-- 6. Observe exceptional transaction types separately.
SELECT transaction_type, COUNT(*) AS rows, SUM(line_value_gbp) AS value_gbp
FROM cjb_retail.retail_transactions GROUP BY 1 ORDER BY 1;
