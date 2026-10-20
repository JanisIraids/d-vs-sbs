"""Independent maximum-family checks of the adaptive block-elimination problem."""

import itertools
import unittest
from functools import lru_cache

from scripts.block_drop import BlockDropProblem
from scripts.boolean import BooleanFunction
from scripts.families import disjoint_and_or


def maximum_family_unions(function, x):
    """Enumerate sensitive sets and disjoint families directly from the table."""
    value = (function.table >> x) & 1
    sensitive = [
        mask for mask in range(1, 1 << function.n)
        if ((function.table >> (x ^ mask)) & 1) != value
    ]
    minimal = [
        mask for mask in sensitive
        if not any(other != mask and other & mask == other for other in sensitive)
    ]
    best_size = 0
    unions = {0}
    for size in range(1, function.n + 1):
        for family in itertools.combinations(minimal, size):
            if all(a & b == 0 for a, b in itertools.combinations(family, 2)):
                if size > best_size:
                    best_size, unions = size, set()
                unions.add(sum(family))
    return best_size, unions


def family_oracle(function):
    """Solve by hitting unions of enumerated maximum families at each input."""
    families = tuple(maximum_family_unions(function, x) for x in range(1 << function.n))

    def success(queried, answers):
        return all(
            not size or all(queried & union for union in unions)
            for x, (size, unions) in enumerate(families)
            if x & queried == answers
        )

    @lru_cache(maxsize=None)
    def depth(queried, answers):
        if success(queried, answers):
            return 0
        return 1 + min(
            max(depth(queried | (1 << i), answers),
                depth(queried | (1 << i), answers | (1 << i)))
            for i in range(function.n) if not queried & (1 << i)
        )

    return success, depth


class BlockDropTests(unittest.TestCase):
    def test_exhaustive_maximum_family_oracle_through_three_variables(self):
        for n in range(4):
            for table in range(1 << (1 << n)):
                function = BooleanFunction(n, table)
                problem = BlockDropProblem(function)
                expected_success, expected_depth = family_oracle(function)
                for state in itertools.product((-1, 0, 1), repeat=n):
                    queried = sum(1 << i for i, a in enumerate(state) if a != -1)
                    answers = sum(1 << i for i, a in enumerate(state) if a == 1)
                    self.assertEqual(
                        problem.leaf_success(queried, answers),
                        expected_success(queried, answers), (n, table, state),
                    )
                    self.assertEqual(
                        problem.depth(queried, answers),
                        expected_depth(queried, answers), (n, table, state),
                    )
                self.assertLessEqual(problem.depth(), function.metrics()["s"])

    def test_and_or_counterexample_and_original_thresholds(self):
        function = disjoint_and_or(2, 2)
        problem = BlockDropProblem(function)
        self.assertEqual(set(problem.original_bs), {2})
        self.assertEqual(problem.depth(), 3)
        self.assertEqual(problem.depth(pointwise=False), 3)
        self.assertEqual(function.metrics()["s"], 2)
        # Original thresholds stay 2 at every leaf, even if bs dropped earlier.
        self.assertTrue(problem.leaf_success(5, 0))
        self.assertEqual(problem.depth(5, 0), 0)
        restricted = function.restrict(0, 0).restrict(1, 0)
        self.assertTrue(restricted.is_constant)
        # With x_0=0, x_2=1, the residual is x_3: it is a successful leaf,
        # whereas resetting the original problem would require one more query.
        self.assertTrue(problem.leaf_success(5, 4))
        restricted = function.restrict(0, 0).restrict(1, 1)
        self.assertFalse(restricted.is_constant)
        self.assertEqual(BlockDropProblem(restricted).depth(), 1)
        for i in range(4):
            self.assertEqual(problem.depth(1 << i, 1 << i), 2)
        for queried, answers, x in ((3, 1, 13), (5, 5, 5), (9, 9, 9)):
            self.assertFalse(problem.leaf_success(queried, answers))
            family = problem.surviving_maximum_family(x, queried)
            self.assertEqual(len(family), 2)
            self.assertTrue(all(not block & queried for block in family))
            self.assertTrue(all(block in function.minimal_sensitive_blocks(x) for block in family))
            self.assertEqual(family[0] & family[1], 0)

    def test_unequal_and_or_widths_and_global_stop(self):
        for m, k in ((2, 3), (3, 2)):
            problem = BlockDropProblem(disjoint_and_or(m, k))
            self.assertEqual(problem.depth(), m + k - 1)
            self.assertEqual(problem.depth(pointwise=False), 2)
        constant = BlockDropProblem(BooleanFunction(3, 0))
        self.assertEqual(constant.depth(), 0)
        self.assertEqual(constant.depth(pointwise=False), 0)
        with self.assertRaises(ValueError):
            constant.depth(8, 0)
        with self.assertRaises(ValueError):
            constant.depth(1, 2)


if __name__ == "__main__":
    unittest.main()
