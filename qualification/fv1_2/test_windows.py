import copy
import itertools
import random
import unittest

from windows import merge_windows


class Examples(unittest.TestCase):
    def test_contract_examples(self):
        self.assertEqual(merge_windows([(5, 7), (0, 2), (1, 4)]), [(0, 4), (5, 7)])
        self.assertEqual(merge_windows([(1, 3), (3, 5)]), [(1, 5)])
        self.assertEqual(merge_windows([(0, 10), (2, 3), (4, 6)]), [(0, 10)])

    def test_empty_and_single(self):
        self.assertEqual(merge_windows([]), [])
        self.assertEqual(merge_windows(()), [])
        self.assertEqual(merge_windows([(2, 3)]), [(2, 3)])

    def test_duplicates_collapse(self):
        self.assertEqual(merge_windows([(1, 2), (1, 2), (1, 2)]), [(1, 2)])

    def test_gap_of_one_not_merged(self):
        self.assertEqual(merge_windows([(0, 1), (2, 3)]), [(0, 1), (2, 3)])

    def test_same_start_keeps_max_end(self):
        self.assertEqual(merge_windows([(1, 9), (1, 3), (1, 5)]), [(1, 9)])

    def test_nested_does_not_shrink_end(self):
        self.assertEqual(merge_windows([(0, 10), (1, 2), (9, 10), (10, 12)]), [(0, 12)])

    def test_chain_merges(self):
        self.assertEqual(merge_windows([(4, 6), (0, 2), (2, 4), (6, 8)]), [(0, 8)])

    def test_lists_and_tuples_mixed(self):
        self.assertEqual(merge_windows(([0, 1], (1, 2))), [(0, 2)])

    def test_list_tuple_container_subclasses(self):
        class ListWindows(list):
            pass
        class TupleWindows(tuple):
            pass
        values = [ListWindows([(0, 2)]), TupleWindows([(0, 2)]),
                  [ListWindows([0, 2])], [TupleWindows((0, 2))]]
        for value in values:
            before = copy.deepcopy(value)
            with self.subTest(value=value):
                self.assertEqual(merge_windows(value), [(0, 2)])
                self.assertEqual(value, before)

    def test_big_ints(self):
        big = 10 ** 40
        self.assertEqual(
            merge_windows([(big, big + 5), (big + 5, big + 9), (0, 1)]),
            [(0, 1), (big, big + 9)],
        )
        r = merge_windows([(2 ** 100, 2 ** 100 + 1)])
        self.assertEqual(r, [(2 ** 100, 2 ** 100 + 1)])


class Properties(unittest.TestCase):
    def test_permutation_invariant(self):
        base = [(5, 7), (0, 2), (1, 4), (4, 5), (9, 12), (10, 11)]
        expect = merge_windows(base)
        for perm in itertools.permutations(base):
            self.assertEqual(merge_windows(list(perm)), expect)

    def test_idempotent_and_deterministic(self):
        rng = random.Random(12345)
        for _ in range(300):
            ws = []
            for _ in range(rng.randint(0, 12)):
                s = rng.randint(0, 30)
                ws.append((s, s + rng.randint(1, 8)))
            once = merge_windows(ws)
            self.assertEqual(merge_windows(ws), once)
            self.assertEqual(merge_windows(once), once)
            # reference: point coverage on integer unit cells equals input's
            cells = lambda items: {c for a, b in items for c in range(a, b)}
            self.assertEqual(cells(once), cells(ws))
            # output sorted, non-touching, tuples of int
            for (a, b), (c, d) in zip(once, once[1:]):
                self.assertLess(b, c)
            self.assertTrue(all(type(x) is tuple for x in once))

    def test_input_not_mutated_and_new_list(self):
        src = [[5, 7], [0, 2], [1, 4]]
        snap = copy.deepcopy(src)
        out = merge_windows(src)
        self.assertEqual(src, snap)
        self.assertIsNot(out, src)
        t = ((1, 2),)
        self.assertIsInstance(merge_windows(t), list)

    def test_invalid_input_not_mutated(self):
        src = [[0, 1], [3, 3]]
        snap = copy.deepcopy(src)
        with self.assertRaises(ValueError):
            merge_windows(src)
        self.assertEqual(src, snap)


class NegativeControls(unittest.TestCase):
    def test_type_errors_outer(self):
        for bad in (None, 5, "ab", {(0, 1)}, {0: 1}, iter([(0, 1)]), b"", range(2),
                    (x for x in [(0, 1)])):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                merge_windows(bad)

    def test_type_errors_pair_container(self):
        for bad in (5, None, "ab", {0, 1}, {0: 1, 1: 2}, range(2), b"ab", iter((0, 1))):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                merge_windows([bad])

    def test_type_errors_coordinates(self):
        for bad in ((0.0, 1), (0, 1.0), (0, True), (False, 1), ("0", 1), (0, "1"),
                    (None, 1), (0, None), (1.5, 2.5), (0, 1 + 0j)):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                merge_windows([bad])

    def test_int_subclass_rejected(self):
        class MyInt(int):
            pass
        with self.assertRaises(TypeError):
            merge_windows([(MyInt(0), 1)])

    def test_value_errors_length(self):
        for bad in ((), (1,), (0, 1, 2), [], [0]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                merge_windows([bad])

    def test_value_errors_range(self):
        for bad in ((-1, 1), (-3, -1), (0, -1), (3, 3), (0, 0), (5, 2)):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                merge_windows([bad])

    def test_one_bad_window_among_good(self):
        with self.assertRaises(ValueError):
            merge_windows([(0, 1), (1, 2), (4, 4)])
        with self.assertRaises(TypeError):
            merge_windows([(0, 1), (1, 2), (4, True)])

    def test_bool_not_coerced_to_valid_window(self):
        with self.assertRaises(TypeError):
            merge_windows([(False, True)])


if __name__ == "__main__":
    unittest.main()
