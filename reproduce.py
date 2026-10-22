#!/usr/bin/env python3
"""Reproduce every exact certificate and compare with the committed reference.

Run with Python 3.10+ from any working directory:
    python /path/to/repository/reproduce.py --output-dir /path/to/output

No dependencies beyond the standard library are required. The default output
is reproduction-output/ under this repository; data/ remains unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERIFIER = ROOT / 'scripts' / 'verify_counterexample.py'
REFERENCE = ROOT / 'data' / 'counterexample_certificate.json'
METADATA_FIELDS = frozenset({'source_file', 'source_sha256', 'run_command'})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path,
                        default=ROOT / 'reproduction-output',
                        help='Generated output directory (default: repo/reproduction-output).')
    args = parser.parse_args()
    try:
        if sys.version_info < (3, 10):
            raise RuntimeError('Python 3.10 or newer is required.')
        if not __debug__:
            raise RuntimeError('Run without -O so all exact assertions are active.')
        if (args.output_dir.expanduser().resolve() / REFERENCE.name) == REFERENCE.resolve():
            raise ValueError('Choose an output directory outside committed data/.')
        # run_path loads the actual published verifier without creating a
        # package or importing dependencies, and does not invoke its CLI.
        verifier = runpy.run_path(str(VERIFIER), run_name='schubert_public_verifier')
        report = verifier['build_certificate']()
        actual_source_hash = hashlib.sha256(VERIFIER.read_bytes()).hexdigest()
        if report['source_sha256'] != actual_source_hash:
            raise RuntimeError('The certificate does not identify the published verifier.')
        certificate = verifier['write_certificate'](report, args.output_dir)
        # Round-trip through JSON to normalize tuples and lists identically.
        actual = json.loads(certificate.read_text(encoding='utf-8'))
        expected = json.loads(REFERENCE.read_text(encoding='utf-8'))
        actual_stable = {key: value for key, value in actual.items()
                         if key not in METADATA_FIELDS}
        expected_stable = {key: value for key, value in expected.items()
                           if key not in METADATA_FIELDS}
        differing_fields = sorted(key for key in actual_stable.keys() | expected_stable.keys()
                                  if actual_stable.get(key) != expected_stable.get(key)
                                  or (key in actual_stable) != (key in expected_stable))
        if differing_fields:
            raise RuntimeError('Reference mismatch in fields: '+', '.join(differing_fields))
        result = verifier['summary'](report, certificate)
        result.update({'reference_comparison': 'passed',
                       'stable_fields_compared': len(actual_stable),
                       'metadata_fields_ignored': sorted(METADATA_FIELDS),
                       'published_verifier_sha256_checked': True})
        print(json.dumps(result, ensure_ascii=False), flush=True)
        return 0
    except (AssertionError, OSError, ValueError, RuntimeError) as error:
        print(json.dumps({'status': 'failed', 'error': str(error),
                          'error_type': type(error).__name__}, ensure_ascii=False),
              file=sys.stderr, flush=True)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
