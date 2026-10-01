-- Inspect concentration and characteristics of the largest unidentified invoices.
-- Positive merchandise only, matching why_01. This is not net realised revenue.
WITH invoices AS (
 SELECT invoice_month, invoice_no, MIN(invoice_date) AS first_line_time,
        COUNT(DISTINCT country) AS country_count, MIN(country) AS country,
        COUNT(*) AS positive_lines, COUNT(DISTINCT stock_code) AS product_codes,
        SUM(quantity) AS units, SUM(line_value_gbp) AS positive_value_gbp,
        SUM(CASE WHEN duplicate_candidate THEN line_value_gbp ELSE 0 END)
          AS duplicate_candidate_value_gbp
 FROM cjb_retail.retail_transactions
 WHERE regexp_like(stock_code,'^[0-9]{5}[A-Za-z]*$')
   AND quantity>0 AND unit_price_gbp>0 AND customer_id IS NULL
   AND invoice_month IN ('2011-10','2011-11')
 GROUP BY 1,2
), ranked AS (
 SELECT *, ROW_NUMBER() OVER(PARTITION BY invoice_month
              ORDER BY positive_value_gbp DESC,invoice_no) AS invoice_rank,
        SUM(positive_value_gbp) OVER(PARTITION BY invoice_month) AS month_value_gbp
 FROM invoices
)
SELECT *, CAST(positive_value_gbp AS double)/NULLIF(month_value_gbp,0)
          AS share_of_unidentified_month_value
FROM ranked WHERE invoice_rank<=10
ORDER BY invoice_month,invoice_rank;
