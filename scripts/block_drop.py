"""Exact adaptive query cost for eliminating every maximum block packing.

The stopping condition compares residual local block sensitivity with its value
at the *original* input. Thresholds do not reset after an individual query.
Run ``python3 -m scripts.block_drop --output evidence/round-4-witnesses.json``.
"""

import argparse
import json
from functools import lru_cache
from pathlib import Path

from scripts.boolean import BooleanFunction
from scripts.families import disjoint_and_or


@lru_cache(maxsize=65536)
def packing_number(blocks, available):
    """Maximum disjoint packing of the listed blocks inside ``available``."""
    return max(
        (1 + packing_number(blocks, available ^ block)
         for block in blocks if available & block == block),
        default=0,
    )


class BlockDropProblem:
    """A fixed original function and the associated leaf-stopping problem.

    States use original-coordinate masks: ``queried`` records fixed coordinates
    and ``answers`` records their 1 values. A local sensitive block survives
    exactly when it is disjoint from ``queried``.
    """

    def __init__(self, function):
        self.function = function
        self.full_mask = (1 << function.n) - 1
        self.blocks = tuple(
            function.minimal_sensitive_blocks(x) for x in range(1 << function.n)
        )
        self.original_bs = tuple(
            packing_number(blocks, self.full_mask) for blocks in self.blocks
        )
        self.global_bs = max(self.original_bs)
        self._depths = {}
        self._choices = {}

    def _validate_state(self, queried, answers):
        if not 0 <= queried <= self.full_mask or answers & queried != answers:
            raise ValueError("state masks must describe a partial input")

    def local_bs(self, x, queried=0):
        """Residual local bs at the completion ``x`` after fixing ``queried``."""
        self.function.value(x)
        self._validate_state(queried, x & queried)
        return packing_number(self.blocks[x], self.full_mask ^ queried)

    def leaf_success(self, queried, answers, *, pointwise=True):
        """Whether the leaf strictly decreases all applicable original values.

        Pointwise mode compares each completion with its original local bs.
        The optional global mode instead asks whether the residual global bs
        is strictly smaller than the original global bs. Constants pass both.
        """
        self._validate_state(queried, answers)
        for x in range(1 << self.function.n):
            if x & queried != answers:
                continue
            threshold = self.original_bs[x] if pointwise else self.global_bs
            if threshold and self.local_bs(x, queried) >= threshold:
                return False
        return True

    def depth(self, queried=0, answers=0, *, pointwise=True):
        """Least additional worst-case queries, with original thresholds fixed."""
        self._validate_state(queried, answers)
        state = (queried, answers, pointwise)
        if state not in self._depths:
            if self.leaf_success(queried, answers, pointwise=pointwise):
                self._depths[state] = 0
            else:
                candidates = []
                for i in range(self.function.n):
                    bit = 1 << i
                    if queried & bit:
                        continue
                    children = (
                        self.depth(queried | bit, answers, pointwise=pointwise),
                        self.depth(queried | bit, answers | bit, pointwise=pointwise),
                    )
                    candidates.append((1 + max(children), i))
                best_depth, coordinate = min(candidates)
                self._depths[state] = best_depth
                self._choices[state] = coordinate
        return self._depths[state]

    def optimal_tree(self, queried=0, answers=0, *, pointwise=True):
        """Return one optimal tree, with coordinates in the original numbering."""
        depth = self.depth(queried, answers, pointwise=pointwise)
        if not depth:
            return {"queried_mask": queried, "answer_mask": answers, "leaf": True}
        coordinate = self._choices[(queried, answers, pointwise)]
        bit = 1 << coordinate
        return {
            "coordinate": coordinate,
            "0": self.optimal_tree(queried | bit, answers, pointwise=pointwise),
            "1": self.optimal_tree(queried | bit, answers | bit, pointwise=pointwise),
        }

    def surviving_maximum_family(self, x, queried):
        """Return an untouched original maximum family, or None if none survives."""
        available = self.full_mask ^ queried
        target = self.original_bs[x]
        if not target or self.local_bs(x, queried) < target:
            return None
        family = []
        while target:
            block = next(
                block for block in self.blocks[x]
                if available & block == block
                and packing_number(self.blocks[x], available ^ block) == target - 1
            )
            family.append(block)
            available ^= block
            target -= 1
        return tuple(family)


def exhaustive_small_cases(max_vars=3):
    """Audit all truth tables, including constants and irrelevant coordinates."""
    rows = []
    first_failure = None
    for n in range(max_vars + 1):
        failures = 0
        histogram = {}
        for table in range(1 << (1 << n)):
            function = BooleanFunction(n, table)
            problem = BlockDropProblem(function)
            depth = problem.depth()
            sensitivity = max(
                sum(block.bit_count() == 1 for block in blocks)
                for blocks in problem.blocks
            )
            histogram[str(depth)] = histogram.get(str(depth), 0) + 1
            if depth > sensitivity:
                failures += 1
                if first_failure is None:
                    first_failure = {
                        "n": n, "table_hex": hex(table),
                        "s": sensitivity, "pointwise_drop_depth": depth,
                    }
        rows.append({
            "n": n, "functions_checked": 1 << (1 << n),
            "pointwise_drop_depth_histogram": histogram,
            "depth_exceeds_s": failures,
        })
    return {
        "max_vars": max_vars,
        "functions_checked": sum(row["functions_checked"] for row in rows),
        "depth_exceeds_s": sum(row["depth_exceeds_s"] for row in rows),
        "by_arity": rows,
        "first_failure": first_failure,
    }


def and_or_record(m, k):
    function = disjoint_and_or(m, k)
    problem = BlockDropProblem(function)
    return {
        "m": m, "k": k, "n": function.n, "table_hex": hex(function.table),
        "computed_metrics": function.metrics(),
        "computed_pointwise_drop_depth": problem.depth(),
        "computed_global_drop_depth": problem.depth(pointwise=False),
    }


def two_query_obstruction():
    """Symmetry fixes the first query to coordinate 0, answered 1."""
    function = disjoint_and_or(2, 2)
    problem = BlockDropProblem(function)
    branches = []
    for coordinate in (1, 2, 3):
        answer = int(coordinate != 1)
        queried = 1 | (1 << coordinate)
        answers = 1 | (answer << coordinate)
        x = next(
            x for x in range(16)
            if x & queried == answers
            and problem.local_bs(x, queried) == problem.original_bs[x]
        )
        family = problem.surviving_maximum_family(x, queried)
        assert family is not None and len(family) == 2
        assert all(block & queried == 0 for block in family)
        branches.append({
            "second_coordinate": coordinate, "second_answer": answer,
            "queried_mask": queried, "answer_mask": answers,
            "witness_input": x, "witness_output": function.value(x),
            "original_local_bs": problem.original_bs[x],
            "residual_local_bs": problem.local_bs(x, queried),
            "untouched_maximum_family_masks": list(family),
        })
    return {
        "first_coordinate": 0, "first_answer": 1,
        "symmetry": "Permute the two terms and the two coordinates within each term.",
        "all_possible_second_coordinates": branches,
        "optimal_pointwise_tree": problem.optimal_tree(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = {
        "round": 4,
        "arithmetic": "exact integers",
        "input_encoding": "x=sum(x_i*2**i); truth-table bit x is f(x)",
        "mask_encoding": "Bit i indicates original coordinate i; coordinates are zero-based.",
        "pointwise_stopping_condition":
            "For every consistent x with original bs(f,x)>0, residual bs is strictly smaller.",
        "global_stopping_condition":
            "Residual maximum bs is strictly smaller than the original maximum; constants pass.",
        "scope": "Exact minimax computation, original input thresholds retained at every state.",
        "exhaustive_small_cases": exhaustive_small_cases(),
        "and_or_examples": [
            and_or_record(m, k) for m, k in ((2, 2), (2, 3), (3, 2), (3, 3))
        ],
        "two_query_obstruction": two_query_obstruction(),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {arguments.output}")


if __name__ == "__main__":
    main()
