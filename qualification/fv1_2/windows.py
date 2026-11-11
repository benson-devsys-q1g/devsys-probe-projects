"""FV1-2 synthetic task: merge_windows (pure, standard library only, no imports)."""


def _validate(windows):
    if not isinstance(windows, (list, tuple)):
        raise TypeError("windows must be a list or tuple")
    checked = []
    for window in windows:
        if not isinstance(window, (list, tuple)):
            raise TypeError("each window must be a list or tuple")
        if len(window) != 2:
            raise ValueError("each window must have exactly two coordinates")
        start, end = window
        # type() is int (not isinstance) so bool and int subclasses are rejected.
        if type(start) is not int or type(end) is not int:
            raise TypeError("window coordinates must be built-in int (not bool)")
        if start < 0 or end < 0:
            raise ValueError("window coordinates must be non-negative")
        if end <= start:
            raise ValueError("window end must be greater than start")
        checked.append((start, end))
    return checked


def merge_windows(windows):
    """Return a new sorted list of (start, end) tuples with overlapping or
    touching windows merged. Input is validated first and never mutated."""
    ordered = sorted(_validate(windows))
    merged = []
    for start, end in ordered:
        if merged and start <= merged[-1][1]:
            if end > merged[-1][1]:
                merged[-1] = (merged[-1][0], end)
        else:
            merged.append((start, end))
    return merged
