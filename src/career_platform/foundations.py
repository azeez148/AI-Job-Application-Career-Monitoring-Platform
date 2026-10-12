"""Validate Phase 0 contracts. No network, model, database or send access."""
import argparse
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]

def validate_record(record, schema_name):
    schema = json.loads((ROOT / 'schemas' / f'{schema_name}.schema.json').read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(record)

def approval_claims(claims, tenant_id, user_id):
    """Fail closed for malformed/cross-owner records; exclude unverified claims.

    This foundation filter is not authorization. Phase 1 must derive identity
    from authenticated sessions and resolve verification from database records.
    """
    result = []
    seen = set()
    for claim in claims:
        validate_record(claim, 'claim')
        if claim['tenant_id'] != tenant_id or claim['user_id'] != user_id:
            raise ValueError('Claim ownership mismatch')
        if claim['claim_id'] in seen:
            raise ValueError('Duplicate claim identifier')
        seen.add(claim['claim_id'])
        if claim['verification']['status'] == 'verified':
            result.append(claim)
    return result

def evaluation_report(records, minimum=50, maximum=100):
    seen_ids, seen_text, labels = set(), set(), set()
    for record in records:
        validate_record(record, 'evaluation')
        if record['synthetic']:
            raise ValueError('Synthetic data cannot satisfy a phase gate')
        digest = hashlib.sha256(' '.join(record['jd_text'].lower().split()).encode()).hexdigest()
        if record['id'] in seen_ids or digest in seen_text:
            raise ValueError('Duplicate evaluation record')
        seen_ids.add(record['id'])
        seen_text.add(digest)
        labels.add(record['label'])
    return {'count': len(records), 'labels': sorted(labels),
            'dataset_gate_passed': minimum <= len(records) <= maximum and labels == {'strong', 'maybe', 'skip'}}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset', type=Path)
    args = parser.parse_args()
    try:
        records = [json.loads(line) for line in args.dataset.read_text().splitlines() if line.strip()]
        policy = json.loads((ROOT / 'config/policy.json').read_text())['quality']
        report = evaluation_report(records, policy['minimum_evaluation_records'], policy['maximum_evaluation_records'])
        print(json.dumps(report))
        return 0 if report['dataset_gate_passed'] else 1
    except (ValueError, OSError) as error:
        parser.exit(2, f'Dataset validation failed: {type(error).__name__}\n')
    except Exception as error:
        from jsonschema.exceptions import ValidationError
        if isinstance(error, ValidationError):
            parser.exit(2, 'Dataset validation failed: invalid record schema\n')
        raise

if __name__ == '__main__':
    raise SystemExit(main())
