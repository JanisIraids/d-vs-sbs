# Literature baseline

Checked against the linked full texts on **2026-10-20**. Page numbers below are
the papers' printed pages. All claims concern total Boolean functions unless
stated otherwise; notation follows the [glossary](glossary.md).

The exact target $D(f)\le s(f)bs(f)$ and its description as folklore are
user-supplied. This initial search did not locate a published attribution for that
exact inequality. The older $D=O(bs^2)$ question appears explicitly in S05,
Open problem 2, p. 16; it is weaker than the target since $s\le bs$.
This source records its historical status, not a new claim about the current
literature.

## Claims and mechanisms

### L01 — Restriction monotonicity (proved from definitions)

Each of $D,s_b,bs_b,C_b,\deg$ cannot increase under restriction. A sensitive
block in a restriction remains sensitive after extending its input by the fixed
bits. Restricting an original certificate gives a certificate with no more
literals. A decision tree or representing polynomial can likewise be restricted.
These facts provide nonincrease, not strict single-query progress.

### L02 — Small certificates from minimal blocks

**Published:** $C(f)\le s(f)bs(f)$, S05, Theorem 2, p. 10, attributed to
Nisan. S01, Lemma 5.2, pp. 7–8, displays the weaker $C\le bs^2$.

**Derived refinement:**
$$
C(f,x)\le s_{1-b}(f)\,bs(f,x)\quad(f(x)=b),\qquad
C_b(f)\le s_{1-b}(f)\,bs_b(f).
$$
Take a maximum disjoint family of minimal sensitive blocks at $x$. Their union
is a certificate: an opposite-output completion would supply another disjoint
block. At $x^B$, every coordinate of a minimal block $B$ is sensitive, so
$|B|\le s_{1-b}(f)$. Sum over the family. This tracks output classes in the
proof of [S01, Lemma 5.2](https://arxiv.org/pdf/quant-ph/9802049v3#page=7);
the refined formula is not its named statement.

**Use:** an individual certificate fits the desired budget. Paying for repeated
certificates still requires an additional argument.

### L03 — Certificate-query algorithms

**Published:** $D(f)\le C_1(f)bs(f)$, S01, Lemma 5.3, p. 8.
Repeatedly query a consistent 1-certificate. If both outputs survive after
$bs(f)$ unsuccessful rounds, fix a surviving 0-input $y$. Its disagreements
with those 1-certificates, and with one further consistent 1-certificate,
give $bs(f)+1$ disjoint sensitive blocks at that same $y$.
[S01](https://arxiv.org/pdf/quant-ph/9802049v3#page=8)

Output complementation and $bs\le\max(C_0,C_1)$ give
$$
D\le\min(C_0,C_1)bs\le C_0C_1.
$$
The final inequality is also explicitly S05, Corollary 2, p. 16.
Together with L02 this yields $D\le s\,bs^2$, with an extra $bs$ relative
to the target. [S05](https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf#page=16)

### L04 — Querying a monomial: $D\le\deg\,bs$

**Published within a proof:** S02, Lemma 3 and proof of Theorem 4, pp. 3–4.
Query all variables in a maximum-degree monomial of the current exact polynomial.
For every input, that support contains a sensitive block: fixing all coordinates
outside it leaves a nonconstant polynomial. Successive rounds use disjoint
coordinates, hence certify disjoint sensitive blocks at the actual input.
There are at most $bs(f)$ rounds, each of cost at most $\deg(f)$.
The proof states $D(f)\le\deg(f)bs(f)$ explicitly before deriving the displayed
Theorem 4 bound $D(f)\le2\deg(f)^3$.
[S02](https://arxiv.org/pdf/quant-ph/0403168v2#page=3)

**Use:** count progress across batches, charging their actual query sizes.
Merely replacing the maximum-degree monomial cost by $s(f)$ needs a new lemma.

### L05 — The degree baseline gives $D\le s_0s_1bs$

**Published:** $\deg(f)\le\lambda(f)^2$, S03, Theorem 1, pp. 1, 6;
$\lambda(f)^2\le s_0(f)s_1(f)$, Lemma 31, p. 31.
The latter bounds the norm of the bipartite sensitivity matrix by its maximum
row and column sums. Equation (66), p. 31, explicitly records
$\deg(f)\le s_0(f)s_1(f)$.
[S03](https://arxiv.org/pdf/2010.12629v1#page=31)

**Derived combination with L04:**
$$
D(f)\le s_0(f)s_1(f)bs(f)\le s(f)^2bs(f).
$$
This meets the exact target when $\min(s_0,s_1)=1$; otherwise it retains a
factor $\min(s_0,s_1)$. The degree bound alone does not establish the target.

### L06 — Minimum certificates need restriction closure

**Published:** S04, Section 4, equation (16), p. 8:
$$
D(f)\le
\bigl(\operatorname{ndeg}(f)+\operatorname{ndeg}(\neg f)\bigr)
C_{\min}^{\downarrow}(f).
$$
Querying a minimum certificate decreases one polynomial degree. Restriction can
remove every easiest input, increasing $C_{\min}$; the closure controls this.
[S04](https://eccc.weizmann.ac.il/report/2026/005/revision/2/download/#page=8)

### L07 — A polynomial potential with batch progress

**Published:** S04, Definition 12 and Lemma 6, p. 12:
$$
\Psi(p)=\sum_{\varnothing\ne M\in\mathcal M(p)}3^{|M|}|M|!,
$$
where $\mathcal M(p)$ comprises inclusion-maximal monomials. It never increases
under restriction. For a nondeterministic polynomial $p$ of nonconstant $g$
and any $x\in g^{-1}(0)$, some query set of size $O(RC_x(g))$ reduces
$\Psi$ by a factor at most $3/4$, for every answer assignment.
The factorial **multiplies** $3^{|M|}$.
[S04](https://eccc.weizmann.ac.il/report/2026/005/revision/2/download/#page=12)

**Use:** query batches and multiplicative progress are viable modifications;
neither an $s\,bs$ budget nor unit-query progress follows.

## What the baseline requires of new candidates

- Check the initial budget, terminal bound, and both answers to the selected
  query separately.
- Distinguish a monotone complexity measure from a strictly decreasing potential.
- When using an input minimizing a quantity, control that quantity on all later
  restrictions; the original minimum may disappear.
- For batches, account for every queried coordinate. A bound on the number of
  rounds is not a bound on the number of queries.
- Keep exact constants separate from asymptotic bounds. The candidate search
  starts with exact rational or integer arithmetic.

These are research-design consequences of the mechanisms above, not additional
published theorems.

## Sources

| ID | Verified edition and locations |
| --- | --- |
| S01 | Beals, Buhrman, Cleve, Mosca, de Wolf, *Quantum Lower Bounds by Polynomials*, [arXiv quant-ph/9802049v3](https://arxiv.org/pdf/quant-ph/9802049v3), 1998-09-30; Lemmas 5.2–5.3, pp. 7–8. |
| S02 | Midrijanis, *Exact quantum query complexity for total Boolean functions*, [arXiv quant-ph/0403168v2](https://arxiv.org/pdf/quant-ph/0403168v2), 2004-03-27; Lemma 3 and Theorem 4 proof, pp. 3–4. |
| S03 | Aaronson, Ben-David, Kothari, Rao, Tal, *Degree vs. Approximate Degree and Quantum Implications of Huang's Sensitivity Theorem*, [arXiv 2010.12629v1](https://arxiv.org/pdf/2010.12629v1), [submitted 2020-10-23](https://arxiv.org/abs/2010.12629); Theorem 1, Lemma 31, equation (66). |
| S04 | Kothari, Kovacs-Deak, Wang, Yang, *Rational degree is polynomially related to degree*, [ECCC TR26-005 revision 2](https://eccc.weizmann.ac.il/report/2026/005/revision/2/download/), [2026-09-28](https://eccc.weizmann.ac.il/report/2026/005/); Section 4, equation (16), Definition 12, Lemma 6. |
| S05 | Buhrman, de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, [author-hosted manuscript](https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf), dated 2002-10-10; Theorem 2, p. 10, and Corollary 2 / Open problem 2, p. 16. Used for its reproduced arguments and explicit historical statements. |

The search covered these sources and targeted queries for the exact target,
including `"D(f)" "s(f)bs(f)" conjecture` and
`"deterministic" "sensitivity times block sensitivity"`. It is a focused baseline,
not an exhaustive bibliographic review. Source dates are version dates, not
claims of first discovery. Detailed local candidates and failure mechanisms
belong in [research.md](research.md).
