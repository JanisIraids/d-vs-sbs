# R03: depth of a fixed relevance-greedy algorithm

These are local derivations, with no claim of historical novelty. See the [glossary](glossary.md) and [research record](research.md) for definitions and the exact proof obligations.

**Definition.** Retain a fixed total order of coordinates under restriction.
For each relevant $`i`$, set

```math
h_i(g)=\min_{a\in\{0,1\}}\bigl(r(g)-r(g|_{i=a})\bigr).
```

Let $`i_*(g)`$ maximize $`h_i(g)`$, breaking ties by the smallest coordinate
index. Define

```math
\Phi_3(g)=
\begin{cases}
0,&g\text{ constant},\\
1+\max_a\Phi_3(g|_{i_*(g)=a}),&\text{otherwise}.
\end{cases}
```

This is the worst-case depth of a fully specified algorithm, with local
query choices determined only by guaranteed relevance elimination. It is
not optimal decision-tree depth $`D`$: there is no minimization over future
decision trees. It satisfies unit progress for its selected query by
definition. Also $`\Phi_3\le r`$, since only relevant coordinates are queried.
Ordinary addressing is handled efficiently: each address query eliminates
half the data coordinates, so the algorithm reads the address before its
selected datum.

**Budget failure: proved.** For $`k\ge3`$, use two independent address
registers selecting from a shared data array:

```math
H_k(a,b,z)=z_{\mathrm{ind}(a)}
\mathbin{\oplus}z_{\mathrm{ind}(b)}.
```

The coordinate order is all $`2^k`$ data bits first, then the $`k`$ bits of
$`a`$, then the $`k`$ bits of $`b`$. All coordinates are relevant.

Any sensitive block either touches one of the $`2k`$ address coordinates or
flips at least one of the two selected data coordinates. Disjointness gives
$`bs(H_k)\le2k+2`$. Choose addresses $`0^k,1^k`$, set both selected data
values to 0, and set data at every Hamming neighbor of either address to 1.
For $`k\ge3`$ these requirements are consistent. All $`2k+2`$ indicated
coordinates are sensitive. Reading both addresses and at most two data bits
therefore shows

```math
s(H_k)=bs(H_k)=D(H_k)=2k+2.
```

To determine the greedy depth, answer each data query 0 until only the last
datum $`z_q`$ remains; answer that query 1. At every preceding state, let
$`U\ne\varnothing`$ be the unknown data addresses, with all fixed data zero.
All remaining data coordinates and all $`2k`$ address coordinates are relevant.

- For a data query with $`|U|\ge2`$, its 0-branch leaves the same property
  with one fewer unknown datum, so $`h_i=1`$. If $`|U|=1`$, its 1-branch
  leaves $`[a=q]\oplus[b=q]`$, with every address bit relevant, again giving
  $`h_i=1`$.
- For a bit of address $`a`$, choose the branch whose allowed half contains
  some $`p\in U`$. Every remaining $`a`$-bit is relevant by varying $`a`$
  along an edge incident to $`p`$ within that half. Every $`b`$-bit remains
  relevant because $`b`$ is unrestricted. Every unknown datum remains
  relevant: select it using $`b`$, and select a different datum using $`a`$.
  The allowed half contains at least two addresses, so this is possible.
  Thus this branch loses only the queried coordinate, giving $`h_i=1`$.
  The same argument applies to bits of $`b`$.

All scores are therefore 1, and the stipulated tie rule queries all data
first. After answering the last datum 1, the remaining function is
$`[a=q]\oplus[b=q]`$. Answer all address queries consistently with $`a=b=q`$.
Every unqueried address bit stays relevant until queried: changing that bit
would change exactly one equality indicator. The path has length
$`2^k+2k`$; combined with the upper bound $`r`$, this proves

```math
\Phi_3(H_k)=2^k+2k.
```

At $`k=9`$, $`\Phi_3=530>400=s\,bs`$, while $`D=20`$.

The failure concerns this precise greedy rule, including its tie rule.
It does not rule out every tie-breaking policy or every use of relevance.
The structural obstruction is joint conditional relevance: fixing a single
address bit leaves the other selector able to access every datum.

## Final scheme review and next obligation

The progression isolates four different losses: maxima discard changes;
certificate mass repeats shared coordinates; coordinate count adds mutually
exclusive possibilities; one-query relevance elimination misses information
that becomes useful after several queries.

**Costed batches.** Both addressing examples admit two short successive batches:
first query one or both complete address registers, then query the at most
one or two data bits selected by those answers. Their total cost is respectively
$`k+1`$ and $`2k+2`$. This explains the
examples but does not identify a suitable batch in every total function.
The certificate and monomial algorithms in the literature provide established
templates for this direction.

**State potentials.** A potential may record an explicitly selected batch or
partially resolved certificate/block information. Any such proposal must define
the state, charge all queries, and account for answers incompatible with its
selected certificates. Additional state alone supplies no budget theorem.

**Exact missing lemma for a next round.** Specify an independently motivated
account $`V`$ with terminal lower bound zero and initial
$`V(f)\le s(f)bs(f)`$. At every nonterminal state, exhibit a nonempty query
batch $`B`$ such that every answer assignment lowers the account by at least
$`|B|`$, or supply an equally explicit amortized inequality bounding the
total cost on every path. For a single-query proposal this reduces to P01.
No account satisfying this lemma has been established here. A productive
next candidate must explain how it handles both certificate overlap and
joint conditional relevance before computational testing.

## Finite and compact witness checks

All 65,814 truth tables through four variables satisfy the budget and progress
tests for this candidate. This finite result is compatible with the proved
530-variable budget counterexample. On $`H_2`$, exact computation gives
$`D=6`$, $`s=bs=6`$, and greedy depth 8. Exact path checks for $`H_2,H_3`$ reproduce
all 8 and 14 successive queries of the proof, respectively.

For $`H_9`$, the witness script evaluates compact integer inputs, verifies a
relevance edge for each of the 530 coordinates, and finds local sensitivity 20.
It does **not** construct the full truth table. The exact global values
$`s=bs=D=20`$ and $`\Phi_3=530`$ are separately labeled analytical results.

See [full audit](../evidence/round-3.json) and
[curated witnesses](../evidence/round-3-witnesses.json).

```sh
python3 -m scripts.audit --candidates greedy_relevance_depth --max-vars 4 --output evidence/round-3.json
python3 -m scripts.witnesses --round 3 --output evidence/round-3-witnesses.json
```
