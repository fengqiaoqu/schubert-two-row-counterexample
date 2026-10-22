# 两行 Schubert 系数线性上界猜想的无限反例族

[English](README.en.md)

本仓库给出一个无限反例族，否定 Tao–Zheng（2024）预印本 **Conjecture 1.3 按原文印出的陈述**。其中一个实例的 Schubert 系数为 $9$，而猜想给出的上界为 $6$。仓库包含完整证明、可复现的整数计算及来源记录。

发现优先权尚未确立。该结果针对一个具体的公开猜想；一般 Schubert 系数的正组合计数规则问题（原研究题号 03-0007）仍未解决。证据与核查范围见 [status.json](status.json) 和 [NOTICE.md](NOTICE.md)。

## 问题是什么

Schubert 多项式由排列标记，它们的乘积可以再写成 Schubert 多项式的整数线性组合：

$$
\mathfrak S_u\mathfrak S_v=\sum_w c_{u,v}^{w}\mathfrak S_w.
$$

这些非负整数 $c_{u,v}^{w}$ 称为 Schubert 系数。对于 Grassmannian 排列，Schubert 多项式就是 Schur 多项式，相应系数成为经典的 Littlewood–Richardson 系数。

Tao 和 Zheng 的预印本 *Bounds on Schubert Coefficients in the Two-Row Case*，第 2 页 Conjecture 1.3，考虑 $w\in S_{n_2}$ 与一个 $k$-Grassmannian 排列 $\tau\in S_{n_1}$ 的乘积，其中 $\mathfrak S_\tau=s_\lambda(x_1,\ldots,x_k)$，分拆 $\lambda$ 有两行。它对乘积中的系数提出线性上界

$$
0\le c_{w,\tau}^{v}\le n_2-k.
$$

原文 [PDF](https://arxiv.org/pdf/2411.19735v1) 与 [HTML](https://arxiv.org/html/2411.19735v1) 的表述一致。完整书目信息及假设核对见 [references.md](references.md)。

## 反例与证明

对每个整数 $m\ge6$，取

$$
k=m+1,\qquad n_2=2m+1,\qquad n_1=3m-1,
$$

$$
\mu=(m,m-1,\ldots,1,0),\qquad
\nu=(m,m,m-1,\ldots,2,1),\qquad
\lambda=(m-2,2).
$$

将这些分拆转换为下降位置相同的 $k$-Grassmannian 排列，便得到满足原猜想参数条件的 $w,\tau,v$，且

$$
c_{w,\tau}^{v}=c_{\mu,\lambda}^{\nu}
=\binom m2-m
=\frac{m(m-3)}2
>m=n_2-k.
$$

取 $m=6$，参数为 $k=7$、$n_2=13$、$n_1=17$，得到

$$
\boxed{c_{w,\tau}^{v}=9>13-7=6.}
$$

证明的关键是：斜形 $\nu/\mu$ 由 $m$ 个不同行、不同列的孤立格组成。Littlewood–Richardson 规则把目标系数化为具有 $m-2$ 个 $1$、两个 $2$ 的合法读词数；反射计数给出 $\binom m2-m$。另一个证明使用 Jacobi–Trudi 公式和两次 Pieri 计数。完整论证还检查了排列和有限对称群的范围，见[中文证明](docs/proof.zh-CN.md)。

这两份论证证明整个无限族；有限计算提供补充核验。$m=6$ 仅是上述家族的起点，不表示所有可能反例中的最小值。

## 从哪里读起

| 文件 | 内容 |
| --- | --- |
| [docs/proof.zh-CN.md](docs/proof.zh-CN.md) | 中文完整证明、具体排列和原猜想的假设核对 |
| [docs/summary.en.md](docs/summary.en.md) | 英文数学摘要 |
| [scripts/verify_counterexample.py](scripts/verify_counterexample.py) | 使用精确整数运算的验证代码 |
| [data/counterexample_certificate.json](data/counterexample_certificate.json) | 随仓库保存的计算证书 |
| [references.md](references.md) | 原始文献与来源记录 |
| [status.json](status.json) | 数学结论、验证状态和优先权边界 |
| [NOTICE.md](NOTICE.md) | 出处、AI 辅助及公开使用说明 |
| [SHA256SUMS](SHA256SUMS) | 所列文件的 SHA-256 校验值 |

## 复现

需要 **Python 3.10 或更高版本**，只使用 Python 标准库，无需安装第三方依赖。在仓库根目录执行：

```sh
python reproduce.py
```

默认将本次复现结果写入 `reproduction-output/`。也可以指定输出目录：

```sh
python reproduce.py --output-dir my-output
```

运行结果可与仓库保存的[计算证书](data/counterexample_certificate.json)及[证明中的公式](docs/proof.zh-CN.md)核对。计算涉及有限实例；无限族的结论由数学证明给出。

## 如何引用结论

建议准确表述为：

> 对 Tao–Zheng（2024）预印本 Conjecture 1.3 的如印陈述，给出一个无限反例族；该族中 $c_{w,\tau}^{v}=m(m-3)/2>m=n_2-k$，其中一个实例为 $9>6$。

该结论未确立发现优先权，尚未经外部同行评议。详细说明见 [NOTICE.md](NOTICE.md)。欢迎依据原文假设、完整证明和复现代码进行独立审查。
