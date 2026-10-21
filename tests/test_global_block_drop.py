"""Independent finite checks of the global-maximum stopping condition."""

import unittest

from scripts.global_block_drop import (
    certificate_family_record,
    check_maximum_input_equivalence,
    probability_bound_record,
)
from scripts.star_block_drop import StarOR


class GlobalBlockDropTests(unittest.TestCase):
    def test_every_partial_assignment_through_three_variables(self):
        result = check_maximum_input_equivalence()
        self.assertEqual(result["functions_checked"], 278)
        self.assertEqual(result["partial_assignments_checked"], 7070)

    def test_exact_certificate_reduction_with_multiple_copies(self):
        result = certificate_family_record("AND copies", 3, ((7, 7),), 2)
        self.assertEqual(result["bs"], 3)
        self.assertEqual(result["computed_global_drop_depth"], 2)

    def test_exact_certificate_reduction_with_opposite_assignments(self):
        result = certificate_family_record("opposite assignments", 3, ((7, 0), (7, 7)), 1)
        self.assertEqual(result["inner_bs0"], 2)
        self.assertEqual(result["computed_global_drop_depth"], 1)

    def test_exact_certificate_reduction_with_nontrivial_hitting_number(self):
        star = StarOR(3, groups=1)
        result = certificate_family_record("star", 9, star.local_certificates, 1)
        self.assertEqual(result["support_hitting_number"], 2)
        self.assertEqual(result["computed_global_drop_depth"], 2)

    def test_probability_bounds_and_strict_gap(self):
        result = probability_bound_record()
        self.assertTrue(result["sum_of_failure_bounds_below_one"])
        self.assertGreater(result["global_drop_depth_lower_bound"], result["sensitivity"])
        with self.assertRaises(ValueError):
            probability_bound_record(128)


if __name__ == "__main__":
    unittest.main()
