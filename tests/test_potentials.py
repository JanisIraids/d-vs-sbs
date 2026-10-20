"""Independent checks of potential definitions and small family witnesses."""

import unittest

from scripts.boolean import BooleanFunction
from scripts.families import addressing, disjoint_and_or, double_addressing, parity
from scripts.potentials import (
    BASELINE,
    greedy_query,
    greedy_relevance_depth,
    potential,
    prime_literal_mass,
)


def direct_prime_certificates(function):
    """Enumerate constant subcubes directly, then remove nonminimal ones."""
    certificates = []
    for mask in range(1 << function.n):
        for values in range(1 << function.n):
            if values & ~mask:
                continue
            outputs = {
                (function.table >> x) & 1 for x in range(1 << function.n)
                if x & mask == values
            }
            if len(outputs) == 1:
                certificates.append((mask, values, outputs.pop()))
    return tuple(sorted(
        certificate for certificate in certificates
        if not any(
            other[0] != certificate[0]
            and other[0] & certificate[0] == other[0]
            and certificate[1] & other[0] == other[1]
            and other[2] == certificate[2]
            for other in certificates
        )
    ))


class PotentialTests(unittest.TestCase):
    def test_prime_literal_mass_against_direct_subcubes_through_three_variables(self):
        for n in range(4):
            for table in range(1 << (1 << n)):
                function = BooleanFunction(n, table)
                primes = direct_prime_certificates(function)
                self.assertEqual(function.prime_implicants(), primes, (n, table))
                totals = [
                    sum(mask.bit_count() for mask, _values, b in primes if b == output)
                    for output in (0, 1)
                ]
                self.assertEqual(prime_literal_mass(function), min(totals), (n, table))

    def test_prime_mass_strictly_decreases_for_every_relevant_query(self):
        for n in range(4):
            for table in range(1 << (1 << n)):
                function = BooleanFunction(n, table)
                value = prime_literal_mass(function)
                for coordinate in function.relevant_coordinates():
                    for answer in (0, 1):
                        self.assertLess(
                            prime_literal_mass(function.restrict(coordinate, answer)),
                            value,
                            (n, table, coordinate, answer),
                        )
        self.assertEqual(prime_literal_mass(parity(3)), 12)
        self.assertEqual(prime_literal_mass(disjoint_and_or(2, 2)), 4)

    def test_addressing_relevant_variables_and_metrics(self):
        function = addressing(2)
        self.assertEqual(function.n, 6)
        self.assertEqual(potential("relevant_variables", function), 6)
        self.assertEqual(
            {key: function.metrics()[key] for key in ("s", "bs", "d")},
            {"s": 3, "bs": 3, "d": 3},
        )
        for address in range(4):
            for data in range(16):
                self.assertEqual(function.value(address | (data << 2)), (data >> address) & 1)

    def test_double_addressing_greedy_depth_witness(self):
        function = double_addressing(2)
        self.assertEqual(function.n, 8)
        self.assertEqual(function.relevant_coordinates(), tuple(range(8)))
        self.assertEqual(greedy_query(function), 0)
        self.assertEqual(greedy_relevance_depth(function), 8)
        self.assertEqual(
            {key: function.metrics()[key] for key in ("s", "bs", "d")},
            {"s": 6, "bs": 6, "d": 6},
        )
        for data in range(16):
            for a in range(4):
                for b in range(4):
                    x = data | (a << 4) | (b << 6)
                    self.assertEqual(function.value(x), ((data >> a) ^ (data >> b)) & 1)

    def test_double_addressing_long_branch_preserves_original_coordinate_ids(self):
        function = double_addressing(2)
        original_input = 8 | (3 << 4) | (3 << 6)
        remaining = list(range(function.n))
        trace = []
        while not function.is_constant:
            coordinate = greedy_query(function)
            original_coordinate = remaining.pop(coordinate)
            answer = (original_input >> original_coordinate) & 1
            trace.append((original_coordinate, answer))
            function = function.restrict(coordinate, answer)
        self.assertEqual(
            trace,
            [(0, 0), (1, 0), (2, 0), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
        )
        self.assertEqual(function.table, 0)

    def test_greedy_rule_and_recurrence_through_three_variables(self):
        for n in range(4):
            for table in range(1 << (1 << n)):
                function = BooleanFunction(n, table)
                if function.is_constant:
                    self.assertEqual(greedy_relevance_depth(function), 0)
                    continue
                coordinates = function.relevant_coordinates()
                scores = {
                    coordinate: max(
                        len(function.restrict(coordinate, answer).relevant_coordinates())
                        for answer in (0, 1)
                    )
                    for coordinate in coordinates
                }
                expected = min(coordinates, key=lambda coordinate: (scores[coordinate], coordinate))
                self.assertEqual(greedy_query(function), expected, (n, table))
                child_depths = [
                    greedy_relevance_depth(function.restrict(expected, answer))
                    for answer in (0, 1)
                ]
                self.assertEqual(
                    greedy_relevance_depth(function), 1 + max(child_depths), (n, table)
                )

    def test_terminal_values_and_dummy_coordinate_invariance(self):
        candidates = ("prime_literal_mass", "relevant_variables", "greedy_relevance_depth")
        for n in range(4):
            for output in (0, 1):
                constant = BooleanFunction(n, output * ((1 << (1 << n)) - 1))
                for name in BASELINE + candidates:
                    self.assertEqual(potential(name, constant), 0, (name, n, output))
                with self.assertRaises(ValueError):
                    greedy_query(constant)
            for table in range(1 << (1 << n)):
                function = BooleanFunction(n, table)
                extended = BooleanFunction.from_callable(
                    n + 1, lambda x: function.value(x & ((1 << n) - 1))
                )
                for name in candidates:
                    self.assertEqual(
                        potential(name, extended), potential(name, function), (name, n, table)
                    )

    def test_family_boundary_cases(self):
        self.assertEqual(parity(0), BooleanFunction(0, 0))
        self.assertEqual(addressing(0), BooleanFunction(1, 2))
        self.assertTrue(double_addressing(0).is_constant)
        self.assertEqual(disjoint_and_or(1, 1), BooleanFunction(1, 2))
        for constructor, arguments in (
            (addressing, (-1,)),
            (double_addressing, (-1,)),
            (disjoint_and_or, (0, 2)),
            (disjoint_and_or, (2, 0)),
        ):
            with self.assertRaises(ValueError):
                constructor(*arguments)


if __name__ == "__main__":
    unittest.main()
