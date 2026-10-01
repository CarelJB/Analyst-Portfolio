# Early-November bulk purchases: evidence for the stocking hypothesis

Source: supplied Athena export retained unchanged in `evidence/athena_unidentified_invoices.csv`. The query selects the ten largest unidentified positive merchandise invoices in October and November, not all invoices or net sales.

November's two largest unidentified invoices were:

| Invoice | Date | Positive merchandise value GBP | Units | Product codes |
|---|---|---:|---:|---:|
| 574941 | 7 November 2011 | 52940.94 | 14149 | 101 |
| 576365 | 14 November 2011 | 50653.91 | 13956 | 99 |

Combined value is GBP 103,594.85, or 32.8% of November's unidentified positive merchandise value. Both precede 25 November Black Friday. Roughly 140 units per product code on average is consistent with bulk purchasing across an assortment. It does not establish buyer identity, product-level quantities, resale intent or holiday motivation. The two invoices cannot be linked to one buyer because customer IDs are absent.

The timing supports investigating pre-holiday stocking rather than attributing the largest invoices to purchases made on Black Friday itself. Two other top-ten invoices are dated 25 November, so holiday-event activity remains possible. A top-ten extract cannot establish daily demand patterns or the absence of a broader event effect.

The two largest invoices equal 29.5% of the entire October-to-November positive merchandise value increase. This is a scale comparison, not a causal attribution or matched baseline: October also contains large invoices. Removing these two alone would still leave November positive merchandise value above October, so they do not explain all growth.

No exact duplicate-candidate value is flagged on the listed top-ten invoices. This does not rule out aggregated records, other duplicate forms or later reversals.

## Product detail verified in Athena

The supplied product export is retained as `evidence/athena_bulk_products.csv`. Its 101 and 99 product groups reconcile exactly to the previously exported invoice values and quantities. All codes satisfy the provisional merchandise rule; no negative net product groups or flagged duplicate lines appear in this export. This does not rule out reversals on other invoices.

The invoices share 81 product codes, out of 119 distinct codes across both. Descriptions explicitly containing CHRISTMAS or XMAS account for 17 codes and GBP 11,520.95 (21.8%) on invoice 574941, and 16 codes and GBP 14,653.74 (28.9%) on invoice 576365. Combined: GBP 26,174.69, or 25.3% of the two invoices. This transparent keyword rule is a description-based indicator, not a complete seasonal classification.

For example, PAPER CHAIN KIT 50'S CHRISTMAS appears in quantities of 478 and 688; JUMBO BAG 50'S CHRISTMAS in quantities of 484 and 392. Non-explicitly-seasonal lines also have substantial quantities: POPCORN HOLDER at 1,820 and 1,130, and RABBIT NIGHT LIGHT at 628 and 404.

The observed pattern is bulk quantities across a substantially overlapping assortment with a meaningful Christmas component, recorded on two dates a week apart ahead of Black Friday. This strengthens the pre-holiday stocking hypothesis. It does not establish wholesaler identity or stocking intent. Weekly aggregated channel transactions are an alternative explanation compatible with missing IDs, broad assortment and timing; no channel information is available to resolve it.

Business action conditional on confirmation: if wholesale stocking is established, review advance availability and supplier lead times for the recurring assortment and ask known accounts about pre-season requirements. If these are channel summaries, obtain transaction-level records before treating each invoice as one customer's basket. Neither pattern by itself justifies an inventory order quantity.

Next: examine the daily pattern using `sql/why_06_daily_holiday_pattern.sql`, then investigate reversals and verify transaction provenance. A single season and no promotion history cannot identify a causal Black Friday effect.
