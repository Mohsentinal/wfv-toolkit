from __future__ import annotations

import datetime as dt

from wfvkit.splits import (
    naive_time_split,
    walk_forward_splits,
)


def _d(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s)


def test_naive_time_split_basic():
    times = [_d("2025-01-01"), _d("2025-01-02"), _d("2025-01-03"), _d("2025-01-04")]
    train_idx, test_idx = naive_time_split(times, train_end=_d("2025-01-03"))

    assert train_idx == [0, 1]          # strictly < train_end
    assert test_idx == [2, 3]           # >= train_end


def test_walk_forward_splits_counts_and_order():
    # 10 days, windowed splits
    times = [_d(f"2025-01-{day:02d}") for day in range(1, 11)]

    splits = list(
        walk_forward_splits(
            times=times,
            train_size=5,
            test_size=2,
            step=2,
            embargo=0,
        )
    )

    # Expected:
    # train [0..4], test [5..6]
    # train [2..6], test [7..8]
    assert len(splits) == 2

    (tr0, te0) = splits[0]
    (tr1, te1) = splits[1]

    assert tr0 == [0, 1, 2, 3, 4]
    assert te0 == [5, 6]

    assert tr1 == [2, 3, 4, 5, 6]
    assert te1 == [7, 8]
