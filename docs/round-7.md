# R07: packing volume and a relevance cap

**Result:** charging the sizes of minimal blocks has the right initial budget
but insufficient range. Replacing it by capped relevance repairs that example
and still fails single-query progress. These are repository derivations.

## Candidate: total size of a disjoint minimal-block family

Define the **minimal-block packing volume**

```math
W(f)=\max_x\max_{\mathcal F\subseteq\mathcal B_x(f)\text{ disjoint}}
\sum_{B\in\mathcal F}|B|.
```

Minimality is essential. Every minimal block has size at most $`s(f)`$,
and a disjoint family has at most $`bs(f)`$ members. Therefore
$`W\le s\,bs`$. Constants have volume zero. Restriction only deletes minimal
blocks, so $`W`$ cannot increase. This proposal would pay for unequal block
sizes rather than allocating one identical payment to each eliminated block.

**Counterexample: odd majority.** For $`n=2t+1\ge3`$,

```math
W(\mathrm{MAJ}_{2t+1})=2t\lt D(\mathrm{MAJ}_{2t+1})=2t+1.
```

At a 0-input with at least one 1, all minimal sensitive blocks consist of
zeros, so their union has at most $`2t`$ indices. At the all-zero input,
minimal blocks have size $`t+1`$, and at most one can be packed. Complementation
handles 1-inputs. At an input with one 1, two disjoint sets of $`t`$ zeros
attain volume $`2t`$. Majority needs all $`2t+1`$ queries in the worst case:
an adversary can leave $`t`$ observed zeros and $`t`$ observed ones before
the final query.

Every first query also has volume $`2t`$ on **both** answers. If its answer
is 0, use the all-one remaining input; if it is 1, use the all-zero remaining
input. Two size-$`t`$ minimal blocks cover the remaining variables.
The range failure rules out any telescoping scheme starting with $`W`$,
even with adaptive batches or additional intermediate state.

More generally, suppose permutations preserving $`f`$ act transitively on
its relevant variable indices and $`W(f)\lt r(f)`$. Translate a maximum-volume
packing so that any specified query index lies outside its union. Answer
according to the translated witness. The packing survives, so no query
guarantees a volume decrease. This is a general symmetry mechanism; the
stronger inequality $`W\lt D`$ needs its own proof.

## Repair: cap the relevance account by the target budget

Consider

```math
V(f)=\min\{r(f),s(f)bs(f)\}.
```

It pays every query when relevance attains the minimum, including the
majority example. The remaining question is progress when the product
attains the minimum.

Let $`A_k`$ be ordinary addressing and substitute four disjoint copies into
$`(z_1\land z_2)\lor(z_3\land z_4)`$, obtaining $`J_k`$. For $`k\ge6`$,

```math
s_0=s_1=bs_0=bs_1=C_0=C_1=2(k+1),\qquad
r(J_k)=4(2^k+k).
```

The certificate upper bounds and sensitivity witnesses give these equalities.
After querying any variable, the affected addressing copy remains nonconstant.
For 0-side witnesses use the other child of its AND term; for 1-side witnesses
use the untouched other AND term. Thus all six maxima survive **every** answer.
Residual relevance is $`(7/2)2^k+4k-1`$ after an address query and
$`4(2^k+k)-1`$ after a data query. Both exceed $`4(k+1)^2`$.

At $`k=6`$, this gives $`r=280`$, $`V=196`$, and child relevance 247 or
279: every first query preserves $`V`$. The mechanism combines redundancy
that preserves maxima with addressing that makes the relevance cap inactive.

**Scope:** this only refutes single-query progress. At $`k=6`$, evaluating
one whole AND term costs at most 14 queries and leaves a constant or a
function with at most 140 relevant variables. Its account decrease is at
least 56. An unfinished batch must therefore be represented in the state;
the initial plateau does not preclude amortization.

## Next candidate and verification

[R08](round-8.md) gives explicit certificate accounts and an account for
unfinished batches. [R09](round-9.md) tests full monomial batches against
the capped product above.

The [evidence](../evidence/amortized-witnesses.json) checks small majority
instances and labels the addressing-family values as evaluations of proved
formulas, not enumeration of their large truth tables.

```sh
python3 -m scripts.amortized --output evidence/amortized-witnesses.json
```
