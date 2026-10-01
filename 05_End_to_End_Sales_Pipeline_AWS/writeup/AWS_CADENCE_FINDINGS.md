# Prioritising customer follow-up using buying intervals

Evidence: original Athena export retained as `evidence/athena_customer_cadence.csv`; corrected export with identifiers retained as `evidence/athena_customer_cadence_identified.csv`. All 244 records match across the original six fields, and all 244 customer IDs are populated and unique. Historical snapshot: 10 December 2011. The export contains customers with at least three purchase dates, GBP 1,000 net merchandise value and 60 calendar days since last purchase. The identified export now supports an account review list for this historical exercise.

Of the 244 qualifying rows:

- 67 have not yet exceeded their own approximate median purchase interval. A blanket 60-day inactivity rule could unnecessarily target them.
- 96 exceed twice their usual interval, representing GBP 233,585.24 of historical net value. This is not forecast revenue at risk or recoverable revenue.
- 43 of those 96 have at least six distinct purchase dates, giving at least five observed intervals. These represent GBP 141,551.68 of historical net value and provide a more substantial starting history for account review.

For example, one row has 11 purchase dates, a typical interval of nine days and 157 days since its last purchase. Another has a typical interval of 196 days and only 68 days since last purchase. Treating both as equally overdue would ignore observed behaviour.

Twice the usual gap and six purchase dates are illustrative review criteria, not validated churn thresholds. Approximate medians, seasonal demand and short histories limit certainty. The data explains why some accounts merit review, but not why purchasing stopped. Account notes, stock availability, service records and customer feedback would distinguish possible causes.

Reconciliation correction: the earlier local list had 234 customers because recency floored elapsed timestamp days. Athena counts calendar dates and includes ten customers on the 60-day boundary. Applying calendar dates locally reproduces 244 customers and GBP 551,211.05 historical net value. Use the Athena calendar-date definition consistently going forward; the earlier 234 count is superseded.
