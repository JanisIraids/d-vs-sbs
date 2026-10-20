"""Named total Boolean functions used by the finite potential audits."""

from scripts.boolean import BooleanFunction


def parity(n):
    """Parity on n coordinates, including the zero-coordinate constant."""
    return BooleanFunction.from_callable(n, lambda x: x.bit_count() % 2)


def disjoint_and_or(m, k):
    """OR of m disjoint k-input ANDs, with consecutive blocks of k bits."""
    if not isinstance(m, int) or not isinstance(k, int) or m < 1 or k < 1:
        raise ValueError("m and k must be positive integers")
    block = (1 << k) - 1
    return BooleanFunction.from_callable(
        m * k,
        lambda x: any((x >> (j * k)) & block == block for j in range(m)),
    )


def addressing(k):
    """Return z_a: k low address bits, followed by 2**k data coordinates."""
    if not isinstance(k, int) or k < 0:
        raise ValueError("k must be a nonnegative integer")
    address_mask = (1 << k) - 1
    return BooleanFunction.from_callable(
        k + (1 << k), lambda x: (x >> (k + (x & address_mask))) & 1
    )


def double_addressing(k):
    """Return z_a XOR z_b, with data first, then the two k-bit addresses.

    Coordinate order is material for the greedy query rule: its tie break
    chooses the smallest remaining index, which prioritizes data coordinates.
    These constructors materialize truth tables and are for small k only.
    """
    if not isinstance(k, int) or k < 0:
        raise ValueError("k must be a nonnegative integer")
    data_count = 1 << k
    address_mask = data_count - 1

    def value(x):
        a = (x >> data_count) & address_mask
        b = (x >> (data_count + k)) & address_mask
        return ((x >> a) ^ (x >> b)) & 1

    return BooleanFunction.from_callable(data_count + 2 * k, value)
