"""Auditable batch retail ETL. Local by default; explicit --upload for S3 writes."""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = ['InvoiceNo','StockCode','Description','Quantity','InvoiceDate','UnitPrice','CustomerID','Country']
OUTPUT = ['source_row','invoice_no','stock_code','description','quantity','invoice_date','unit_price_gbp','customer_id','country','line_value_gbp','transaction_type','missing_customer','duplicate_candidate','invoice_month']

def clean_row(row, line):
    """Keep cancellations and unknown customers; reject invalid financial records."""
    reason=[]
    invoice=row['InvoiceNo'].strip(); stock=row['StockCode'].strip(); country=row['Country'].strip()
    if not invoice: reason.append('missing_invoice')
    if not stock: reason.append('missing_stock_code')
    if not country: reason.append('missing_country')
    try:
        quantity=Decimal(row['Quantity'])
        if not quantity.is_finite() or quantity != quantity.to_integral_value() or quantity==0 or abs(quantity)>10**9: raise ValueError()
        quantity=int(quantity)
    except (InvalidOperation,ValueError):
        quantity=0;reason.append('invalid_or_zero_quantity')
    try:
        price=Decimal(row['UnitPrice'])
        if not price.is_finite() or price<0 or price>Decimal('1000000000') or price != price.quantize(Decimal('.0001')): raise ValueError()
    except (InvalidOperation,ValueError):
        price=Decimal(0);reason.append('invalid_or_negative_unit_price')
    try:
        date=datetime.strptime(row['InvoiceDate'].strip(),'%Y-%m-%d %H:%M:%S')
    except ValueError:
        date=None;reason.append('invalid_invoice_date')
    customer=row['CustomerID'].strip()
    if customer:
        try:
            num=Decimal(customer)
            if not num.is_finite() or num<=0 or num!=num.to_integral_value() or num>10**12: raise ValueError()
            customer=str(int(num))
        except (InvalidOperation,ValueError):reason.append('invalid_customer_id')
    cancelled=invoice.upper().startswith('C')
    if cancelled and quantity>0:reason.append('cancellation_positive_quantity')
    if reason:return None,reason
    kind='cancellation' if cancelled else 'negative_adjustment' if quantity<0 else 'zero_price' if price==0 else 'sale'
    # Preserve source precision to four decimal places; do not silently round source prices to cents.
    return [line,invoice,stock,' '.join(row['Description'].split()),quantity,date.strftime('%Y-%m-%d %H:%M:%S'),str(price),customer,country,str(quantity*price),kind,str(not bool(customer)).lower(),'false',date.strftime('%Y-%m')],[]

def run(source:Path, output:Path):
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    # Content-addressed output separates reruns and changed sources without deleting history.
    run_dir=output/digest[:16]
    if run_dir.exists():raise FileExistsError(f'Run already exists: {run_dir}. Reuse its outputs or choose another --output directory.')
    run_dir.mkdir(parents=True)
    for folder in ['transactions','quarantine','reports']:(run_dir/folder).mkdir()
    counts=Counter();reasons=Counter();seen=set();monthly=defaultdict(lambda:Counter());countries=defaultdict(lambda:Counter());customers=set(); invoices=set()
    total=Decimal(0);positive=Decimal(0);negative=Decimal(0);duplicate_value=Decimal(0)
    minimum=None;maximum=None
    try:
        with source.open(newline='',encoding='utf-8-sig') as src, gzip.open(run_dir/'transactions/part-00000.csv.gz','wt',newline='',encoding='utf-8') as dest, (run_dir/'quarantine/rejected.csv').open('w',newline='',encoding='utf-8') as rejects:
            reader=csv.DictReader(src)
            if reader.fieldnames!=COLUMNS:raise ValueError(f'Expected columns in order: {COLUMNS}; got {reader.fieldnames}')
            writer=csv.writer(dest);writer.writerow(OUTPUT)
            reject=csv.writer(rejects);reject.writerow(['source_row','reasons','raw_record_json'])
            for line,row in enumerate(reader,2):
                counts['input_rows']+=1
                if None in row or any(v is None for v in row.values()):
                    result=None;issues=['malformed_csv_record']
                else:result,issues=clean_row(row,line)
                if issues:
                    counts['rejected_rows']+=1;reasons.update(issues);reject.writerow([line,';'.join(issues),json.dumps(row,ensure_ascii=False)]);continue
                fingerprint=tuple(row[k] for k in COLUMNS)
                duplicate=fingerprint in seen;seen.add(fingerprint)
                result[12]=str(duplicate).lower()
                counts['duplicate_candidates']+=int(duplicate)
                counts['accepted_rows']+=1;counts[result[10]+'_rows']+=1;counts['missing_customer_rows']+=int(not result[7])
                value=Decimal(result[9]);total+=value
                positive+=max(value,Decimal(0));negative+=min(value,Decimal(0))
                if duplicate:duplicate_value+=value
                invoices.add(result[1])
                if result[7]:customers.add(result[7])
                minimum=min(minimum,result[5]) if minimum else result[5];maximum=max(maximum,result[5]) if maximum else result[5]
                for groups,key in [(monthly,result[13]),(countries,result[8])]:
                    groups[key]['rows']+=1;groups[key]['net_value_gbp']+=value;groups[key]['positive_value_gbp']+=max(value,Decimal(0));groups[key]['negative_value_gbp']+=min(value,Decimal(0))
                writer.writerow(result)
        assert counts['input_rows']==counts['accepted_rows']+counts['rejected_rows']
        assert total==positive+negative
        for name,groups in [('monthly',monthly),('country',countries)]:
            with (run_dir/f'reports/{name}_summary.csv').open('w',newline='',encoding='utf-8') as f:
                w=csv.writer(f);w.writerow([name,'rows','positive_value_gbp','negative_value_gbp','net_value_gbp'])
                for key,values in sorted(groups.items()):w.writerow([key,values['rows'],values['positive_value_gbp'],values['negative_value_gbp'],values['net_value_gbp']])
        report={'status':'complete','created_utc':datetime.now(timezone.utc).isoformat(),'source_file':source.name,'source_sha256':digest,'currency':'GBP','counts':dict(counts),'rejection_reasons':dict(reasons),'positive_line_value_gbp':str(positive),'negative_line_value_gbp':str(negative),'net_line_value_gbp':str(total),'duplicate_candidate_value_gbp':str(duplicate_value),'distinct_invoice_numbers':len(invoices),'known_customers':len(customers),'first_invoice':minimum,'last_invoice':maximum,'row_reconciliation_passed':True,'value_reconciliation_passed':True,'policy':'Duplicate candidates retained because no unique line identifier exists. Missing customers retained. Negative and cancellation lines retained. Net line value is not profit or cash received.'}
        (run_dir/'reports/quality_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        write_sql(run_dir,'cjb-retail-pipeline',digest[:16])
        return run_dir,report
    except Exception as exc:
        (run_dir/'FAILED.txt').write_text(str(exc),encoding='utf-8');raise

def write_sql(run_dir,bucket,run_id):
    strings=',\n  '.join(f'`{c}` string' for c in OUTPUT)
    table=f'retail_lines_{run_id}'
    sql=f'''-- Execute each statement separately in Athena. Query results need their own S3 prefix.
CREATE DATABASE IF NOT EXISTS cjb_retail;

CREATE EXTERNAL TABLE IF NOT EXISTS cjb_retail.{table} (
  {strings}
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ('separatorChar'=',', 'quoteChar'='"', 'escapeChar'='\\\\')
STORED AS TEXTFILE
LOCATION 's3://{bucket}/Processed/runs/{run_id}/transactions/'
TBLPROPERTIES ('skip.header.line.count'='1');

CREATE OR REPLACE VIEW cjb_retail.retail_transactions AS
SELECT CAST(source_row AS bigint) AS source_row, invoice_no, stock_code, description,
       CAST(quantity AS bigint) AS quantity, CAST(invoice_date AS timestamp) AS invoice_date,
       CAST(unit_price_gbp AS decimal(20,4)) AS unit_price_gbp,
       NULLIF(customer_id, '') AS customer_id, country,
       CAST(line_value_gbp AS decimal(28,4)) AS line_value_gbp,
       transaction_type, CAST(missing_customer AS boolean) AS missing_customer,
       CAST(duplicate_candidate AS boolean) AS duplicate_candidate, invoice_month
FROM cjb_retail.{table};
'''
    (run_dir/'athena_setup.sql').write_text(sql,encoding='utf-8')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=ROOT/'data_raw/Online_Retail.csv')
    p.add_argument('--output',type=Path,default=ROOT/'data_processed')
    p.add_argument('--bucket',default='cjb-retail-pipeline');p.add_argument('--region',default='eu-north-1');p.add_argument('--profile')
    p.add_argument('--s3-key',help='Read this exact source object instead of local CSV; case-sensitive.')
    p.add_argument('--upload',action='store_true',help='Upload this completed run to Processed/runs/<hash>/; never changes raw objects.')
    args=p.parse_args();s3=None
    if args.s3_key or args.upload:
        import boto3
        s3=boto3.Session(profile_name=args.profile,region_name=args.region).client('s3')
    source=args.input
    if args.s3_key:
        source=ROOT/'data_downloaded'/Path(args.s3_key).name;source.parent.mkdir(exist_ok=True)
        s3.download_file(args.bucket,args.s3_key,str(source))
    run_dir,report=run(source,args.output)
    write_sql(run_dir,args.bucket,report['source_sha256'][:16])
    if args.upload:
        prefix=f"Processed/runs/{report['source_sha256'][:16]}/"
        if s3.list_objects_v2(Bucket=args.bucket,Prefix=prefix,MaxKeys=1).get('KeyCount',0):raise RuntimeError('S3 run prefix already contains objects; refusing to overwrite.')
        files=[f for f in run_dir.rglob('*') if f.is_file()]
        for file in sorted(files,key=lambda f:f.name=='quality_report.json'):
            s3.upload_file(str(file),args.bucket,prefix+file.relative_to(run_dir).as_posix(),ExtraArgs={'ServerSideEncryption':'AES256'})
        print(f'Uploaded to s3://{args.bucket}/{prefix}')
    print(json.dumps(report,indent=2));print(f'Output: {run_dir}')

if __name__=='__main__':main()
