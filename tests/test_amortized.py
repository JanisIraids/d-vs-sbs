"""Independent checks of amortized certificate accounts and obstructions."""

import itertools
import unittest

from scripts.amortized import (
    capped_relevance_record, check_batch_accounts, choose_batch,
    extremal_parameters, majority_record, portfolio_depth, refined_potential,
    restriction_closure, shortest_certificate_sizes, weighted_blocks,
    level_profiles, profile_accounts, profile_potential, refined_accounts,
    shortest_certificate_algorithm_depth, shortest_certificate_input_cost,
    amplified_certificate_record,
    monomial_charge_record, multilinear_coefficients, separated_pair_monomial_record,
)
from scripts.boolean import BooleanFunction, decision_tree_depth
from scripts.families import addressing


class AmortizedTests(unittest.TestCase):
    def test_weighted_packing_against_direct_disjoint_families(self):
        for table in range(256):
            function = BooleanFunction(3, table)
            expected = 0
            for x in range(8):
                blocks = function.minimal_sensitive_blocks(x)
                for selected in itertools.chain.from_iterable(
                    itertools.combinations(blocks, count)
                    for count in range(len(blocks) + 1)
                ):
                    union = 0
                    for block in selected:
                        if union & block:
                            break
                        union |= block
                    else:
                        expected = max(expected, union.bit_count())
            self.assertEqual(weighted_blocks(function), expected)

    def test_shortest_certificates_and_closures_by_explicit_restrictions(self):
        for table in range(256):
            function = BooleanFunction(3, table)
            explicit = [0, 0, 0]
            for assignment in itertools.product((None, 0, 1), repeat=3):
                residual = function
                for i in reversed(range(3)):
                    if assignment[i] is not None:
                        residual = residual.restrict(i, assignment[i])
                if residual.is_constant:
                    self.assertEqual(shortest_certificate_sizes(residual), (0, 0))
                    continue
                c = tuple(min(mask.bit_count() for mask, _value, _output
                              in residual.prime_implicants(output))
                          for output in (0, 1))
                self.assertEqual(shortest_certificate_sizes(residual), c)
                for j, value in enumerate((*c, min(c))):
                    explicit[j] = max(explicit[j], value)
            self.assertEqual(restriction_closure(function), tuple(explicit))

    def test_batch_progress_and_unit_credit_with_resets(self):
        audit = check_batch_accounts()
        self.assertEqual(audit["functions_checked"], 278)
        self.assertTrue(audit["all_checks_passed"])

    def test_weighted_majority_plateau(self):
        for n in (3, 5):
            record = majority_record(n)
            self.assertEqual(record["weighted_blocks"], n - 1)
            self.assertEqual(record["optimal_depth_audit_only"], n)

    def test_closure_improvement_and_small_shortest_certificate_obstruction(self):
        function = BooleanFunction(3, 22)
        self.assertLess(restriction_closure(function)[0], extremal_parameters(function)[4])
        obstruction = BooleanFunction(4, 7128)
        self.assertEqual(shortest_certificate_sizes(obstruction), (3, 3))
        self.assertEqual(restriction_closure(obstruction), (3, 3, 3))
        self.assertEqual(extremal_parameters(obstruction), (2, 2, 3, 3, 3, 3))

    def test_specified_policy_obeys_account_and_canonical_choices(self):
        for table in range(256):
            function = BooleanFunction(3, table)
            depth = portfolio_depth(function)
            self.assertGreaterEqual(depth, decision_tree_depth(function))
            self.assertLessEqual(depth, refined_potential(function))
            if not function.is_constant:
                account, indices, certificate = choose_batch(function)
                self.assertEqual(indices, tuple(sorted(indices)))
                if certificate is not None:
                    output = account - 1 if account in (1, 2) else None
                    expected = min(function.prime_implicants(output),
                                   key=lambda item: (item[0].bit_count(), *item))
                    self.assertEqual(certificate, expected)

    def test_level_profiles_against_explicit_restrictions(self):
        for table in range(256):
            function = BooleanFunction(3, table)
            expected = [{}, {}, {}]
            for assignment in itertools.product((None, 0, 1), repeat=3):
                residual = function
                for i in reversed(range(3)):
                    if assignment[i] is not None:
                        residual = residual.restrict(i, assignment[i])
                if residual.is_constant:
                    continue
                _s0, _s1, bs0, bs1, _c0, _c1 = extremal_parameters(residual)
                c0, c1 = shortest_certificate_sizes(residual)
                for j, (level, cost) in enumerate(zip(
                    (bs1, bs0, bs0 + bs1 - 1), (c0, c1, min(c0, c1))
                )):
                    expected[j][level] = max(expected[j].get(level, 0), cost)
            for actual, direct in zip(level_profiles(function), expected):
                self.assertEqual({j: value for j, value in enumerate(actual) if value}, direct)
            self.assertTrue(all(left <= right for left, right in zip(
                profile_accounts(function), refined_accounts(function))))
            self.assertLessEqual(portfolio_depth(function, profile=True), profile_potential(function))

    def test_large_counterexample_arithmetic_is_labeled(self):
        record = capped_relevance_record()
        self.assertEqual(record["budget"], 196)
        self.assertEqual(record["relevant_variables"], 280)
        self.assertEqual(record["child_relevance"]["address_query"], 247)
        self.assertIn("analytically", record["scope"])

    def test_shortest_policy_depth_against_direct_input_simulation(self):
        for table in range(256):
            function = BooleanFunction(3, table)
            actual = max(shortest_certificate_input_cost(function, x) for x in range(8))
            self.assertEqual(shortest_certificate_algorithm_depth(function), actual)
            self.assertGreaterEqual(actual, decision_tree_depth(function))
            self.assertLessEqual(actual, len(function.relevant_coordinates()))

    def test_amplification_budget_failure_and_algorithm_upper_bound(self):
        for depth in (2, 4, 8):
            record = amplified_certificate_record(depth)
            self.assertGreater(record["profile_portfolio_lower_bound"], record["s_times_bs_budget"])
            self.assertLessEqual(record["shortest_certificate_algorithm_depth_upper_bound"],
                                 record["s_times_bs_budget"])
            self.assertIn("analytically", record["scope"])

    def test_multilinear_coefficients_reconstruct_every_small_truth_table(self):
        for table in range(256):
            function = BooleanFunction(3, table)
            coefficients = multilinear_coefficients(function)
            for x in range(8):
                self.assertEqual(sum(value for mask, value in enumerate(coefficients)
                                     if mask & x == mask), function.value(x))

    def test_monomial_charge_counterexample_and_product_repair(self):
        record = monomial_charge_record(BooleanFunction(4, 863))
        self.assertEqual(record["degree"], 3)
        self.assertFalse(record["fixed_s_charge_passes"])
        self.assertTrue(record["current_product_charge_passes"])
        self.assertEqual(record["maximum_degree_monomials"], [
            {"mask": 13, "guaranteed_bs_drop": 1, "guaranteed_product_drop": 3},
            {"mask": 14, "guaranteed_bs_drop": 1, "guaranteed_product_drop": 3},
        ])

    def test_product_and_capped_product_analytical_counterexample(self):
        plain = separated_pair_monomial_record(13)
        self.assertTrue(plain["current_product_charge_fails"])
        self.assertFalse(plain["capped_product_charge_fails"])
        addressed = separated_pair_monomial_record(101, 7)
        self.assertTrue(addressed["current_product_charge_fails"])
        self.assertTrue(addressed["capped_product_charge_fails"])
        self.assertEqual(addressed["every_maximum_monomial_size"], 40400)
        self.assertEqual(addressed["product_drop_on_exhibited_answer"], 38208)

    def test_shortest_policy_skips_a_newly_irrelevant_planned_variable(self):
        function = addressing(1)
        # The canonical batch plans the address and the first datum. On an
        # address-one answer that datum is irrelevant and must be skipped.
        for x in range(8):
            self.assertEqual(shortest_certificate_input_cost(function, x), 2)
        self.assertEqual(shortest_certificate_algorithm_depth(function), 2)

    def test_separated_pair_small_truth_table_and_exhibited_branches(self):
        # Two four-literal assignments with three opposite shared literals.
        first, second = 15, 23
        function = BooleanFunction.from_callable(
            5, lambda x: int(x & first == 0 or x & second == second)
        )
        self.assertEqual(extremal_parameters(function)[:4], (1, 4, 2, 4))
        record = monomial_charge_record(function)
        self.assertEqual(record["degree"], 4)
        self.assertEqual([item["mask"] for item in record["maximum_degree_monomials"]],
                         [first, second])
        for mask, shared_answer in ((first, 1), (second, 0)):
            residual = function
            indices = [i for i in range(5) if mask & (1 << i)]
            for step, i in enumerate(indices):
                residual = residual.restrict(i - step, shared_answer if i < 3 else 0)
            self.assertFalse(residual.is_constant)
            self.assertEqual(residual.n, 1)


if __name__ == "__main__":
    unittest.main()
