"""Reproduce curated round witnesses with exact finite or compact evaluations.

Run ``python3 -m scripts.witnesses --round 3 --output evidence/round-3-witnesses.json``.
Large-family formulas come from the linked proofs, not a full truth-table search.
"""

import argparse
import json
from pathlib import Path

from scripts.families import addressing, disjoint_and_or, double_addressing, parity
from scripts.potentials import greedy_query, greedy_relevance_depth


def exact_record(function):
    metrics = function.metrics()
    return {
        "n": function.n,
        "table_hex": hex(function.table),
        "computed_metrics": metrics,
        "computed_relevant_coordinates": list(function.relevant_coordinates()),
        "computed_budget": metrics["s"] * metrics["bs"],
    }


def prime_masses(function):
    totals = [0, 0]
    for mask, _, output in function.prime_implicants():
        totals[output] += mask.bit_count()
    return {"W0": totals[0], "W1": totals[1], "phi": min(totals)}


def child_values(function, evaluate):
    return [
        {"coordinate": i, "answers": [
            {"answer": a, **evaluate(function.restrict(i, a))} for a in (0, 1)
        ]}
        for i in function.relevant_coordinates()
    ]


def greedy_trace(k):
    function = double_addressing(k)
    labels = list(range(function.n))
    trace = []
    while not function.is_constant:
        relevant = function.relevant_coordinates()
        scores = {
            i: min(len(relevant) - len(function.restrict(i, a).relevant_coordinates())
                   for a in (0, 1))
            for i in relevant
        }
        chosen = greedy_query(function)
        original = labels[chosen]
        answer = int(original >= (1 << k) - 1)
        assert set(scores.values()) == {1}
        assert chosen == min(scores, key=lambda i: (-scores[i], i))
        trace.append({"coordinate": original, "answer": answer, "score": scores[chosen]})
        function = function.restrict(chosen, answer)
        labels.pop(chosen)
    assert [step["coordinate"] for step in trace] == list(range((1 << k) + 2 * k))
    return {"k": k, "computed_path_length": len(trace), "trace": trace,
            "terminal_value": function.value(0),
            "scope": "One exact greedy path; no global metrics or recursive depth."}


def compact_address_witness(k, double=False):
    """Check explicit edges and one local sensitivity, without a truth table."""
    count = 1 << k
    q = count - 1
    if double:
        n = count + 2 * k
        def evaluate(x):
            a, b = (x >> count) & q, (x >> (count + k)) & q
            return ((x >> a) ^ (x >> b)) & 1
        neighbors = {1 << i for i in range(k)} | {q ^ (1 << i) for i in range(k)}
        sensitive_input = (q << (count + k)) | sum(1 << j for j in neighbors)
        edges = [(j, (j << count) | ((j ^ 1) << (count + k))) for j in range(count)]
        edges += [(count + register * k + i, 1 << (1 << i))
                  for register in (0, 1) for i in range(k)]
        bound = 2 * k + 2
    else:
        n = k + count
        def evaluate(x):
            return (x >> (k + (x & q))) & 1
        sensitive_input = sum(1 << (k + (1 << i)) for i in range(k))
        edges = [(i, 1 << (k + (1 << i))) for i in range(k)]
        edges += [(k + j, j) for j in range(count)]
        bound = k + 1
    checked_edges = []
    for coordinate, x in sorted(edges):
        outputs = [evaluate(x), evaluate(x ^ (1 << coordinate))]
        assert outputs[0] != outputs[1]
        checked_edges.append({"coordinate": coordinate, "input_hex": hex(x), "outputs": outputs})
    sensitive = [i for i in range(n)
                 if evaluate(sensitive_input) != evaluate(sensitive_input ^ (1 << i))]
    assert len(sensitive) == bound
    assert [edge["coordinate"] for edge in checked_edges] == list(range(n))
    return {
        "k": k, "n": n, "truth_table_materialized": False,
        "computed_checks": {
            "relevance_edges": checked_edges,
            "sensitivity_input_hex": hex(sensitive_input),
            "sensitivity_input_output": evaluate(sensitive_input),
            "sensitive_coordinates_at_this_input": sensitive,
            "local_sensitivity": len(sensitive),
        },
        "analytical_results": {
            "source": f"docs/round-{3 if double else 2}.md",
            "s": bound, "bs": bound, "d": bound, "phi": n,
            "budget": bound * bound,
            "status": "Proved formulas; upper bounds and greedy depth are not inferred from edge checks.",
        },
    }


def round_evidence(number):
    if number == 1:
        examples = []
        for name, function in (("parity3", parity(3)), ("and_or_2x2", disjoint_and_or(2, 2))):
            examples.append({"name": name, **exact_record(function),
                             "computed_prime_masses": prime_masses(function),
                             "computed_children": child_values(function, prime_masses)})
        return {"exact_examples": examples}
    if number == 2:
        function = addressing(2)
        return {
            "exact_A2": {**exact_record(function), "computed_phi": len(function.relevant_coordinates()),
                         "computed_children": child_values(
                             function, lambda g: {"phi": len(g.relevant_coordinates())})},
            "compact_A5": compact_address_witness(5),
        }
    function = double_addressing(2)
    return {
        "exact_H2": {**exact_record(function),
                     "computed_greedy_depth": greedy_relevance_depth(function),
                     "checked_path": greedy_trace(2)},
        "path_only_H3": greedy_trace(3),
        "compact_H9": compact_address_witness(9, double=True),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", type=int, required=True, choices=(1, 2, 3))
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = {
        "round": arguments.round, "arithmetic": "exact integers",
        "input_encoding": "x=sum(x_i*2**i); truth-table bit x is f(x)",
        "address_encoding": "A_k: low k bits address; H_k: data, then a, then b",
        "scope": "Curated witnesses. Computed checks and analytical formulas are separated.",
        **round_evidence(arguments.round),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {arguments.output}")


if __name__ == "__main__":
    main()
