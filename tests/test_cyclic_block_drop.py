"""Independent checks of the compact cyclic-pattern witnesses."""

import random
import unittest

from scripts.cyclic_block_drop import CyclicPattern


def naive_evaluate(k, x):
    """Directly check the defining word, independently of mask rotation."""
    n = k ** 3
    bits = [(x >> i) & 1 for i in range(n)]
    for start in range(n):
        block = [bits[(start + i) % n] for i in range(k ** 2)]
        if block[:k] != [1, 1] + [0] * (k - 2):
            continue
        if all(block[j * k:j * k + 5] == [1] * 5 for j in range(1, k)):
            if block[-3:] == [1] * 3:
                return True
    return False


class CyclicPatternTests(unittest.TestCase):
    def test_evaluator_matches_independent_word_definition(self):
        pattern = CyclicPattern(8)
        rng = random.Random(20261020)
        inputs = [0, pattern.full_mask, pattern.ones_mask]
        inputs += [rng.getrandbits(pattern.n) for _ in range(8)]
        for shift in (0, 1, 17, pattern.n - 1):
            positive = pattern.ones_mask
            noise = rng.getrandbits(pattern.n) & ~pattern.support_mask
            inputs.append(pattern.rotate(positive | noise, shift))
        inputs += [
            pattern.ones_mask ^ (1 << i)
            for i in (0, 2, 7, 8, 60, 63, 64, 511)
        ]
        for x in inputs:
            with self.subTest(x=x):
                self.assertEqual(pattern.evaluate(x), naive_evaluate(8, x))

    def test_sparse_witness_has_exactly_the_certificate_singletons(self):
        pattern = CyclicPattern(9)
        x = pattern.ones_mask
        self.assertTrue(pattern.evaluate(x))
        sensitive = {
            i for i in range(pattern.n)
            if not pattern.evaluate(x ^ (1 << i))
        }
        self.assertEqual(sensitive, pattern.support)
        self.assertEqual(len(sensitive), 6 * pattern.k - 2)

    def test_queries_on_zero_transcript_leave_an_untouched_witness(self):
        pattern = CyclicPattern(8)
        rng = random.Random(1701)
        count = (pattern.n - 1) // len(pattern.support)
        queries = rng.sample(range(pattern.n), count)
        queried = sum(1 << i for i in queries)
        surviving = [
            (ones, zeros)
            for ones, zeros in pattern.translates
            if not queried & (ones | zeros)
        ]
        self.assertGreaterEqual(
            len(surviving), pattern.n - count * len(pattern.support)
        )
        ones, zeros = surviving[0]
        self.assertEqual(ones & queried, 0)
        self.assertTrue(pattern.evaluate(ones))
        for i in range(pattern.n):
            if (ones | zeros) & (1 << i):
                self.assertFalse(pattern.evaluate(ones ^ (1 << i)))

    def test_invalid_pattern_and_input_are_rejected(self):
        for k in (0, 7, 8.5):
            with self.assertRaises(ValueError):
                CyclicPattern(k)
        pattern = CyclicPattern(8)
        for x in (-1, 1 << pattern.n):
            with self.assertRaises(ValueError):
                pattern.evaluate(x)


if __name__ == "__main__":
    unittest.main()
