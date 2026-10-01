-- Calendar includes zero-transaction days; compare like weekdays.
-- Black Friday 2011-11-25; US Cyber Monday 2011-11-28.
-- Event dates are reference markers, not a causal classification.
WITH calendar AS (
 SELECT day FROM UNNEST(sequence(DATE '2011-10-01',DATE '2011-12-09',INTERVAL '1' DAY)) AS t(day)
), daily AS (
 SELECT CAST(invoice_date AS date) AS day,
 COUNT(DISTINCT CASE WHEN quantity>0 AND unit_price_gbp>0 THEN invoice_no END) AS positive_invoices,
 SUM(CASE WHEN quantity>0 AND unit_price_gbp>0 THEN line_value_gbp ELSE 0 END) AS positive_value_gbp,
 SUM(line_value_gbp) AS net_value_gbp,
 SUM(CASE WHEN customer_id IS NULL AND quantity>0 AND unit_price_gbp>0 THEN line_value_gbp ELSE 0 END) AS unidentified_positive_gbp,
 SUM(CASE WHEN invoice_no IN ('574941','576365') AND quantity>0 AND unit_price_gbp>0 THEN line_value_gbp ELSE 0 END) AS two_bulk_invoices_gbp
 FROM cjb_retail.retail_transactions
 WHERE regexp_like(stock_code,'^[0-9]{5}[A-Za-z]*$')
 AND invoice_date>=TIMESTAMP '2011-10-01 00:00:00'
 AND invoice_date<TIMESTAMP '2011-12-10 00:00:00'
 GROUP BY 1
)
SELECT c.day, day_of_week(c.day) AS weekday_monday_is_1,
 COALESCE(d.positive_invoices,0) AS positive_invoices,
 COALESCE(d.positive_value_gbp,0) AS positive_value_gbp,
 COALESCE(d.net_value_gbp,0) AS net_value_gbp,
 COALESCE(d.unidentified_positive_gbp,0) AS unidentified_positive_gbp,
 COALESCE(d.two_bulk_invoices_gbp,0) AS two_bulk_invoices_gbp,
 COALESCE(d.positive_value_gbp,0)-COALESCE(d.two_bulk_invoices_gbp,0) AS positive_value_excluding_two_bulk_invoices_gbp
FROM calendar c LEFT JOIN daily d ON c.day=d.day
ORDER BY c.day;
