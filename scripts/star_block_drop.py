"""Compact witnesses for a quadratic block-elimination obstruction.

Each vertex of K_t defines a certificate on three copies of every incident
edge. At an edge u<v, certificate u requires 000 and certificate v requires
111. The function is an OR of m such gadgets, with m=3(t-1) by default.

The reported exact formula is analytical; the checks verify explicit finite
witnesses and certificate incidences, not a minimax search.
"""

import argparse
import itertools
import json
from pathlib import Path


class StarOR:
    """Evaluate the disjoint OR without materializing its truth table."""

    def __init__(self, t, groups=None):
        if not isinstance(t, int) or isinstance(t, bool) or t < 3:
            raise ValueError("t must be an integer at least 3")
        self.t = t
        self.k = 3 * (t - 1)
        self.m = self.k if groups is None else groups
        if not isinstance(self.m, int) or isinstance(self.m, bool) or self.m < 1:
            raise ValueError("groups must be a positive integer")
        self.edges = tuple(itertools.combinations(range(t), 2))
        self.group_width = 3 * len(self.edges)
        self.n = self.m * self.group_width
        self.group_mask = (1 << self.group_width) - 1
        certificates = []
        for vertex in range(t):
            mask = values = 0
            for edge_index, (lower, upper) in enumerate(self.edges):
                if vertex in (lower, upper):
                    triple = 7 << (3 * edge_index)
                    mask |= triple
                    if vertex == upper:
                        values |= triple
            certificates.append((mask, values))
        self.local_certificates = tuple(certificates)
        # Read each triple in increasing coordinate order as (0, 0, 1).
        local_background = sum(4 << (3 * j) for j in range(len(self.edges)))
        self.background = sum(
            local_background << (group * self.group_width)
            for group in range(self.m)
        )

    def _validate_input(self, x, width):
        if not isinstance(x, int) or not 0 <= x < (1 << width):
            raise ValueError("input must encode a bit string of the required length")

    def satisfied_vertices(self, local_input):
        """Return all satisfied local certificates; at most one can match."""
        self._validate_input(local_input, self.group_width)
        return tuple(
            vertex for vertex, (mask, values) in enumerate(self.local_certificates)
            if local_input & mask == values
        )

    def value(self, x):
        self._validate_input(x, self.n)
        for group in range(self.m):
            local_input = (x >> (group * self.group_width)) & self.group_mask
            if any(local_input & mask == values
                   for mask, values in self.local_certificates):
                return 1
        return 0

    def certificate(self, group, vertex):
        """Return a certificate as original-coordinate (support, values) masks."""
        if not 0 <= group < self.m or not 0 <= vertex < self.t:
            raise ValueError("group or vertex outside its allowed range")
        shift = group * self.group_width
        mask, values = self.local_certificates[vertex]
        return mask << shift, values << shift

    def planted_input(self, group, vertex):
        mask, values = self.certificate(group, vertex)
        return (self.background & ~mask) | values

    def edge_cover(self):
        """An edge cover of K_t with ceil(t/2) edges."""
        result = [(vertex, vertex + 1) for vertex in range(0, self.t - 1, 2)]
        if self.t % 2:
            result.append((0, self.t - 1))
        return tuple(result)

    def upper_bound_query_mask(self):
        """An optimal query set: one coordinate per edge of each edge cover."""
        queried = 0
        indices = {edge: j for j, edge in enumerate(self.edges)}
        local_cover = sum(1 << (3 * indices[edge]) for edge in self.edge_cover())
        for group in range(self.m):
            queried |= local_cover << (group * self.group_width)
        return queried


def verify_family(t):
    """Check certificate geometry and all flips of one full planted input."""
    function = StarOR(t)
    certificates = function.local_certificates
    sizes = [mask.bit_count() for mask, _ in certificates]
    assert sizes == [function.k] * t
    conflicts = [
        ((left_values ^ right_values) & left_mask & right_mask).bit_count()
        for (left_mask, left_values), (right_mask, right_values)
        in itertools.combinations(certificates, 2)
    ]
    assert set(conflicts) == {3}
    incidences = [
        sum(bool(mask & (1 << coordinate)) for mask, _ in certificates)
        for coordinate in range(function.group_width)
    ]
    assert set(incidences) == {2}
    assert function.value(function.background) == 0
    for group in range(function.m):
        for vertex in range(t):
            mask, _ = function.certificate(group, vertex)
            witness = function.planted_input(group, vertex)
            assert (witness ^ function.background) & ~mask == 0
            assert function.value(witness) == 1

    vertex = t // 2
    witness = function.planted_input(0, vertex)
    support, _ = function.certificate(0, vertex)
    actual_sensitive = sum(
        1 << coordinate for coordinate in range(function.n)
        if function.value(witness ^ (1 << coordinate)) == 0
    )
    assert actual_sensitive == support

    queried = function.upper_bound_query_mask()
    assert all(
        queried & function.certificate(group, vertex)[0]
        for group in range(function.m) for vertex in range(t)
    )
    cover_size = (t + 1) // 2
    assert queried.bit_count() == function.m * cover_size
    return {
        "t": t,
        "groups_m": function.m,
        "variables_per_group": function.group_width,
        "variables_n": function.n,
        "analytic_bounds": {
            "s0": function.m,
            "s1": function.k,
            "s": function.k,
            "bs0": function.m * t,
            "bs1": function.k,
            "bs": function.m * t,
            "beta": function.m * cover_size,
            "beta_lower": function.m * cover_size,
            "beta_upper": function.m * cover_size,
            "beta_over_s_lower": cover_size,
            "global_block_drop_cost": 1,
            "exact_beta_source": "analytical equality; no minimax search",
        },
        "finite_checks": {
            "local_certificates_checked": t,
            "certificate_support_size": function.k,
            "certificate_pairs_checked": len(conflicts),
            "minimum_pairwise_conflicts": min(conflicts),
            "maximum_pairwise_conflicts": max(conflicts),
            "incidences_per_coordinate": 2,
            "background_output": 0,
            "planted_inputs_checked": function.m * t,
            "representative_planted_group": 0,
            "representative_planted_vertex": vertex,
            "representative_coordinate_flips_checked": function.n,
            "representative_sensitive_mask_hex": hex(actual_sensitive),
            "representative_certificate_mask_hex": hex(support),
            "representative_sensitivity": actual_sensitive.bit_count(),
            "upper_bound_query_count": queried.bit_count(),
            "upper_bound_hits_every_certificate_support": True,
            "edge_cover": [list(edge) for edge in function.edge_cover()],
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = {
        "round": 5,
        "arithmetic": "exact integers",
        "construction": "OR of 3(t-1) disjoint complete-graph star gadgets",
        "coordinate_encoding":
            "Groups first; lexicographically ordered edges within each group; "
            "three consecutive coordinates per edge; x=sum(x_i*2**i).",
        "background_triple_in_increasing_coordinate_order": [0, 0, 1],
        "scope":
            "Analytical sensitivity and exact block-elimination formulas, supported "
            "by finite certificate and planted-witness checks. No minimax beta search.",
        "examples": [verify_family(t) for t in (3, 4, 8, 16)],
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {arguments.output}")


if __name__ == "__main__":
    main()
