"""Compact witnesses for the cyclic-pattern block-elimination obstruction.

The truth table has 2**(k**3) entries and is never materialized. This script
checks sparse inputs and cyclic translates; the sensitivity upper bound comes
from Chakraborty's published Claim 3.3, not exhaustive computation.
"""

import argparse
import json
from pathlib import Path


SOURCE = "https://dmtcs.episciences.org/552/pdf"


class CyclicPattern:
    """Chakraborty's pattern on k**3 coordinates, with zero-based indices."""

    def __init__(self, k):
        if not isinstance(k, int) or k < 8:
            raise ValueError("the pattern requires an integer k >= 8")
        self.k = k
        self.n = k ** 3
        self.full_mask = (1 << self.n) - 1
        self.ones = frozenset(
            {0, 1}
            | {j * k + i for j in range(1, k) for i in range(5)}
            | set(range(k * k - 3, k * k))
        )
        self.zeros = frozenset(range(2, k))
        self.support = self.ones | self.zeros
        self.ones_mask = sum(1 << i for i in self.ones)
        self.zeros_mask = sum(1 << i for i in self.zeros)
        self.support_mask = self.ones_mask | self.zeros_mask
        self.translates = tuple(
            (self.rotate(self.ones_mask, shift),
             self.rotate(self.zeros_mask, shift))
            for shift in range(self.n)
        )

    def rotate(self, mask, shift):
        """Move coordinate i to (i + shift) modulo n."""
        shift %= self.n
        return ((mask << shift) | (mask >> (self.n - shift))) & self.full_mask

    def evaluate(self, x):
        """Whether an input contains any cyclic translate of the pattern."""
        if not isinstance(x, int) or not 0 <= x <= self.full_mask:
            raise ValueError("input must be an n-bit nonnegative integer")
        return any(
            x & ones == ones and not x & zeros
            for ones, zeros in self.translates
        )


def witness_record(k):
    """Check the finite witnesses underlying the analytical lower bound."""
    pattern = CyclicPattern(k)
    x = pattern.ones_mask
    support_size = len(pattern.support)
    assert len(pattern.ones) == 5 * k
    assert len(pattern.zeros) == k - 2
    assert support_size == 6 * k - 2
    assert pattern.evaluate(x)
    assert not pattern.evaluate(0)

    sensitive = {
        i for i in range(pattern.n)
        if not pattern.evaluate(x ^ (1 << i))
    }
    assert sensitive == pattern.support

    fresh_counts = [
        (ones & ~x).bit_count()
        for ones, _ in pattern.translates[1:]
    ]
    assert min(fresh_counts) >= 2

    incidence = [0] * pattern.n
    for shift in range(pattern.n):
        for i in pattern.support:
            incidence[(i + shift) % pattern.n] += 1
    assert min(incidence) == max(incidence) == support_size

    lower_bound = (pattern.n + support_size - 1) // support_size
    queried = (1 << (lower_bound - 1)) - 1
    avoiding_shift = next(
        shift for shift, (ones, zeros) in enumerate(pattern.translates)
        if not queried & (ones | zeros)
    )
    shifted_ones, shifted_zeros = pattern.translates[avoiding_shift]
    shifted_support = shifted_ones | shifted_zeros
    assert not queried & shifted_support
    assert not queried & shifted_ones
    assert pattern.evaluate(shifted_ones)
    shifted_sensitive = {
        i for i in range(pattern.n)
        if not pattern.evaluate(shifted_ones ^ (1 << i))
    }
    assert shifted_sensitive == {
        (i + avoiding_shift) % pattern.n for i in pattern.support
    }

    return {
        "k": k,
        "n": pattern.n,
        "positive_literal_count": len(pattern.ones),
        "negative_literal_count": len(pattern.zeros),
        "certificate_support_size": support_size,
        "positive_coordinates": sorted(pattern.ones),
        "negative_coordinates": sorted(pattern.zeros),
        "sparse_witness_value": 1,
        "single_bit_flips_checked_at_each_witness": pattern.n,
        "sparse_witness_sensitive_coordinates": sorted(sensitive),
        "minimum_fresh_positive_coordinates_of_nonidentity_translate":
            min(fresh_counts),
        "cyclic_translates_checked": pattern.n,
        "translate_support_incidence_per_coordinate": support_size,
        "derived_local_bs_at_sparse_witness": support_size,
        "local_bs_justification":
            "A family of support_size sensitive singleton blocks matches "
            "the support_size certificate upper bound.",
        "proved_lower_bound_beta": lower_bound,
        "lower_bound_formula": "ceil(n / (6*k - 2))",
        "example_all_zero_transcript": {
            "queried_coordinates": list(range(lower_bound - 1)),
            "avoiding_shift": avoiding_shift,
            "consistent_shifted_sparse_witness": True,
            "untouched_maximum_singleton_family_size": support_size,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parameters", type=int, nargs="+", default=[8, 9, 12, 16])
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = {
        "round": 5,
        "arithmetic": "exact integers",
        "coordinate_encoding": "Coordinates are 0,...,n-1, with cyclic addition.",
        "source": {
            "url": SOURCE,
            "location": "Section 3, Claim 3.3, printed pages 56-57",
            "published_claim":
                "s_1=6*k-2 and s_0=Theta(n/k^2); hence s=Theta(k) for n=k^3.",
        },
        "proved_family_bounds": {
            "n": "k^3",
            "sensitivity": "Theta(k)",
            "block_elimination_cost": "Theta(k^2)",
            "lower_bound":
                "The all-zero transcript must hit every translated "
                "maximum-singleton-family support, so beta >= ceil(n/(6*k-2)).",
            "upper_bound":
                "The general beta <= degree <= s_0*s_1 bound gives O(k^2).",
            "exact_cost": "Not claimed.",
        },
        "scope":
            "Checks all one-bit flips at two explicit sparse witnesses, all "
            "cyclic translates, and one avoiding transcript per parameter. "
            "Does not enumerate truth tables or compute global sensitivity "
            "or optimal block-elimination depth.",
        "examples": [witness_record(k) for k in arguments.parameters],
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {arguments.output}")


if __name__ == "__main__":
    main()
