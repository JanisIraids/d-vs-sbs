# R10: charge only executed shortest-certificate batches

**Status: tentative.** The procedure below is fully specified and handles
the new account counterexamples within the target budget. A general proof
of its budget, or a counterexample, remains missing. Its underlying
shortest-certificate algorithm is the published template in
[S08, Section 5](literature.md#sources); the tie rule and pruning below are
repository conventions.

## Procedure and exact obligation

At each nonconstant batch boundary:

1. Choose a shortest certificate of either output. Break ties by increasing
   support mask, then value mask, then output. Masks use the inherited order
   of remaining input variables, as in the implementation.
2. Process its variable indices in increasing order. Query an index only if
   it is still relevant. Stop immediately if the function becomes constant.
3. Otherwise finish this planned batch and choose a new shortest certificate.
   A mismatch with the chosen certificate alone does not restart the batch.

No variable is queried twice. Skipping a variable already irrelevant in the
current restriction preserves the residual function. For the certificate
progress argument, assign such skipped variables arbitrary values at no query
cost; the resulting total restriction computes the same residual function.

Write $`A_{\mathrm{sc}}(f)`$ for this fixed algorithm's worst-case query cost.
It is not minimized over decision trees, certificate choices, or query orders.
The unproved obligation is precisely

```math
A_{\mathrm{sc}}(f)\le s(f)bs(f)
\qquad\text{for every total Boolean function }f.
```

The remaining cost of this predetermined policy is a state potential, including
the unprocessed part of its current batch. It vanishes at termination and
decreases by at least one at each charged query. This observation does not
prove its initial budget; exact $`D`$ is not used to define or select the policy.

## What is already proved

For arbitrary $`f`$, restriction-closed shortest-certificate accounts from
[R08](round-8.md) give

```math
A_{\mathrm{sc}}(f)
\le C_{\min}^{\downarrow}(f)
\bigl(bs_0(f)+bs_1(f)-1\bigr).
```

Indeed every nonconstant completed batch lowers the opposite-output block
sensitivity by at least one. A nonconstant function has both output-specific
block sensitivities at least one, so at most $`bs_0+bs_1-1`$ batches occur.
Pruning can only reduce the cost of a planned batch. R08 shows why this
universal upper bound can greatly exceed the target.

There is also a useful structural bound. Let $`H\circ A_k`$ replace each
of $`n`$ logical variables of a nonconstant function $`H`$ by a disjoint
addressing function. Put $`q=k+1`$. Then, independently of certificate ties,

```math
A_{\mathrm{sc}}(H\circ A_k)\le n(q+3).
```

A shortest certificate of a disjoint composition contains only inner copies
whose outputs it forces. Literals in an unforced copy would be removable.
Within each forced copy it uses a shortest certificate of the required output;
otherwise replace it by a smaller one.

At the first use of an untouched $`A_k`$, that certificate has exactly $`q`$
literals. If it specifies $`a`$ address variables, it must specify all
$`2^{k-a}`$ accessible data values. Equality in
$`a+2^{k-a}\ge k+1`$ requires $`a=k`$ or $`a=k-1`$. Therefore, after
the planned queries, at most one address variable and two data variables
remain relevant in that copy, regardless of the observed answers. Later
queries cost at most three more. If pruning skips part of this work, the
skipped variables stay irrelevant. While a logical copy remains relevant,
each variable relevant to its inner restriction is also globally relevant:
the independent other copies can realize a witness making that logical input
sensitive. Thus pruning either skips an already irrelevant inner variable,
or the whole copy has become permanently irrelevant. Charge at most $`q+3`$
to each inner copy.

For R08's $`G^{\circ d}\circ A_{4d+10}`$, this bounds the cost by
$`4^d(4d+14)\le(4d+11)^2 6^d=s\,bs`$, although every tested certificate
profile has an unbounded initial-budget excess. For R09's padded two-pattern
family the bound is $`11m(2q-3)\lt64q^2=s\,bs`$; here its separate pattern
parameter $`q`$ is as defined in R09. Thus those account failures do not
refute this procedure.

## Verification and next search

The [exact implementation](../scripts/amortized.py) compares the fixed-policy
recurrence with direct simulation on every input through three variables.
It also checks all functions through four variables. Their budget checks are
weak evidence: every function in that finite collection already has
$`r\le s\,bs`$, and this policy never exceeds $`r`$.

Next seek a total family with $`r\gt s\,bs`$ where successive shortest
certificates expose many fresh variables without either reducing future
certificate costs or making unqueried variables irrelevant. Treat a bad tie
rule separately from failure of all shortest-certificate choices. A successful
charging proof must bound actual executed costs and track skipped progress
levels; it cannot sum independent worst-case costs at every possible level.

```sh
python3 -m unittest discover -s tests
python3 -m scripts.amortized --output evidence/amortized-witnesses.json
```
