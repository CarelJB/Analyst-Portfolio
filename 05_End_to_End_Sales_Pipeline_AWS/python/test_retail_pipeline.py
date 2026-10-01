import csv
import gzip
import tempfile
import unittest
from pathlib import Path
from retail_pipeline import COLUMNS, clean_row, run

class PipelineTests(unittest.TestCase):
    def row(self,**changes):
        d=dict(zip(COLUMNS,['100','ABC','Test, "product"', '2','2011-01-01 10:00:00','2.55','12345.0','United Kingdom']));d.update(changes);return d
    def test_sale(self):
        r,e=clean_row(self.row(),2);self.assertEqual(e,[]);self.assertEqual(r[9],'5.10');self.assertEqual(r[7],'12345')
    def test_cancel(self):
        r,e=clean_row(self.row(InvoiceNo='C100',Quantity='-2'),2);self.assertEqual(e,[]);self.assertEqual(r[10],'cancellation');self.assertEqual(r[9],'-5.10')
    def test_unknown_customer(self):
        r,e=clean_row(self.row(CustomerID=''),2);self.assertEqual(e,[]);self.assertEqual(r[11],'true')
    def test_bad_values(self):
        for changes in [{'Quantity':'1.5'},{'Quantity':'0'},{'UnitPrice':'NaN'},{'UnitPrice':'-1'},{'InvoiceDate':'bad'},{'InvoiceNo':'C100'},{'CustomerID':'123.4'}]:
            with self.subTest(changes=changes):self.assertTrue(clean_row(self.row(**changes),2)[1])
    def test_run_reconciliation_and_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);src=root/'test.csv'
            with src.open('w',newline='',encoding='utf-8') as f:
                w=csv.DictWriter(f,fieldnames=COLUMNS);w.writeheader();w.writerows([self.row(),self.row(),self.row(Quantity='0'),self.row(InvoiceNo='C100',Quantity='-2')])
            folder,report=run(src,root/'out')
            self.assertEqual(report['counts']['input_rows'],4);self.assertEqual(report['counts']['accepted_rows'],3);self.assertEqual(report['counts']['rejected_rows'],1);self.assertEqual(report['counts']['duplicate_candidates'],1);self.assertEqual(report['net_line_value_gbp'],'5.10')
            with gzip.open(folder/'transactions/part-00000.csv.gz','rt',newline='',encoding='utf-8') as f:
                rows=list(csv.DictReader(f));self.assertEqual(rows[0]['description'],'Test, "product"');self.assertEqual(rows[1]['duplicate_candidate'],'true')
            with self.assertRaises(FileExistsError):run(src,root/'out')

if __name__=='__main__':unittest.main()
