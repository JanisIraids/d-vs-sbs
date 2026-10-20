# R02: count each relevant coordinate once

These are local derivations, with no claim of historical novelty. See the [glossary](glossary.md) and [research record](research.md) for definitions and the exact proof obligations.

**Definition.** Remove the multiplicity from R01:

```math
\Phi_2(g)=\left|\bigcup_{b=0}^1\ \bigcup_{P\in\mathcal P_b(g)}
\mathrm{dom}(P)\right|=r(g),
```

where $`r(g)`$ denotes the number of relevant coordinates. An irrelevant
coordinate cannot occur in a prime certificate, since its literal can be
deleted. Conversely, the [R01](round-1.md) relevance-edge argument places each relevant
coordinate in a prime certificate of each output.

**Unit progress: proved for every relevant query.** Restriction cannot make
an irrelevant coordinate relevant, and querying a relevant coordinate removes
that coordinate. Thus $`r(g|_{i=a})\le r(g)-1`$ for both answers. This corrects
parity's multiplicity problem: $`\Phi_2(\mathrm{PARITY}_n)=n`$.

**Budget failure: proved.** The addressing function is

```math
A_k(a,z)=z_{\mathrm{ind}(a)},
```

with $`k`$ address bits and $`2^k`$ independent data bits. All $`k+2^k`$
coordinates are relevant. At any input a disjoint sensitive-block family has
at most $`k`$ blocks touching address bits and at most one remaining block:
an address-free sensitive block must flip the currently selected datum.
Thus $`bs(A_k)\le k+1`$. Set the selected datum to 0 and the data at every
Hamming-neighbor address to 1; all $`k`$ address bits and the selected data bit
are then sensitive. Consequently

```math
s(A_k)=bs(A_k)=D(A_k)=k+1.
```

For $`D`$, the upper bound reads the address and its datum, while $`D\ge s`$
gives the reverse inequality. At $`k=5`$, $`\Phi_2=37>36=s\,bs`$, the first
violation in this family. The gap grows exponentially with $`k`$.

**Scheme review after R02.** Counting distinct coordinates still charges
mutually exclusive future possibilities together. Conditional relevance
must enter the accounting. A possible repair is to choose queries according
to how many relevant coordinates their answers eliminate; R03 makes this
proposal precise. A different repair would query an identifying batch and
charge its actual cost. Neither proposal supplies a universal budget bound.

**Finite audit.** No budget or progress failure occurs on any of the 65,814
truth tables through four variables. The proved family above demonstrates
why this finite success is insufficient. The curated evidence computes all
parameters of $`A_2`$, and checks explicit relevance edges for all 37 coordinates
of $`A_5`$ together with an input of sensitivity 6. It labels the global upper
bounds and exact $`D`$ as analytical conclusions, not results of those edge checks.

See [full audit](../evidence/round-2.json) and
[curated witnesses](../evidence/round-2-witnesses.json).

```sh
python3 -m scripts.audit --candidates relevant_variables --max-vars 4 --output evidence/round-2.json
python3 -m scripts.witnesses --round 2 --output evidence/round-2-witnesses.json
```
