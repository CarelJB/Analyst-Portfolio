# Cloud verification record

Evidence provenance: CloudShell output supplied by Jaco on 30 September 2026 and Athena results supplied on 1 October 2026. These are user-provided execution results, not an independent inspection of the AWS account.

Source SHA-256: `c820e928a9cb01d05738b0c36b5033ef661eccfb82f09f2e5ce8542da73b0b99`.

CloudShell reported successful upload to `s3://cjb-retail-pipeline/Processed/runs/c820e928a9cb01d0/` in `eu-north-1`. All 541,909 source rows reconcile to 541,907 accepted and 2 rejected for negative unit price.

| Athena check | Observed, matching local report |
|---|---:|
| Accepted rows | 541907 |
| Distinct invoices | 25898 |
| Known customers | 4372 |
| Missing customer rows | 135078 |
| Duplicate candidates retained | 5268 |
| Net line value GBP | 9769872.0540 |
| First invoice | 2010-12-01 08:26:00.000 |
| Last invoice | 2011-12-09 12:50:00.000 |

This verifies the manually executed S3 → CloudShell Python ETL → S3 → Athena path for this source version. It does not establish scheduling, production monitoring or validation of every business query. Net line value is not profit or cash received. December 2011 is incomplete.

## Monthly business query verified

On 1 October 2026, Jaco supplied the exported monthly Athena CSV and a screenshot of its completed execution. All 13 month keys, row counts, net values and negative values match the local monthly summary exactly. Copies are retained in `evidence/athena_monthly_results.csv` and `evidence/athena_monthly_results.png`.

The screenshot records 10.35 MB scanned and 1.807 seconds runtime for this execution; these are observations, not performance guarantees.

November 2011 net line value was GBP 1,461,756.25, up 36.5% from October, while transaction lines increased 39.5%. Line counts are not order counts. This comparison does not establish the cause or prove recurring seasonality.

December 2011 covers only 1–9 December. Its negative entries total GBP 205,124.67 in magnitude, equivalent to 32.1% of its positive line value (GBP 638,792.68). This is a value ratio, not a return rate: cancellation and adjustment records need investigation before attribution.

## December negative entries investigated

The supplied Athena export is saved as `evidence/athena_december_negative_invoices.csv`. All 20 invoice groups, counts and values match an independent aggregation of the locally processed transactions.

The three largest entries account for 96.47% of December's negative value:

| Invoice | Negative value GBP | Detail from locally processed source |
|---|---:|---|
| C581484 | -168469.60 | Customer 16446, stock 23843, quantity -80995 at GBP 2.08 |
| C580605 | -17836.46 | Stock AMAZONFEE, description AMAZON FEE |
| C580604 | -11586.50 | Stock AMAZONFEE, description AMAZON FEE |

The largest entry alone represents 82.13% of December's negative value. The local source contains positive invoice 581483 for the same customer, stock and price, quantity +80995, at 09:15 on 9 December 2011. C581484 follows at 09:27. Their values offset exactly to zero. This strongly suggests a reversal, but the data provides no explicit linkage or reason proving an entry error or customer return.

The two AMAZON FEE descriptions show why treating every C-prefixed entry as a merchandise return would be misleading. Keep the original records and technical cancellation classification, and distinguish fees when defining business KPIs. Do not infer cash refunds or customer dissatisfaction from these entries.

Detailed line inspection was subsequently confirmed against Jaco's Athena export on 1 October 2026. All four records match the locally processed source across all eight exported fields, including timestamps, descriptions, quantities and exact decimal values. The unchanged export is retained in `evidence/athena_december_transaction_detail.csv`. A useful business recommendation is to flag large offsetting transactions and report fees separately from merchandise cancellations before interpreting return metrics.
