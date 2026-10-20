"""Exact invariants of small total Boolean functions, using integer bit masks.

An input is ``x = sum(x_i * 2**i)`` and bit ``x`` of ``table`` is ``f(x)``.
Coordinate sets are integer masks in the same least-significant-bit order.
Restricting a coordinate removes it and renumbers remaining coordinates in
ascending order. Empty output classes have output-specific maxima zero.

The methods use exponential algorithms intended for small truth tables. No
floating-point arithmetic or external libraries are used.
"""

from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Dict, Optional, Tuple


@dataclass(frozen=True)
class BooleanFunction:
    """An immutable total function on exactly ``n`` displayed coordinates."""

    n: int
    table: int

    def __post_init__(self):
        if not isinstance(self.n, int) or self.n < 0:
            raise ValueError("n must be a nonnegative integer")
        if not isinstance(self.table, int) or not 0 <= self.table < 1 << (1 << self.n):
            raise ValueError("table must have exactly 2**n available bits")

    @classmethod
    def from_callable(cls, n: int, function: Callable[[int], int]):
        """Evaluate ``function(x)`` for integer inputs ``0 <= x < 2**n``."""
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a nonnegative integer")
        table = 0
        for x in range(1 << n):
            value = function(x)
            if value not in (0, 1):
                raise ValueError("function values must be 0 or 1")
            table |= int(value) << x
        return cls(n, table)

    @property
    def is_constant(self) -> bool:
        return self.table in (0, (1 << (1 << self.n)) - 1)

    def value(self, x: int) -> int:
        if not isinstance(x, int) or not 0 <= x < 1 << self.n:
            raise ValueError("input lies outside the Boolean cube")
        return (self.table >> x) & 1

    def restrict(self, coordinate: int, answer: int):
        """Fix one coordinate and remove it from the displayed input."""
        if not isinstance(coordinate, int) or not 0 <= coordinate < self.n:
            raise ValueError("coordinate lies outside the input")
        if answer not in (0, 1):
            raise ValueError("answer must be 0 or 1")
        return _restrict(self, coordinate, int(answer))

    def relevant_coordinates(self) -> Tuple[int, ...]:
        """Coordinates whose two restrictions differ as truth tables."""
        return tuple(
            i for i in range(self.n)
            if self.restrict(i, 0).table != self.restrict(i, 1).table
        )

    def minimal_sensitive_blocks(self, x: int) -> Tuple[int, ...]:
        """Inclusion-minimal nonempty masks B with ``f(x xor B) != f(x)``."""
        self.value(x)  # Validate even for a constant function.
        return _minimal_sensitive_blocks(self, x)

    def minimal_certificates(self, x: int) -> Tuple[int, ...]:
        """Inclusion-minimal coordinate masks certifying the output at x."""
        blocks = self.minimal_sensitive_blocks(x)
        return _minimal_hitting_sets(self.n, blocks)

    def prime_implicants(self, output: Optional[int] = None):
        """Return distinct minimal certificates as ``(mask, values, output)``.

        ``values`` is masked by ``mask``. With output=None both outputs are
        included; output=1 returns prime implicants in the usual DNF sense.
        """
        if output not in (None, 0, 1):
            raise ValueError("output must be 0, 1, or None")
        certificates = set()
        for x in range(1 << self.n):
            value = self.value(x)
            if output is None or output == value:
                certificates.update(
                    (mask, x & mask, value)
                    for mask in self.minimal_certificates(x)
                )
        return tuple(sorted(certificates))

    def metrics(self) -> Dict[str, int]:
        return metrics(self)


@lru_cache(maxsize=131072)
def _restrict(function, coordinate, answer):
    low_mask = (1 << coordinate) - 1
    table = 0
    for x in range(1 << (function.n - 1)):
        original = (x & low_mask) | ((x & ~low_mask) << 1) | (answer << coordinate)
        table |= ((function.table >> original) & 1) << x
    return BooleanFunction(function.n - 1, table)


@lru_cache(maxsize=None)
def _masks_by_size(n):
    return tuple(sorted(range(1 << n), key=lambda mask: (mask.bit_count(), mask)))


@lru_cache(maxsize=65536)
def _minimal_sensitive_blocks(function, x):
    value = (function.table >> x) & 1
    blocks = []
    for mask in _masks_by_size(function.n)[1:]:
        if ((function.table >> (x ^ mask)) & 1) != value:
            if not any(mask & block == block for block in blocks):
                blocks.append(mask)
    return tuple(blocks)


@lru_cache(maxsize=32768)
def _minimal_hitting_sets(n, blocks):
    certificates = []
    for mask in _masks_by_size(n):
        if all(mask & block for block in blocks):
            if not any(mask & previous == previous for previous in certificates):
                certificates.append(mask)
    return tuple(certificates)


@lru_cache(maxsize=32768)
def _local_parameters(n, blocks):
    """Sensitivity, disjoint block packing, and minimum certificate size.

    Any sensitive block contains a minimal one, so shrinking blocks preserves
    disjointness. Certificates are precisely hitting sets of sensitive blocks:
    otherwise an opposite-output input agrees on every fixed coordinate.
    """
    sensitivity = sum(block.bit_count() == 1 for block in blocks)

    @lru_cache(maxsize=None)
    def packing(available):
        return max(
            (1 + packing(available ^ block)
             for block in blocks if available & block == block),
            default=0,
        )

    block_sensitivity = packing((1 << n) - 1)
    certificate = next(
        mask.bit_count() for mask in _masks_by_size(n)
        if all(mask & block for block in blocks)
    )
    return sensitivity, block_sensitivity, certificate


@lru_cache(maxsize=None)
def decision_tree_depth(function: BooleanFunction) -> int:
    """Exact D via the minimax recurrence, with constant functions at zero."""
    if function.is_constant:
        return 0
    return 1 + min(
        max(
            decision_tree_depth(function.restrict(i, 0)),
            decision_tree_depth(function.restrict(i, 1)),
        )
        for i in function.relevant_coordinates()
    )


@lru_cache(maxsize=None)
def _metric_tuple(function):
    sensitivity = [0, 0]
    block_sensitivity = [0, 0]
    certificate = [0, 0]
    for x in range(1 << function.n):
        output = (function.table >> x) & 1
        s, bs, c = _local_parameters(
            function.n, function.minimal_sensitive_blocks(x)
        )
        sensitivity[output] = max(sensitivity[output], s)
        block_sensitivity[output] = max(block_sensitivity[output], bs)
        certificate[output] = max(certificate[output], c)
    return (
        *sensitivity, *block_sensitivity, *certificate,
        decision_tree_depth(function),
        max(sensitivity), max(block_sensitivity), max(certificate),
    )


def metrics(function: BooleanFunction) -> Dict[str, int]:
    """Return all exact maxima, with an independent dictionary on each call."""
    keys = ("s0", "s1", "bs0", "bs1", "c0", "c1", "d", "s", "bs", "c")
    return dict(zip(keys, _metric_tuple(function)))


def clear_caches():
    """Release enumeration caches; mathematical results are unaffected."""
    for function in (
        _restrict, _masks_by_size, _minimal_sensitive_blocks,
        _minimal_hitting_sets, _local_parameters, decision_tree_depth,
        _metric_tuple,
    ):
        function.cache_clear()
