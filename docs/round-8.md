# R08: certificate accounts and their budget obstruction

**Result:** certificate costs give valid amortized progress accounts, including
accounts that vary the charge with block sensitivity. An explicit family makes
their initial budgets exceed $`s\,bs`$ by an unbounded factor, even after taking
their minimum with the number of relevant variables. The failure concerns the
accounts, not the query cost of every certificate algorithm.

## Certificate batches pay an opposite-side account

For nonconstant $`g`$ and $`b\in\{0,1\}`$, define

```math
c_b(g)=\min_{g(x)=b}C(g,x),\qquad
P_b(g)=C_b(g)bs_{1-b}(g).
```

Choose a shortest $`b`$-certificate $`p:Q\to\{0,1\}`$ and query its entire
domain. Let $`h`$ be a nonconstant resulting restriction. For any consistent
opposite-output input $`x`$, the set
$`B=\{i\in Q:x_i\ne p(i)\}`$ is a nonempty sensitive block: overwriting it
makes $`x`$ satisfy $`p`$. Every sensitive-block packing in $`h`$ avoids $`B`$.
Therefore

```math
bs_{1-b}(h)\le bs_{1-b}(g)-1,
```

and restriction monotonicity of certificate complexity gives

```math
P_b(h)\le P_b(g)-C_b(g)\le P_b(g)-|Q|.
```

Set accounts to zero on constants; terminal branches satisfy the same
inequality. This recovers $`D\le C_bbs_{1-b}`$, the side-specific refinement
of the certificate argument in [S01, Lemma 5.3](https://arxiv.org/pdf/quant-ph/9802049v3#page=8).

This account already handles **every R06 separated-subcube family**:
there $`C_1(F)=q`$, $`bs_0(F)=mb`$, and $`mb\lt q`$, so
$`P_1(F)=qmb\lt q^2=s(F)bs(F)`$. The conclusion does not require a bound on
the ambient number of variables.

## Restriction closure and variable charges

Define $`K_b(g)`$ as the maximum of $`c_b(h)`$ over nonconstant restrictions
$`h`$ of $`g`$. It is restriction-monotone and at most $`C_b(g)`$. Replacing
$`C_b`$ by $`K_b`$ in the preceding proof gives another valid account,
$`K_b(g)bs_{1-b}(g)`$.

A finer account charges separately for each attainable value of opposite-side
block sensitivity. For integer $`j\ge1`$, define

```math
w_{b,j}(g)=\max\{c_b(h):h\text{ is a nonconstant restriction of }g,
                         \ bs_{1-b}(h)=j\},
```

```math
A_b(g)=\sum_{j=1}^{bs_{1-b}(g)}w_{b,j}(g).
```

An empty maximum is zero. Restriction cannot increase any profile entry.
Querying a shortest $`b`$-certificate decreases the upper summation index,
removing an entry at least as large as the batch cost. Hence
$`A_b(h)\le A_b(g)-|Q|`$ on every branch, and
$`A_b\le K_bbs_{1-b}`$.

For certificates of either output, put $`c_{\min}=\min(c_0,c_1)`$ and
$`R(g)=bs_0(g)+bs_1(g)-1`$ on nonconstant functions. Define
$`w_{\mathrm{mix},j}(g)`$ analogously, maximizing $`c_{\min}(h)`$ over
restrictions with $`R(h)=j`$, and set

```math
A_{\mathrm{mix}}(g)=\sum_{j=1}^{R(g)}w_{\mathrm{mix},j}(g).
```

Querying a shortest certificate decreases $`R`$ by at least one whenever
the result remains nonconstant. Thus this account also pays every batch.
The established baseline is
$`D\le C_{\min}^{\downarrow}(bs_0+bs_1)`$, proved by the shortest-certificate
algorithm in [S08, Lemma 6, Section 5](https://drops.dagstuhl.de/storage/00lipics/lipics-vol284-fsttcs2023/LIPIcs.FSTTCS.2023.27/LIPIcs.FSTTCS.2023.27.pdf#page=13).
The profiles above are local refinements of that argument.

The minimum of any collection of valid batch accounts remains valid: choose
a minimizing account and its prescribed batch; at the child, the minimum is
at most that account's new value. This also permits including the relevance
count $`r(g)`$, whose batch is one relevant-variable query.

For **unit-query progress**, store credit $`B=V(g)`$ at the start of a batch
chosen for account $`V`$. After $`t`$ queries its credit is $`B-t`$. At batch
completion reset to $`V(h)\le B-|Q|`$; this cannot increase credit. Constants
receive zero. This is a potential of the algorithm's state, including its
unfinished batch. Each query spends at least one unit.

## A family with uniform certificate complexity

Use the four-variable function

```math
G(u,a,b,v)=(u\oplus v)(a\oplus b)\oplus v\oplus b.
```

It returns $`v\oplus a`$ when $`u\oplus v=1`$, and $`v\oplus b`$ otherwise.
At every input its minimal sensitive blocks are two singletons and the pair
of remaining variable indices. This follows by checking the four values of
$`(u\oplus v,a\oplus b)`$. Consequently every input has
$`s_x=2`$, $`bs_x=C_x=3`$. Querying $`u,v`$ and the selected data variable
gives $`D(G)=3`$.

This is Savický's $`\alpha_2(u,v,a,b)`$. Its balanced compositions, with
$`s=2^d`$ and $`bs=C=3^d`$, are established in
[S09, Example 2.9 and Theorem 3.14](https://eccc.weizmann.ac.il/report/2013/191/revision/2/download/#page=21).
The substitution and restriction argument below are local derivations.

Let $`A_k`$ be standard addressing with $`k`$ address variables and
$`2^k`$ data variables; write $`q=k+1`$. Every input has $`C_x=bs_x=q`$.
Indeed, a certificate fixing $`a`$ address variables must fix all
$`2^{k-a}`$ compatible data variables, so its size is at least
$`a+2^{k-a}\ge q`$. The standard certificate attains $`q`$.

For a matching packing, use the selected data variable and one block for
each address bit: the address bit alone if its neighboring data value differs,
or that address bit together with the neighboring data variable otherwise.
These $`q`$ blocks are disjoint. Both outputs also admit sensitivity $`q`$.

Define the disjoint composition $`F_{d,k}=G^{\circ d}\circ A_k`$ and
$`T=q3^d`$. Then

```math
D(F_{d,k})=C(F_{d,k},x)=bs(F_{d,k},x)=T\quad\text{for every }x,
```

```math
s(F_{d,k})=q2^d,\qquad r(F_{d,k})=4^d(k+2^k).
```

Certificates must determine enough child outputs to certify the outer
function; undetermined outputs vary independently. Thus uniform certificate
costs multiply. Disjoint sensitive-block packings give the matching lower
bound. Recursive three-query evaluation gives $`D=T`$. Choosing maximally
sensitive child inputs of the required outputs attains the sensitivity bound.

## Every intermediate level is attainable

For each $`0\le j\le T`$, there is a restriction $`H_j`$ with pointwise
$`C_x=bs_x=j`$; $`H_0`$ is constant. Address-prefix restrictions establish
the base case: they leave $`A_t`$, plus irrelevant variables, realizing every
cost from one through $`q`$.

Inductively let each child have uniform cost $`t`$. Restrict the child
corresponding to $`v`$ to any uniform cost $`\ell\le t`$. The two singleton
blocks and remaining pair give weighted certificate and packing costs
$`2t+\ell`$: either the cheaper child is a singleton, or the pair contributes
$`\min(\ell,t)`$. This realizes every level from $`2t`$ through $`3t`$.

Fixing $`v`$ leaves a multiplexer with selector $`u`$. Restrict its selector
child to cost $`\ell\le t`$. Fixing selector and selected data costs
$`t+\ell`$; when both data agree, fixing both instead costs $`2t`$.
A matching packing uses the selected-data blocks and selector blocks,
combining the latter with the other data blocks when the data agree.
Thus every input has cost $`t+\ell`$, realizing levels $`t`$ through $`2t`$.
Finally fix the selector and restrict the selected child for levels below $`t`$.

## Unbounded budget excess

Each $`H_j`$ contributes $`j`$ to both one-sided profiles, and to mixed
profile index $`2j-1`$. Therefore

```math
A_0(F_{d,k}),\ A_1(F_{d,k}),\ A_{\mathrm{mix}}(F_{d,k})
\ge T(T+1)/2.
```

Take $`k=4d+10`$. Then $`r(F_{d,k})\ge T^2`$ for sufficiently large $`d`$.
The ordinary and restriction-closed products equal $`T^2`$, since the
original function already has $`c_0=c_1=C_0=C_1=T`$. Even the minimum of
all these accounts and relevance consequently satisfies

```math
\frac{V(F_{d,k})}{s(F_{d,k})bs(F_{d,k})}
\ge\frac12\left(\frac32\right)^d\longrightarrow\infty.
```

**Failure mechanism:** charging a worst possible certificate at every
attainable progress level ignores levels skipped by a large batch. Those
restrictions need not occur at the chosen algorithm's batch boundaries.
This refutes the initial budgets, while $`D=T`$ remains well within
$`s\,bs`$. The next obligation is to account for actual decreases or actual
algorithmic costs. Finite checks are recorded in the
[amortized audit](../evidence/amortized-witnesses.json); the unbounded result
rests on the preceding induction.
