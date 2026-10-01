-- Largest invoices behind 23 November's positive merchandise value.
WITH invoices AS (
 SELECT invoice_no, MIN(invoice_date) AS first_line_time,
   MAX(customer_id) AS customer_id, COUNT(DISTINCT customer_id) AS identified_ids,
   MIN(country) AS country, COUNT(DISTINCT country) AS countries,
   COUNT(*) AS positive_lines, COUNT(DISTINCT stock_code) AS products,
   SUM(quantity) AS units, SUM(line_value_gbp) AS positive_value_gbp,
   SUM(CASE WHEN regexp_like(upper(description),'CHRISTMAS|XMAS')
       THEN line_value_gbp ELSE 0 END) AS explicitly_christmas_value_gbp,
   SUM(CASE WHEN duplicate_candidate THEN line_value_gbp ELSE 0 END) AS duplicate_candidate_value_gbp
 FROM cjb_retail.retail_transactions
 WHERE invoice_date>=TIMESTAMP '2011-11-23 00:00:00'
   AND invoice_date<TIMESTAMP '2011-11-24 00:00:00'
   AND regexp_like(stock_code,'^[0-9]{5}[A-Za-z]*$')
   AND quantity>0 AND unit_price_gbp>0
 GROUP BY invoice_no
)
SELECT *, CAST(positive_value_gbp AS double)/SUM(positive_value_gbp) OVER()
 AS share_of_day_positive_value
FROM invoices ORDER BY positive_value_gbp DESC,invoice_no;
