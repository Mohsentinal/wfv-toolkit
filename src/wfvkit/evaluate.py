from __future__ import annotations

from collections.abc import Callable, Iterable

from .metrics import mean_score

ScoreFn = Callable[[list[int], list[int]], float]


def evaluate_splits(
    splits: Iterable[tuple[list[int], list[int]]],
    score_fn: ScoreFn,
) -> list[float]:
    """
    Evaluate a user-provided score function over a sequence of train/test splits.

    ``score_fn`` should accept ``(train_idx, test_idx)`` and return a numeric score.
    """
    results: list[float] = []
    for train_idx, test_idx in splits:
        results.append(float(score_fn(train_idx, test_idx)))
    return results


def summarize_scores(scores: Iterable[float]) -> dict[str, float | int]:
    """Return a tiny summary for a collection of split scores."""
    vals = list(scores)
    if not vals:
        raise ValueError("scores must contain at least one value")
    return {
        "count": len(vals),
        "mean": mean_score(vals),
        "min": min(vals),
        "max": max(vals),
    }
