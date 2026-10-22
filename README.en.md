# An infinite family of counterexamples to a two-row Schubert coefficient bound

[中文](README.md)

This repository gives an infinite family of counterexamples to **Conjecture 1.3 as printed** in Tao–Zheng's 2024 preprint, *Bounds on Schubert Coefficients in the Two-Row Case*. One example has coefficient $9$, exceeding the proposed bound $6$.

Priority has not been established. The general problem of finding a positive combinatorial counting rule for arbitrary Schubert structure constants remains unresolved. See [status.json](status.json) and [NOTICE.md](NOTICE.md) for the scope and review status.

## The statement and counterexample

Schubert structure constants are the nonnegative integers in

$$
\mathfrak S_u\mathfrak S_v=\sum_w c_{u,v}^{w}\mathfrak S_w.
$$

The conjecture considers $w\in S_{n_2}$ and a $k$-Grassmannian permutation $\tau\in S_{n_1}$ corresponding to a two-row partition $\lambda$, and proposes

$$
0\le c_{w,\tau}^{v}\le n_2-k.
$$

The original statement is on page 2 of [arXiv:2411.19735v1](https://arxiv.org/pdf/2411.19735v1). Its hypotheses are checked explicitly in the proof.

For every integer $m\ge6$, set

$$
k=m+1,\qquad n_2=2m+1,\qquad n_1=3m-1,
$$

$$
\mu=(m,m-1,\ldots,1,0),\qquad
\nu=(m,m,m-1,\ldots,2,1),\qquad
\lambda=(m-2,2).
$$

The associated $k$-Grassmannian permutations satisfy all parameters of the conjecture, while

$$
c_{w,\tau}^{v}=c_{\mu,\lambda}^{\nu}
=\binom m2-m
=\frac{m(m-3)}2
>m=n_2-k.
$$

For $m=6$, this is $9>6$, with $k=7$, $n_2=13$, and $n_1=17$.

The skew diagram $\nu/\mu$ consists of $m$ cells in distinct rows and columns. The Littlewood–Richardson rule reduces the coefficient to a ballot-word count. A second proof uses Jacobi–Trudi and Pieri. The proofs establish the infinite family; the exact computations provide additional checks. The example at $m=6$ is not claimed to be a smallest counterexample among all possible inputs.

## Read and reproduce

- [Full proof in Chinese](docs/proof.zh-CN.md)
- [Mathematical summary in English](docs/summary.en.md)
- [Exact verification code](scripts/verify_counterexample.py) and [archived certificate](data/counterexample_certificate.json)
- [References](references.md), [status](status.json), [notice](NOTICE.md), and [SHA-256 checksums](SHA256SUMS)

Use **Python 3.10+**; only the standard library is required. From the repository root, run:

```sh
python reproduce.py
```

Results are written to `reproduction-output/` by default. To choose another directory:

```sh
python reproduce.py --output-dir my-output
```

Compare the results with the archived certificate and the formulas in the proof. Finite computational checks do not replace the proof of the infinite family.

## Scope

An accurate description is: “An infinite family of counterexamples to Conjecture 1.3 as printed in Tao–Zheng (2024), with $c_{w,\tau}^{v}=m(m-3)/2>m=n_2-k$.”

This result has not undergone external peer review, and no claim of first discovery is made. Source attribution and AI-assistance information are recorded in [NOTICE.md](NOTICE.md). Independent review of the statement, proof, and code is welcome.
