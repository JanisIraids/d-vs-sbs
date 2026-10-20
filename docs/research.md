# Research record

Target: **T01.** Every total Boolean function satisfies \(D(f)\le s(f)bs(f)\).
The exact formulation and folklore attribution were supplied by the project
owner; published attribution remains unresolved. See the [glossary](glossary.md)
for notation and [literature](literature.md) for source-backed starting points.

## Proof contract

**P01 (proved, elementary).** Suppose a potential is defined on every restriction
of \(f\), is nonnegative on constants, and satisfies
\[
\forall g\text{ nonconstant}\quad
\exists i\in\operatorname{Rel}(g)\quad
\forall a\in\{0,1\}:\quad
\Phi(g|_{i=a})\le\Phi(g)-1.
\]
Then \(D(f)\le\Phi(f)\): choose such an \(i\) at each node and telescope along
every path to a constant. Thus the independent initial bound
\(\Phi(f)\le s(f)bs(f)\) would prove T01. Existence of a favorable answer,
expected progress, or decrease only after an uncharged batch is insufficient.
For decrement \(\delta>0\) and terminal lower bound \(L\), the bound instead is
\(\lfloor(\Phi(f)-L)/\delta\rfloor\); constants cannot be suppressed.

Exact \(D\) is a validation reference, not a proposed independently justified
potential. A counterexample to an obligation of P01 is not a counterexample
to T01.

## Baseline: extremal-parameter potentials

**B01 (proved).** For
\[
F_{m,k}=\bigvee_{j=1}^{m}\bigwedge_{\ell=1}^{k}x_{j,\ell},
\qquad m,k\ge2,
\]
\[
(s_0,bs_0,C_0)=(m,m,m),\quad
(s_1,bs_1,C_1)=(k,k,k),\quad D=mk.
\]
A 0-certificate chooses one zero in each term; a 1-certificate fixes all
variables of one term. Inputs with exactly one zero per term, or exactly one
satisfied term, respectively realize sensitivities \(m\) and \(k\). The
inequalities \(s_b\le bs_b\le C_b\) give equality. The representing multilinear
polynomial has a nonzero monomial containing all \(mk\) variables, so
\(D\ge\deg=mk\); querying all variables matches this.

Fixing **any** coordinate to 1 leaves all terms nonempty and an untouched
length-\(k\) term. The same certificate and sensitivity witnesses show that
all six maxima are preserved.

**F01: preserved maxima (proved mechanism).** Every potential depending only on
\((s_0,s_1,bs_0,bs_1,C_0,C_1)\) therefore fails P01 on this family.
This includes \(bs_0+bs_1\), \(bs\), \(bs_0bs_1\), \(s\,bs\), and \(C_0C_1\),
regardless of how their values are rescaled. The four-variable case has
\(D=s\,bs=bs_0+bs_1=4\), but the 1-answer preserves the sum for every query.

**F02: insufficient range (proved mechanism).** For \(m=k=t\ge3\),
\(D=t^2>2t=bs_0+bs_1\). With terminal floor zero and unit query charges, the
unscaled sum cannot pay for all queries even if batching is permitted.
Separately, on a dictator its initial value is 2 while \(s\,bs=1\), so its
normalization also violates the requested budget. These are different failures.

## Proof-scheme review after the baseline

**S01 (proposed direction).** Preserve more than extrema: certificate sizes,
their multiplicities, or sensitive-block incidence may record changes hidden
by F01. Any refinement still needs its own initial-budget proof.

**S02 (known template, not a proof of T01).** Query a whole certificate or
maximum-degree monomial, and charge its actual size. The source-backed
certificate and monomial algorithms in the literature record establish
weaker bounds without requiring block sensitivity to drop after each bit.
The elementary certificate construction \(C\le s\,bs\) alone does not give a
decision algorithm: answers may disagree with the input whose certificate
was chosen.

## Computational evidence

The baseline audit exhaustively enumerates all truth tables through four
variables, including constants and functions with irrelevant displayed
coordinates. It checks the initial budget, P01, and the independent diagnostic
\(D>\Phi\), separately. It saves a first counterexample and both successor
values for every relevant query.

Reproduce:

```sh
python3 -m unittest discover -s tests
python3 -m scripts.audit --max-vars 4 --output evidence/baseline.json
```

The [baseline evidence](../evidence/baseline.json) is finite verification;
B01, F01, and F02 above are analytical proofs.
