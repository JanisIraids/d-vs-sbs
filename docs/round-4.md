# R04: eliminating a block from every maximum family

**Result: refuted for a uniform adaptive algorithm.** The four-variable function
$`F_{2,2}=(x_0\land x_1)\lor(x_2\land x_3)`$ has sensitivity 2, but needs
3 queries to achieve the proposed elimination at every input. More generally,
the exact cost for $`F_{m,k}`$, the OR of $`m`$ disjoint width-$`k`$ ANDs, is
$`m+k-1`$. These are local derivations, with no claim of historical novelty.

## Exact condition and the known-input distinction

Write $`\mathcal B_x(g)`$ for the minimal sensitive blocks at $`x`$.
Fixing coordinates $`Q`$ according to $`x`$ eliminates precisely the blocks
intersecting $`Q`$:

```math
\mathcal B_{x_{\bar Q}}(g|_{x_Q})
=\{B\in\mathcal B_x(g):B\cap Q=\varnothing\}.
```

Sensitivity of any remaining block, and of every subset of it, is unchanged.
Thus eliminating at least one block from **every maximum disjoint family**
is equivalent to strictly decreasing local block sensitivity.

Define the **block-elimination cost** $`\beta(g)`$ as the minimum worst-case
depth of a deterministic query tree whose every leaf restriction $`\rho`$
satisfies

```math
\forall x\supseteq\rho:\qquad
bs(g|_\rho,x_{\overline{\mathrm{dom}(\rho)}})<bs(g,x).
```

Set $`\beta(g)=0`$ for constant $`g`$, where elimination is vacuous.
The thresholds on the right refer to the function **at the start of the
batch**, not to an intermediate restriction. The proposed lemma is
$`\beta(g)\le s(g)`$. If true universally, its iteration would prove T01:
each round lowers local block sensitivity along the actual input, so there
are at most $`bs(f)`$ rounds, each costing at most $`s(f)`$.

For a **known input** $`x`$, the analogous assertion is true. Choose any
minimal sensitive block $`B`$ at $`x`$. It intersects some member of every
maximum disjoint family; otherwise it could be added to that family.
Querying $`B`$ therefore suffices, and $`|B|\le s(g)`$ by the minimal-block
lemma underlying the certificate proof. See
[S05, Lemma 3 and Theorem 2, p. 10](https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf#page=10).
This gives an input-dependent set, not one query algorithm that finds the
required coordinates for every unknown input.

## Four-variable counterexample, including adaptivity

For $`f=F_{2,2}`$, $`s(f)=2`$ and $`bs(f,x)=2`$ at every input.
At a 0-input, the zero coordinates in each AND term form two disjoint minimal
blocks. At a 1-input, two disjoint minimal blocks each select one coordinate
from every satisfied term. A certificate of size 2 gives the matching upper
bound in both cases.

By symmetry the first query is $`x_0`$; answer **1**. There are only two
types of second query:

| Second query | Answer | Residual function | Consistent input $`(x_0,x_1,x_2,x_3)`$ | Untouched maximum family |
| --- | --- | --- | --- | --- |
| $`x_1`$ | 0 | $`x_2\land x_3`$ | $`(1,0,1,1)`$ | $`\{\{2\},\{3\}\}`$ |
| $`x_2`$ (or symmetrically $`x_3`$) | 1 | $`x_1\lor x_3`$ | $`(1,0,1,0)`$ | $`\{\{1\},\{3\}\}`$ |

Each surviving family has two minimal blocks, all disjoint from the queried
coordinates. Consequently two adaptive queries cannot suffice. Three queries
always leave at most one variable, so $`\beta(F_{2,2})=3>2=s(F_{2,2})`$.
Nevertheless $`D(F_{2,2})=4=s(F_{2,2})bs(F_{2,2})`$.

## Exact family: cost of simultaneous progress

For $`m,k\ge2`$, the local values are
$`bs(F_{m,k},x)=m`$ on 0-inputs and $`bs(F_{m,k},x)=k`$ on 1-inputs.
At a 0-input the zero set of each term is a minimal block, and a
0-certificate has size $`m`$. At a 1-input construct $`k`$ disjoint blocks,
each choosing one coordinate in every satisfied term; one satisfied term is
a certificate of size $`k`$. Also $`s(F_{m,k})=\max(m,k)`$ by B01.

**Upper bound.** Query one whole term and one coordinate in every other term.
This costs $`m+k-1`$. If the full term is true, the restriction is constant.
Otherwise at most $`m-1`$ terms survive, each of width at most $`k-1`$.
The residual local block sensitivity is at most $`m-1`$ on 0-inputs and
$`k-1`$ on 1-inputs, as witnessed by certificates of those sizes.

**Adaptive lower bound.** In each term, answer its first $`k-1`$ queries 1
and its last query 0. A term is therefore either untouched, partly queried,
or fully queried and false.

- If no term is false yet, setting all remaining bits to 0 gives a consistent
  0-input with residual block sensitivity $`m`$: every term retains its
  nonempty zero block.
- If some term is false but another is untouched, make that untouched term
  true and set all other unqueried bits to 0. Its $`k`$ singleton blocks form
  an untouched maximum family at this consistent 1-input.

A successful leaf must therefore fully query some term and touch every other
term, costing at least $`k+(m-1)`$. Hence

```math
\beta(F_{m,k})=m+k-1>\max(m,k)=s(F_{m,k}).
```

On the balanced family, $`bs(F_{t,t},x)=t`$ for every input. The same proof
therefore refutes even the weaker requirement that every leaf have
**global** block sensitivity below its original value: that too costs
$`2t-1`$, approaching twice the sensitivity.

## Consequence for the proof scheme

At a nonconstant successful leaf, progress on 0-inputs requires eliminating a
term, whereas progress on 1-inputs requires shortening every surviving term.
Adaptivity does not avoid the cost of meeting both conditions.

**PS03 (family calculation; universal extension open).** Allow unequal batch
costs with explicit amortization. The upper-bound batch leaves at most
$`m-1`$ terms of width $`k-1`$, and

```math
m+k-1=mk-(m-1)(k-1).
```

Repeating on $`F_{t,t}`$ costs at most
$`(2t-1)+(2t-3)+\cdots+1=t^2=s\,bs`$. Thus the first batch exceeds $`s`$
while the full algorithm meets the conjectured budget. The missing general
lemma is an account bounded initially by $`s\,bs`$ whose drop pays each
batch's actual cost. This family calculation supplies no such account for
arbitrary total functions.

## Reproducible finite evidence

The exact evaluator retains original local thresholds and optimizes over both
answers to every possible next query. Its stopping condition is independently
checked by enumerating maximum families. See
[evidence](../evidence/round-4-witnesses.json) and
[implementation](../scripts/block_drop.py).

All **278** truth tables through three variables satisfy $`\beta\le s`$,
so the four-variable counterexample has minimum arity by exhaustive check.
Exact computations give costs 3, 4, 4, and 5 for $`F_{2,2}`$, $`F_{2,3}`$,
$`F_{3,2}`$, and $`F_{3,3}`$, respectively. The global-only costs for the
two unbalanced examples are both 2; their local and global conditions differ.

```sh
python3 -m unittest discover -s tests
python3 -m scripts.block_drop --output evidence/round-4-witnesses.json
```
