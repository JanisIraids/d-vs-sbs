# Glossary

Definitions are repository conventions unless a source is specified. All functions
are **total Boolean functions** $`f:\{0,1\}^{I}\to\{0,1\}`$, where $`I`$ is a finite
set of variable indices. A restriction is again total on its remaining variables.

## Inputs, restrictions, and queries

| Term | Definition |
| --- | --- |
| $`x^B`$ | Input obtained from $`x`$ by flipping precisely the variables indexed by $`B\subseteq I`$; $`x^i=x^{\{i\}}`$. |
| Literal | A requirement $`x_i=a`$ on an input variable, with $`a\in\{0,1\}`$. |
| Partial assignment $`\rho`$ | A function $`\rho:A\to\{0,1\}`$ for $`A\subseteq I`$, specifying the literal $`x_i=\rho(i)`$ for each $`i\in A`$. It leaves variables outside $`A`$ unspecified. |
| Domain / support of a partial assignment | $`\mathrm{dom}(\rho)=A`$, the set of variable indices to which values are assigned, including both 0 and 1 assignments. It is distinct from the assignment $`\rho`$ itself. |
| Fix an input variable | Assign it a specified value, as in $`x_i=a`$. Restricting a function substitutes those assigned values. |
| Certificate subcube | The set of all full inputs extending a certificate. |
| Hamming distance | Number of variable indices at which two full inputs differ; for two sets of inputs, the minimum such distance between their members. |
| Restriction $`f\vert _\rho`$ | Substitute $`\rho`$ and retain the variables indexed outside $`\mathrm{dom}(\rho)`$. The empty restriction gives $`f`$. |
| Query / branch | A query reveals one previously unqueried $`x_i`$; answer $`a`$ gives the branch $`f\vert _{x_i=a}`$. |
| Relevant input variable | $`x_i`$ such that $`f(x)\ne f(x^i)`$ for some $`x`$. Flipping an irrelevant variable never changes the output. |
| $`\mathrm{Rel}(f)`$, $`r(f)`$ | Set of relevant variable indices and its cardinality. The implementation retains their relative order when removing fixed variables. |
| Constant / terminal | A function taking a single value on all its inputs, including a function on no input variables. Terminal states require no further queries. |
| $`D(f)`$ | Minimum, over exact deterministic decision trees computing $`f`$, of their maximum number of queries on any input. Constants have $`D=0`$. |
| Monotone Boolean function | $`x_i\le y_i`$ for every $`i`$ implies $`f(x)\le f(y)`$. Distinct from a potential being monotone under restrictions. |
| Unate Boolean function | A function that becomes monotone after complementing a fixed subset of input variables. |

For nonconstant $`f`$,

```math
D(f)=1+\min_{i\in I}\max_{a\in\{0,1\}}D(f|_{x_i=a}).
```

For an address vector $`a=(a_0,\ldots,a_{k-1})`$,
$`\mathrm{ind}(a)=\sum_j a_j2^j`$ selects a datum in a $`2^k`$-entry array.
**Standard addressing** is $`A_k(a,z)=z_{\mathrm{ind}(a)}`$, with $`k`$
address variables and $`2^k`$ data variables. In a **disjoint composition**
$`f\circ g`$, each input variable of $`f`$ is replaced by the output of a
separate copy of $`g`$ on disjoint input variables. The notation $`f^{\circ d}`$
means $`d`$ balanced levels of this composition.
The symbol $`\oplus`$ is XOR (addition modulo 2), and $`[E]`$ is 1 if statement
$`E`$ is true and 0 otherwise. **Conditional relevance** means relevance in a
specified restriction, rather than in the original function.
**Joint conditional relevance** describes the R03 obstruction: several query
answers together eliminate variables even though every single query has an
answer retaining all the other relevant variables.

In R03, the **guaranteed relevance loss** of querying $`x_i`$ is
$`h_i(g)=r(g)-\max_a r(g|_{i=a})`$. The **relevance-greedy rule** chooses a
maximizer $`i_*(g)`$, breaking ties by a fixed inherited variable order.
Its algorithm depth $`\Phi_3`$ uses that rule at every node, without optimizing
over decision trees. In R01, **certificate multiplicity** is repeated counting
of the same input variable across distinct prime certificates.

## Local and output-specific measures

| Notation / term | Definition |
| --- | --- |
| $`s(f,x)`$ | Number of variable indices $`i`$ with $`f(x)\ne f(x^i)`$. |
| Sensitive block at $`x`$ | Nonempty $`B\subseteq I`$ satisfying $`f(x^B)\ne f(x)`$. |
| Minimal sensitive block | A sensitive block with no proper sensitive subset at the same input. “Minimal” always means inclusion-minimal, not minimum cardinality. |
| $`\mathcal B_x(g)`$ | Set of all minimal sensitive blocks of $`g`$ at $`x`$. Fixing variables according to $`x`$ retains exactly the blocks disjoint from the set of fixed variable indices. |
| Disjoint block family | Pairwise disjoint sensitive blocks at one fixed input. |
| Maximal / maximum family | Maximal: no further block can be added while preserving disjointness. Maximum: largest possible number of blocks. |
| $`bs(f,x)`$ | Size of a maximum disjoint block family at $`x`$. |
| Certificate for $`x`$ | A partial assignment contained in $`x`$ whose every completion has output $`f(x)`$. |
| $`b`$-certificate | A partial assignment whose every completion has output $`b`$. |
| $`C(f,x)`$ | Minimum number of literals in a certificate for $`x`$. |
| $`c_b(f)`$ | Minimum certificate size over inputs of output $`b`$, for nonconstant $`f`$. Distinct from the maximum $`C_b(f)`$. |
| Prime $`b`$-certificate | A $`b`$-certificate from which no literal can be removed while remaining a $`b`$-certificate. Distinct assignments on the same support are distinct certificates. |
| $`\mathcal P_b(f)`$, $`W_b(f)`$ | Set of all prime $`b`$-certificates and its literal mass $`W_b(f)=\sum_{P\in\mathcal P_b(f)}\vert P\vert `$. For a constant $`b`$, the sole prime $`b`$-certificate is empty, and $`\mathcal P_{1-b}=\varnothing`$; both masses are zero. |

For $`M\in\{s,bs,C\}`$, define

```math
M_b(f)=\max_{x:f(x)=b}M(f,x),\qquad M(f)=\max\{M_0(f),M_1(f)\}.
```

**Subscripts $`0,1`$ refer to output classes, never to answers to a query.**
Maxima over absent output classes are zero. Consequently all six output-specific
measures vanish on constants. A certificate-size profile records more than just
$`C_0,C_1`$; its particular population and multiplicities must be specified.

## Polynomial and auxiliary notation

- $`\deg(f)`$: degree of the unique real multilinear polynomial representing
  $`f`$ on the Boolean cube; use degree zero for constants.
- A **maximum-degree monomial** has support of size $`\deg(p)`$.
  An **inclusion-maximal monomial** has nonzero coefficient and support contained
  in no other monomial support of $`p`$. These notions differ.
- $`\lambda(f)`$: spectral norm of the adjacency matrix connecting exactly
  the pairs $`x,x^i`$ with different outputs.
- A **nondeterministic polynomial** $`p`$ for $`f`$ satisfies
  $`p(x)\ne0\iff f(x)=1`$. The minimum degree is $`\mathrm{ndeg}(f)`$;
  set this to zero for constants, including the zero polynomial for constant 0.
- $`\mathrm{rdeg}(f)=\min_{p/q=f,\ q(x)\ne0}\max(\deg p,\deg q)`$
  on the Boolean cube, with real multilinear $`p,q`$.
- $`C_{\min}(f)=\min_x C(f,x)`$;
  $`M^\downarrow(f)=\max_\rho M(f|_\rho)`$ is the **restriction closure** of $`M`$.
- $`RC_x(f)`$: minimum expected query count on input $`x`$ of a randomized
  verifier accepting $`x`$ surely and rejecting every opposite-output input with
  probability at least $`1/2`$.

The last three conventions match [S04](literature.md#sources).

## Amortized candidate accounts

These conventions are used in [R07](round-7.md), [R08](round-8.md), and
[R10](round-10.md). All accounts and closure measures below are zero on constants.
Restriction maxima range over nonconstant restrictions and include the empty
restriction; an empty maximum is zero.

| Notation / term | Definition |
| --- | --- |
| Minimal-block packing volume $`W(f)`$ | Maximum of $`\sum_{B\in\mathcal F}\vert B\vert`$ over inputs $`x`$ and disjoint families $`\mathcal F\subseteq\mathcal B_x(f)`$. Distinct from prime-certificate literal mass $`W_b`$. |
| Capped relevance $`V(f)`$ | $`\min\{r(f),s(f)bs(f)\}`$ in R07 and R09. An account denoted generically by $`V`$ elsewhere must be specified separately. |
| Raw certificate account $`P_b(f)`$ | $`C_b(f)bs_{1-b}(f)`$, paid by querying a shortest $`b`$-certificate. |
| $`K_b(f)`$ | Maximum shortest $`b`$-certificate size $`c_b(h)`$ over nonconstant restrictions $`h`$ of $`f`$. Its account is $`K_b(f)bs_{1-b}(f)`$. |
| Mixed closure $`C_{\min}^{\downarrow}(f)`$ | Maximum of $`c_{\min}(h)=\min\{c_0(h),c_1(h)\}`$ over nonconstant restrictions. The implementation calls this $`K_{\mathrm{mix}}`$; it need not equal $`\min(K_0,K_1)`$. |
| Mixed progress level $`R(f)`$ | $`bs_0(f)+bs_1(f)-1`$ for nonconstant $`f`$. |
| One-sided level profile $`w_{b,j}(f)`$ | Maximum $`c_b(h)`$ over nonconstant restrictions with $`bs_{1-b}(h)=j`$; $`j\ge1`$. Its account is $`A_b(f)=\sum_{j=1}^{bs_{1-b}(f)}w_{b,j}(f)`$. |
| Mixed level profile $`w_{\mathrm{mix},j}(f)`$ | Maximum $`c_{\min}(h)`$ over nonconstant restrictions with $`R(h)=j`$. Its account is $`A_{\mathrm{mix}}(f)=\sum_{j=1}^{R(f)}w_{\mathrm{mix},j}(f)`$. |
| Batch account | A nonnegative function with a specified batch at each nonconstant state, such that every resulting branch of cost $`t`$ and residual function $`h`$ satisfies $`V(h)\le V(g)-t`$. Constants have account zero. |
| Unfinished-batch credit | Store the starting account $`B=V(g)`$ and the unprocessed batch. After $`t`$ queries credit is $`B-t`$; completion resets it to $`V(h)\le B-t`$. This is a state potential. |
| Canonical pruned shortest-certificate algorithm | Choose a shortest certificate of either output, breaking ties by support mask, value mask, then output. Process its variable indices increasingly, skip variables that have become irrelevant, and stop at constants. Otherwise finish the batch before choosing another certificate, even after a mismatch. |
| $`A_{\mathrm{sc}}(f)`$ | Worst-case query cost of that fixed algorithm. There is no minimization over certificate choices, query orders, or decision trees. Its remaining cost also depends on any unfinished batch. |

Masks encode index sets and assignments in the inherited variable order,
with the lowest-indexed variable as the least significant bit. The canonical
rule compares certificate size before the three tie-breaking fields.

## Progress conditions and evidence status

A **function potential** is a real-valued function $`\Phi(g)`$ of the current
restricted function. A **state potential** may also depend on specified
algorithmic memory; the state and its update rule must then be defined.

The **unit progress condition** is

```math
\forall g\text{ nonconstant}\quad
\exists i\quad\forall a\in\{0,1\}:\quad
\Phi(g|_{x_i=a})\le\Phi(g)-1.
```

Here $`g`$ ranges over every reachable restriction; proving the condition for all
total functions suffices. The query is chosen before its answer. Nonincrease
alone does not establish unit progress.

The **initial budget** is $`s(f)bs(f)`$. If terminal potentials are at least $`L`$,
each selected query decreases $`\Phi`$ by at least $`\delta>0`$, and
$`(\Phi(f)-L)/\delta\le s(f)bs(f)`$, telescoping gives the exact target.
A constant-factor upper bound is recorded separately. A **batch** queries a
specified set of remaining input variables at cost equal to its size; all answer
assignments must satisfy the claimed progress bound. An **adaptive batch**
is a query tree with a specified stopping condition; its cost is its maximum
path length. **Amortized accounting**
allows individual steps without decrease only with an explicit bound on total
query cost along every root-to-terminal path.

In [R04](round-4.md), a block is **eliminated** at a consistent input when it
intersects the set of queried variable indices and hence cannot be flipped within the
restriction. The **block-elimination cost** $`\beta(g)`$ is the least adaptive
batch cost that eliminates a block from every maximum disjoint family at
every input. Equivalently, every leaf strictly lowers local block sensitivity
for every consistent input, relative to $`g`$ at the start of the batch.
Constants have $`\beta=0`$. A **uniform algorithm** is one query tree that
works for every unknown input; input-dependent existence of a query set is
a weaker requirement.

In [R05](round-5.md), a **hitting set** for a family $`\mathcal S`$ intersects
every member; its minimum size is the **transversal number** $`\tau(\mathcal S)`$.
A **background input** is a fixed input whose answers define the adversarial
transcript. A **witness support** contains both a witness's disagreements with
that background and every variable index in its chosen maximum block family.
Missing it preserves both consistency and the whole family.

The **weaker block-elimination task** only requires eliminating some minimal
sensitive block at each input, without requiring strict local block-sensitivity
decrease. R05's lower bounds apply to this task too, because its hard inputs
have only one maximum family and that family contains all minimal blocks.
**Global block-sensitivity progress** asks instead for each leaf restriction
to have smaller $`bs`$ than the original function; it need not reduce local
block sensitivity at every input.

In [R06](round-6.md), the **global block-sensitivity decrease cost**
$`\beta_{\max}(f)`$ is the minimum worst-case depth of a deterministic adaptive
query tree whose every leaf $`\rho`$ has $`bs(f\vert_\rho)\lt bs(f)`$.
Equivalently, only consistent inputs with original $`bs(f,x)=bs(f)`$ must
have their local block sensitivity decrease. Constants have
$`\beta_{\max}=0`$, and $`\beta_{\max}\le\beta`$. Two partial assignments
**conflict** at an index if both specify it and assign opposite values;
their number of conflicts equals the minimum Hamming distance between their
satisfying subcubes. The **codimension** of a certificate subcube is the
number of variables specified by its defining partial assignment.

The **complete graph** $`K_t`$ has $`t`$ vertices and one edge for every
unordered pair. An **edge cover** selects edges incident to every vertex. A **cyclic translate**
adds a fixed offset to variable indices modulo the input length.
A function is **cyclically invariant** if translating the input does not change
its output. A permutation group is **transitive** on a specified index set if
it can send any variable index in that set to any other.

| Status / failure | Meaning |
| --- | --- |
| Proved | A complete argument is supplied for the stated domain. |
| Refuted candidate | An explicit counterexample violates a specified obligation; this does not refute the target conjecture. |
| Finite evidence | Exact verification on an explicitly bounded collection, without a universal conclusion. |
| Tentative | Candidate survived the stated checks; a precise unproved obligation remains. |
| Progress failure | Every possible query has an answer violating the proposed decrease. |
| Plateau | A branch leaves the potential unchanged. |
| Budget failure | The normalized initial potential exceeds $`s(f)bs(f)`$. |
| Insufficient range | Available decrease is less than $`D(f)`$; even ideal query choices cannot fund all required queries. |
| Terminal failure | Claimed terminal bound does not hold. |
| Failure mechanism | A proved structural reason for failure, preferably covering a family rather than a single truth table. |

Identifiers: `L` denotes literature/derived baseline claims, `S` sources, `T`
the target, `P` proof contracts, `B` baseline claims, `F` failure mechanisms,
`PS` proof-scheme proposals, and `R` candidate rounds. Names such as
“works” or “fails” must specify which obligation and domain they concern.
