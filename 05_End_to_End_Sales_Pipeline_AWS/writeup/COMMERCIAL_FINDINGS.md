# Where should the retailer focus its effort?

Historical exploratory brief. The later [main case study](CASE_STUDY.md) and Athena investigation notes supersede this brief where definitions or counts differ. In particular, the initial 234-account elapsed-time result below was corrected to 244 using calendar days; the final cadence analysis prioritises 43 accounts with longer purchasing histories and absences exceeding twice their usual interval. No locally calculated metric should be presented as independently executed in Athena unless its export is linked in the investigation notes.

## Decision brief

Prioritise existing customer relationships and review inactive repeat buyers before recommending a broad discount campaign. Protect availability of products bought by many different customers. Plan fulfilment around invoice volume, not transaction value alone.

These recommendations are retrospective, as at 10 December 2011. This historical public dataset cannot identify customers to contact today or prove that any proposed action would increase profit.

## 1. Protect the customer relationships supporting most of the business

Of 4,363 identified customers with merchandise records, the highest-value 437 (approximately 10%) account for 60.3% of net merchandise value. The top ten alone account for 16.5%. Their concentration is similar when duplicate candidates are excluded: the top-ten share becomes 16.6%.

**Meaning:** losing a small number of substantial accounts could materially affect transaction value. Treating every customer identically would overlook this dependency.

**Action:** review the leading accounts for service issues, purchasing cadence and availability of their usual products. Assign responsibility for account follow-up before offering blanket discounts. Verify contribution margin and credit exposure when those records become available; transaction value does not establish profitability.

**Measure:** subsequent 90-day purchasing and net merchandise value among the priority accounts, plus on-time delivery and contribution margin when available. This dataset provides the purchase baseline, not delivery or margin measures.

## 2. Create a specific follow-up list, rather than declaring customers lost

An illustrative rule identifies 234 customers who purchased on at least three separate days, generated at least GBP 1,000 net merchandise value and had not purchased for at least 60 days by 10 December 2011. Their observed historical net value totals GBP 525,635. This is not forecast recoverable revenue.

Examples include customer 12939 (GBP 11,582 net, six purchasing days, 64 days since last purchase) and 16180 (GBP 10,217 net, seven purchasing days, 100 days since last purchase).

**Meaning:** these are established buyers worth reviewing, rather than an undifferentiated mailing list. Some may buy seasonally or have naturally long purchase intervals; the rule does not establish churn.

**Action:** inspect usual buying intervals, prior cancellations and account notes, then trial a helpful stock or replenishment message with suitable customers. Use a randomly selected holdout group among otherwise eligible accounts to distinguish campaign effects from customers returning anyway. No outreach has been performed.

**Measure:** incremental purchase rate and net value over 30–60 days versus the holdout. Evaluate margin after campaign costs before expanding.

The candidate table is in `data_processed/commercial_analysis/follow_up_candidates.csv`. Its thresholds are analyst-selected prioritisation assumptions, not an optimised predictive model.

## 3. Investigate the second-purchase opportunity

Among 2,430 customers whose first observed positive merchandise purchase was January–August 2011, 1,037 (42.7%) had a second distinct positive invoice within 90 days. The remaining 57.3% had no second qualifying invoice in that window. All included cohorts have at least 90 days of subsequent observation.

**Meaning:** there is a measurable follow-up opportunity after the first observed purchase, but no benchmark here proves performance is poor. First observed purchase is not necessarily the customer's first-ever purchase, and two invoices may be part of the same buying occasion.

**Action:** validate invoice splitting and link pre-period purchase history before calling this a new-customer retention metric. Then test post-purchase support and relevant replenishment reminders against a holdout rather than immediately discounting.

**Measure:** subsequent distinct purchasing-day conversion within 90 days, net transaction value and, with cost data, contribution after campaign spending.

## 4. Protect products with broad customer demand

| Product code | Latest observed description | Identified buying customers |
|---|---|---:|
| 22423 | REGENCY CAKESTAND 3 TIER | 881 |
| 85123A | CREAM HANGING HEART T-LIGHT HOLDER | 856 |
| 47566 | PARTY BUNTING | 708 |

Descriptions can change; product codes define the grouping. Counts use positive-priced positive-quantity lines and do not prove purchases were ultimately retained.

**Meaning:** these products reach many customers, making them useful starting points for an availability review. Ranking solely by value could instead prioritise isolated bulk purchases or reversals.

**Action:** check current stock, supplier lead times, recent demand and margin for these products before setting replenishment levels. This dataset has no stock-on-hand or lost-sales information, so it cannot prove stockouts or justify an order quantity.

**Measure:** availability, fulfilment rate and missed-order value once inventory and service records are joined. Assess customer experience through delivery and service measures rather than assuming purchasing indicates satisfaction.

## 5. Prepare operations for more invoices, not just more value

From October to November 2011, positive merchandise invoice count increased from 2,005 to 2,751 (37.2%). Positive merchandise value increased from GBP 1.107m to GBP 1.458m (31.7%), while value per invoice fell from GBP 551.95 to GBP 529.90 (4.0%).

**Meaning:** invoice workload grew faster than transaction value. Staffing based only on value growth could understate order-handling demand. Invoices are a workload proxy, not confirmed shipments; item counts and split shipments also matter.

**Action:** use daily invoice and line volumes alongside picking capacity to plan busy periods. Validate with shipment records. One annual cycle cannot establish a reliable seasonal forecast.

**Measure:** dispatch time, backlog, picking hours per shipment and error rate after joining operational records.

## 6. Fix the gap in customer visibility

Records without customer IDs represent 14.7% of positive merchandise value. These transactions contribute to total demand but cannot be included reliably in customer-level follow-up or retention analysis.

**Action:** investigate whether the gap comes from particular channels, guest purchases or failed data capture before proposing a remedy. Where appropriate, improve consistent customer identifiers without assuming every missing ID is an error.

**Measure:** share of transaction value linked to a valid customer, by channel. Avoid reporting customer retention as representative of the entire business until coverage is understood.

## Definitions and evidence

These new calculations were run locally on the same source version already reconciled with Athena. They are not yet independently executed in Athena. The reproducible analysis is `python/commercial_analysis.py`; output tables and summary are in `data_processed/commercial_analysis/`.

Merchandise is provisionally defined as stock codes matching five digits followed by optional letters. This excludes fee and administrative codes, but is a heuristic that must be checked against a product master. It retains 538,914 rows; excluded records have combined net value of GBP -22,438.376. Raw records remain unchanged. Net metrics include negative and cancellation lines; positive metrics use positive quantities and prices. Known-customer concentration includes customers with negative-only records. Customer purchase measures use positive invoice records; returns do not erase purchase events. Duplicate candidates remain unless sensitivity results explicitly say otherwise.

Currency outputs are rounded for discussion. Exploratory aggregation uses floating-point arithmetic with source-total reconciliation within GBP 0.0001; the production ETL and Athena monetary fields retain decimal precision. These findings do not establish profit, customer satisfaction, causal drivers or realised improvements.
