"""Reproducible exploratory commercial analysis; outputs are local, not Athena exports."""
from pathlib import Path
import json
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data_processed' / 'commercial_analysis'
OUT.mkdir(exist_ok=True)
d = pd.read_csv(ROOT / 'data_processed/c820e928a9cb01d0/transactions/part-00000.csv.gz', dtype={'customer_id': 'string', 'stock_code': 'string', 'invoice_no': 'string'})
d['invoice_date'] = pd.to_datetime(d.invoice_date)
# Provisional merchandise proxy, not a validated product master. Preserve source data.
merch = d.stock_code.str.fullmatch(r'\d{5}[A-Za-z]*', na=False)
m = d[merch].copy()
pos = m[(m.quantity > 0) & (m.unit_price_gbp > 0)].copy()
known = pos[pos.customer_id.notna()].copy()
orders = known.groupby(['customer_id', 'invoice_no']).agg(date=('invoice_date', 'min'), value=('line_value_gbp', 'sum')).reset_index()
customers = orders.groupby('customer_id').agg(orders=('invoice_no', 'nunique'), first=('date', 'min'), last=('date', 'max'), positive_value=('value', 'sum'))
customers['net_value'] = m[m.customer_id.notna()].groupby('customer_id').line_value_gbp.sum()
customers['recency_days'] = (pd.Timestamp('2011-12-10') - customers['last'].dt.normalize()).dt.days
customers['purchase_days'] = orders.assign(day=orders.date.dt.normalize()).groupby('customer_id').day.nunique()
customers = customers.sort_values('net_value', ascending=False)
customers.to_csv(OUT / 'customer_summary.csv')
net_all_known = m[m.customer_id.notna()].groupby('customer_id').line_value_gbp.sum().sort_values(ascending=False)
net_den = net_all_known.sum()
top_n = math.ceil(len(net_all_known) * .1)
repeat = customers.orders >= 2
# Same observation window: first observed purchase Jan-Aug; second distinct invoice within 90 days.
eligible = customers[(customers['first'] >= '2011-01-01') & (customers['first'] < '2011-09-01')].copy()
ordered = orders.sort_values(['customer_id','date','invoice_no'])
second = ordered.groupby('customer_id').nth(1).set_index('customer_id')['date']
eligible['second'] = eligible.index.map(second)
eligible['repeat_90d'] = (eligible['second'] - eligible['first']).dt.total_seconds().div(86400).le(90)
cohorts = eligible.groupby(eligible['first'].dt.strftime('%Y-%m')).agg(customers=('orders','size'), repeat_90d=('repeat_90d','sum'))
cohorts['repeat_rate'] = cohorts.repeat_90d / cohorts.customers
cohorts.to_csv(OUT / 'cohorts.csv')
# An illustrative follow-up rule, not a learned churn model.
candidates = customers[(customers.purchase_days >= 3) & (customers.net_value >= 1000) & (customers.recency_days >= 60)].copy()
candidates.to_csv(OUT / 'follow_up_candidates.csv')
products = m.groupby('stock_code').agg(net_value=('line_value_gbp','sum'))
products['buying_customers'] = known.groupby('stock_code').customer_id.nunique()
products['positive_invoices'] = pos.groupby('stock_code').invoice_no.nunique()
products['description'] = pos.groupby('stock_code').description.last()
products.sort_values('buying_customers', ascending=False).head(20).to_csv(OUT / 'products_by_customer_reach.csv')
monthly = pos.groupby('invoice_month').agg(positive_value=('line_value_gbp','sum'), invoices=('invoice_no','nunique'))
monthly['value_per_invoice'] = monthly.positive_value / monthly.invoices
monthly.to_csv(OUT / 'monthly_positive_merchandise.csv')
countries = m.groupby('country').line_value_gbp.sum().sort_values(ascending=False)
countries.to_csv(OUT / 'country_net_merchandise.csv')
summary = dict(source_rows=len(d), merchandise_proxy_rows=len(m), excluded_net_value=float(d.loc[~merch,'line_value_gbp'].sum()),
    positive_merchandise_value=float(pos.line_value_gbp.sum()), unknown_customer_positive_value_share=float(pos.loc[pos.customer_id.isna(),'line_value_gbp'].sum()/pos.line_value_gbp.sum()),
    net_known_customers=len(net_all_known), net_known_value=float(net_den), top10_customer_share=float(net_all_known.head(10).sum()/net_den), top10percent_customer_count=top_n,
    top10percent_customer_share=float(net_all_known.head(top_n).sum()/net_den), purchasing_customers=len(customers), repeat_customers=int(repeat.sum()),
    repeat_customer_positive_value_share=float(customers.loc[repeat,'positive_value'].sum()/customers.positive_value.sum()), eligible_90d_customers=len(eligible), repeat_90d_customers=int(eligible.repeat_90d.sum()),
    follow_up_candidates=len(candidates), follow_up_historical_net_value=float(candidates.net_value.sum()), top_follow_up=candidates.head(5).reset_index().to_dict('records'),
    top_products=products.sort_values('buying_customers',ascending=False).head(5).reset_index().to_dict('records'), monthly=monthly.loc[['2011-10','2011-11']].reset_index().to_dict('records'))
# Sensitivity: repeat concentration without flagged duplicate candidates.
dedup = m[(~m.duplicate_candidate) & m.customer_id.notna()].groupby('customer_id').line_value_gbp.sum().sort_values(ascending=False)
summary['top10_customer_share_without_duplicate_candidates'] = float(dedup.head(10).sum()/dedup.sum())
assert len(d)==541907
assert abs(d.line_value_gbp.sum()-9769872.054)<.0001
assert len(eligible)>0 and eligible.repeat_90d.sum()<=len(eligible)
(OUT / 'summary.json').write_text(json.dumps(summary,indent=2,default=str),encoding='utf-8')
print(json.dumps(summary,indent=2,default=str))
