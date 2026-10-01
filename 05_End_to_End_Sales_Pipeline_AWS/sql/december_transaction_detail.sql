-- Inspect the largest negative entries and the corresponding positive candidate.
SELECT invoice_no, invoice_date, customer_id, stock_code, description,
       quantity, unit_price_gbp, line_value_gbp, transaction_type
FROM cjb_retail.retail_transactions
WHERE invoice_no IN ('581483', 'C581484', 'C580604', 'C580605')
ORDER BY invoice_date, invoice_no;
