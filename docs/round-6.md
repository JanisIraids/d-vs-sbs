# R06: quadratic cost even for global-maximum progress

**Result: the weakened requirement still has a quadratic counterexample.**
A probabilistically constructed family has $`s=bs`$ and
$`\beta_{\max}=\Theta(s^2)`$, even for adaptive deterministic queries.
The argument below proves existence for every sufficiently large parameter;
it is not inferred from finite experiments. These are repository derivations;
no historical novelty is claimed.

## Definition

Keep $`\beta`$ for R04's every-input cost. For a nonconstant total Boolean function $`f`$, let $`\beta_{\max}(f)`$ be the minimum worst-case depth of a deterministic adaptive query tree whose every leaf $`\rho`$ satisfies

```math
bs(f|_\rho)\lt bs(f).
```

Equivalently, a leaf must decrease local block sensitivity at each consistent input $`x`$ with $`bs(f,x)=bs(f)`$. Restriction cannot increase local block sensitivity, so inputs below the original maximum cannot invalidate this equivalence. Set $`\beta_{\max}=0`$ on constants. Thresholds refer to the function at the start of the batch.

## General separated-subcube lemma

Let $`p_1,\ldots,p_M`$ be partial assignments on $`N`$ input variables, each with domain $`S_j`$ of size $`q\ge1`$. Assume any two assignments conflict on at least three variable indices. Their satisfying subcubes are consequently at Hamming distance at least three. Let $`g(x)=1`$ exactly when $`x`$ satisfies some $`p_j`$, and suppose $`g`$ has a 0-input. Here assignments **conflict** at an index when both specify it and require opposite values. Write

```math
b=bs_0(g),\qquad \tau=\min\{|Q|:Q\cap S_j\ne\varnothing\text{ for all }j\}.
```

Then $`s_0(g)=1`$ and $`s_1(g)=bs_1(g)=q`$. At a 1-input, the unique satisfied assignment's $`q`$ specified variables are sensitive, and its certificate bounds block sensitivity from above. At a 0-input, one certificate can give at most one neighboring 1-input, while neighbors satisfying different certificates would contradict the distance-three assumption. Flipping a specified variable at any 1-input supplies a 0-input with sensitivity one.

For a positive integer $`m`$ satisfying $`mb\lt q`$, let $`F=\mathrm{OR}_m\circ g`$ on disjoint sets of variables. Then

```math
s(F)=bs(F)=q,\qquad \beta_{\max}(F)=m\tau.
```

Indeed $`s_0(F)=m`$, $`s_1(F)=q`$, $`bs_0(F)=mb`$, and every 1-input has block sensitivity exactly $`q`$. For the last assertion, at an input with several true copies, enumerate the $`q`$ sensitive variables in each true copy and form $`q`$ disjoint blocks, each containing one enumerated variable from every true copy. Flipping one such block makes every true copy false. Any satisfied certificate gives the matching upper bound $`q`$.

For the lower bound, choose a 0-input $`z`$ of $`g`$ and follow an arbitrary successful tree on $`(z,\ldots,z)`$. If its queried variables in some copy miss $`S_j`$, overwrite that copy's variables indexed by $`S_j`$ according to $`p_j`$. The resulting input agrees with the whole transcript, has a unique true copy, and has all $`q`$ sensitive singletons untouched. Its local block sensitivity remains the global maximum $`q`$. Thus every copy's queried set must hit all $`S_j`$, giving depth at least $`m\tau`$.

Conversely, query a minimum hitting set in every copy. At every consistent 1-input, a satisfied certificate loses at least one unqueried literal, leaving a certificate of size at most $`q-1`$. At every consistent 0-input, local block sensitivity is already at most $`mb\lt q`$. Every resulting leaf therefore has global block sensitivity at most $`q-1`$.

## Linear separation of subcubes bounds the opposite-side block sensitivity

For $`0\lt\delta\le1`$, if any two accepting subcubes of $`g`$ have Hamming distance at least $`\delta N`$, then $`bs_0(g)\le2/\delta`$.

To prove this, fix a 0-input and $`r\ge2`$ disjoint minimal sensitive blocks $`B_1,\ldots,B_r`$. Minimality forces each block to equal the set of mismatched literals of the partial assignment it reaches. Thus distinct blocks reach distinct accepting subcubes. Their endpoints differ in precisely $`B_i\cup B_j`$, so

```math
|B_i|+|B_j|\ge\delta N\quad(i\ne j).
```

Summing over unordered pairs and using disjointness yields

```math
\binom r2\delta N\le(r-1)\sum_i|B_i|\le(r-1)N,
```

and hence $`r\le2/\delta`$. The case $`r=1`$ also satisfies the claimed bound.

## Existence of the required partial assignments

For all sufficiently large $`N`$ divisible by $`128`$, put

```math
q=N/2,\quad M=\lfloor e^{N/512}\rfloor,\quad h=\lfloor N/4096\rfloor.
```

Choose $`M`$ independent uniformly random $`q`$-element supports, and independently assign a fair bit to each selected variable. With positive probability both conditions hold:

1. Every two assignments conflict on at least $`N/16`$ variable indices.
2. No set of $`h`$ variable indices meets all supports; thus $`\tau\ge h+1`$.

For condition 1, fix one assignment. Generate the second by independently leaving each variable unspecified with probability $`1/2`$, or specifying either bit with probability $`1/4`$, and condition its domain to have size $`q`$. Before conditioning, the number of conflicts is $`\mathrm{Bin}(q,1/4)`$, with mean $`N/8`$. The Chernoff bound gives probability at most $`e^{-N/64}`$ for fewer than $`N/16`$ conflicts. The conditioning event has probability at least $`1/(N+1)`$, because the central binomial probability is the largest among $`N+1`$ probabilities summing to one. Thus the pair's failure probability is at most $`(N+1)e^{-N/64}`$. The union bound over pairs is at most

```math
M^2(N+1)e^{-N/64}\le(N+1)e^{-3N/256}=o(1).
```

For condition 2, any fixed $`h`$-element set $`Q`$ is avoided by a random support with probability

```math
\frac{\binom{N-h}{q}}{\binom Nq}=\prod_{j=0}^{h-1}\frac{N/2-j}{N-j}\ge3^{-h}\ge e^{-2h}.
```

The probability that $`Q`$ meets all $`M`$ supports is at most $`\exp(-M e^{-2h})`$. Taking the union bound over at most $`2^N`$ sets gives

```math
\Pr[\tau\le h]\le\exp\!\left(N\log2-\tfrac12e^{3N/2048}\right)=o(1).
```

The two failure probabilities sum to less than one for sufficiently large $`N`$. Also, $`M2^{-q}\lt 1`$, so the union of the accepting subcubes cannot cover the whole Boolean cube; a background 0-input exists.

## Consequence

For these partial assignments, $`b\le32`$. Choose $`m=N/128`$. Then $`mb\le32m=N/4=q/2\lt q`$, so the lemma applies:

```math
s(F)=bs(F)=N/2,
```

```math
\beta_{\max}(F)=m\tau
\ge\frac{N}{128}\left(\left\lfloor\frac{N}{4096}\right\rfloor+1\right)
\gt\frac{N^2}{524288}.
```

Querying all $`mN`$ variables gives the matching $`O(N^2)`$ upper bound. Therefore

```math
\beta_{\max}(F)=\Theta(s(F)^2),\qquad \beta_{\max}(F)/s(F)\longrightarrow\infty.
```

The original conjecture is unaffected: $`F`$ has only $`mN=s(F)bs(F)/32`$ input variables. This rules out requiring a global block-sensitivity decrease after every $`O(s)`$ deterministic batch. It leaves amortized charging schemes possible.

The argument does not yield R05's bounded-error randomized extension. Each support occupies half the variables, so a constant number of uniformly random queries in a copy hits any fixed support with constant probability. Requiring a transcript valid for every completion is a different randomized success condition.

## Verification and next obligation

The [finite audit](../evidence/round-6-witnesses.json) checks the maximum-input
condition against global progress on every partial assignment through three
variables, and checks the exact hitting-set formula on small certificate
systems. A numerical evaluation of the two probability bounds supplements
the asymptotic existence proof; it does not generate the large random family.

```sh
python3 -m unittest discover -s tests
python3 -m scripts.global_block_drop --output evidence/round-6-witnesses.json
```

**PS05.** Passing from every input to global maximizers does not restore an
$`O(s)`$ per-batch bound. A remaining scheme must pay unequal batch costs by
amortization, use a different progress measure, or exploit larger decreases
when an expensive batch is performed. None of those conclusions follows
from the existence proof here.
