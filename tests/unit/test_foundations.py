import unittest
from jsonschema.exceptions import ValidationError
from career_platform.foundations import approval_claims, evaluation_report, validate_record

def claim():
    return dict(claim_id='c1', tenant_id='t1', user_id='u1', kind='skill', value='Python',
        source=dict(document_id='d1', sha256='a'*64, locator='page 1', quote='Python'),
        verification=dict(status='verified', reviewer_id='u1', reviewed_at='2026-10-12T12:00:00Z'))

def records(n=50):
    return [dict(id=str(i), jd_text=f'Example role number {i} requiring Python development',
        source_url='https://example.com/jobs/'+str(i), label=['strong','maybe','skip'][i%3],
        rated_by='test-reviewer', rated_at='2026-10-12T12:00:00Z', synthetic=False) for i in range(n)]

class FoundationsTests(unittest.TestCase):
    def test_all_claim_kinds(self):
        for kind in ['employer','title','dates','skill','metric','education','certification']:
            c=claim(); c['kind']=kind
            validate_record(c,'claim')
    def test_excludes_unverified(self):
        for status in ['pending','rejected']:
            c=claim(); c['verification']['status']=status
            self.assertEqual(approval_claims([c],'t1','u1'),[])
        self.assertEqual(approval_claims([claim()],'t1','u1'),[claim()])
    def test_rejects_cross_owner(self):
        for tenant,user in [('other','u1'),('t1','other')]:
            with self.assertRaises(ValueError): approval_claims([claim()],tenant,user)
    def test_rejects_duplicate_claim(self):
        with self.assertRaises(ValueError): approval_claims([claim(),claim()],'t1','u1')
    def test_verified_requires_review(self):
        for field in ['reviewer_id','reviewed_at']:
            c=claim(); c['verification'][field]=None
            with self.assertRaises(ValidationError): validate_record(c,'claim')
    def test_rejects_invalid_timestamp_and_source(self):
        c=claim(); c['verification']['reviewed_at']='yesterday'
        with self.assertRaises(ValidationError): validate_record(c,'claim')
        c=claim(); c['source']['sha256']='invalid'
        with self.assertRaises(ValidationError): validate_record(c,'claim')
    def test_evaluation_size_boundaries(self):
        for count, passed in [(0,False),(49,False),(50,True),(100,True),(101,False)]:
            self.assertEqual(evaluation_report(records(count))['dataset_gate_passed'],passed)
    def test_requires_all_tiers(self):
        data=records()
        for row in data: row['label']='strong'
        self.assertFalse(evaluation_report(data)['dataset_gate_passed'])
    def test_rejects_synthetic(self):
        data=records(); data[0]['synthetic']=True
        with self.assertRaises(ValueError): evaluation_report(data)
    def test_rejects_duplicate_text_and_ids(self):
        for field in ['id','jd_text']:
            data=records(); data[1][field]=data[0][field]
            with self.assertRaises(ValueError): evaluation_report(data)
