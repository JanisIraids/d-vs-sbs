"""Exact finite checks of weighted blocks and amortized certificate accounts.

Candidate accounts and query choices never consult optimal decision-tree
depth. The audit imports that invariant solely for comparison. Large-family
records evaluate formulas proved in the documentation, not truth tables.
"""

import argparse
import json
from functools import lru_cache
from pathlib import Path

from scripts.boolean import BooleanFunction, _local_parameters


@lru_cache(maxsize=None)
def extremal_parameters(function):
    """Return (s0,s1,bs0,bs1,C0,C1) without computing decision-tree depth."""
    result = [0] * 6
    for x in range(1 << function.n):
        output = function.value(x)
        local = _local_parameters(
            function.n, function.minimal_sensitive_blocks(x)
        )
        for parameter, value in enumerate(local):
            index = 2 * parameter + output
            result[index] = max(result[index], value)
    return tuple(result)


@lru_cache(maxsize=None)
def _weighted_packing(n, blocks):
    @lru_cache(maxsize=None)
    def pack(available):
        return max(
            (block.bit_count() + pack(available ^ block)
             for block in blocks if block & available == block),
            default=0,
        )
    return pack((1 << n) - 1)


@lru_cache(maxsize=None)
def weighted_blocks(function):
    """Maximum total size of disjoint inclusion-minimal sensitive blocks."""
    return max(
        _weighted_packing(function.n, function.minimal_sensitive_blocks(x))
        for x in range(1 << function.n)
    )


@lru_cache(maxsize=None)
def _forcing_costs(function):
    """Shortest certificates; n+1 is a sentinel for an absent output."""
    if function.is_constant:
        return ((0, function.n + 1) if function.table == 0
                else (function.n + 1, 0))
    children = [
        _forcing_costs(function.restrict(i, answer))
        for i in function.relevant_coordinates() for answer in (0, 1)
    ]
    return tuple(1 + min(child[output] for child in children)
                 for output in (0, 1))


def shortest_certificate_sizes(function):
    """Return c0,c1 on nonconstants; use (0,0) on constants by convention."""
    return (0, 0) if function.is_constant else _forcing_costs(function)


@lru_cache(maxsize=None)
def restriction_closure(function):
    """Return K0,K1,Kmix: restriction maxima of c0,c1,min(c0,c1)."""
    if function.is_constant:
        return (0, 0, 0)
    c0, c1 = shortest_certificate_sizes(function)
    children = [
        restriction_closure(function.restrict(i, answer))
        for i in function.relevant_coordinates() for answer in (0, 1)
    ]
    initial = (c0, c1, min(c0, c1))
    return tuple(max(initial[j], *(child[j] for child in children))
                 for j in range(3))


def raw_accounts(function):
    """The relevance and classical certificate/block-sensitivity bounds."""
    if function.is_constant:
        return (0, 0, 0)
    _s0, _s1, bs0, bs1, c0, c1 = extremal_parameters(function)
    return (len(function.relevant_coordinates()), c0 * bs1, c1 * bs0)


def refined_accounts(function):
    """Accounts in deterministic tie order: relevance, P0, P1, Pmix."""
    if function.is_constant:
        return (0, 0, 0, 0)
    _s0, _s1, bs0, bs1, _c0, _c1 = extremal_parameters(function)
    k0, k1, kmix = restriction_closure(function)
    return (len(function.relevant_coordinates()), k0 * bs1,
            k1 * bs0, kmix * (bs0 + bs1 - 1))


def refined_potential(function):
    return min(refined_accounts(function))


@lru_cache(maxsize=None)
def level_profiles(function):
    """Return restriction-maximal certificate costs indexed by drop level.

    The first two profiles use opposite-output block sensitivity. The third
    uses bs0+bs1-1. Entry zero is always zero; constants have empty profiles.
    """
    if function.is_constant:
        return ((), (), ())
    _s0, _s1, bs0, bs1, _c0, _c1 = extremal_parameters(function)
    c0, c1 = shortest_certificate_sizes(function)
    levels = (bs1, bs0, bs0 + bs1 - 1)
    costs = (c0, c1, min(c0, c1))
    profiles = [[0] * (level + 1) for level in levels]
    for j in range(3):
        profiles[j][levels[j]] = costs[j]
    for i in function.relevant_coordinates():
        for answer in (0, 1):
            children = level_profiles(function.restrict(i, answer))
            for j, child in enumerate(children):
                for level, cost in enumerate(child):
                    profiles[j][level] = max(profiles[j][level], cost)
    return tuple(tuple(profile) for profile in profiles)


def profile_accounts(function):
    return (len(function.relevant_coordinates()),
            *(sum(profile) for profile in level_profiles(function)))


def profile_potential(function):
    return min(profile_accounts(function))


def choose_batch(function, profile=False):
    """Choose the first minimum account and its canonical query batch.

    Certificates are ordered by (size, mask, values, output). Variables in
    the chosen mask are queried in increasing index order. The returned
    certificate is None for the one-variable relevance batch.
    """
    if function.is_constant:
        raise ValueError("a constant function needs no batch")
    accounts = profile_accounts(function) if profile else refined_accounts(function)
    index = min(range(4), key=lambda j: accounts[j])
    if index == 0:
        return index, (function.relevant_coordinates()[0],), None
    output = index - 1 if index in (1, 2) else None
    certificate = min(
        function.prime_implicants(output),
        key=lambda item: (item[0].bit_count(), *item),
    )
    mask, _values, _output = certificate
    indices = tuple(i for i in range(function.n) if mask & (1 << i))
    return index, indices, certificate


def batch_leaves(function, profile=False):
    """Enumerate (restriction, cost) leaves, stopping early at constants."""
    _account, indices, _certificate = choose_batch(function, profile=profile)

    def visit(current, position):
        if current.is_constant or position == len(indices):
            yield current, position
            return
        # All preceding selected indices were smaller and have been removed.
        current_index = indices[position] - position
        for answer in (0, 1):
            yield from visit(current.restrict(current_index, answer), position + 1)

    yield from visit(function, 0)


def shortest_batch(function):
    """Canonical shortest certificate of either output, then increasing indices."""
    if function.is_constant:
        raise ValueError("a constant function needs no batch")
    certificate = min(function.prime_implicants(),
                      key=lambda item: (item[0].bit_count(), *item))
    mask, _values, _output = certificate
    return tuple(i for i in range(function.n) if mask & (1 << i))


def _shortest_batch_leaves(function):
    indices = shortest_batch(function)

    def visit(current, position, removed):
        if current.is_constant or position == len(indices):
            yield current, removed
            return
        i = indices[position] - removed
        if i not in current.relevant_coordinates():
            yield from visit(current, position + 1, removed)
            return
        for answer in (0, 1):
            yield from visit(current.restrict(i, answer), position + 1, removed + 1)

    yield from visit(function, 0, 0)


@lru_cache(maxsize=None)
def shortest_certificate_algorithm_depth(function):
    """Fixed shortest-certificate policy, skipping newly irrelevant variables.

    Finish the planned batch before selecting another certificate, even if
    an answer already contradicts it. This is a fixed algorithm, not optimal D.
    """
    if function.is_constant:
        return 0
    return max(cost + shortest_certificate_algorithm_depth(residual)
               for residual, cost in _shortest_batch_leaves(function))


def shortest_certificate_input_cost(function, x):
    """Direct simulation at one input, independent of the depth recurrence."""
    function.value(x)
    count = 0
    while not function.is_constant:
        indices = shortest_batch(function)
        removed = 0
        for original_index in indices:
            i = original_index - removed
            if i not in function.relevant_coordinates():
                continue
            answer = (x >> i) & 1
            function = function.restrict(i, answer)
            x = (x & ((1 << i) - 1)) | ((x >> (i + 1)) << i)
            count += 1
            removed += 1
            if function.is_constant:
                break
    return count


@lru_cache(maxsize=None)
def portfolio_depth(function, profile=False):
    """Depth of the specified batch policy, without optimal-depth queries."""
    if function.is_constant:
        return 0
    return max(cost + portfolio_depth(residual, profile=profile)
               for residual, cost in batch_leaves(function, profile=profile))


def check_batch_accounts(max_vars=3):
    """Check every certificate choice and assignment, including state credit.

    This audit verifies all three certificate accounts, not merely whichever
    one the portfolio selects. Queries are substituted directly from each
    certificate mask, independently of batch_leaves and choose_batch.
    """
    functions = leaves = query_steps = resets = 0
    for n in range(max_vars + 1):
        for table in range(1 << (1 << n)):
            function = BooleanFunction(n, table)
            functions += 1
            if function.is_constant:
                assert refined_potential(function) == 0
                continue
            c0, c1 = shortest_certificate_sizes(function)
            initial_variants = (refined_accounts(function), profile_accounts(function))
            for mask, values, output in function.prime_implicants():
                size = mask.bit_count()
                eligible = []
                if size == (c0, c1)[output]:
                    eligible.append(output + 1)
                if size == min(c0, c1):
                    eligible.append(3)
                if not eligible:
                    continue
                indices = tuple(i for i in range(n) if mask & (1 << i))
                for answers in range(1 << size):
                    residual = function
                    for step, i in enumerate(indices):
                        residual = residual.restrict(i - step, (answers >> step) & 1)
                        for initial_accounts in initial_variants:
                            for account in eligible:
                                before = initial_accounts[account] - step
                                after = initial_accounts[account] - step - 1
                                assert after == before - 1 and after >= 0
                                query_steps += 1
                    final_variants = (refined_accounts(residual), profile_accounts(residual))
                    for initial_accounts, final_accounts in zip(initial_variants, final_variants):
                        for account in eligible:
                            credit = initial_accounts[account] - size
                            assert final_accounts[account] <= credit
                            assert min(final_accounts) <= credit
                            resets += 1
                    leaves += 1
            for use_profile, potential in ((False, refined_potential), (True, profile_potential)):
                for residual, cost in batch_leaves(function, profile=use_profile):
                    assert cost + potential(residual) <= potential(function)
                assert portfolio_depth(function, profile=use_profile) <= potential(function)
    return {"max_vars": max_vars, "functions_checked": functions,
            "certificate_answer_leaves_checked": leaves,
            "unit_credit_steps_checked": query_steps,
            "nonincreasing_resets_checked": resets,
            "all_checks_passed": True}


def check_budgets(max_vars=4):
    """Exhaustive finite budget audit; relevance makes these sizes easy."""
    records = []
    names = ("relevance", "P0", "P1", "Pmix")
    for n in range(max_vars + 1):
        counts = {name: 0 for name in names}
        refined_failures = profile_failures = raw_failures = relevance_failures = 0
        algorithm_failures = 0
        for table in range(1 << (1 << n)):
            function = BooleanFunction(n, table)
            s0, s1, bs0, bs1, _c0, _c1 = extremal_parameters(function)
            budget = max(s0, s1) * max(bs0, bs1)
            accounts = refined_accounts(function)
            profile_values = profile_accounts(function)
            assert all(left <= right for left, right in zip(profile_values, accounts))
            for name, value in zip(names, accounts):
                counts[name] += value > budget
            refined_failures += min(accounts) > budget
            profile_failures += min(profile_values) > budget
            raw_failures += min(raw_accounts(function)) > budget
            relevance_failures += accounts[0] > budget
            algorithm_failures += shortest_certificate_algorithm_depth(function) > budget
        records.append({"variables": n, "functions_checked": 1 << (1 << n),
                        "refined_portfolio_budget_failures": refined_failures,
                        "profile_portfolio_budget_failures": profile_failures,
                        "raw_portfolio_budget_failures": raw_failures,
                        "relevance_budget_failures": relevance_failures,
                        "shortest_certificate_algorithm_budget_failures": algorithm_failures,
                        "individual_account_budget_failures": counts})
    return {"max_vars": max_vars, "records": records,
            "limitation": "Every audited function has r <= s*bs; portfolio budget success follows already from its relevance account."}


def majority_record(n):
    from scripts.boolean import decision_tree_depth
    if n < 3 or n % 2 == 0:
        raise ValueError("use an odd number of variables at least three")
    function = BooleanFunction.from_callable(n, lambda x: int(x.bit_count() > n // 2))
    weighted = weighted_blocks(function)
    children = [[weighted_blocks(function.restrict(i, answer)) for answer in (0, 1)]
                for i in range(n)]
    assert weighted == n - 1 and all(pair == [weighted, weighted] for pair in children)
    return {"variables": n, "table": function.table, "weighted_blocks": weighted,
            "child_weighted_blocks": children,
            "optimal_depth_audit_only": decision_tree_depth(function)}


def closure_record(n, table):
    function = BooleanFunction(n, table)
    return {"variables": n, "table": table,
            "shortest_certificates": shortest_certificate_sizes(function),
            "closure_K0_K1_Kmix": restriction_closure(function),
            "extremal_s0_s1_bs0_bs1_C0_C1": extremal_parameters(function),
            "raw_accounts": raw_accounts(function),
            "refined_accounts": refined_accounts(function),
            "level_profiles": level_profiles(function),
            "profile_accounts": profile_accounts(function),
            "policy_depth": portfolio_depth(function),
            "profile_policy_depth": portfolio_depth(function, profile=True),
            "shortest_certificate_algorithm_depth": shortest_certificate_algorithm_depth(function)}


def capped_relevance_record(k=6):
    """Evaluate the proved OR2-AND2-addressing formulas; no giant table."""
    if k < 6:
        raise ValueError("the stated plateau uses k >= 6")
    relevant = 4 * ((1 << k) + k)
    sensitivity = 2 * (k + 1)
    budget = sensitivity ** 2
    children = {"address_query": 7 * (1 << (k - 1)) + 4 * k - 1,
                "data_query": relevant - 1}
    assert min(children.values()) > budget
    return {"k": k, "relevant_variables": relevant,
            "sensitivity": sensitivity, "block_sensitivity": sensitivity,
            "budget": budget, "child_relevance": children,
            "potential_before_and_after_every_query_answer": budget,
            "scope": "Arithmetic evaluation of analytically proved formulas, not truth-table enumeration."}


def amplified_certificate_record(depth):
    """Evaluate the proved G-depth/addressing family, with G table 0x1bd8."""
    if not isinstance(depth, int) or depth < 1:
        raise ValueError("depth must be a positive integer")
    k = 4 * depth + 10
    q = k + 1
    sensitivity = (2 ** depth) * q
    block_sensitivity = (3 ** depth) * q
    relevant = (4 ** depth) * ((1 << k) + k)
    product_account = block_sensitivity ** 2
    profile_lower_bound = block_sensitivity * (block_sensitivity + 1) // 2
    algorithm_upper_bound = (4 ** depth) * (q + 3)
    budget = sensitivity * block_sensitivity
    assert relevant >= product_account
    assert algorithm_upper_bound <= budget
    if depth >= 2:
        assert profile_lower_bound > budget
    return {
        "composition_depth": depth, "base_table": 7128, "address_bits": k,
        "address_certificate_size": q, "relevant_variables": relevant,
        "sensitivity": sensitivity, "block_sensitivity": block_sensitivity,
        "C0_C1_c0_c1_K0_K1_Kmix": block_sensitivity,
        "s_times_bs_budget": budget,
        "raw_and_closure_portfolio": product_account,
        "profile_portfolio_lower_bound": profile_lower_bound,
        "profile_budget_ratio_numerator": profile_lower_bound,
        "profile_budget_ratio_denominator": budget,
        "shortest_certificate_algorithm_depth_upper_bound": algorithm_upper_bound,
        "scope": "Arithmetic evaluation of analytically proved composition and restriction-level formulas; no large truth table or exact algorithm depth computed.",
    }


def multilinear_coefficients(function):
    """Integer coefficients of the unique real multilinear polynomial."""
    coefficients = [function.value(x) for x in range(1 << function.n)]
    for i in range(function.n):
        for mask in range(1 << function.n):
            if mask & (1 << i):
                coefficients[mask] -= coefficients[mask ^ (1 << i)]
    return tuple(coefficients)


def monomial_charge_record(function):
    """Check every maximum-degree monomial and every answer assignment."""
    if function.is_constant:
        return {"variables": function.n, "table": function.table, "degree": 0,
                "fixed_s_charge_passes": True, "current_product_charge_passes": True,
                "maximum_degree_monomials": []}
    coefficients = multilinear_coefficients(function)
    degree = max(mask.bit_count() for mask, value in enumerate(coefficients) if value)
    masks = [mask for mask, value in enumerate(coefficients)
             if value and mask.bit_count() == degree]
    s0, s1, bs0, bs1, _c0, _c1 = extremal_parameters(function)
    sensitivity, block_sensitivity = max(s0, s1), max(bs0, bs1)
    records = []
    for mask in masks:
        indices = tuple(i for i in range(function.n) if mask & (1 << i))
        worst_bs = worst_product = 0
        for answers in range(1 << degree):
            residual = function
            for step, i in enumerate(indices):
                residual = residual.restrict(i - step, (answers >> step) & 1)
            rs0, rs1, rb0, rb1, _rc0, _rc1 = extremal_parameters(residual)
            worst_bs = max(worst_bs, rb0, rb1)
            worst_product = max(worst_product, max(rs0, rs1) * max(rb0, rb1))
        records.append({"mask": mask,
                        "guaranteed_bs_drop": block_sensitivity - worst_bs,
                        "guaranteed_product_drop": sensitivity * block_sensitivity - worst_product})
    return {"variables": function.n, "table": function.table, "degree": degree,
            "sensitivity": sensitivity, "block_sensitivity": block_sensitivity,
            "fixed_s_charge_passes": any(degree <= sensitivity * item["guaranteed_bs_drop"] for item in records),
            "current_product_charge_passes": any(degree <= item["guaranteed_product_drop"] for item in records),
            "maximum_degree_monomials": records}


def check_monomial_charges(max_vars=4):
    rows = []
    first_failure = None
    for n in range(max_vars + 1):
        fixed_failures = product_failures = 0
        for table in range(1 << (1 << n)):
            result = monomial_charge_record(BooleanFunction(n, table))
            fixed_failures += not result["fixed_s_charge_passes"]
            product_failures += not result["current_product_charge_passes"]
            if first_failure is None and not result["fixed_s_charge_passes"]:
                first_failure = result
        rows.append({"variables": n, "functions_checked": 1 << (1 << n),
                     "fixed_s_charge_failures": fixed_failures,
                     "current_product_charge_failures": product_failures})
    return {"max_vars": max_vars, "records": rows,
            "first_fixed_s_charge_failure": first_failure,
            "scope": "Existence of a qualifying maximum-degree monomial checked against every assignment; finite success is not a proof for larger functions."}


def separated_pair_monomial_record(q, address_bits=0):
    """Evaluate the proved two-separated-certificates obstruction formulas."""
    if q < 13 or not isinstance(q, int):
        raise ValueError("use an integer certificate size at least thirteen")
    if not isinstance(address_bits, int) or address_bits < 0:
        raise ValueError("address_bits must be a nonnegative integer")
    copies = (q - 1) // 2
    factor = address_bits + 1
    inner_variables = (1 << address_bits) + address_bits
    relevant = copies * (2 * q - 3) * inner_variables
    residual_relevant = copies * (q - 3) * inner_variables
    sensitivity = q * factor
    residual_sensitivity = (q - 3) * factor
    budget = sensitivity ** 2
    residual_budget = residual_sensitivity ** 2
    cost = copies * q * factor
    product_drop = budget - residual_budget
    capped_drop = min(relevant, budget) - min(residual_relevant, residual_budget)
    return {
        "certificate_size": q, "copies": copies, "address_bits": address_bits,
        "sensitivity_and_block_sensitivity": sensitivity,
        "residual_sensitivity_and_block_sensitivity": residual_sensitivity,
        "relevant_variables": relevant, "residual_relevant_variables": residual_relevant,
        "s_times_bs": budget, "residual_s_times_bs": residual_budget,
        "every_maximum_monomial_size": cost,
        "product_drop_on_exhibited_answer": product_drop,
        "capped_relevance_product_drop_on_exhibited_answer": capped_drop,
        "current_product_charge_fails": cost > product_drop,
        "capped_product_charge_fails": cost > capped_drop,
        "scope": "Arithmetic evaluation of proved formulas. The exhibited answer for every maximum monomial is analytical, not enumerated on the large function.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = {
        "rounds": [7, 8, 9, 10],
        "scope": "Finite exact audits and explicitly labeled analytical formula evaluations.",
        "batch_and_state_account_audit": check_batch_accounts(),
        "finite_budget_audit": check_budgets(),
        "weighted_block_counterexamples": [majority_record(3), majority_record(5)],
        "closure_examples": [closure_record(3, 22), closure_record(4, 7128)],
        "capped_relevance_counterexample": capped_relevance_record(),
        "amplified_certificate_counterexamples": [
            amplified_certificate_record(depth) for depth in (1, 2, 4, 8)
        ],
        "finite_monomial_charge_audit": check_monomial_charges(),
        "separated_pair_monomial_counterexamples": [
            separated_pair_monomial_record(q) for q in (13, 25, 101)
        ] + [separated_pair_monomial_record(101, address_bits=7)],
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {arguments.output}")


if __name__ == "__main__":
    main()
