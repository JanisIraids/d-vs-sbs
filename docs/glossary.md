# Glossary

Definitions are repository conventions unless a source is specified. All functions
are **total Boolean functions** $f:\{0,1\}^{I}\to\{0,1\}$, where $I$ is a finite
coordinate set. A restriction is again total on its remaining coordinates.

## Inputs, restrictions, and queries

| Term | Definition |
| --- | --- |
| $x^B$ | Input obtained from $x$ by flipping precisely the coordinates in $B\subseteq I$; $x^i=x^{\{i\}}$. |
| Literal | A coordinate-value requirement $x_i=a$, with $a\in\{0,1\}$. |
| Partial assignment $\rho$ | A consistent set of literals on distinct coordinates. Its support $\operatorname{dom}(\rho)$ is the set of fixed coordinates. |
| Restriction $f\vert _\rho$ | Substitute $\rho$ and retain the coordinates outside $\operatorname{dom}(\rho)$. The empty restriction gives $f$. |
| Query / branch | A query reveals one previously unqueried $x_i$; answer $a$ gives the branch $f\vert _{x_i=a}$. |
| Relevant coordinate | $i$ such that $f(x)\ne f(x^i)$ for some $x$. An irrelevant coordinate never changes the output. |
| $\operatorname{Rel}(f)$, $r(f)$ | Set of relevant coordinates and its cardinality. The implementation retains their relative order when removing fixed coordinates. |
| Constant / terminal | A function taking a single value on all its inputs, including a function on no coordinates. Terminal states require no further queries. |
| $D(f)$ | Minimum, over exact deterministic decision trees computing $f$, of their maximum number of queries on any input. Constants have $D=0$. |
| Monotone Boolean function | $x_i\le y_i$ for every $i$ implies $f(x)\le f(y)$. Distinct from a potential being monotone under restrictions. |

For nonconstant $f$,
$$
D(f)=1+\min_{i\in I}\max_{a\in\{0,1\}}D(f|_{x_i=a}).
$$

For an address vector $a=(a_0,\ldots,a_{k-1})$,
$\operatorname{ind}(a)=\sum_j a_j2^j$ selects a datum in a $2^k$-entry array.
The symbol $\oplus$ is XOR (addition modulo 2), and $[E]$ is 1 if statement
$E$ is true and 0 otherwise. **Conditional relevance** means relevance in a
specified restriction, rather than in the original function.
**Joint conditional relevance** describes the R03 obstruction: several query
answers together eliminate coordinates even though every single query has an
answer retaining all the other relevant coordinates.

In R03, the **guaranteed relevance loss** of coordinate $i$ is
$h_i(g)=r(g)-\max_a r(g|_{i=a})$. The **relevance-greedy rule** chooses a
maximizer $i_*(g)$, breaking ties by a fixed inherited coordinate order.
Its algorithm depth $\Phi_3$ uses that rule at every node, without optimizing
over decision trees. In R01, **certificate multiplicity** is repeated counting
of the same coordinate across distinct prime certificates.

## Local and output-specific measures

| Notation / term | Definition |
| --- | --- |
| $s(f,x)$ | Number of coordinates $i$ with $f(x)\ne f(x^i)$. |
| Sensitive block at $x$ | Nonempty $B\subseteq I$ satisfying $f(x^B)\ne f(x)$. |
| Minimal sensitive block | A sensitive block with no proper sensitive subset at the same input. “Minimal” always means inclusion-minimal, not minimum cardinality. |
| Disjoint block family | Pairwise disjoint sensitive blocks at one fixed input. |
| Maximal / maximum family | Maximal: no further block can be added while preserving disjointness. Maximum: largest possible number of blocks. |
| $bs(f,x)$ | Size of a maximum disjoint block family at $x$. |
| Certificate for $x$ | A partial assignment contained in $x$ whose every completion has output $f(x)$. |
| $b$-certificate | A partial assignment whose every completion has output $b$. |
| $C(f,x)$ | Minimum number of literals in a certificate for $x$. |
| Prime $b$-certificate | A $b$-certificate from which no literal can be removed while remaining a $b$-certificate. Distinct assignments on the same support are distinct certificates. |
| $\mathcal P_b(f)$, $W_b(f)$ | Set of all prime $b$-certificates and its literal mass $W_b(f)=\sum_{P\in\mathcal P_b(f)}\vert P\vert $. For a constant $b$, the sole prime $b$-certificate is empty, and $\mathcal P_{1-b}=\varnothing$; both masses are zero. |

For $M\in\{s,bs,C\}$, define
$$
M_b(f)=\max_{x:f(x)=b}M(f,x),\qquad M(f)=\max\{M_0(f),M_1(f)\}.
$$
**Subscripts $0,1$ refer to output classes, never to answers to a query.**
Maxima over absent output classes are zero. Consequently all six output-specific
measures vanish on constants. A certificate-size profile records more than just
$C_0,C_1$; its particular population and multiplicities must be specified.

## Polynomial and auxiliary notation

- $\deg(f)$: degree of the unique real multilinear polynomial representing
  $f$ on the Boolean cube; use degree zero for constants.
- A **maximum-degree monomial** has support of size $\deg(p)$.
  An **inclusion-maximal monomial** has nonzero coefficient and support contained
  in no other monomial support of $p$. These notions differ.
- $\lambda(f)$: spectral norm of the adjacency matrix connecting exactly
  the pairs $x,x^i$ with different outputs.
- A **nondeterministic polynomial** $p$ for $f$ satisfies
  $p(x)\ne0\iff f(x)=1$. The minimum degree is $\operatorname{ndeg}(f)$;
  set this to zero for constants, including the zero polynomial for constant 0.
- $\operatorname{rdeg}(f)=\min_{p/q=f,\ q(x)\ne0}\max(\deg p,\deg q)$
  on the Boolean cube, with real multilinear $p,q$.
- $C_{\min}(f)=\min_x C(f,x)$;
  $M^\downarrow(f)=\max_\rho M(f|_\rho)$ is the **restriction closure** of $M$.
- $RC_x(f)$: minimum expected query count on input $x$ of a randomized
  verifier accepting $x$ surely and rejecting every opposite-output input with
  probability at least $1/2$.

The last three conventions match [S04](literature.md#sources).

## Progress conditions and evidence status

A **function potential** is a real-valued function $\Phi(g)$ of the current
restricted function. A **state potential** may also depend on specified
algorithmic memory; the state and its update rule must then be defined.

The **unit progress condition** is
$$
\forall g\text{ nonconstant}\quad
\exists i\quad\forall a\in\{0,1\}:\quad
\Phi(g|_{x_i=a})\le\Phi(g)-1.
$$
Here $g$ ranges over every reachable restriction; proving the condition for all
total functions suffices. The query is chosen before its answer. Nonincrease
alone does not establish unit progress.

The **initial budget** is $s(f)bs(f)$. If terminal potentials are at least $L$,
each selected query decreases $\Phi$ by at least $\delta>0$, and
$(\Phi(f)-L)/\delta\le s(f)bs(f)$, telescoping gives the exact target.
A constant-factor upper bound is recorded separately. A **batch** queries a
specified set of remaining coordinates at cost equal to its size; all answer
assignments must satisfy the claimed progress bound. **Amortized accounting**
allows individual steps without decrease only with an explicit bound on total
query cost along every root-to-terminal path.

| Status / failure | Meaning |
| --- | --- |
| Proved | A complete argument is supplied for the stated domain. |
| Refuted candidate | An explicit counterexample violates a specified obligation; this does not refute the target conjecture. |
| Finite evidence | Exact verification on an explicitly bounded collection, without a universal conclusion. |
| Tentative | Candidate survived the stated checks; a precise unproved obligation remains. |
| Progress failure | Every possible query has an answer violating the proposed decrease. |
| Plateau | A branch leaves the potential unchanged. |
| Budget failure | The normalized initial potential exceeds $s(f)bs(f)$. |
| Insufficient range | Available decrease is less than $D(f)$; even ideal query choices cannot fund all required queries. |
| Terminal failure | Claimed terminal bound does not hold. |
| Failure mechanism | A proved structural reason for failure, preferably covering a family rather than a single truth table. |

Identifiers: `L` denotes literature/derived baseline claims, `S` sources, `T`
the target, `P` proof contracts, `B` baseline claims, `F` failure mechanisms,
`PS` proof-scheme proposals, and `R` candidate rounds. Names such as
“works” or “fails” must specify which obligation and domain they concern.
