# Research record

Target: **T01.** Every total Boolean function satisfies $`D(f)\le s(f)bs(f)`$.
The exact formulation and folklore attribution were supplied by the project
owner; published attribution remains unresolved. See the [glossary](glossary.md)
for notation and [literature](literature.md) for source-backed starting points.

## Proof contract

**P01 (proved, elementary).** Suppose a potential is defined on every restriction
of $`f`$, is nonnegative on constants, and satisfies

```math
\forall g\text{ nonconstant}\quad
\exists i\in\mathrm{Rel}(g)\quad
\forall a\in\{0,1\}:\quad
\Phi(g|_{i=a})\le\Phi(g)-1.
```

Then $`D(f)\le\Phi(f)`$: choose such an $`i`$ at each node and telescope along
every path to a constant. Thus the independent initial bound
$`\Phi(f)\le s(f)bs(f)`$ would prove T01. Existence of a favorable answer,
expected progress, or decrease only after an uncharged batch is insufficient.
For decrement $`\delta>0`$ and terminal lower bound $`L`$, the bound instead is
$`\lfloor(\Phi(f)-L)/\delta\rfloor`$; constants cannot be suppressed.

Exact $`D`$ is a validation reference, not a proposed independently justified
potential. A counterexample to an obligation of P01 is not a counterexample
to T01.

After finding a failure, seek its broadest proved form before selecting the
next candidate: generalize the mechanism, distinguish exact coefficients from
unbounded losses, test adaptive and weaker variants, and establish scope
boundaries. Follow the [research workflow](workflow.md).

## Baseline: extremal-parameter potentials

**B01 (proved).** For

```math
F_{m,k}=\bigvee_{j=1}^{m}\bigwedge_{\ell=1}^{k}x_{j,\ell},
\qquad m,k\ge2,
```

```math
(s_0,bs_0,C_0)=(m,m,m),\quad
(s_1,bs_1,C_1)=(k,k,k),\quad D=mk.
```

A 0-certificate chooses one zero in each term; a 1-certificate fixes all
variables of one term. Inputs with exactly one zero per term, or exactly one
satisfied term, respectively realize sensitivities $`m`$ and $`k`$. The
inequalities $`s_b\le bs_b\le C_b`$ give equality. The representing multilinear
polynomial has a nonzero monomial containing all $`mk`$ variables, so
$`D\ge\deg=mk`$; querying all variables matches this.

Fixing **any** coordinate to 1 leaves all terms nonempty and an untouched
length-$`k`$ term. The same certificate and sensitivity witnesses show that
all six maxima are preserved.

**F01: preserved maxima (proved mechanism).** Every potential depending only on
$`(s_0,s_1,bs_0,bs_1,C_0,C_1)`$ therefore fails P01 on this family.
This includes $`bs_0+bs_1`$, $`bs`$, $`bs_0bs_1`$, $`s\,bs`$, and $`C_0C_1`$,
regardless of how their values are rescaled. The four-variable case has
$`D=s\,bs=bs_0+bs_1=4`$, but the 1-answer preserves the sum for every query.

**F02: insufficient range (proved mechanism).** For $`m=k=t\ge3`$,
$`D=t^2>2t=bs_0+bs_1`$. With terminal floor zero and unit query charges, the
unscaled sum cannot pay for all queries even if batching is permitted.
Separately, on a dictator its initial value is 2 while $`s\,bs=1`$, so its
normalization also violates the requested budget. These are different failures.

## Proof-scheme review after the baseline

**PS01 (proposed direction).** Preserve more than extrema: certificate sizes,
their multiplicities, or sensitive-block incidence may record changes hidden
by F01. Any refinement still needs its own initial-budget proof.

**PS02 (known template, not a proof of T01).** Query a whole certificate or
maximum-degree monomial, and charge its actual size. The source-backed
certificate and monomial algorithms in the literature record establish
weaker bounds without requiring block sensitivity to drop after each bit.
The elementary certificate construction $`C\le s\,bs`$ alone does not give a
decision algorithm: answers may disagree with the input whose certificate
was chosen.

## Computational evidence

The baseline audit exhaustively enumerates all truth tables through four
variables, including constants and functions with irrelevant displayed
coordinates. It checks the initial budget, P01, and the independent diagnostic
$`D>\Phi`$, separately. It saves a first counterexample and both successor
values for every relevant query.

Reproduce:

```sh
python3 -m unittest discover -s tests
python3 -m scripts.audit --max-vars 4 --output evidence/baseline.json
```

The [baseline evidence](../evidence/baseline.json) is finite verification;
B01, F01, and F02 above are analytical proofs.

## Failure-informed rounds

| Round | Refinement | Disposition |
| --- | --- | --- |
| [R01](round-1.md) | Count prime-certificate literals instead of maxima | Progress proved; parity gives unbounded budget excess |
| [R02](round-2.md) | Count each relevant coordinate once | Progress proved; addressing gives unbounded budget excess |
| [R03](round-3.md) | Query for guaranteed relevance loss, then count that algorithm's depth | Progress proved; two independent selectors defeat the fixed tie rule |
| [R04](round-4.md) | Eliminate a block from every maximum family at every input within $`s`$ adaptive queries | Refuted: exact cost $`m+k-1>s`$ on disjoint AND–OR |
| [R05](round-5.md) | Allow any constant multiple of $`s`$ for block elimination | Refuted: exact family cost $`s\lceil t/2\rceil=\Theta(s^2)`$; quadratic is optimal |
| [R06](round-6.md) | Require progress only at inputs attaining global $`bs`$ | Refuted: separated certificate subcubes give $`\beta_{\max}=\Theta(s^2)`$ even with $`bs=s`$ |

Each round states its exact definition, an analytical failure mechanism, finite
checks, and reproduction commands. The initial baseline contains 65,814
functions; none violates T01. This does not prove T01 outside that finite set.

## First milestone conclusions

The baseline and all three new rounds are complete. None establishes T01;
none remains an untested or tentative candidate. R01–R03 each has a complete
progress proof and an unbounded family of budget failures. The [final scheme
review](round-3.md#final-scheme-review-and-next-obligation) proposes costed batches
or explicit algorithmic state, with a precise missing accounting lemma.

The next priority is a candidate that shares charges across certificates while
recognizing relevance eliminated by several answers together. A new scalar
combination of the six maxima is already excluded by F01. Changing the greedy
tie rule alone requires fresh evaluation; the R03 proof refutes only the
stated rule, not all relevance-based algorithms.

## Block-elimination proposal

**F03: simultaneous local progress is too costly (proved).** The proposed
$`s`$-query batch lowering local block sensitivity at every input already
fails on $`F_{2,2}`$: $`s=2`$ but three queries are necessary, even adaptively.
[R04](round-4.md) proves the exact cost $`m+k-1`$ for $`F_{m,k}`$.
For a known input, querying any minimal sensitive block does suffice within
$`s`$; the failure concerns one algorithm for every unknown input.

**PS03: amortize unequal batch costs.** On $`F_{t,t}`$, successive batches
of costs at most $`2t-1,2t-3,\ldots,1`$ achieve the desired elimination and
total exactly $`t^2=s\,bs`$ in the worst case. Thus this stronger batch
lemma is false on a family satisfying the target with equality.
A general account paying actual batch costs remains open.

## Generalizing block-elimination failures

**F04: untouched witness supports (proved).** Fix a background input and
witnesses with maximum block families. Each successful transcript on the
background must hit every set containing a witness's disagreements and its
whole family. Thus the transversal number of these supports lower-bounds
$`\beta`$, even for adaptive algorithms.

[R05](round-5.md) gives an elementary family with
$`s=3(t-1)`$ and $`\beta=s\lceil t/2\rceil`$. Its planted inputs have only
sensitive singletons, so the same quadratic lower bound holds for eliminating
any one minimal block, and extends to bounded-error randomized procedures.
A cyclically invariant family supplies a second application.

The general monomial bound $`\beta\le\deg\le s_0s_1\le s^2`$ shows quadratic
growth is optimal. In contrast, every unate function satisfies
$`\beta\le s_0+s_1-1`$: R04's factor approaching 2 is sharp for that entire
class, and cannot refute $`O(s)`$ by monotone amplification.

**PS04: reconsider which inputs require progress.** The elementary quadratic
example nevertheless lowers global $`bs`$ after any single query. Its failure
therefore isolates the simultaneous local requirement. A global-progress
scheme is a separate question, addressed by R06 below; an amortized account
remains an unproved direction.

## Global-maximum progress also has quadratic cost

**F05: distant certificates with hard-to-hit supports (proved).**
[R06](round-6.md) proves that progress only at original block-sensitivity
maximizers is exactly global $`bs`$ decrease. A probabilistic family still
requires $`\Theta(s^2)`$ adaptive deterministic queries for one such decrease.

The general mechanism is exact. Let $`g`$ accept the union of certificate
subcubes of common codimension $`q`$, pairwise distance at least three.
Let $`\tau`$ be the transversal number of their supports and $`b=bs_0(g)`$.
For $`mb\lt q`$, the OR of $`m`$ disjoint copies satisfies

```math
s(F)=bs(F)=q,\qquad \beta_{\max}(F)=m\tau.
```

Linear distance between these subcubes bounds $`b`$ by a constant. Exponentially
many random partial assignments with half their variables specified have that
distance and $`\tau=\Omega(q)`$ simultaneously. Taking $`m=\Theta(q)`$
makes the hard 1-inputs global maximizers and gives the quadratic lower bound.
This escapes R05's obstruction, where $`b`$ grew with the support transversal.
The existence proof, including explicit probability bounds, is independent of
the finite checks. No historical novelty or bounded-error randomized lower
bound is claimed.

**PS05: global progress still requires amortization or another measure.**
The constructed functions have only $`s\,bs/32`$ input variables, so the
target conjecture holds for them by querying all variables. What fails is
the demand for a global $`bs`$ decrease within every $`O(s)`$ batch. A viable
scheme must account for unequal costs or larger decreases, or change its
progress measure; no such general accounting lemma is established here.
