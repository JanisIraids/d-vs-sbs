# R01: prime-certificate literal mass

These are local derivations, with no claim of historical novelty. See the [glossary](glossary.md) and [research record](research.md) for definitions and the exact proof obligations.

**Definition.** Let

```math
\Phi_1(g)=\min_{b\in\{0,1\}}W_b(g),\qquad
W_b(g)=\sum_{P\in\mathcal P_b(g)}|P|.
```

This counts all prime certificates, not a minimum cover. It retains certificate
sizes and multiplicities that the six extremal parameters in F01 discard.

**Unit progress: proved for every relevant query.** Fix relevant $`i`$, an
answer $`a`$, and output $`b`$. Every prime $`b`$-certificate $`Q`$ of
$`g|_{i=a}`$ lifts to a prime $`b`$-certificate
$`P\subseteq Q\cup\{i=a\}`$ of $`g`$. Minimality of $`Q`$ forces
$`P\setminus\{i=a\}=Q`$: this projection is already a certificate of the
restriction. Consequently $`P`$ equals either $`Q`$ or $`Q\cup\{i=a\}`$.
Choosing one lift for each $`Q`$ gives an injection into $`\mathcal P_b(g)`$.

Relevance of $`i`$ supplies a prime $`b`$-certificate $`P_*`$ containing $`i`$:
at the $`b`$-endpoint of a relevance edge, every certificate must fix $`i`$.
If the injection uses $`P_*`$, that certificate loses one literal; otherwise
its positive length is omitted from the child sum. Thus

```math
W_b(g|_{i=a})\le W_b(g)-1.
```

Taking the parent-minimizing output $`b`$ proves the same inequality for
$`\Phi_1`$. The argument includes constant children under the glossary's
empty-certificate conventions.

**Repair of F01.** For the disjoint OR of $`m`$ width-$`k`$ conjunctions,
the prime 1-certificates are the $`m`$ terms, whereas a prime 0-certificate
chooses one zero per term. Hence $`W_1=mk`$, $`W_0=mk^m`$, and
$`\Phi_1=mk`$. A 1-answer decreases the total term width by one; a 0-answer
removes an entire term.

**Budget failure: proved.** For parity on $`n\ge1`$ variables every certificate
fixes all variables, and each output has $`2^{n-1}`$ prime certificates.
Therefore

```math
\Phi_1(\mathrm{PARITY}_n)=n2^{n-1},\qquad
s(\mathrm{PARITY}_n)bs(\mathrm{PARITY}_n)=n^2.
```

At $`n=3`$, $`12>9`$. The ratio is unbounded, so a fixed rescaling cannot
repair the normalized budget. The mechanism is certificate multiplicity:
the same coordinates are charged separately across many assignments.

**Finite audit.** All 65,814 truth tables through four variables satisfy unit
progress; 28,964 violate the initial budget. The first budget witness in the
documented enumeration is the complement of three-bit majority (`0x17`):
$`\Phi_1=6>s\,bs=4`$. Parity gives the unbounded family used above.
See [full audit](../evidence/round-1.json) and
[curated witnesses](../evidence/round-1-witnesses.json).

```sh
python3 -m scripts.audit --candidates prime_literal_mass --max-vars 4 --output evidence/round-1.json
python3 -m scripts.witnesses --round 1 --output evidence/round-1-witnesses.json
```
