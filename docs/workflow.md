# Research workflow

Keep definitions in the [glossary](glossary.md), source-backed claims in the
[literature record](literature.md), and compact conclusions in the
[research record](research.md). Each candidate round supplies its proof or
counterexample and reproducible evidence.

## Evaluate one precise proposal

State the potential or algorithm, its information and stopping rule, and all
quantifiers. Check terminal values, progress on every required branch, and
the total query budget separately. Distinguish a known-input construction from
one algorithm for an unknown input. Exact bounds and bounds up to a constant
are different obligations.

Start with simple functions and exact small cases, then seek an analytical
mechanism. Mark each obligation proved, refuted, or tentative with its precise
remaining lemma. Computation supports a claim only over its stated scope.

## Generalize every failure

Before closing a failed candidate, **try to establish the broadest justified
scope of its failure**.

1. Extract the mechanism and remove assumptions the proof does not use.
   Replace an isolated truth table by a parameterized family or a general
   lemma when possible.
2. Quantify the loss. A ratio above 1 refutes an exact coefficient; refuting
   every constant multiple requires an unbounded ratio. Seek matching upper
   bounds to identify the strongest possible separation.
3. Test robustness to adaptive choices, tie rules, rescaling, batching, and
   composition. Consider weaker success conditions and randomized algorithms
   when the same argument applies; state their models explicitly.
4. Identify the scope boundary. Prove upper bounds for classes where the
   obstruction cannot grow, and state which weakened schemes remain viable.
   Do not infer hardness of local progress from a global maximum, or vice versa.
5. Record the strongest proved statement, its assumptions, the mechanism of
   failure, and any unresolved extension. A plausible amplification is a
   tentative lead until its hypotheses and bound are proved.

The goal is the broadest supported conclusion, not an unsupported claim that
every possible generalization has been exhausted. R04's coefficient-1
counterexample and [R05's quadratic separation](round-5.md) illustrate this
step.

## Feed the obstruction into the next round

Propose the next measure in response to the accumulated mechanisms. Explain
which failures it addresses before testing it. Periodically reconsider the
proof scheme itself, including what must decrease, at which inputs, and
whether costs should be amortized across rounds.

Use protected inline math and fenced `math` blocks in repository Markdown;
prefer `\mathrm`, `\lt`, and `\gt` to known problematic renderings.
Verify substantive mathematics independently, run relevant tests, inspect
rendered formulas, and commit and push completed research updates.
