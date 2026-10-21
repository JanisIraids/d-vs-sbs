# Deterministic queries versus sensitivity × block sensitivity

Research target: $`D(f)\le s(f)\,bs(f)`$ for every **total** Boolean function.
We seek independently defined progress measures or amortized query procedures
whose total cost on **every** path is at most that budget.

## Current conclusions

| Candidate | Status | Failure mechanism |
| --- | --- | --- |
| $`bs_0+bs_1`$ | Refuted as a unit-progress potential | Preserved maxima; also insufficient range |
| $`bs,\ bs_0bs_1,\ s\,bs,\ C_0C_1`$ | Refuted as single-query potentials | Preserved maxima |
| [Prime-certificate literal mass](docs/round-1.md) | Progress proved; budget refuted | Repeated variables across many certificates |
| [Relevant-variable count](docs/round-2.md) | Progress proved; budget refuted | Adds mutually exclusive future possibilities |
| [Fixed relevance-greedy depth](docs/round-3.md) | Progress proved; budget refuted | Misses relevance eliminated by several answers together |
| [Block elimination in at most $`s`$ adaptive queries](docs/round-4.md) | Refuted | Simultaneous local progress costs $`m+k-1`$ on disjoint AND–OR |
| [Block elimination in $`O(s)`$ adaptive queries](docs/round-5.md) | Refuted; quadratic cost is optimal in order | Untouched witness supports force $`\Theta(s^2)`$ queries |
| [Global $`bs`$ decrease in $`O(s)`$ adaptive queries](docs/round-6.md) | Refuted even when $`bs=s`$ | Distant certificate subcubes with hard-to-hit supports force $`\Theta(s^2)`$ queries |
| [Minimal-block packing volume; capped relevance](docs/round-7.md) | Range failure; single-query progress failure | Majority has too little volume; addressing keeps the relevance cap inactive |
| [Certificate products and restriction-level profiles](docs/round-8.md) | Amortized progress proved; budgets refuted | Reserving a certificate payment at every level overcounts levels that batches skip |
| [Full maximum-degree monomial batches](docs/round-9.md) | Product-decrease charge refuted with unbounded loss | Every monomial has a branch making many planned queries irrelevant |
| [Pruned shortest-certificate procedure](docs/round-10.md) | **Tentative:** general budget unproved | Counts actual executed queries; proved to handle the new counterexample families |

For an OR of disjoint ANDs, every query has a 1-answer preserving
$`(s_0,s_1,bs_0,bs_1,C_0,C_1)`$. This rules out **every** potential depending
only on those six maxima. It does not refute the target conjecture.

The latest rounds distinguish **valid progress from an adequate initial
budget**. Certificate accounts pay for complete batches and supply a state
potential decreasing at every query. They prove the target for the entire
R06 separated-subcube family. However, an explicit composition family makes
even refined certificate profiles exceed $`s\,bs`$ by an unbounded factor.

Charging the full size of a maximum-degree monomial to the decrease in
$`\min\{r,s\,bs\}`$ also fails with unbounded loss, for every monomial
choice. That failure concerns full batches; skipping newly irrelevant
variables remains viable. R10 specifies one such shortest-certificate
procedure and proves it meets the target on both new counterexample families.
The universal inequality for its actual query cost is **unproved**.

## Reading and reproduction

- [Glossary](docs/glossary.md): exact definitions and status labels.
- [Literature](docs/literature.md): source-backed claims and proof mechanisms.
- [Research record](docs/research.md): proofs, failures, and proof-scheme reviews.
- [Workflow](docs/workflow.md): candidate evaluation and generalization of failures.
- [Evidence](evidence/): reproducible finite audits; not general proofs.

Python 3.10 or later, standard library only:

```sh
python3 -m unittest discover -s tests
python3 -m scripts.audit --max-vars 4 --output evidence/baseline.json
python3 -m scripts.amortized --output evidence/amortized-witnesses.json
```

Each round links its exact reproduction commands and evidence. The baseline
potentials and R01–R03 were audited on all **65,814** truth tables through four
variables. The relevance count and greedy depth pass that finite budget audit
but fail on the larger proved families. Unit tests check the exact engine and
candidate semantics. Large-family evidence distinguishes direct witness checks from
analytical upper bounds.

Truth table bit $`x`$ is $`f(x)`$, where $`x=\sum_i x_i2^i`$. Variable indices
are zero-based; restrictions remove an input variable and renumber in ascending order.
Exact $`D`$ is computed only for validation, never used to define a candidate.

## Research workflow

Specify one candidate and the failure it addresses; evaluate its terminal
value, budget, and progress separately; record a proof, a verified failure,
or a tentative status with a precise missing lemma. Feed every failure into
the next round. **Before closing a failure, seek its broadest proved scope:**
extract a general mechanism, quantify exact versus asymptotic losses, test
adaptivity and weaker obligations, and establish boundaries or matching upper
bounds. See the [workflow](docs/workflow.md). Review the proof scheme periodically.

Next priority: prove or refute the [R10 actual-cost budget](docs/round-10.md).
Seek examples with $`r\gt s\,bs`$ where successive shortest certificates expose
fresh variables without enough compensating progress. Track skipped levels
and irrelevant variables explicitly; an independent maximum payment at every
possible block-sensitivity level is already ruled out by R08.
