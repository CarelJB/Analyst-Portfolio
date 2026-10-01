-- Establish whether the two largest identified buyers were unusual on Nov 23.
-- Full observed history; retain negative lines for net-value interpretation.
SELECT customer_id, CAST(invoice_date AS date) AS purchase_date,
 COUNT(DISTINCT CASE WHEN quantity>0 AND unit_price_gbp>0 THEN invoice_no END) AS positive_invoices,
 SUM(CASE WHEN quantity>0 AND unit_price_gbp>0 THEN quantity ELSE 0 END) AS positive_units,
 SUM(CASE WHEN quantity>0 AND unit_price_gbp>0 THEN line_value_gbp ELSE 0 END) AS positive_value_gbp,
 SUM(line_value_gbp) AS net_value_gbp
FROM cjb_retail.retail_transactions
WHERE customer_id IN ('14088','14646')
 AND regexp_like(stock_code,'^[0-9]{5}[A-Za-z]*$')
GROUP BY customer_id,CAST(invoice_date AS date)
ORDER BY customer_id,purchase_date;
