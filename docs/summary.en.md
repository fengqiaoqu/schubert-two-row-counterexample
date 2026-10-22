# An infinite family violating a two-row Schubert coefficient bound

Date: 2026-10-22.

This note gives counterexamples to Conjecture 1.3, **as stated**, on page 2 of Tao–Zheng, *Bounds on Schubert Coefficients in the Two-Row Case*, arXiv:2411.19735v1. The conjecture bounds the coefficient in a product of an arbitrary Schubert polynomial and a two-row Schur polynomial by $n_2-k$. The family below has coefficient $m(m-3)/2$ and conjectured bound $m$, for every integer $m\ge6$.

Priority has not been established, and this note has not undergone external peer review. Internal mathematical and computational checks are not external peer review. The general positive combinatorial rule problem for arbitrary Schubert structure constants (03-0007) remains unresolved.

See the [full Chinese proof](proof.zh-CN.md), [references](../references.md), [computation certificate](../data/counterexample_certificate.json), and [verification script](../scripts/verify_counterexample.py).

## The conjecture being tested

Let $\tau\in S_{n_1}$ be $k$-Grassmannian with associated two-row partition $\lambda$, let $w\in S_{n_2}$, and set $n=\max(n_1,n_2)$. The printed conjecture asserts that the coefficients in

$$
\mathfrak S_w s_\lambda(x_1,\ldots,x_k)
=\sum_{v\in S_n}c_{w,\tau}^{v}\mathfrak S_v
$$

satisfy $0\le c_{w,\tau}^{v}\le n_2-k$. Its statement does not include the additional hypotheses $n_2-k<\lambda_2$ or a decreasing tail of $w$ that appear in the preceding Theorem 1.2.

## The family

For $m\ge6$, set

$$
k=m+1,\qquad n_2=2m+1,\qquad n_1=3m-1,
$$

$$
\mu=(m,m-1,\ldots,1,0),\qquad
\nu=(m,m,m-1,\ldots,2,1),\qquad
\lambda=(m-2,2).
$$

For a partition $\rho$ with at most $k$ parts, pad it with zeros and define $g_k(\rho)$ by taking its first $k$ values to be $i+\rho_{k+1-i}$, $1\le i\le k$, followed by the unused positive integers in increasing order. Then

$$
g_k(\rho)\in S_{k+\rho_1},\qquad
\mathfrak S_{g_k(\rho)}=s_\rho(x_1,\ldots,x_k).
$$

Take $w=g_k(\mu)$, $v=g_k(\nu)$, and $\tau=g_k(\lambda)$, padding $\tau$ by fixed points to $S_{3m-1}$. Explicitly,

$$
w=(1,3,\ldots,2m+1,\ 2,4,\ldots,2m),
$$

$$
v=(2,4,\ldots,2m,2m+1,\ 1,3,\ldots,2m-1).
$$

Both have their unique descent at $k$. The minimal symmetric group containing $w$ is $S_{2m+1}$.

**Theorem.** These parameters satisfy

$$
\boxed{
c_{w,\tau}^{v}=c_{\mu,\lambda}^{\nu}
=\binom m2-\binom m1
=\frac{m(m-3)}2>m=n_2-k.
}
$$

The ratio of the actual coefficient to the conjectured bound is $(m-3)/2$, which is unbounded.

## Two proofs of the coefficient

The skew diagram $\nu/\mu$ consists of the $m$ cells $(r,m+2-r)$, $2\le r\le m+1$. They lie in distinct rows and distinct columns. Its LR tableaux of content $(m-2,2)$ are therefore exactly the ballot words containing $m-2$ ones and two twos. Reflection of the first prefix having one more two than one bijects the bad words with words of content $(m-1,1)$. Thus the count is $\binom m2-m$.

Alternatively, Jacobi–Trudi gives

$$
s_{(m-2,2)}=h_{m-2}h_2-h_{m-1}h_1.
$$

Every subset of the isolated cells can be added to $\mu$ while retaining a partition, and both the subset and its complement are horizontal strips. Two applications of Pieri therefore give coefficients $\binom m2$ and $m$ for $s_\nu$ in the two terms, respectively. Their difference proves the same formula.

The finite summation range causes no ambiguity: every surviving Schur output $\rho$ has at most $k$ rows and first part at most $\mu_1+\lambda_1=2m-2$. Consequently $g_k(\rho)\in S_{k+\rho_1}\subseteq S_{3m-1}$. The entire stable polynomial product fits the conjecture's stated $S_n$ range.

## An explicit instance and the computation certificate

At $m=6$, the parameters are $k=7$, $n_2=13$, $n_1=17$, with

$$
w=(1,3,5,7,9,11,13,2,4,6,8,10,12),
$$

$$
\tau=(1,2,3,4,5,8,11,6,7,9,10,12,13,14,15,16,17),
$$

$$
v=(2,4,6,8,10,12,13,1,3,5,7,9,11).
$$

Their lengths are $21$, $6$, and $27$, respectively. The coefficient is $9>13-7=6$. All nine LR reading words are listed in the full proof.

The certificate also includes a **different**, smaller-$k$ example: $k=6$, $\mu=(5,4,3,2,1,0)$, $\nu=(6,5,4,3,2,1)$, $\lambda=(4,2)$, $n_2=12$, and $n_1=15$. Its coefficient is again $9>6$. The certificate's top-level parameters refer to this example; its `infinite_family` field records the family above.

The Python standard-library script checks fifteen family members, $m=6,\ldots,20$. For the separate $k=6$ example, it additionally constructs Schur polynomials from semistandard tableaux, checks Jacobi–Trudi, and obtains $9$ using both a $720$-term alternant extraction and $21$ divided differences. These finite checks supplement the two uniform proofs; they neither establish priority nor resolve the general Schubert counting problem.

Run from the repository root:

```bash
python scripts/verify_counterexample.py
```
