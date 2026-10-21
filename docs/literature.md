# Literature baseline

The initial sources were checked against the linked full texts on **2026-10-20**;
S08–S09 were added and checked on **2026-10-21**. Page numbers below are the
papers' printed pages. All claims concern total Boolean functions unless
stated otherwise; notation follows the [glossary](glossary.md).

The exact target $`D(f)\le s(f)bs(f)`$ and its description as folklore are
user-supplied. This initial search did not locate a published attribution for that
exact inequality. The older $`D=O(bs^2)`$ question appears explicitly in S05,
Open problem 2, p. 16; it is weaker than the target since $`s\le bs`$.
This source records its historical status, not a new claim about the current
literature.

## Claims and mechanisms

### L01 — Restriction monotonicity (proved from definitions)

Each of $`D,s_b,bs_b,C_b,\deg`$ cannot increase under restriction. A sensitive
block in a restriction remains sensitive after extending its input by the fixed
bits. Restricting an original certificate gives a certificate with no more
literals. A decision tree or representing polynomial can likewise be restricted.
These facts provide nonincrease, not strict single-query progress.

### L02 — Small certificates from minimal blocks

**Published:** $`C(f)\le s(f)bs(f)`$, S05, Theorem 2, p. 10, attributed to
Nisan. S01, Lemma 5.2, pp. 7–8, displays the weaker $`C\le bs^2`$.

**Derived refinement:**

```math
C(f,x)\le s_{1-b}(f)\,bs(f,x)\quad(f(x)=b),\qquad
C_b(f)\le s_{1-b}(f)\,bs_b(f).
```

Take a maximum disjoint family of minimal sensitive blocks at $`x`$. Their union
is a certificate: an opposite-output completion would supply another disjoint
block. At $`x^B`$, every coordinate of a minimal block $`B`$ is sensitive, so
$`|B|\le s_{1-b}(f)`$. Sum over the family. This tracks output classes in the
proof of [S01, Lemma 5.2](https://arxiv.org/pdf/quant-ph/9802049v3#page=7);
the refined formula is not its named statement.

**Use:** an individual certificate fits the desired budget. Paying for repeated
certificates still requires an additional argument. Even eliminating one block
from every maximum family at every input can require more than $`s(f)`$
adaptive queries; [R04](round-4.md) proves an exact disjoint AND–OR obstruction
and explains the known-input versus uniform-algorithm distinction.

### L03 — Certificate-query algorithms

**Published:** $`D(f)\le C_1(f)bs(f)`$, S01, Lemma 5.3, p. 8.
Repeatedly query a consistent 1-certificate. If both outputs survive after
$`bs(f)`$ unsuccessful rounds, fix a surviving 0-input $`y`$. Its disagreements
with those 1-certificates, and with one further consistent 1-certificate,
give $`bs(f)+1`$ disjoint sensitive blocks at that same $`y`$.
[S01](https://arxiv.org/pdf/quant-ph/9802049v3#page=8)

Output complementation and $`bs\le\max(C_0,C_1)`$ give

```math
D\le\min(C_0,C_1)bs\le C_0C_1.
```

The final inequality is also explicitly S05, Corollary 2, p. 16.
Together with L02 this yields $`D\le s\,bs^2`$, with an extra $`bs`$ relative
to the target. [S05](https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf#page=16)

### L04 — Querying a monomial: $`D\le\deg\,bs`$

**Published within a proof:** S02, Lemma 3 and proof of Theorem 4, pp. 3–4.
Query all variables in a maximum-degree monomial of the current exact polynomial.
For every input, that support contains a sensitive block: fixing all coordinates
outside it leaves a nonconstant polynomial. Successive rounds use disjoint
coordinates, hence certify disjoint sensitive blocks at the actual input.
There are at most $`bs(f)`$ rounds, each of cost at most $`\deg(f)`$.
The proof states $`D(f)\le\deg(f)bs(f)`$ explicitly before deriving the displayed
Theorem 4 bound $`D(f)\le2\deg(f)^3`$.
[S02](https://arxiv.org/pdf/quant-ph/0403168v2#page=3)

**Use:** count progress across batches, charging their actual query sizes.
Merely replacing the maximum-degree monomial cost by $`s(f)`$ needs a new lemma.
The same support argument gives $`\beta(f)\le\deg(f)`$; [R05](round-5.md)
shows that a universal $`O(s)`$ replacement is false for local block elimination.

### L05 — The degree baseline gives $`D\le s_0s_1bs`$

**Published:** $`\deg(f)\le\lambda(f)^2`$, S03, Theorem 1, pp. 1, 6;
$`\lambda(f)^2\le s_0(f)s_1(f)`$, Lemma 31, p. 31.
The latter bounds the norm of the bipartite sensitivity matrix by its maximum
row and column sums. Equation (66), p. 31, explicitly records
$`\deg(f)\le s_0(f)s_1(f)`$.
[S03](https://arxiv.org/pdf/2010.12629v1#page=31)

**Derived combination with L04:**

```math
D(f)\le s_0(f)s_1(f)bs(f)\le s(f)^2bs(f).
```

This meets the exact target when $`\min(s_0,s_1)=1`$; otherwise it retains a
factor $`\min(s_0,s_1)`$. The degree bound alone does not establish the target.

### L06 — Minimum certificates need restriction closure

**Published:** S04, Section 4, equation (16), p. 8:

```math
D(f)\le
\bigl(\mathrm{ndeg}(f)+\mathrm{ndeg}(\neg f)\bigr)
C_{\min}^{\downarrow}(f).
```

Querying a minimum certificate decreases one polynomial degree. Restriction can
remove every easiest input, increasing $`C_{\min}`$; the closure controls this.
[S04](https://eccc.weizmann.ac.il/report/2026/005/revision/2/download/#page=8)

### L07 — A polynomial potential with batch progress

**Published:** S04, Definition 12 and Lemma 6, p. 12:

```math
\Psi(p)=\sum_{\varnothing\ne M\in\mathcal M(p)}3^{|M|}|M|!,
```

where $`\mathcal M(p)`$ comprises inclusion-maximal monomials. It never increases
under restriction. For a nondeterministic polynomial $`p`$ of nonconstant $`g`$
and any $`x\in g^{-1}(0)`$, some query set of size $`O(RC_x(g))`$ reduces
$`\Psi`$ by a factor at most $`3/4`$, for every answer assignment.
The factorial **multiplies** $`3^{|M|}`$.
[S04](https://eccc.weizmann.ac.il/report/2026/005/revision/2/download/#page=12)

**Use:** query batches and multiplicative progress are viable modifications;
neither an $`s\,bs`$ budget nor unit-query progress follows.

### L08 — Separated certificates and cyclic sparse witnesses

**Published:** S06, Lemmas 3–4, pp. 7, 9, give the OR-composition sensitivity
identities and describe functions whose accepting inputs form certificate
subcubes separated by Hamming distance at least 3. Such functions have
$`s_0=1`$; the fixed certificate coordinates are sensitive at each accepting
input. [S06](https://eccc.weizmann.ac.il/report/2018/205/download/#page=9)

**Published:** S07, Section 3, Claim 3.3, pp. 56–57, defines a cyclic pattern
on $`n`$ variables with $`6a-2`$ fixed positions,
$`s_1=6a-2`$, and $`s_0=\Theta(n/a^2)`$. The pattern extended by zeros
has all fixed positions sensitive. Taking $`n=a^3`$ gives $`s=\Theta(a)`$.
[S07](https://dmtcs.episciences.org/552/pdf#page=6)

**New use in this repository:** R05 converts these certificate witnesses into
adaptive-query lower bounds through hitting sets. The exact star-family
formula and the cyclic $`\Omega(s^2)`$ block-elimination lower bound are
derived here; they are not statements attributed to S06 or S07.

### L09 — Amortizing shortest-certificate queries

**Published:** S08, Lemma 6 and its proof in Section 5, pp. 27:13–27:14,
repeatedly query a shortest certificate of the current restriction, allowing
either output. The proof establishes

```math
D(f)\le C_{\min}^{\downarrow}(f)\bigl(bs_0(f)+bs_1(f)\bigr)
\le2C_{\min}^{\downarrow}(f)bs(f).
```

The paper writes $`C_{\min}^{*}`$ for our restriction closure
$`C_{\min}^{\downarrow}`$. Each certificate batch removes an opposite-output
sensitive block, controlling the number of batches of each output.
[S08](https://drops.dagstuhl.de/storage/00lipics/lipics-vol284-fsttcs2023/LIPIcs.FSTTCS.2023.27/LIPIcs.FSTTCS.2023.27.pdf#page=13)

**Local refinements:** [R08](round-8.md) uses the progress index
$`bs_0+bs_1-1`$, keeps separate shortest-certificate costs at different
block-sensitivity levels, and converts batch accounts to unit-query state
credit. These refinements are derived here. Neither the published bound nor
these accounts establish the target budget; R08 gives an unbounded obstruction.

### L10 — A recursively composed family with uniform local parameters

**Published:** S09, Example 2.9, p. 7, defines

```math
\alpha_2(x_1,x_2,x_3,x_4)
=(x_1\oplus x_2)(x_3\oplus x_4)\oplus x_2\oplus x_4.
```

Lemma 3.13, p. 20, gives composition bounds for sensitivity, block sensitivity,
and certificate complexity. Theorem 3.14, p. 21, applies them to the balanced
$`d`$-fold composition on $`4^d`$ variables, obtaining $`s=2^d`$ and
$`bs=C=3^d`$. These local parameters are uniform over inputs.
[S09](https://eccc.weizmann.ac.il/report/2013/191/revision/2/download/#page=21)

**New use in this repository:** R08's $`G(u,a,b,v)`$ equals
$`\alpha_2(u,v,a,b)`$. Its addressing substitution, restrictions realizing
every intermediate certificate/block-sensitivity level, and the resulting
failure of certificate-profile budgets are local derivations, not statements
attributed to S09.

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
| S06 | Chaubal, Gál, *New Constructions with Quadratic Separation between Sensitivity and Block Sensitivity*, [ECCC TR18-205](https://eccc.weizmann.ac.il/report/2018/205/download/), 2018; Lemmas 3–4, pp. 7, 9. |
| S07 | Chakraborty, *On the sensitivity of cyclically-invariant Boolean functions*, [DMTCS 13:4 (2011), 51–60](https://dmtcs.episciences.org/552/pdf); Section 3, Claim 3.3, pp. 56–57. |
| S08 | Chugh, Podder, Sanyal, *Decision Tree Complexity Versus Block Sensitivity and Degree*, [FSTTCS 2023, Article 27](https://drops.dagstuhl.de/storage/00lipics/lipics-vol284-fsttcs2023/LIPIcs.FSTTCS.2023.27/LIPIcs.FSTTCS.2023.27.pdf); Lemma 6 and Section 5, pp. 27:13–27:14. |
| S09 | Savický, *Boolean functions with a vertex-transitive group of automorphisms*, [ECCC TR13-191 revision 2](https://eccc.weizmann.ac.il/report/2013/191/revision/2/download/), [2015-05-14](https://eccc.weizmann.ac.il/report/2013/191/); Example 2.9, p. 7; Lemma 3.13, p. 20; Theorem 3.14, p. 21. |

The search covered these sources and targeted queries for the exact target,
including `"D(f)" "s(f)bs(f)" conjecture` and
`"deterministic" "sensitivity times block sensitivity"`. It is a focused baseline,
not an exhaustive bibliographic review. Source dates are version dates, not
claims of first discovery. Detailed local candidates and failure mechanisms
belong in [research.md](research.md).
