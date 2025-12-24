from __future__ import annotations

import datetime as dt
from collections.abc import Iterator, Sequence


def naive_time_split(
    times: Sequence[dt.datetime],
    train_end: dt.datetime,
) -> tuple[list[int], list[int]]:
    """
    Simple chronological split:
      - train indices: times < train_end
      - test indices:  times >= train_end

    Assumes `times` are comparable and represent the timeline.
    """
    train_idx: list[int] = []
    test_idx: list[int] = []

    for i, t in enumerate(times):
        if t < train_end:
            train_idx.append(i)
        else:
            test_idx.append(i)

    return train_idx, test_idx


def walk_forward_splits(
    times: Sequence[dt.datetime],
    train_size: int,
    test_size: int,
    step: int,
    embargo: int = 0,
) -> Iterator[tuple[list[int], list[int]]]:
    """
    Windowed walk-forward splits on index space (not time-deltas).

    Example (10 points):
      train_size=5, test_size=2, step=2
      -> train [0..4], test [5..6]
      -> train [2..6], test [7..8]
      stops before incomplete test window.

    `embargo` is accepted for API symmetry (actual embargo application
    is handled separately in wfvkit.leakage).
    """
    if train_size <= 0:
        raise ValueError("train_size must be > 0")
    if test_size <= 0:
        raise ValueError("test_size must be > 0")
    if step <= 0:
        raise ValueError("step must be > 0")
    if embargo < 0:
        raise ValueError("embargo must be >= 0")

    n = len(times)
    start = 0

    while True:
        train_start = start
        train_end = train_start + train_size
        test_start = train_end
        test_end = test_start + test_size

        if test_end > n:
            break  # incomplete test window → stop

        train_idx = list(range(train_start, train_end))
        test_idx = list(range(test_start, test_end))

        yield train_idx, test_idx

        start += step
