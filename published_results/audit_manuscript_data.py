#!/usr/bin/env python3
"""Read-only checks of packaged aggregate evidence; never runs a decoder.

Python 3.10+ is sufficient for hash/count checks. SciPy is optional and enables
recalculation of the saved exact binomial tests and CP component intervals.
Output is printed unless --output is explicitly supplied. This script neither
opens raw shot truth nor fits a model, and does not recreate timing bootstraps.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def audit(root: Path) -> dict[str, Any]:
    failures: list[str] = []
    checks = 0
    def check(ok: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not ok:
            failures.append(label)
    def close(a: float, b: float, label: str) -> None:
        check(math.isclose(a, b, rel_tol=2e-10, abs_tol=2e-12), label)

    for manifest in ('FIGURE_PROVENANCE.csv', 'DATA_PROVENANCE.csv'):
        for entry in rows(root / manifest):
            path = root / entry['package_file']
            check(path.is_file(), f"missing:{path.name}")
            if path.is_file():
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                check(digest == entry['sha256'], f"hash:{path.name}")
    c10 = json.loads((root / 'data_C10_primary.json').read_text())
    c12 = rows(root / 'data_C12_pairs.csv')
    cost = c10['primary_cost']
    close(cost['ratio'], cost['candidate_amortized_seconds'] / cost['reference_amortized_seconds'], 'C10 service ratio')
    close(cost['reduction'], 1.0 - cost['ratio'], 'C10 reduction')
    check(cost['one_sided95_ratio_upper'] < .8, 'C10 frozen cost guard')
    records = c10['high_noise_sector_bounds'] + c12
    for i, r in enumerate(records):
        n, ce, re_, h, res = (int(r[k]) for k in ('N','candidate_errors','reference_errors','harms','rescues'))
        both, correct = int(r['both_wrong']), int(r['both_correct'])
        label = f"paired row {i}"
        check(ce == both + h and re_ == both + res, label + ': marginal counts')
        check(n == both + correct + h + res, label + ': total')
        check(ce - re_ == h - res, label + ': excess identity')
        d = float(r.get('net_risk_difference', r.get('net_risk', 'nan')))
        close(d, (h-res)/n, label + ': risk difference')
        if r.get('ratio') not in (None, ''):
            close(float(r['ratio']), float(r['candidate_service_ms'])/float(r['reference_service_ms']), label + ': service ratio')
    for r in rows(root/'data_C12_accuracy.csv'):
        cats = sum(int(r[k]) for k in ('no_path','invalid_or_undefined_output','nonempty_terminal_truth_missing','truth_present_wrong_terminal_choice'))
        check(cats == int(r['errors']), r['cohort'] + '/' + r['method'] + ': failure partition')
        check(int(r['correct']) + int(r['errors']) == int(r['N']), r['cohort'] + '/' + r['method'] + ': denominator')
    for r in rows(root/'data_compiler_summary.csv'):
        blocks, events = int(r['blocks']), int(r['events_per_direction'])
        predicted = 2 * 8 * (16*blocks + 2*16*events)
        check(predicted == int(r['numeric_two_direction_bytes']), r['model'] + ': payload formula')
        close(float(r['numeric_two_direction_MiB']), predicted/(1024**2), r['model'] + ': MiB')
    statistical = 'SKIPPED: SciPy is not installed; integrity and arithmetic checks still ran.'
    try:
        import scipy
        from scipy.stats import beta, binom
    except ImportError:
        pass
    else:
        def lower(k: int, n: int) -> float:
            return 0.0 if k == 0 else float(beta.ppf(.0125, k, n-k+1))
        def upper(k: int, n: int) -> float:
            return 1.0 if k == n else float(beta.ppf(.9875, k+1, n-k))
        for i, r in enumerate(records):
            n, h, res = (int(r[k]) for k in ('N','harms','rescues'))
            lo, hi = lower(h,n)-upper(res,n), upper(h,n)-lower(res,n)
            saved_lo = float(r.get('CP_net_lower',r.get('net_risk_95_lower','nan')))
            saved_hi = float(r.get('CP_net_upper',r.get('net_risk_95_upper','nan')))
            close(lo,saved_lo,f'paired row {i}: CP lower')
            close(hi,saved_hi,f'paired row {i}: CP upper')
            if r.get('exact_one_sided_benefit_p') not in (None,''):
                p = float(binom.sf(res-1,h+res,.5)) if h+res else 1.0
                expected = float(r['exact_one_sided_benefit_p'])
                check(math.isclose(p, expected, rel_tol=1e-8, abs_tol=1e-300), f'paired row {i}: exact benefit p')
        statistical = f'Recomputed CP component bounds and saved exact paired one-sided tests using SciPy {scipy.__version__}.'
    return {'status': 'PASS' if not failures else 'FAIL', 'checks': checks,
            'failures': failures, 'paired_records': len(records),
            'statistical_checks': statistical,
            'scope': 'Aggregate-table arithmetic and copied-file integrity only. No new scientific samples, decoder calls, timing bootstrap, training, or independent hardware reproduction.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(args.root.resolve())
    text = json.dumps(result, indent=2)
    print(text)
    if args.output:
        args.output.write_text(text+'\n', encoding='utf-8')
    return 0 if result['status'] == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
