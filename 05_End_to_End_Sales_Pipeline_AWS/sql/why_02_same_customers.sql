-- Hold customer identity constant to distinguish composition from behaviour.
-- Selection: customers with positive merchandise purchases in BOTH months.
WITH cm AS (
 SELECT customer_id, invoice_month, COUNT(DISTINCT invoice_no) AS invoices,
        SUM(quantity) AS units, SUM(line_value_gbp) AS positive_value_gbp
 FROM cjb_retail.retail_transactions
 WHERE regexp_like(stock_code, '^[0-9]{5}[A-Za-z]*$')
   AND quantity>0 AND unit_price_gbp>0 AND customer_id IS NOT NULL
   AND invoice_month IN ('2011-10','2011-11')
 GROUP BY 1,2
), both_months AS (
 SELECT customer_id FROM cm GROUP BY 1 HAVING COUNT(*)=2
)
SELECT invoice_month, COUNT(*) AS same_customers, SUM(invoices) AS invoices,
 SUM(positive_value_gbp) AS positive_value_gbp,
 SUM(positive_value_gbp)/SUM(invoices) AS value_per_invoice_gbp,
 CAST(SUM(units) AS double)/SUM(invoices) AS units_per_invoice
FROM cm JOIN both_months USING(customer_id) GROUP BY 1 ORDER BY 1;
