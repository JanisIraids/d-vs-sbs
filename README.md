# Deterministic queries versus sensitivity × block sensitivity

Research target: $`D(f)\le s(f)\,bs(f)`$ for every **total** Boolean function.
We seek independently defined progress measures with a sufficient initial
budget and a query that decreases the measure on **both** answers.

## Current conclusions

| Candidate | Status | Failure mechanism |
| --- | --- | --- |
| $`bs_0+bs_1`$ | Refuted as a unit-progress potential | Preserved maxima; also insufficient range |
| $`bs,\ bs_0bs_1,\ s\,bs,\ C_0C_1`$ | Refuted as single-query potentials | Preserved maxima |
| [Prime-certificate literal mass](docs/round-1.md) | Progress proved; budget refuted | Repeated coordinates across many certificates |
| [Relevant-coordinate count](docs/round-2.md) | Progress proved; budget refuted | Adds mutually exclusive future possibilities |
| [Fixed relevance-greedy depth](docs/round-3.md) | Progress proved; budget refuted | Misses relevance eliminated by several answers together |

For an OR of disjoint ANDs, every query has a 1-answer preserving
$`(s_0,s_1,bs_0,bs_1,C_0,C_1)`$. This rules out **every** potential depending
only on those six maxima. It does not refute the target conjecture.

The three new candidates respectively fail on parity ($`12>9`$), addressing
($`37>36`$), and two independent selectors ($`530>400`$). Each has a complete
progress proof and an unbounded family of budget failures; the conjecture
remains unresolved.

## Reading and reproduction

- [Glossary](docs/glossary.md): exact definitions and status labels.
- [Literature](docs/literature.md): source-backed claims and proof mechanisms.
- [Research record](docs/research.md): proofs, failures, and proof-scheme reviews.
- [Evidence](evidence/): reproducible finite audits; not general proofs.

Python 3.10 or later, standard library only:

```sh
python3 -m unittest discover -s tests
python3 -m scripts.audit --max-vars 4 --output evidence/baseline.json
```

Each round links its exact reproduction commands and evidence. Every candidate
was audited on all **65,814** truth tables through four variables. The relevance
count and greedy depth pass that finite budget audit but fail on the larger
proved families. Fourteen unit tests check the exact engine and candidate
semantics. Large-family evidence distinguishes direct witness checks from
analytical upper bounds.

Truth table bit $`x`$ is $`f(x)`$, where $`x=\sum_i x_i2^i`$. Coordinates are
zero-based; restrictions remove a coordinate and renumber in ascending order.
Exact $`D`$ is computed only for validation, never used to define a candidate.

## Research workflow

Specify one candidate and the failure it addresses; evaluate its terminal
value, budget, and progress separately; record a proof, a verified failure,
or a tentative status with a precise missing lemma. Feed every failure into
the next round. Review changes to the proof scheme periodically.

The initial milestone—literature, simple candidates, and three further
rounds—is complete. Next priority: share certificate charges while accounting
for relevance eliminated by several queries. See the
[proof-scheme review](docs/round-3.md#final-scheme-review-and-next-obligation)
for batch/state proposals and the missing universal lemma.
