# R05: quadratic cost of eliminating a block

**Result: the uniform bound $`\beta(f)=O(s(f))`$ is false.** There are total
Boolean functions with $`\beta(f)=\Theta(s(f)^2)`$, even when success is
weakened to eliminating **any one minimal sensitive block** at each input.
The lower bound permits adaptive queries. Quadratic growth is optimal:

```math
\beta(f)\le\deg(f)\le s_0(f)s_1(f)\le s(f)^2.
```

Here $`\beta`$ is the local, every-input cost defined in [R04](round-4.md).
The bounds concern the cost of one batch, not a counterexample to T01.
The lower bounds below are repository derivations; no historical novelty is
claimed.

## General failure mechanism: untouched witness supports

Fix a background input $`z`$. For witnesses $`x_j`$ and maximum disjoint
minimal-block families $`\mathcal F_j`$ at those witnesses, define

```math
S_j=\{i:x_{j,i}\ne z_i\}\ \cup\!
\bigcup_{B\in\mathcal F_j}B.
```

Follow any algorithm's answers on $`z`$. If its queried set misses $`S_j`$,
then $`x_j`$ is consistent with the transcript and its entire maximum family
survives. Every successful transcript must therefore hit every $`S_j`$:

```math
\beta(f)\ge\tau(\{S_j\}).
```

Here $`\tau`$ is the minimum hitting-set size. The query choices may be fully
adaptive. If each $`\mathcal F_j`$ contains **all** minimal blocks at $`x_j`$,
the same argument also forbids eliminating even one block there.

For cyclic translates of one support of size $`q`$ on $`n`$ coordinates,
each queried coordinate hits $`q`$ of the $`n`$ translates. The bound becomes
$`\beta(f)\ge\lceil n/q\rceil`$. The analogous incidence argument applies
to any transitive permutation group preserving the background.

## Elementary family with an exact batch cost

Choose $`t\ge3`$ and put $`k=3(t-1)`$. For each unordered pair of vertices of
$`K_t`$, introduce **three Boolean coordinates**. In a pair $`u\lt v`$,
value 0 favors $`u`$ and value 1 favors $`v`$. Let $`p_v`$ fix all coordinates
incident to $`v`$ to favor $`v`$, and write $`S_v`$ for its support.
Define $`g_t=1`$ precisely when some $`p_v`$ is satisfied.

Each $`S_v`$ has size $`k`$. Any two certificates disagree on their three
shared coordinates, and each coordinate belongs to exactly two supports.
The sets of inputs satisfying different certificates have Hamming distance
at least 3.

Consequently $`s_0(g_t)=1`$: a 0-input can be one bit from at most one such
set, with a unique erroneous literal. At a 1-input exactly one certificate
is satisfied, all its $`k`$ coordinates are sensitive, and every minimal
sensitive block is one of those singletons. Thus $`s_1(g_t)=k`$.
These elementary separated-certificate facts also appear in
[S06, Lemmas 3–4](literature.md#sources).

Now take an OR of $`m=k`$ disjoint copies:

```math
F_t=\bigvee_{j=1}^{k}g_t^{(j)},\qquad
N=3k\binom{t}{2},\qquad s_0(F_t)=s_1(F_t)=k.
```

At a 0-input, sensitivities add across copies. At a 1-input, only a sole
true copy can contribute sensitive coordinates, giving the stated values.

**Adaptive lower bound.** Use the background with triple `001` on every
edge in every copy; every copy evaluates to 0. If the transcript misses
some $`S_v`$ in copy $`j`$, impose $`p_v`$ there and leave all other bits
as in the background. This consistent 1-input has exactly the $`k`$ sensitive
singletons in that support as its minimal blocks. All remain untouched.

Every copy must therefore have all its vertex supports hit. A coordinate
hits only two vertices, so at least $`\lceil t/2\rceil`$ queries per copy
are necessary.

**Matching nonadaptive upper bound.** In each copy choose an edge cover of
$`K_t`$ with $`\lceil t/2\rceil`$ edges, and query one coordinate per chosen
edge. This hits every $`S_v`$.

At any 1-input of $`F_t`$, local block sensitivity is $`k`$: combine the
$`\ell`$th sensitive coordinate of each true copy into a block, for each
$`1\le\ell\le k`$. These $`k`$ blocks are disjoint, and any satisfied
certificate gives the matching upper bound. After the queries, a satisfied
certificate has at most $`k-1`$ unqueried literals, so local block sensitivity
drops.

At a 0-input of $`g_t`$, let $`D_v`$ be the coordinates disagreeing with
$`p_v`$. The $`t`$ sets $`D_v`$ are nonempty and partition all coordinates:
the two endpoints demand opposite values on each coordinate. They are
exactly the minimal sensitive blocks, since flipping $`D_v`$ satisfies
$`p_v`$. Hence every 0-input of $`F_t`$ has $`kt`$ disjoint minimal blocks
partitioning all coordinates. Any nonempty query set eliminates at least
one, strictly lowering local block sensitivity.

This proves the exact formula

```math
\beta(F_t)=k\left\lceil\frac t2\right\rceil,\qquad
\frac{\beta(F_t)}{s(F_t)}
=\left\lceil\frac t2\right\rceil\longrightarrow\infty.
```

In particular, $`\beta(F_t)=\Theta(k^2)=\Theta(s(F_t)^2)`$. At the planted
1-inputs, the unique maximum family contains every minimal block; the weaker
“eliminate any one block” task has the same exact cost on this family.

**Scope boundary.** Here $`bs_0(F_t)=kt`$ and $`bs_1(F_t)=k`$.
Any single query strictly lowers the **global** maximum block sensitivity
on both answers: it destroys one of the partition blocks at every 0-input,
and $`k\lt kt-1`$. Thus this quadratic obstruction does not refute a
batch scheme requiring only global-maximum progress.

## Upper bounds and the limit of the old obstruction

Query the support of a maximum-degree monomial of a nonconstant $`f`$.
After fixing its complement arbitrarily, its top coefficient remains
nonzero, so the resulting function is nonconstant. At every input, the
queried support therefore contains a sensitive block. Any maximum family
avoiding that support could be extended by this block, a contradiction.
This proves $`\beta(f)\le\deg(f)`$ using the mechanism in L04.
L05 supplies $`\deg(f)\le s_0(f)s_1(f)`$, proving the opening universal bound.

A different useful upper bound is
$`\beta(f)\le c_0(f)+c_1(f)-1`$, where $`c_b(f)=\min_{x:f(x)=b}C(f,x)`$.
Query the union of supports of minimum opposite-output certificates.
Their supports intersect because their assignments must conflict.
At every input the opposite certificate supplies a sensitive block contained
in this union.

For a monotone function every minimal $`b`$-certificate has size at most
$`s_b`$: set precisely its required 1s, or dually its required 0s, to obtain
a sensitivity witness. Complementing input coordinates preserves the
conclusion for every **unate** function. Thus

```math
\beta(f)\le s_0(f)+s_1(f)-1\le2s(f)-1
\qquad(f\text{ nonconstant and unate}).
```

R04's balanced AND–OR family attains this bound. Its factor approaching 2
cannot be amplified beyond all constants by monotone composition.

## Cyclically invariant companion

The mechanism also applies with cyclic symmetry. Chakraborty's pattern
function has $`n=a^3`$ coordinates, $`a\ge8`$, sensitivity $`\Theta(a)`$,
and a certificate support $`S`$ of size $`6a-2`$. Its zero-extended witness
has every support coordinate sensitive, so its minimal blocks are exactly
those singletons.
[S07, Section 3, Claim 3.3, pp. 56–57](https://dmtcs.episciences.org/552/pdf#page=6)

Following the all-zero transcript and counting translated supports gives
$`\beta\ge\lceil a^3/(6a-2)\rceil`$. Together with the universal upper bound,
this is another $`\Theta(s^2)`$ separation, even within cyclically invariant
total functions. The explicit pattern and compact witnesses are in the
[script](../scripts/cyclic_block_drop.py) and
[evidence](../evidence/round-5-cyclic-witnesses.json).

## Randomized extension and proof-scheme consequence

Suppose a classical randomized query procedure must succeed at each input
with probability at least $`p\gt0`$. On each planted star-family input,
success requires querying its support. Using the same random choices on
that input and the background gives identical answers until the support is
first hit, so the hitting event has the same probability on both inputs.
There are $`kt`$ supports; each query meets only two. Consequently

```math
\mathbb E[\text{queries on the background}]
\ge \frac{p\,kt}{2}=\Omega(s(F_t)^2)
\qquad(p\text{ fixed}).
```

This covers bounded error as well as exact deterministic algorithms.
The success condition is block elimination at the actual input; demanding
success for all completions of the resulting leaf can only be stronger.

**PS04.** Requiring progress simultaneously at every input can itself consume
the entire quadratic sensitivity budget. Further candidates should examine
global-maximum progress or amortized costs, and must prove their own bounds.
This result does not settle either alternative or T01.

## Verification

The star-family tests exhaust all 512 inputs of the three-vertex inner
gadget, independently checking sensitivities and minimal blocks. Compact
checks verify larger certificate incidences, planted witnesses, and the
matching edge-cover batches. The cyclic checks evaluate all single-bit flips
at explicit witnesses and all shifts for $`a=8,9,12,16`$.
These finite checks supplement the general proofs; they do not enumerate
the large truth tables.

```sh
python3 -m unittest discover -s tests
python3 -m scripts.star_block_drop --output evidence/round-5-star-witnesses.json
python3 -m scripts.cyclic_block_drop --output evidence/round-5-cyclic-witnesses.json
```
