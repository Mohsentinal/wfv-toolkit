from __future__ import annotations

from collections.abc import Iterable


def embargo_after(test_idx: Iterable[int], embargo: int) -> set[int]:
    """
    Return a set of indices that should be excluded *after* the test window.

    Example
    -------
    If test indices end at k and ``embargo=2``, exclude ``{k+1, k+2}``.
    """
    if embargo < 0:
        raise ValueError("embargo must be >= 0")

    test_idx_list = list(test_idx)
    if not test_idx_list or embargo == 0:
        return set()

    m = max(test_idx_list)
    return {m + i for i in range(1, embargo + 1)}


def purge_overlap(train_idx: list[int], test_idx: list[int]) -> list[int]:
    """
    Remove any training indices that overlap with the test indices.

    Keeps original order.
    """
    test_set = set(test_idx)
    return [i for i in train_idx if i not in test_set]


def purge_by_horizon(train_idx: list[int], test_idx: list[int], horizon: int) -> list[int]:
    """
    Drop training indices whose *forward-looking labels* would reach into the test set.

    If labels at index ``i`` use information from the next ``horizon`` samples,
    and the test set begins at ``k = min(test_idx)``, then any training sample
    with ``i + horizon >= k`` leaks future information from the test period.

    We therefore keep only training indices ``i < k - horizon``.

    Parameters
    ----------
    train_idx:
        Ordered training indices.
    test_idx:
        Ordered or unordered test indices.
    horizon:
        Number of forward steps used by the label.

    Returns
    -------
    list[int]
        Purged training indices, preserving original order.
    """
    if horizon < 0:
        raise ValueError("horizon must be >= 0")
    if not test_idx or horizon == 0:
        return list(train_idx)

    k = min(test_idx)
    cutoff = k - horizon
    return [i for i in train_idx if i < cutoff]


def drop_indices(train_idx: list[int], blocked_idx: Iterable[int]) -> list[int]:
    """
    Remove arbitrary blocked indices from a training set while preserving order.

    This is handy for applying an embargo set back onto the candidate train set.
    """
    blocked = set(blocked_idx)
    if not blocked:
        return list(train_idx)
    return [i for i in train_idx if i not in blocked]
