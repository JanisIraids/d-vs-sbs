# R09: maximum-degree monomial batches overcharge product decrease

**Result: refuted with an unbounded loss, for every maximum-degree monomial.**
Querying an entire maximum-degree monomial can cost arbitrarily more than the
resulting decrease in $`s\,bs`$, even after capping that account by relevance.
This is a failure of the specified charge, not of the target conjecture.
These are repository derivations; no historical novelty is claimed.

## Candidate and a first repair

Let $`M`$ be the set of variable indices in a maximum-degree monomial of the
real multilinear polynomial of a nonconstant function $`g`$. The candidate
queries every variable in $`M`$, paying $`|M|=\deg(g)`$. It asks for some such
monomial satisfying, for every answer assignment $`\alpha`$ on $`M`$,

```math
|M|\le\Phi(g)-\Phi(g|_\alpha),
\qquad \Phi(g)=s(g)bs(g).
```

The weaker account using fixed initial sensitivity times the block-sensitivity
drop already fails on the four-variable truth table `0x22fa`: its sensitivity
and block sensitivity are both 2, its degree is 3, and each maximum-degree
monomial has an answer leaving a dictator. Cost 3 exceeds that account's
drop 2. The current product drops from 4 to 1 and repairs this example.
The following family defeats that repair and every constant-factor relaxation.

## Two certificates with a small shared part

Fix $`q\ge13`$ and $`m=\lfloor(q-1)/2\rfloor`$. Define $`g_q`$ using shared
variables $`z_1,z_2,z_3`$ and two private sets $`a_1,\ldots,a_{q-3}`$ and
$`b_1,\ldots,b_{q-3}`$. It accepts either partial assignment:

```math
p_0:\ z_1=z_2=z_3=0,\ a_i=1\text{ for all }i;
\qquad
p_1:\ z_1=z_2=z_3=1,\ b_i=1\text{ for all }i.
```

Their supports each have size $`q`$ and intersect in exactly three indices.
The accepting subcubes have distance three, so
$`s_0(g_q)=1`$ and $`s_1(g_q)=bs_1(g_q)=C_1(g_q)=q`$.
At a 0-input, every minimal sensitive block is a certificate's mismatch set;
there are at most two such blocks. These also admit a hitting set of size two.
Setting all private variables to 1 and the shared variables to 001 makes
the two mismatch sets disjoint and nonempty. Thus $`bs_0(g_q)=C_0(g_q)=2`$.

For $`F_q=\mathrm{OR}_m\circ g_q`$ on disjoint variables, this gives

```math
s(F_q)=bs(F_q)=C(F_q)=q,
\qquad r(F_q)=m(2q-3).
```

Indeed its 0-side sensitivity is $`m`$, its 0-side block sensitivity and
certificate complexity are $`2m\lt q`$, and the corresponding 1-side maxima
are $`q`$.

The polynomial of $`g_q`$ is

```math
\prod_{j=1}^{3}(1-z_j)\prod_i a_i
+\prod_{j=1}^{3}z_j\prod_i b_i.
```

Its only degree-$`q`$ monomials have the two certificate supports. Consequently
$`\deg(F_q)=mq`$, and every maximum-degree monomial chooses one certificate
support in every copy. Distinct choices have distinct supports, so their
nonzero coefficients cannot cancel.

## Every choice has a bad branch

In each copy, answer its three shared queries according to the **other**
certificate. The selected certificate becomes false; answer its private
queries arbitrarily. The untouched private variables of the other certificate
remain a conjunction. Therefore the residual function is exactly
$`\mathrm{OR}_m\circ\mathrm{AND}_{q-3}`$, with sensitivity and block
sensitivity both $`q-3`$.

The batch cost and account decrease are respectively

```math
mq,
\qquad q^2-(q-3)^2=6q-9.
```

Since $`m\ge6`$, the cost exceeds the decrease. Their ratio is
$`\Theta(q)`$, so no universal constant repairs this charge. Changing the
maximum-monomial tie rule cannot help: every choice has such a branch.
However, $`r(F_q)\lt q^2`$, so relevance capping repairs this particular family.

## Addressing defeats relevance capping

Replace each input variable of $`F_q`$ by an independent addressing function
$`A_7`$: seven address variables select one of 128 data variables. Call the
result $`H_q`$. Each gadget has 135 relevant variables, degree 8, and sensitivity
maxima 8 on both outputs. At every input its certificate complexity and block
sensitivity are 8. For the latter, take the selected-data singleton; for each
address bit take its singleton if the neighboring datum differs, otherwise
pair that bit with its neighboring datum. These eight blocks are disjoint.

Composition and the matching certificate upper bounds give

```math
s(H_q)=bs(H_q)=8q,\qquad
r(H_q)=135m(2q-3),\qquad \deg(H_q)=8mq.
```

Every maximum-degree monomial selects an outer maximum-degree monomial and,
in each selected gadget, all seven address variables and one datum. Set each
queried address register to select its queried datum. That datum can then
supply the bad logical answer above. The residual function $`H'_q`$ is
$`\mathrm{OR}_m\circ\mathrm{AND}_{q-3}\circ A_7`$, so

```math
s(H'_q)=bs(H'_q)=8(q-3),\qquad r(H'_q)=135m(q-3).
```

For $`q\ge13`$, relevance exceeds $`s\,bs`$ both before and after this batch.
Thus $`\Phi=\min\{r,s\,bs\}`$ still has decrease $`64(6q-9)`$ against cost
$`8mq`$. For $`q\ge97`$ the cost is larger, and the ratio
$`mq/[8(6q-9)]`$ grows without bound.

## Mechanism, scope, and next step

Three shared answers eliminate each selected certificate; querying its private
variables supplies no further progress against the alternative certificate.
The coarse product also overestimates the remaining AND–OR evaluation cost.
This refutes charging **full nonadaptive monomial batches**, including adaptive
choices between batches. It does not refute pruning queries once they become
irrelevant, different adaptive batches, or accounting for actual future costs.

The target remains true here: evaluating all logical inputs via their address
gadgets costs $`8m(2q-3)\lt8q^2\lt s(H_q)bs(H_q)`$.
Even global progress is cheap in the unlifted family: one shared query per
copy shortens every surviving 1-certificate, while the 0-side was already
below $`q`$. The [R06 hitting-set formula](round-6.md#general-separated-subcube-lemma)
gives the exact value $`\beta_{\max}(F_q)=m`$. The obstruction is wasted batch
queries, not universal hardness.

[R10](round-10.md) retains actual path costs as a tentative next candidate.
The [shared finite evidence](../evidence/amortized-witnesses.json) supplements
the analytical family proof:

```sh
python3 -m scripts.amortized --output evidence/amortized-witnesses.json
```
