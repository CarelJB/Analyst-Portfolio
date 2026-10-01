# What explains October-to-November growth?

Evidence: user-supplied Athena export retained unchanged in `evidence/athena_growth_drivers.csv`. The six groups sum to the previously calculated positive merchandise totals: GBP 1,106,666.53 in October and GBP 1,457,742.24 in November. Increase: GBP 351,075.71 (31.7%). This is positive merchandise value, not the net transaction metric from the earlier monthly query.

| Group | October GBP | November GBP | Change GBP | Share of total increase |
|---|---:|---:|---:|---:|
| Unidentified | 101023.63 | 315596.47 | +214572.84 | 61.1% |
| Previously observed | 842289.95 | 1007089.44 | +164799.49 | 46.9% |
| First observed that month | 163352.95 | 135056.33 | -28296.62 | -8.1% |

Unrounded contributions total 100%; rounded figures differ slightly. Contribution shares describe an arithmetic decomposition, not causal effects.

## Main explanation supported so far

The biggest contribution came from unidentified purchases. Their invoices rose only from 102 to 109 (6.9%), but value per invoice rose from GBP 990.43 to GBP 2,895.38 (192.3%). Units per invoice increased 171.5%, while weighted value per unit increased 7.7%. Much larger recorded invoice quantities, rather than a large increase in invoice count, explain most of this group's value growth. These could represent large orders, aggregated transactions or other recording behaviour; the export cannot distinguish them.

The unidentified share of positive merchandise value rose from 9.1% to 21.6%. Therefore, customer acquisition or retention cannot explain the majority of growth from the evidence currently available. Inspect invoice concentration and underlying records before attributing the increase to a repeatable commercial improvement.

## Identified customer behaviour

Previously observed buying customers rose 33.2% (1004 to 1337); invoices per customer rose 13.6%. However, their value per invoice fell 21.0%, with units per invoice down 21.7% and weighted value per unit up 0.9%. Smaller unit baskets, rather than a fall in aggregate unit value, explain the smaller invoices arithmetically. Product mix can change weighted unit value, so this is not proof prices held constant or discounts were absent. The groups do not contain identical customers: October's first-observed buyers may become November's previously observed buyers.

First-observed buyers fell from 357 to 323 (9.5%) and their value per invoice fell 12.5%, driven mainly by fewer units per invoice. Their total positive value fell 17.3%. First observed is not necessarily newly acquired, and this dataset has no acquisition spend or channel records.

## Next tests and business relevance

### Same-customer test completed in Athena

The subsequent user-supplied export, retained in `evidence/athena_same_customers.csv`, compares the same 616 customers purchasing in both months. Invoices increased from 1,049 to 1,263 (+20.4%), but positive merchandise value fell from GBP 647,606.83 to GBP 627,727.36 (-3.1%). Value per invoice fell 19.5% (GBP 617.36 to GBP 497.01), and units per invoice fell 20.7% (354.99 to 281.59). Thus smaller invoices also occur when customer identity is held constant; changing customer composition is not the sole explanation. More invoices do not establish more buying occasions, since invoices may be split.

This group did not generate the overall positive-value increase. That finding does not contradict the increase for all previously observed customers: that broader group changes membership between months. The same-customer result alone neither confirms nor rejects wholesale stocking in the unidentified group. It also does not establish stock shortages, discounts or buyer motivation. Await the unidentified-invoice export to test timing and concentration.

1. Run `sql/why_04_unidentified_invoices.sql`. Are larger unidentified invoices concentrated in a few records or spread across the group? Inspect high-contribution invoice lines and later negative records before interpreting them as demand. If they are aggregated channel sales, obtain customer-level channel records; if exceptional bulk orders, separate them in planning; if duplicated or reversed, preserve the audit trail and correct the reporting interpretation.
2. Run `sql/why_02_same_customers.sql`. Do smaller baskets persist when customer identities are held constant? Then inspect product-level unit and price mix for that group.
3. Only after these tests, choose operational or marketing interventions. No evidence currently establishes stockouts, advertising success, dissatisfaction or genuine price changes.

November has 30 days versus October's 31. Monthly changes are not daily rates. The provisional merchandise code rule and retained duplicate candidates follow the original query. Positive-value metrics may include subsequently reversed purchases; reconcile to net metrics before presenting a final business conclusion.
