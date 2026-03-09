from __future__ import annotations

from collections.abc import Iterable


def accuracy_score(y_true: Iterable[int], y_pred: Iterable[int]) -> float:
    """Compute simple classification accuracy."""
    yt = list(y_true)
    yp = list(y_pred)
    if len(yt) != len(yp):
        raise ValueError("y_true and y_pred must have the same length")
    if not yt:
        raise ValueError("y_true and y_pred must be non-empty")
    matches = sum(int(a == b) for a, b in zip(yt, yp))
    return matches / len(yt)


def mean_score(scores: Iterable[float]) -> float:
    """Return the arithmetic mean of one or more scores."""
    vals = list(scores)
    if not vals:
        raise ValueError("scores must contain at least one value")
    return sum(vals) / len(vals)
