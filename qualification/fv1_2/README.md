# FV1-2 synthetic task: merge_windows

Synthetic qualification data only. `windows.py` provides `merge_windows(windows)`,
a pure function (standard library only, no imports, no I/O, no mutation).

## Contract

- Input: list or tuple of windows; each window is a list or tuple of exactly two
  built-in `int` values (`bool` and int subclasses are rejected), `0 <= start < end`.
- `TypeError`: wrong outer/pair container, or non-int/bool coordinate.
- `ValueError`: pair length != 2, negative coordinate, or `end <= start`.
- No coercion. Error text is unspecified.
- Output: new list of `(start, end)` tuples sorted by start. Overlapping and
  touching windows merge (`(1,3),(3,5)` -> `(1,5)`); nested windows keep the maximum
  end; duplicates collapse; `[]` -> `[]`. Deterministic, idempotent, order-independent,
  arbitrary integer precision.

Examples: `[(5,7),(0,2),(1,4)]` -> `[(0,4),(5,7)]`; `[(1,3),(3,5)]` -> `[(1,5)]`;
`[(0,10),(2,3),(4,6)]` -> `[(0,10)]`.

## Test command (from this directory)

    python3 -B -m unittest -v test_windows

## Limitations

- All windows are validated before merging; when several are invalid, which error is
  raised follows input order, and within one window the check order is: container
  (TypeError), length (ValueError), coordinate types (TypeError), range (ValueError).
- Strict `type(x) is int`: `int` subclasses (e.g. IntEnum) are rejected.
- List/tuple containers and their ordinary subclasses are accepted; other containers are rejected.
- Sorting is O(n log n); no streaming or generator input.
