"""Finite checks for the global-maximum block-sensitivity drop problem.

The random-certificate theorem is proved in docs/round-6.md. These checks
verify small instances of its exact reduction and evaluate its probability
bounds; they do not sample or enumerate the exponentially large construction.
"""

import argparse
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path

from scripts.block_drop import BlockDropProblem
from scripts.boolean import BooleanFunction
from scripts.star_block_drop import StarOR


def independent_local_bs(function, x, available):
    """Pack all sensitive subsets directly, without the minimal-block engine."""
    sensitive = tuple(
        block for block in range(1, 1 << function.n)
        if block & available == block
        and function.value(x ^ block) != function.value(x)
    )

    @lru_cache(maxsize=None)
    def pack(unused):
        return max(
            (1 + pack(unused ^ block) for block in sensitive
             if block & unused == block),
            default=0,
        )

    return pack(available)


def check_maximum_input_equivalence(max_vars=3):
    """Check every partial assignment of every truth table up to max_vars."""
    functions_checked = states_checked = 0
    for n in range(max_vars + 1):
        full = (1 << n) - 1
        for table in range(1 << (1 << n)):
            function = BooleanFunction(n, table)
            problem = BlockDropProblem(function)
            original = tuple(
                independent_local_bs(function, x, full)
                for x in range(1 << n)
            )
            maximum = max(original)
            for queried in range(1 << n):
                answers = queried
                while True:
                    remaining_bs = {
                        x: independent_local_bs(function, x, full ^ queried)
                        for x in range(1 << n) if x & queried == answers
                    }
                    maximum_inputs_drop = not maximum or all(
                        residual < maximum
                        for x, residual in remaining_bs.items()
                        if original[x] == maximum
                    )
                    global_drop = not maximum or max(remaining_bs.values()) < maximum
                    assert maximum_inputs_drop == global_drop
                    assert global_drop == problem.leaf_success(
                        queried, answers, pointwise=False
                    )
                    states_checked += 1
                    if answers == 0:
                        break
                    answers = (answers - 1) & queried
            functions_checked += 1
    return {
        "max_vars": max_vars,
        "functions_checked": functions_checked,
        "partial_assignments_checked": states_checked,
        "all_comparisons_passed": True,
    }


def certificate_family_record(name, n, certificates, copies):
    """Independently check beta_max(OR_m g)=m*tau on a small truth table."""
    certificates = tuple(certificates)
    sizes = {support.bit_count() for support, _ in certificates}
    assert len(sizes) == 1
    q = next(iter(sizes))
    assert q > 0
    assert all(0 < support < 1 << n and values & support == values
               for support, values in certificates)
    conflicts = [
        ((left_values ^ right_values) & left & right).bit_count()
        for (left, left_values), (right, right_values)
        in itertools.combinations(certificates, 2)
    ]
    assert not conflicts or min(conflicts) >= 3

    def inner_value(x):
        return int(any(x & support == values for support, values in certificates))

    inner = BooleanFunction.from_callable(n, inner_value)
    inner_problem = BlockDropProblem(inner)
    bs0 = max(inner_problem.original_bs[x]
              for x in range(1 << n) if not inner.value(x))
    assert copies * bs0 < q
    hit_mask = min(
        (mask for mask in range(1 << n)
         if all(mask & support for support, _ in certificates)),
        key=lambda mask: (mask.bit_count(), mask),
    )
    tau = hit_mask.bit_count()
    full_function = BooleanFunction.from_callable(
        n * copies,
        lambda x: int(any(inner_value((x >> (n * j)) & ((1 << n) - 1))
                          for j in range(copies))),
    )
    problem = BlockDropProblem(full_function)
    sensitivities = [0, 0]
    for x in range(1 << full_function.n):
        output = full_function.value(x)
        sensitivities[output] = max(
            sensitivities[output],
            sum(full_function.value(x ^ (1 << i)) != output
                for i in range(full_function.n)),
        )
    assert problem.global_bs == q
    assert sensitivities == [copies, q]
    computed_depth = problem.depth(pointwise=False)
    assert computed_depth == copies * tau

    background = next(x for x in range(1 << n) if not inner.value(x))
    full_background = sum(background << (n * j) for j in range(copies))
    planted_checked = 0
    for j in range(copies):
        for support, values in certificates:
            mask, assignment = support << (n * j), values << (n * j)
            planted = (full_background & ~mask) | assignment
            expected_blocks = tuple(1 << i for i in range(full_function.n)
                                    if mask & (1 << i))
            assert problem.blocks[planted] == expected_blocks
            assert problem.original_bs[planted] == problem.global_bs
            planted_checked += 1
    return {
        "name": name, "inner_variables": n, "copies": copies,
        "certificate_masks_and_values": [list(pair) for pair in certificates],
        "certificate_size": q, "minimum_pair_conflicts": min(conflicts, default=None),
        "inner_bs0": bs0, "support_hitting_number": tau,
        "s0": sensitivities[0], "s1": sensitivities[1], "bs": problem.global_bs,
        "computed_global_drop_depth": computed_depth,
        "formula_global_drop_depth": copies * tau,
        "planted_maximum_inputs_checked": planted_checked,
    }


def probability_bound_record(n=262144):
    """Evaluate log bounds from the existence proof, without sampling patterns."""
    if n < 65536 or n % 128:
        raise ValueError("n must be a multiple of 128 at least 65536")
    q, copies, h = n // 2, n // 128, n // 4096
    conflict_log_bound = math.log(n + 1) - 3 * n / 256
    # The coverage failure bound is exp(n*log(2)-exp(3*n/2048)/2).
    # Check that its exponent is below -1 in logarithms, avoiding overflow.
    coverage_below_exp_minus_one = (
        3 * n / 2048 > math.log(2 * (n * math.log(2) + 1))
    )
    assert conflict_log_bound < -1 and coverage_below_exp_minus_one
    return {
        "n": n, "q": q, "copies": copies, "h": h,
        "conflict_failure_log_upper_bound": conflict_log_bound,
        "coverage_failure_below_exp_minus_one": coverage_below_exp_minus_one,
        "sum_of_failure_bounds_below_one": True,
        "global_drop_depth_lower_bound": copies * (h + 1),
        "sensitivity": q,
        "scope": "Numerical checks of analytical bounds; no random family sampled.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    star = StarOR(3, groups=1)
    result = {
        "round": 6,
        "scope": "Exact small checks and numerical probability bounds, not a finite proof of the asymptotic theorem.",
        "maximum_input_equivalence": check_maximum_input_equivalence(),
        "finite_certificate_families": [
            certificate_family_record("OR of two three-bit ANDs", 3, ((7, 7),), 2),
            certificate_family_record("Two opposite three-bit assignments", 3, ((7, 0), (7, 7)), 1),
            certificate_family_record("Three-vertex star gadget", 9, star.local_certificates, 1),
        ],
        "probability_bound_check": probability_bound_record(),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {arguments.output}")


if __name__ == "__main__":
    main()
