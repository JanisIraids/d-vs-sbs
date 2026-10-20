"""Reproduce exact potential audits: python3 -m scripts.audit --help."""

import argparse
import json
from pathlib import Path

from scripts.boolean import BooleanFunction
from scripts.potentials import BASELINE, potential


def inspect(name, function):
    value = potential(name, function)
    metrics = function.metrics()
    queries = []
    for coordinate in function.relevant_coordinates():
        children = [
            potential(name, function.restrict(coordinate, answer))
            for answer in (0, 1)
        ]
        queries.append({
            "coordinate": coordinate,
            "child_potentials": children,
            "adversarial_answer": 1 if children[1] >= children[0] else 0,
        })
    best_decrease = (
        value - min(max(query["child_potentials"]) for query in queries)
        if queries else None
    )
    return {
        "n": function.n,
        "table": hex(function.table),
        "metrics": metrics,
        "potential": value,
        "budget": metrics["s"] * metrics["bs"],
        "best_decrease": best_decrease,
        "queries": queries,
    }


def exhaustive(names, max_vars):
    summaries = {
        name: {
            "by_arity": [],
            "first_budget_failure": None,
            "first_progress_failure": None,
            "first_depth_exceeds_potential": None,
        } for name in names
    }
    conjecture_failures = 0
    for n in range(max_vars + 1):
        counts = {
            name: {
                "n": n, "functions": 1 << (1 << n),
                "budget_failures": 0, "progress_failures": 0,
                "depth_exceeds_potential": 0,
            } for name in names
        }
        for table in range(1 << (1 << n)):
            function = BooleanFunction(n, table)
            metrics = function.metrics()
            conjecture_failures += metrics["d"] > metrics["s"] * metrics["bs"]
            for name in names:
                value = potential(name, function)
                budget_failure = value > metrics["s"] * metrics["bs"]
                depth_failure = metrics["d"] > value
                progress_failure = False
                if not function.is_constant:
                    progress_failure = not any(
                        all(
                            potential(name, function.restrict(i, a)) <= value - 1
                            for a in (0, 1)
                        )
                        for i in function.relevant_coordinates()
                    )
                flags = (
                    ("budget_failures", "first_budget_failure", budget_failure),
                    ("progress_failures", "first_progress_failure", progress_failure),
                    ("depth_exceeds_potential", "first_depth_exceeds_potential",
                     depth_failure),
                )
                for counter, first, failed in flags:
                    if failed:
                        counts[name][counter] += 1
                        if summaries[name][first] is None:
                            summaries[name][first] = inspect(name, function)
        for name in names:
            summaries[name]["by_arity"].append(counts[name])
        print(f"Finished all {1 << (1 << n)} truth tables on {n} variables.",
              flush=True)
    return {
        "scope": {
            "domain": "total Boolean functions",
            "max_vars": max_vars,
            "function_count": sum(1 << (1 << n) for n in range(max_vars + 1)),
            "table_encoding": "bit x is f(x); x=sum_i x_i*2**i",
            "arithmetic": "exact integers",
            "enumeration": "all tables, increasing arity then integer table",
            "conjecture_counterexamples": conjecture_failures,
            "status": "finite exhaustive evidence, not a general proof",
        },
        "candidates": summaries,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", nargs="+", default=list(BASELINE))
    parser.add_argument("--max-vars", type=int, default=4, choices=range(5))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    # Validate before starting the enumeration.
    for name in args.candidates:
        potential(name, BooleanFunction(0, 0))
    report = exhaustive(args.candidates, args.max_vars)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
