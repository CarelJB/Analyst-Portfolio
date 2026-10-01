# Explain the business patterns in Athena

Status: growth-driver and same-customer queries executed in Athena, with exports supplied by Jaco. See [growth findings](AWS_GROWTH_FINDINGS.md). The cadence and unidentified-invoice drill-downs still await AWS evidence. Other local commercial findings remain exploratory leads, not completed AWS evidence.

## Start with why November grew

Run `sql/why_01_growth_drivers.sql` in Athena and export the result. It separates first-observed, previously observed and unidentified customers for October and November. Within identified groups, positive value equals customer count × invoices per customer × value per invoice (apart from displayed rounding). Value per invoice can be decomposed into units per invoice × value per unit.

Compare absolute value changes by group first. Then determine which factors changed. An increase in first-observed customers is not proof of successful advertising: there are no acquisition-source or campaign records. October has 31 days and November 30, so compare activity per day as well as monthly totals. Product mix affects value per unit; it is not a pure price measure. Positive lines may include later-reversed purchases, so net-value reconciliation remains necessary before a final commercial conclusion.

Run `sql/why_02_same_customers.sql` next. This keeps the customers constant across months. If invoice size falls overall but not among the same customers, customer composition is a plausible contributor. If it falls within the same-customer group too, investigate their units and product mix. This subgroup excludes entrants and departing customers, so it is not a whole-business estimate or causal experiment.

Next drill-down depends on these results: rank product-level contributions to the value change, examine the same product's realised unit price and units, and check cancellations among the largest contributors. Do not assume Christmas demand, discounting or customer dissatisfaction from a calendar pattern.

## Ask whether inactive customers are unusually late

Run `sql/why_03_customer_cadence.sql`. It compares recency against each customer's approximate median gap between distinct buying days. A customer silent for 60 days after weekly purchases is a different follow-up priority from one normally purchasing every 90 days. At least three days gives only two intervals for some customers, so inspect history before acting.

This explains the prioritisation, not the reason for inactivity. Stock availability, service issues, competitor switching and normal buying cycles remain hypotheses. Resolve them with stock/fulfilment records and account conversations. No such records exist in this dataset.

## Evidence standard

For each finding retain: the business question, competing explanations, Athena query and exported result, what the evidence supports, what it cannot decide, and an action or next test. Python may independently check calculations; AWS results must support the portfolio's analytical claims.

Athena engine 3 functions reference: https://docs.aws.amazon.com/athena/latest/ug/functions-env3.html
