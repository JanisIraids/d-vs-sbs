"""Independent finite checks of the exact truth-table engine."""

import itertools
import unittest
from functools import lru_cache

from scripts.boolean import BooleanFunction, decision_tree_depth


def brute_local(function, x):
    """Use all sensitive blocks and all subcube assignments, without helpers."""
    n = function.n
    value = (function.table >> x) & 1
    blocks = [
        mask for mask in range(1, 1 << n)
        if ((function.table >> (x ^ mask)) & 1) != value
    ]
    sensitivity = sum(
        ((function.table >> (x ^ (1 << i))) & 1) != value
        for i in range(n)
    )
    block_sensitivity = 0
    for count in range(1, n + 1):
        for chosen in itertools.combinations(blocks, count):
            if all(a & b == 0 for a, b in itertools.combinations(chosen, 2)):
                block_sensitivity = count
                break
    certificates = [
        mask for mask in range(1 << n)
        if all(
            ((function.table >> y) & 1) == value
            for y in range(1 << n) if (x ^ y) & mask == 0
        )
    ]
    certificate = min(mask.bit_count() for mask in certificates)
    minimal_blocks = tuple(sorted(
        (mask for mask in blocks
         if not any(other != mask and other & mask == other for other in blocks)),
        key=lambda mask: (mask.bit_count(), mask),
    ))
    minimal_certificates = tuple(sorted(
        (mask for mask in certificates
         if not any(other != mask and other & mask == other for other in certificates)),
        key=lambda mask: (mask.bit_count(), mask),
    ))
    return sensitivity, block_sensitivity, certificate, minimal_blocks, minimal_certificates


def brute_depth(function):
    """Solve decision trees on surviving original inputs, without restrictions."""
    @lru_cache(maxsize=None)
    def solve(inputs):
        if len({(function.table >> x) & 1 for x in inputs}) == 1:
            return 0
        depths = []
        for coordinate in range(function.n):
            left = tuple(x for x in inputs if not (x >> coordinate) & 1)
            right = tuple(x for x in inputs if (x >> coordinate) & 1)
            if left and right:
                depths.append(1 + max(solve(left), solve(right)))
        return min(depths)

    return solve(tuple(range(1 << function.n)))


class BooleanFunctionTests(unittest.TestCase):
    def test_input_validation_and_bit_order(self):
        for n, table in ((-1, 0), (0, 2), (2, 16), (2, -1)):
            with self.assertRaises(ValueError):
                BooleanFunction(n, table)
        function = BooleanFunction.from_callable(3, lambda x: (x >> 1) & 1)
        self.assertEqual(function.table, 0b11001100)
        self.assertEqual(function.relevant_coordinates(), (1,))
        self.assertEqual(function.restrict(1, 1).table, 15)
        with self.assertRaises(ValueError):
            function.restrict(3, 0)
        with self.assertRaises(ValueError):
            function.restrict(0, 2)
        with self.assertRaises(ValueError):
            function.value(8)
        with self.assertRaises(ValueError):
            BooleanFunction.from_callable(2, lambda x: 2)

    def test_exhaustive_against_independent_definitions_through_three_variables(self):
        for n in range(4):
            for table in range(1 << (1 << n)):
                function = BooleanFunction(n, table)
                expected = dict.fromkeys(("s0", "s1", "bs0", "bs1", "c0", "c1"), 0)
                for x in range(1 << n):
                    s, bs, c, blocks, certificates = brute_local(function, x)
                    output = (table >> x) & 1
                    for name, value in (("s", s), ("bs", bs), ("c", c)):
                        key = name + str(output)
                        expected[key] = max(expected[key], value)
                    self.assertEqual(function.minimal_sensitive_blocks(x), blocks)
                    self.assertEqual(function.minimal_certificates(x), certificates)
                expected["d"] = brute_depth(function)
                for name in ("s", "bs", "c"):
                    expected[name] = max(expected[name + "0"], expected[name + "1"])
                self.assertEqual(function.metrics(), expected, (n, table))

    def test_standard_families(self):
        for n in range(7):
            for value in (0, 1):
                constant = BooleanFunction(n, value * ((1 << (1 << n)) - 1))
                self.assertTrue(constant.is_constant)
                self.assertEqual(set(constant.metrics().values()), {0})
                self.assertEqual(constant.prime_implicants(), ((0, 0, value),))
            if not n:
                continue
            conjunction = BooleanFunction.from_callable(n, lambda x: x == (1 << n) - 1)
            disjunction = BooleanFunction.from_callable(n, lambda x: x != 0)
            parity = BooleanFunction.from_callable(n, lambda x: x.bit_count() % 2)
            for name in ("s", "bs", "c"):
                self.assertEqual((conjunction.metrics()[name + "0"],
                                  conjunction.metrics()[name + "1"]), (1, n))
                self.assertEqual((disjunction.metrics()[name + "0"],
                                  disjunction.metrics()[name + "1"]), (n, 1))
                self.assertEqual((parity.metrics()[name + "0"],
                                  parity.metrics()[name + "1"]), (n, n))
            self.assertEqual(decision_tree_depth(conjunction), n)
            self.assertEqual(decision_tree_depth(disjunction), n)
            self.assertEqual(decision_tree_depth(parity), n)
        for threshold in range(1, 6):
            function = BooleanFunction.from_callable(5, lambda x: x.bit_count() >= threshold)
            self.assertEqual(function.metrics()["s0"], 6 - threshold)
            self.assertEqual(function.metrics()["s1"], threshold)
            self.assertEqual(function.metrics()["d"], 5)

    def test_and_or_preservation_obstruction(self):
        function = BooleanFunction.from_callable(
            4, lambda x: (x & 3) == 3 or (x & 12) == 12
        )
        expected = {key: 2 for key in ("s0", "s1", "bs0", "bs1", "c0", "c1")}
        self.assertEqual(
            {key: function.metrics()[key] for key in expected}, expected
        )
        self.assertEqual(function.metrics()["d"], 4)
        for coordinate in range(4):
            restricted = function.restrict(coordinate, 1)
            self.assertEqual(
                {key: restricted.metrics()[key] for key in expected}, expected
            )

    def test_coordinate_symmetries_output_complement_and_irrelevant_variables(self):
        for table in range(256):
            function = BooleanFunction(3, table)
            original = function.metrics()
            complemented = BooleanFunction(3, table ^ 255).metrics()
            for name in ("s", "bs", "c"):
                self.assertEqual(complemented[name + "0"], original[name + "1"])
                self.assertEqual(complemented[name + "1"], original[name + "0"])
            self.assertEqual(complemented["d"], original["d"])
            flipped = BooleanFunction.from_callable(3, lambda x: function.value(x ^ 5))
            permuted = BooleanFunction.from_callable(
                3, lambda x: function.value(((x & 1) << 2) | (x & 2) | ((x & 4) >> 2))
            )
            extended = BooleanFunction.from_callable(4, lambda x: function.value(x & 7))
            self.assertEqual(flipped.metrics(), original)
            self.assertEqual(permuted.metrics(), original)
            self.assertEqual(extended.metrics(), original)
            self.assertEqual(extended.restrict(3, 0), function)
            self.assertEqual(extended.restrict(3, 1), function)
            for coordinate in range(3):
                for answer in (0, 1):
                    restricted = function.restrict(coordinate, answer)
                    for key, value in restricted.metrics().items():
                        self.assertLessEqual(value, original[key])

    def test_restriction_renumbering_and_prime_implicants(self):
        function = BooleanFunction.from_callable(4, lambda x: x.bit_count() == 2)
        for coordinate in range(4):
            for answer in (0, 1):
                restricted = function.restrict(coordinate, answer)
                for x in range(8):
                    bits = [(x >> i) & 1 for i in range(3)]
                    bits.insert(coordinate, answer)
                    original = sum(bit << i for i, bit in enumerate(bits))
                    self.assertEqual(restricted.value(x), function.value(original))
        conjunction = BooleanFunction.from_callable(2, lambda x: x == 3)
        self.assertEqual(conjunction.prime_implicants(1), ((3, 3, 1),))
        self.assertEqual(conjunction.prime_implicants(0), ((1, 0, 0), (2, 0, 0)))
        first = conjunction.metrics()
        first["d"] = -1
        self.assertEqual(conjunction.metrics()["d"], 2)


if __name__ == "__main__":
    unittest.main()
