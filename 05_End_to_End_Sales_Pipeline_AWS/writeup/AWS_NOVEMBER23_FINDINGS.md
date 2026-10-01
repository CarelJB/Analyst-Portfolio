# Why did recorded value peak on 23 November?

Evidence: supplied Athena exports saved as `evidence/athena_november_wednesdays.csv` and `evidence/athena_november23_invoices.csv`. The 130 invoice rows reconcile exactly to GBP 76,241.63 positive merchandise value.

Compared with 16 November, both dates have 130 positive invoices, but value increased GBP 13,700.99 (21.9%). The top-three invoice totals increased from GBP 14,435.93 to GBP 24,386.16: that GBP 9,950.23 difference accounts arithmetically for 72.6% of the day-to-day increase. This compares each day's largest invoices, not the same buyers, and is not causal attribution.

The three leading invoices on 23 November were 578305 (customer 14088, UK, GBP 10,584.77, 2,111 units across 132 products), 578140 (customer 14646, Netherlands, GBP 7,952.68, 5,760 units across 42 products), and 578149 (unidentified, UK, GBP 5,848.71). Together they represent 32.0% of daily positive value. Customer 14646 also has invoice 578143 for GBP 1,835.96; account-level analysis must aggregate invoices before interpreting buying occasions.

Against the mean of the four other November Wednesdays, total value is 33.2% higher, invoice count 17.9% higher, and value excluding each day's three largest invoices is 18.1% higher. Thus the peak combines high invoice activity with large baskets, and is not entirely explained by three outliers. The prior-week comparison holds invoice count constant and shows the importance of invoice size.

Negative entries total GBP 745.22; net merchandise value remains GBP 75,496.41. Flagged duplicate-candidate positive value is GBP 257.18, small relative to the peak. Neither check establishes that later reversals are absent.

Explicit CHRISTMAS/XMAS descriptions account for GBP 7,135.38 (about 9.4%) of positive value. The two largest invoices have none under that keyword rule. This weakens a narrow explanation based solely on explicitly Christmas-labelled goods, but does not exclude gift purchasing or seasonal stocking of general products.

## Customer-history evidence

The subsequent supplied Athena export is retained as `evidence/athena_key_customer_history.csv`.

Customer 14088 recorded GBP 10,584.77 on 23 November, the largest positive purchasing-day value in its observed history, 20.3% above its previous maximum of GBP 8,801.51 on 19 July. It had other large purchasing days in January, June and October, so large orders were not unique to the holiday period. November positive value was GBP 16,851.61 versus GBP 8,132.31 in October. The 23 November quantity of 2,111 units was below the 2,565 units on 19 July: a monetary record is not necessarily a quantity record. Product/price mix remains relevant.

Customer 14646 recorded THREE positive invoices totalling GBP 10,078.64 and 7,244 units on 23 November. The earlier discussion mentioned only its two larger invoices; the daily aggregate includes a further GBP 290.00. Nine earlier purchasing days had higher positive value, including GBP 25,833.56 on 20 October. November total was GBP 25,225.41, below October's GBP 39,740.95. The event-day amount is therefore within this customer's previously observed range, rather than evidence of an exceptional holiday surge. This does not prove routine replenishment or the reason for purchase.

Together the customers account for GBP 20,663.41, or 27.1% of 23 November's positive merchandise value. The best supported explanation is a busy day coinciding with large purchases by established customers: one account's highest observed value day and another account's non-record bulk buying. Their net values equal positive values on the date; this does not exclude later reversals or establish settlement.

Business implication: incorporate major-account ordering variability into short-term workload planning and seek advance order visibility. Do not treat the day's aggregate peak as demonstrated Black Friday uplift or extrapolate it across all customers. Holiday motivation, channel identity and inventory needs remain unobserved. Product-level comparison can explain price/mix versus units, but only commercial records or buyer feedback can establish intent.
