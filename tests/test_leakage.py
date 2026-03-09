from __future__ import annotations

import pytest

from wfvkit.leakage import drop_indices, embargo_after, purge_by_horizon, purge_overlap


def test_embargo_after_basic():
    test_idx = [10, 11]
    embargoed = embargo_after(test_idx=test_idx, embargo=2)
    assert embargoed == {12, 13}


def test_purge_overlap_basic():
    train_idx = [0, 1, 2, 3, 4, 5]
    test_idx = [3, 4]
    purged = purge_overlap(train_idx=train_idx, test_idx=test_idx)
    assert purged == [0, 1, 2, 5]


def test_purge_by_horizon_basic():
    train_idx = list(range(10))
    test_idx = [10, 11, 12]
    purged = purge_by_horizon(train_idx, test_idx, horizon=3)
    assert purged == [0, 1, 2, 3, 4, 5, 6]


def test_purge_by_horizon_zero_is_noop():
    train_idx = [0, 1, 2]
    test_idx = [5, 6]
    assert purge_by_horizon(train_idx, test_idx, horizon=0) == train_idx


def test_purge_by_horizon_rejects_negative():
    with pytest.raises(ValueError):
        purge_by_horizon([0, 1], [5], horizon=-1)


def test_drop_indices_basic():
    train_idx = [0, 1, 2, 3, 4, 5]
    blocked = {2, 4, 10}
    assert drop_indices(train_idx, blocked) == [0, 1, 3, 5]
