"""Independent checks of the complete-graph star construction."""

import unittest

from scripts.star_block_drop import StarOR, verify_family


class StarBlockDropTests(unittest.TestCase):
    def test_all_nine_bit_gadget_inputs_from_explicit_edge_constraints(self):
        function = StarOR(3, groups=1)
        edges = ((0, 1), (0, 2), (1, 2))

        def independently_satisfied(x):
            return tuple(
                vertex for vertex in range(3)
                if all(
                    ((x >> (3 * index)) & 7) == (0 if vertex == lower else 7)
                    for index, (lower, upper) in enumerate(edges)
                    if vertex in (lower, upper)
                )
            )

        truth_table = [bool(independently_satisfied(x)) for x in range(512)]
        sensitivities = [0, 0]
        positive_inputs = 0
        for x in range(512):
            satisfied = independently_satisfied(x)
            self.assertLessEqual(len(satisfied), 1)
            self.assertEqual(function.satisfied_vertices(x), satisfied)
            self.assertEqual(function.value(x), truth_table[x])
            sensitive = sum(
                truth_table[x] != truth_table[x ^ (1 << coordinate)]
                for coordinate in range(9)
            )
            sensitivities[truth_table[x]] = max(
                sensitivities[truth_table[x]], sensitive
            )
            if truth_table[x]:
                positive_inputs += 1
                self.assertEqual(sensitive, 6)
            else:
                # Independently enumerate all minimal sensitive blocks from
                # the truth table, then compare with the certificate discrepancies.
                sensitive_blocks = [
                    block for block in range(1, 512) if truth_table[x ^ block]
                ]
                minimal_blocks = {
                    block for block in sensitive_blocks
                    if not any(
                        smaller != block and smaller & block == smaller
                        for smaller in sensitive_blocks
                    )
                }
                discrepancies = {
                    sum(
                        1 << (3 * index + copy)
                        for index, (lower, upper) in enumerate(edges)
                        if vertex in (lower, upper)
                        for copy in range(3)
                        if ((x >> (3 * index + copy)) & 1)
                        != int(vertex == upper)
                    )
                    for vertex in range(3)
                }
                self.assertEqual(minimal_blocks, discrepancies)
                self.assertEqual(len(discrepancies), 3)
                self.assertNotIn(0, discrepancies)
                self.assertEqual(sum(discrepancies), 511)
                self.assertTrue(all(
                    left & right == 0
                    for left in discrepancies for right in discrepancies
                    if left != right
                ))
        self.assertEqual(positive_inputs, 24)
        self.assertEqual(sensitivities, [1, 6])

    def test_smallest_gadget_support_hitting_number(self):
        function = StarOR(3, groups=1)
        supports = [mask for mask, _ in function.local_certificates]
        minimum = min(
            queried.bit_count() for queried in range(512)
            if all(queried & mask for mask in supports)
        )
        self.assertEqual(minimum, 2)
        for coordinate in range(9):
            self.assertEqual(
                sum(bool(mask & (1 << coordinate)) for mask in supports), 2
            )

    def test_full_planted_witnesses_and_upper_query_sets(self):
        for t in (3, 4, 5):
            record = verify_family(t)
            k = 3 * (t - 1)
            cover = (t + 1) // 2
            self.assertEqual(record["analytic_bounds"]["beta_lower"], k * cover)
            self.assertEqual(
                record["finite_checks"]["upper_bound_query_count"],
                k * cover,
            )
            self.assertEqual(
                record["finite_checks"]["representative_sensitivity"], k
            )

    def test_invalid_parameters_and_inputs(self):
        for t in (0, 2, True, 3.5):
            with self.assertRaises(ValueError):
                StarOR(t)
        for groups in (0, -1, False):
            with self.assertRaises(ValueError):
                StarOR(3, groups=groups)
        function = StarOR(3)
        with self.assertRaises(ValueError):
            function.value(1 << function.n)
        with self.assertRaises(ValueError):
            function.certificate(function.m, 0)
        with self.assertRaises(ValueError):
            function.certificate(0, function.t)


if __name__ == "__main__":
    unittest.main()
