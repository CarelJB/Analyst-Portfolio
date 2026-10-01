-- Days are distinct purchase dates: invoice splitting on a day adds no interval.
-- Illustrative rule, not proof of churn. Historical snapshot 10 December 2011.
WITH days AS (
 SELECT DISTINCT customer_id, CAST(invoice_date AS date) AS purchase_day
 FROM cjb_retail.retail_transactions
 WHERE regexp_like(stock_code,'^[0-9]{5}[A-Za-z]*$')
   AND quantity>0 AND unit_price_gbp>0 AND customer_id IS NOT NULL
), gaps AS (
 SELECT *, date_diff('day',LAG(purchase_day) OVER
   (PARTITION BY customer_id ORDER BY purchase_day),purchase_day) AS gap_days
 FROM days
), cadence AS (
 SELECT customer_id, COUNT(*) AS purchase_days, MAX(purchase_day) AS last_purchase,
   approx_percentile(gap_days,0.5) AS typical_gap_days,
   date_diff('day',MAX(purchase_day),DATE '2011-12-10') AS days_since_purchase
 FROM gaps GROUP BY 1
), net AS (
 SELECT customer_id,SUM(line_value_gbp) AS net_value_gbp
 FROM cjb_retail.retail_transactions
 WHERE regexp_like(stock_code,'^[0-9]{5}[A-Za-z]*$') AND customer_id IS NOT NULL
 GROUP BY 1
)
SELECT c.customer_id, c.purchase_days, c.last_purchase,
 c.typical_gap_days, c.days_since_purchase, n.net_value_gbp,
 CAST(days_since_purchase AS double)/NULLIF(typical_gap_days,0) AS usual_gap_multiple
FROM cadence c JOIN net n ON c.customer_id = n.customer_id
WHERE purchase_days>=3 AND net_value_gbp>=1000 AND days_since_purchase>=60
ORDER BY usual_gap_multiple DESC, net_value_gbp DESC;
