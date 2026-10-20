"""Explicit potential definitions; exact D is used only by the audit."""

from functools import lru_cache


BASELINE = ("bs_sum", "bs", "bs_product", "s_bs", "c_product")


@lru_cache(maxsize=131072)
def prime_literal_mass(function):
    """Minimum total literal count over the two complete prime families."""
    totals = [0, 0]
    for mask, _values, output in function.prime_implicants():
        totals[output] += mask.bit_count()
    return min(totals)


def potential(name, function):
    if name == "prime_literal_mass":
        return prime_literal_mass(function)
    if name == "relevant_variables":
        return len(function.relevant_coordinates())
    values = function.metrics()
    if name == "bs_sum":
        return values["bs0"] + values["bs1"]
    if name == "bs":
        return values["bs"]
    if name == "bs_product":
        return values["bs0"] * values["bs1"]
    if name == "s_bs":
        return values["s"] * values["bs"]
    if name == "c_product":
        return values["c0"] * values["c1"]
    raise ValueError(f"unknown potential: {name}")
