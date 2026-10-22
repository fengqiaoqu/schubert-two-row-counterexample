"""Independent exact certificates for a counterexample to arXiv:2411.19735v1.

Run from the repository root: python reproduce.py
Python 3.10+ and its standard library only. The full exact calculation is always
run. Generated certificates go to reproduction-output/ by default; committed
data are never overwritten by this command.
This refutes the stated linear upper bound, not MathHub 03-0007's positive-rule
problem. The proof uses classical Littlewood--Richardson and Pieri rules.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations, permutations
from math import comb, factorial
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
WIDTH = 15
Mono = tuple[int, ...]
Poly = dict[Mono, int]
MU = (5, 4, 3, 2, 1, 0)
LAM = (4, 2)
NU = (6, 5, 4, 3, 2, 1)
K = 6


def add(p: Poly, q: Poly, scale: int = 1) -> Poly:
    out = dict(p)
    for m, c in q.items():
        out[m] = out.get(m, 0) + scale*c
    return {m: c for m, c in out.items() if c}


def multiply(p: Poly, q: Poly) -> Poly:
    out: Poly = {}
    for a, ca in p.items():
        for b, cb in q.items():
            m = tuple(x+y for x, y in zip(a, b))
            out[m] = out.get(m, 0) + ca*cb
    return out


def complete(degree: int, k: int) -> Poly:
    out: Poly = {}
    def visit(left: int, values: tuple[int, ...]) -> None:
        if len(values) == k-1:
            out[values+(left,)+(0,)*(WIDTH-k)] = 1
            return
        for exponent in range(left+1):
            visit(left-exponent, values+(exponent,))
    visit(degree, ())
    return out


def schur_tableaux(shape: tuple[int, ...], k: int) -> tuple[Poly, int]:
    cells = [(r, c) for r, length in enumerate(shape) for c in range(length)]
    entries: dict[tuple[int, int], int] = {}
    out: Poly = {}
    count = 0
    def visit(index: int, exponents: list[int]) -> None:
        nonlocal count
        if index == len(cells):
            m = tuple(exponents)+(0,)*(WIDTH-k)
            out[m] = out.get(m, 0)+1
            count += 1
            return
        r, c = cells[index]
        lower = max(1, entries.get((r, c-1), 1), entries.get((r-1, c), 0)+1)
        for value in range(lower, k+1):
            entries[r, c] = value
            exponents[value-1] += 1
            visit(index+1, exponents)
            exponents[value-1] -= 1
        entries.pop((r, c), None)
    visit(0, [0]*k)
    return out, count


def dd(p: Poly, i: int) -> Poly:
    """Zero-based index; exact integer monomial divided difference."""
    out: Poly = {}
    for m, coefficient in p.items():
        a, b = m[i], m[i+1]
        for j in range(abs(a-b)):
            e = list(m)
            if a > b:
                e[i], e[i+1] = a-1-j, b+j
                sign = 1
            else:
                e[i], e[i+1] = a+j, b-1-j
                sign = -1
            e = tuple(e)
            out[e] = out.get(e, 0)+sign*coefficient
    return {m: c for m, c in out.items() if c}


def grassmannian(shape: tuple[int, ...], k: int, n: int) -> tuple[int, ...]:
    padded = shape+(0,)*(k-len(shape))
    first = [i+1+padded[k-1-i] for i in range(k)]
    assert max(first) <= n
    return tuple(first+[x for x in range(1, n+1) if x not in first])


def right_deletion_order(w: tuple[int, ...]) -> tuple[int, ...]:
    current = list(w)
    out = []
    while any(current[i] > current[i+1] for i in range(len(w)-1)):
        i = next(i for i in range(len(w)-1) if current[i] > current[i+1])
        current[i], current[i+1] = current[i+1], current[i]
        out.append(i)
    assert current == list(range(1, len(w)+1))
    return tuple(out)


def horizontal_strip(outer: tuple[int, ...], inner: tuple[int, ...]) -> bool:
    return (all(outer[i] >= inner[i] for i in range(K))
            and all(inner[i] >= outer[i+1] for i in range(K-1)))


def check_infinite_family_examples() -> list[dict[str, object]]:
    """Check examples of the proved family, without padding w by fixed points.

    For every m>=6 take k=m+1, mu=(m,m-1,...,0), nu=(m,m,m-1,...,1),
    and lambda=(m-2,2). Exactly m isolated skew boxes remain in nu/mu.
    Ballot words of content (m-2,2) number C(m,2)-C(m,1)=m(m-3)/2.
    Choosing n2=2m+1 gives bound n2-k=m. This is exceeded for every m>=6.
    Finite examples confirm the formulas; the displayed argument is uniform.
    """
    records: list[dict[str, object]] = []
    for m in range(6, 21):
        k = m+1
        mu = tuple(range(m, -1, -1))
        nu = (m,)+tuple(range(m, 0, -1))
        shape = (m-2, 2)
        cells = [(r+1, nu[r]) for r in range(k) if nu[r] != mu[r]]
        assert len(cells) == m
        assert len({r for r, _ in cells}) == len({c for _, c in cells}) == m
        assert all(nu[r]-mu[r] in (0, 1) for r in range(k))
        lattice_words = []
        for twos in combinations(range(m), 2):
            word = tuple(2 if i in twos else 1 for i in range(m))
            if all(word[:j].count(1) >= word[:j].count(2) for j in range(1, m+1)):
                lattice_words.append(word)
        count = len(lattice_words)
        assert count == comb(m, 2)-comb(m, 1) == m*(m-3)//2
        hooks = [shape[r]-c+sum(length > c for length in shape[r+1:])
                 for r, length in enumerate(shape) for c in range(length)]
        hook_prod = 1
        for value in hooks:
            hook_prod *= value
        assert factorial(m)//hook_prod == count
        counts = []
        for boxes in (m-2, m-1):
            number = 0
            for selected in combinations(range(1, k), boxes):
                middle = tuple(mu[i]+int(i in selected) for i in range(k))
                assert all(middle[i] >= middle[i+1] for i in range(k-1))
                for outer, inner in ((middle, mu), (nu, middle)):
                    assert all(outer[i] >= inner[i] for i in range(k))
                    assert all(inner[i] >= outer[i+1] for i in range(k-1))
                number += 1
            counts.append(number)
        assert counts[0]-counts[1] == count
        n1, n2 = 3*m-1, 2*m+1
        w = grassmannian(mu, k, n2)
        v = grassmannian(nu, k, n2)
        tau = grassmannian(shape, k, n1)
        assert w[-1] != n2 and v[-1] != n2
        assert w == tuple(range(1, 2*m+2, 2))+tuple(range(2, 2*m+1, 2))
        assert v == (tuple(range(2, 2*m+1, 2))+(2*m+1,)
                     +tuple(range(1, 2*m, 2)))
        assert n1 == k+mu[0]+shape[0]
        assert count > n2-k == m
        records.append({'m': m, 'k': k, 'mu': mu, 'lambda': shape, 'nu': nu,
                        'n1': n1, 'n2': n2, 'coefficient': count,
                        'upper_bound': m, 'LR_word_count': count,
                        'pieri_counts': counts, 'w_in_S_n2': w,
                        'v_in_S_n2': v, 'tau_in_S_n1': tau,
                        'w_has_no_trailing_fixed_point': True,
                        'first_LR_word': lattice_words[0],
                        'last_LR_word': lattice_words[-1]})
    return records


def build_certificate() -> dict[str, object]:
    """Run every exact calculation and return a reproducible certificate."""
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10 or newer is required.")
    if not __debug__:
        raise RuntimeError('Run without -O so all exact assertions are active.')
    skew_cells = [(i+1, NU[i]) for i in range(K)]
    assert all(NU[i]-MU[i] == 1 for i in range(K))
    assert len({c for _, c in skew_cells}) == K
    words = []
    for twos in combinations(range(K), LAM[1]):
        word = [2 if i in twos else 1 for i in range(K)]
        if all(word[:j].count(1) >= word[:j].count(2) for j in range(1, K+1)):
            words.append(word)
    assert len(words) == 9
    hook_lengths = [LAM[r]-c+sum(length > c for length in LAM[r+1:])
                    for r, length in enumerate(LAM) for c in range(length)]
    hook_product = 1
    for value in hook_lengths:
        hook_product *= value
    hook_dimension = factorial(K)//hook_product
    assert hook_dimension == len(words) == comb(6, 2)-comb(6, 1) == 9
    pieri_counts = {}
    for boxes in (4, 5):
        allowed = []
        for selected in combinations(range(K), boxes):
            middle = tuple(MU[i]+int(i in selected) for i in range(K))
            if (all(middle[i] >= middle[i+1] for i in range(K-1))
                    and horizontal_strip(middle, MU)
                    and horizontal_strip(NU, middle)):
                allowed.append(middle)
        pieri_counts[boxes] = allowed
    assert len(pieri_counts[4]) == 15 and len(pieri_counts[5]) == 6
    assert len(pieri_counts[4])-len(pieri_counts[5]) == 9
    # A six-variable Schur polynomial is built by enumerating all SSYT,
    # independently of either LR coefficients or the Pieri calculation.
    smu, mu_tableau_count = schur_tableaux(MU, K)
    slam, lam_tableau_count = schur_tableaux(LAM, K)
    jt = add(multiply(complete(4, K), complete(2, K)),
             multiply(complete(5, K), complete(1, K)), -1)
    assert slam == jt
    staircase: Poly = {(0,)*WIDTH: 1}
    for i in range(K):
        for j in range(i+1, K):
            factor = {}
            for index in (i, j):
                e = [0]*WIDTH; e[index] = 1; factor[tuple(e)] = 1
            staircase = multiply(staircase, factor)
    assert smu == staircase
    # Alternant extraction: s_mu*a_delta=a_(mu+delta). The target monomial
    # in (s_mu*s_lambda)*a_delta has exponent nu+delta. Its coefficient is
    # c_(mu,lambda)^nu. Enumerate every one of the 6! alternant terms.
    delta = tuple(range(K-1, -1, -1))
    alternating_exponents = tuple(MU[i]+delta[i] for i in range(K))
    target = tuple(NU[i]+delta[i] for i in range(K))
    alternant_sum = 0
    nonzero_terms = []
    for perm in permutations(range(K)):
        difference = tuple(target[i]-alternating_exponents[perm[i]]
                           for i in range(K))
        if min(difference) < 0:
            continue
        sign = (-1)**sum(perm[i] > perm[j] for i in range(K)
                         for j in range(i+1, K))
        coefficient = slam.get(difference+(0,)*(WIDTH-K), 0)
        alternant_sum += sign*coefficient
        if coefficient:
            nonzero_terms.append({'permutation': perm, 'exponents': difference,
                                  'sign': sign, 'coefficient': coefficient})
    assert alternant_sum == 9 and len(nonzero_terms) == 1
    w = grassmannian(MU, K, 12)
    tau = grassmannian(LAM, K, 15)
    v = grassmannian(NU, K, 15)
    product = multiply(smu, slam)
    extracted = product
    order = right_deletion_order(v)
    stage_sizes = [len(extracted)]
    for i in order:
        extracted = dd(extracted, i)
        stage_sizes.append(len(extracted))
    assert len(order) == sum(NU) == sum(MU)+sum(LAM)
    assert extracted == {(0,)*WIDTH: 9}, extracted
    conjectured_bound = 12-K
    assert 9 > conjectured_bound
    family_records = check_infinite_family_examples()
    report = {
        'claim': 'Counterexample to Conjecture 1.3 as stated in arXiv:2411.19735v1',
        'scope': 'A two-row coefficient upper bound is disproved; the positive '
                 'combinatorial rule sought in MathHub 03-0007 remains unresolved.',
        'source': 'https://arxiv.org/pdf/2411.19735v1', 'source_location': 'Page 2, Conjecture 1.3',
        'mu': MU, 'lambda': LAM, 'nu': NU, 'k': K, 'n1': 15, 'n2': 12, 'n': 15,
        'w_in_S12': w, 'tau_in_S15': tau, 'v_in_S15': v,
        'coefficient': 9, 'conjectured_upper_bound': conjectured_bound,
        'coefficient_exceeds_bound': True,
        'skew_cells_row_column': skew_cells, 'LR_reading_words': words,
        'LR_count': len(words), 'hook_lengths': hook_lengths,
        'hook_dimension': hook_dimension,
        'pieri_h4_h2_intermediates': pieri_counts[4],
        'pieri_h5_h1_intermediates': pieri_counts[5],
        'pieri_counts': [len(pieri_counts[4]), len(pieri_counts[5])],
        'SSYT_counts': {'mu': mu_tableau_count, 'lambda': lam_tableau_count},
        'SSYT_support_sizes': {'mu': len(smu), 'lambda': len(slam), 'product': len(product)},
        'SSYT_vs_Jacobi_Trudi_lambda': True, 'SSYT_vs_staircase_product_mu': True,
        'alternant_terms_tested': factorial(K), 'alternant_nonzero_terms': nonzero_terms,
        'alternant_coefficient': alternant_sum,
        'divided_difference_order_one_based_chronological': [i+1 for i in order],
        'divided_difference_stage_support_sizes': stage_sizes,
        'divided_difference_final_constant': extracted[(0,)*WIDTH],
        'infinite_family': {
            'range': 'Every integer m>=6',
            'k': 'm+1', 'mu': '(m,m-1,...,0)',
            'nu': '(m,m,m-1,...,1)', 'lambda': '(m-2,2)',
            'n1': '3m-1', 'n2': '2m+1',
            'exact_coefficient': 'm(m-3)/2', 'conjectured_upper_bound': 'm',
            'proof': 'nu/mu consists of m distinct singleton rows in distinct '
                     'columns, so its LR tableaux are exactly ballot words with '
                     'm-2 ones and 2 twos. Their number is C(m,2)-C(m,1). '
                     'It exceeds m iff m>5. All products fit S_(3m-1) because '
                     'their Schur shapes have length<=m+1 and width<=2m-2.',
            'finite_examples_checked': family_records,
            'finite_example_count': len(family_records),
            'minimal_embedding_w': True},
        'finite_sum_boundary': 'Every Schur term has length at most 6 and first part '
                               'at most mu_1+lambda_1=9; hence its 6-Grassmannian '
                               'index lies in S15. All terms fit the stated n=max(n1,n2).',
        'source_file': 'scripts/verify_counterexample.py',
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'run_command': 'python reproduce.py',
        'novelty_boundary': 'A concrete mathematical refutation of the displayed '
                            'conjecture. A web search finding no prior refutation '
                            'does not establish priority or community acceptance.'}
    return report


def write_certificate(report: dict[str, object], output_dir: Path) -> Path:
    """Write runtime output while protecting the committed reference data."""
    output_dir = output_dir.expanduser().resolve()
    output_path = output_dir / 'counterexample_certificate.json'
    committed_path = PACKAGE_ROOT / 'data' / 'counterexample_certificate.json'
    if output_path == committed_path.resolve():
        raise ValueError('Choose an output directory outside committed data/.')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n',
                           encoding='utf-8', newline='\n')
    return output_path


def summary(report: dict[str, object], certificate: Path) -> dict[str, object]:
    """Return a compact machine-readable summary of the full computation."""
    family = report['infinite_family']
    return {'status': 'all exact assertions passed',
            'coefficient': report['coefficient'],
            'conjectured_bound': report['conjectured_upper_bound'],
            'LR_words': report['LR_count'], 'hook_dimension': report['hook_dimension'],
            'Pieri_counts': report['pieri_counts'], 'SSYT_counts': report['SSYT_counts'],
            'alternant_terms_tested': report['alternant_terms_tested'],
            'divided_difference_steps': len(report[
                'divided_difference_order_one_based_chronological']),
            'divided_difference_final_constant': report[
                'divided_difference_final_constant'],
            'family_examples_checked': family['finite_example_count'],
            'family_m_range': [family['finite_examples_checked'][0]['m'],
                               family['finite_examples_checked'][-1]['m']],
            'source_file': report['source_file'],
            'source_sha256': report['source_sha256'],
            'certificate': certificate.name}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path,
                        default=PACKAGE_ROOT / 'reproduction-output',
                        help='Generated output directory (default: repo/reproduction-output).')
    args = parser.parse_args()
    report = build_certificate()
    certificate = write_certificate(report, args.output_dir)
    print(json.dumps(summary(report, certificate), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
