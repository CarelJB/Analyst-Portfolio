# Retail transaction analysis with Python, S3 and Athena

Jaco Bouwer | Portfolio project | Validated October 2026

## Business question

Where should the retailer focus customer follow-up, product availability and fulfilment effort? This report brings together the Athena investigations into customer buying intervals, monthly growth, holiday timing and exceptional transactions. The earlier [commercial decision brief](COMMERCIAL_FINDINGS.md) contains exploratory local analysis; the AWS evidence and corrected definitions below take precedence.

The UCI Online Retail dataset contains 541,909 invoice lines from 1 December 2010 to 9 December 2011. Prices are in GBP. This is a historical public-data portfolio exercise, not a client engagement.

## Main business finding: growth can conceal overdue customer relationships

At the historical snapshot of 10 December 2011, a blanket rule of 60 days without purchasing identified 244 customers with at least three purchasing dates and GBP 1,000 historical net merchandise value. Comparing each customer's absence with its own approximate median interval between purchasing dates changed the priorities:

| Finding from Athena | Business meaning |
|---|---|
| 67 of the 244 customers were still within their usual interval | A fixed inactivity threshold can target naturally infrequent buyers unnecessarily. |
| 96 had exceeded twice their usual interval | Their changed behaviour merits investigation; it does not establish churn. |
| 43 of those had at least six purchasing dates and GBP 141,551.68 combined historical net value | This provides a focused review group with at least five observed intervals per customer. Past value is not forecast recoverable sales. |

Customer 16745 illustrates the opportunity: 17 purchasing dates, a typical gap of 13 days, and 87 days since the last purchase. This explains why the account deserves attention, but not why purchasing stopped. The thresholds are illustrative prioritisation rules, not a validated churn model.

### Why it matters

Rising total sales do not show whether individual customer relationships are weakening. Comparing accounts with their own history makes potentially important changes visible while avoiding a uniform assumption that every quiet account is lost. We cannot establish whether the retailer already knew about these accounts or whether follow-up would recover sales.

### How to use the finding

1. Produce a weekly review list based on purchasing intervals, history and value. Start with the 43-account historical group as an example, then validate thresholds against live records and seasonal buying patterns.
2. Review account notes and ask suitable customers about changing requirements, availability or service issues. Capture the reason rather than inferring it from inactivity.
3. Respond to the actual need through relevant replenishment reminders, product availability information or service recovery. Do not assume a discount is necessary.
4. Test the intervention against a comparable randomly selected holdout among eligible accounts. Predefine an appropriate follow-up window and measure incremental purchasing and net value; add product margin and campaign costs before claiming profitability.

No outreach or experiment has been performed, and no sales uplift has been measured. See the [cadence investigation](AWS_CADENCE_FINDINGS.md) and [identified Athena export](../evidence/athena_customer_cadence_identified.csv).

## AWS implementation

The pipeline reads a CSV from Amazon S3, processes it with Python in AWS CloudShell, writes validated compressed CSV and quality reports back to S3, and exposes the accepted records through an Athena table and typed SQL view. Athena provides the SQL query interface and the Glue Data Catalog stores table metadata. No Glue ETL job or crawler is used.

Validation preserves missing customer IDs and cancellations, flags duplicate candidates, and quarantines invalid records with reasons. Decimal arithmetic preserves monetary precision. Source fingerprints and source row numbers support traceability.

The run accepted 541,907 records and quarantined two negative-price records. It retained 135,078 records without customer IDs and flagged 5,268 duplicate candidates without deleting them: the source has no unique invoice-line identifier establishing that repeated rows are errors.

## Verification

Athena reconciliation matched the local pipeline across eight checks, including accepted rows, distinct invoices, known customers, missing customer rows, duplicate candidates, net line value and date boundaries. Net line value was GBP 9,769,872.0540. Five automated tests passed during development.

The 13 monthly result rows, 20 largest December negative invoice groups and four detailed transaction records were independently compared with local outputs. All matched. Evidence consists of exported Athena results supplied by Jaco and the completed CloudShell execution output; see the [verification record](../VERIFICATION.md).

## Findings

### Why November grew

Athena shows positive merchandise value increasing by GBP 351,075.71 from October to November. Unidentified purchases contributed GBP 214,572.84 (61.1% of the increase); previously observed customers contributed GBP 164,799.49 (46.9%); first-observed customers offset this by GBP 28,296.62 (-8.1%). The rounded percentages differ slightly from 100%. This decomposition does not support attributing the majority of growth to identifiable customer acquisition or retention.

The same 616 customers purchasing in both months generated 20.4% more invoices but 3.1% less positive merchandise value. Their units per invoice fell 20.7%. Smaller invoices therefore persist when customer identity is held constant, although invoice splitting and product mix still require interpretation. See [growth findings](AWS_GROWTH_FINDINGS.md).

### Holiday demand: evidence and competing explanations

Two unidentified invoices on 7 and 14 November totalled GBP 103,594.85, shared 81 product codes and included GBP 26,174.69 in explicitly CHRISTMAS/XMAS-labelled goods. Their timing and bulk quantities support advance stocking as a hypothesis. Weekly channel summaries remain an alternative; buyer identity and intent are unavailable. See [bulk-invoice evidence](AWS_BULK_INVOICES.md).

Black Friday's positive merchandise value was 14.4% below the average of the previous three Fridays. November still exceeded October by 22.4% after excluding those two bulk invoices. This favours investigation of broader pre-Christmas trading over a single event-day surge, but neither proves seasonal causation nor rules out all Black Friday influence. UK location alone cannot rule out that influence, and this retailer also has international customers. Every Saturday had zero recorded invoices, highlighting the need to distinguish invoice posting from consumer order timing. See [daily holiday analysis](AWS_HOLIDAY_FINDINGS.md).

### Why 23 November peaked

Against the preceding Wednesday, invoice count was unchanged at 130, but positive merchandise value increased GBP 13,700.99. The difference in each day's three largest invoices accounts arithmetically for 72.6% of that increase. Customers 14088 and 14646 together supplied 27.1% of the day's positive value. Customer 14088 had its highest observed value day; 14646 had nine earlier higher-value days. Thus substantial established-account purchases explain part of the peak without establishing a holiday motive. Seek advance ordering visibility from major accounts when planning workload. See [the full investigation](AWS_NOVEMBER23_FINDINGS.md).

### Reporting quality prevents misleading business conclusions

November 2011 had the highest monthly net line value at GBP 1,461,756.25, up 36.5% from October. Transaction lines increased 39.5% over the same period. Line counts are not order counts, and this short history does not establish recurring seasonality or explain the growth.

December covers only nine days, so its lower monthly total is not evidence of a full-month decline. Its negative entries total GBP 205,124.67 in magnitude, equivalent to 32.1% of positive line value. Investigation showed that three entries account for 96.5% of that negative value:

| Invoice | Negative value GBP | Evidence |
|---|---:|---|
| C581484 | 168,469.60 | Same customer, product and unit price as an equal positive transaction 12 minutes earlier |
| C580605 | 17,836.46 | Product code AMAZONFEE; description AMAZON FEE |
| C580604 | 11,586.50 | Product code AMAZONFEE; description AMAZON FEE |

Positive invoice 581483 records 80,995 units at GBP 2.08 on 9 December at 09:15. C581484 records the opposite quantity at 09:27 for the same customer and product. The two entries net to zero. Their timing and matching fields strongly suggest a reversal, but the source contains no explicit link or reason proving an entry error or a customer return.

The fee descriptions also show why all C-prefixed records cannot be interpreted as merchandise returns. The 32.1% figure is a negative-to-positive value ratio, not a customer return rate. AMAZONFEE's exact accounting purpose and any connection to promotions remain unverified; see the [interpretation note](AMAZONFEE_INTERPRETATION.md).

## Recommended business actions

- Separate fee entries from merchandise cancellations when defining reporting categories, while retaining the original records and an audit trail.
- Flag unusually large, closely timed offsetting transactions for review. Confirm the reason with transaction owners before changing business classifications.
- Label partial reporting periods and compare equivalent date ranges.
- Reconcile dashboard totals to validated transaction outputs before distributing reports.

These are recommendations from the analysis. No commercial savings, customer behaviour changes or operational outcomes have been measured.

## Scope and limitations

This is a manually executed batch pipeline. Scheduling, monitoring, concurrent publication and production recovery are not implemented. Output is gzip CSV; partitioned Parquet is a potential future optimisation. Net line value is not profit, cash received or independently verified recognised revenue. Missing customer IDs limit customer analysis, and retained duplicate candidates affect totals.

## Evidence and source

- [Monthly Athena export](../evidence/athena_monthly_results.csv)
- [Monthly query screenshot](../evidence/athena_monthly_results.png)
- [December negative invoice export](../evidence/athena_december_negative_invoices.csv)
- [Detailed transaction export](../evidence/athena_december_transaction_detail.csv)
- Dataset: Daqing Chen, UCI Online Retail, DOI [10.24432/C5BW33](https://doi.org/10.24432/C5BW33).
