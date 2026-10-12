import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from tests.unit.test_foundations import records

class CliTests(unittest.TestCase):
    def run_cli(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'evaluation.jsonl'; path.write_text(content)
            return subprocess.run([sys.executable,'-m','career_platform.foundations',str(path)],capture_output=True,text=True)
    def test_valid_contract_dataset(self):
        # Generated test fixtures exercise validation, never real quality evidence.
        result=self.run_cli('\n'.join(json.dumps(r) for r in records()))
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertTrue(json.loads(result.stdout)['dataset_gate_passed'])
    def test_insufficient_dataset(self):
        result=self.run_cli('')
        self.assertEqual(result.returncode,1)
        self.assertFalse(json.loads(result.stdout)['dataset_gate_passed'])
    def test_malformed_dataset(self):
        result=self.run_cli('{invalid')
        self.assertEqual(result.returncode,2)
    def test_invalid_schema_does_not_log_personal_data(self):
        result=self.run_cli(json.dumps({'private':'sensitive-resume-content'}))
        self.assertEqual(result.returncode,2)
        self.assertNotIn('sensitive-resume-content',result.stderr)
