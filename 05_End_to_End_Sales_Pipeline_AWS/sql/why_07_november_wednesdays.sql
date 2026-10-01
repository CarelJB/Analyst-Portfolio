-- Explain 23 November against other November Wednesdays (2,9,16,30).
-- Invoice value here includes positive merchandise lines only.
WITH lines AS (
 SELECT * FROM cjb_retail.retail_transactions
 WHERE invoice_date>=TIMESTAMP '2011-11-01 00:00:00'
   AND invoice_date<TIMESTAMP '2011-12-01 00:00:00'
   AND day_of_week(CAST(invoice_date AS date))=3
   AND regexp_like(stock_code,'^[0-9]{5}[A-Za-z]*$')
), positive_invoices AS (
 SELECT CAST(invoice_date AS date) AS day, invoice_no,
   SUM(line_value_gbp) AS value_gbp, SUM(quantity) AS units,
   COUNT(DISTINCT stock_code) AS products,
   MAX(customer_id) AS customer_id, MIN(country) AS country
 FROM lines WHERE quantity>0 AND unit_price_gbp>0
 GROUP BY 1,2
), ranked AS (
 SELECT *, ROW_NUMBER() OVER(PARTITION BY day ORDER BY value_gbp DESC,invoice_no) AS rank_in_day
 FROM positive_invoices
), negatives AS (
 SELECT CAST(invoice_date AS date) AS day,
        SUM(CASE WHEN line_value_gbp<0 THEN line_value_gbp ELSE 0 END) AS negative_value_gbp
 FROM lines GROUP BY 1
)
SELECT r.day, COUNT(*) AS positive_invoices,
 SUM(r.value_gbp) AS positive_value_gbp,
 SUM(r.value_gbp)/COUNT(*) AS value_per_invoice_gbp,
 SUM(r.units) AS units,
 COUNT(DISTINCT r.customer_id) AS identified_buyers,
 SUM(CASE WHEN r.customer_id IS NULL THEN r.value_gbp ELSE 0 END) AS unidentified_value_gbp,
 MAX(r.value_gbp) AS largest_invoice_gbp,
 SUM(CASE WHEN r.rank_in_day<=3 THEN r.value_gbp ELSE 0 END) AS top_three_value_gbp,
 SUM(CASE WHEN r.rank_in_day>3 THEN r.value_gbp ELSE 0 END) AS value_excluding_top_three_gbp,
 MAX(n.negative_value_gbp) AS negative_value_gbp,
 SUM(r.value_gbp)+MAX(n.negative_value_gbp) AS net_value_gbp
FROM ranked r JOIN negatives n ON r.day=n.day
GROUP BY r.day ORDER BY r.day;
