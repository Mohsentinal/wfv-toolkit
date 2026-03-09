from __future__ import annotations

import pytest

from wfvkit.evaluate import evaluate_splits, summarize_scores
from wfvkit.metrics import accuracy_score, mean_score


def test_accuracy_score_basic():
    assert accuracy_score([1, 0, 1, 1], [1, 1, 1, 0]) == 0.5


def test_accuracy_score_rejects_bad_inputs():
    with pytest.raises(ValueError):
        accuracy_score([], [])
    with pytest.raises(ValueError):
        accuracy_score([1], [1, 0])


def test_mean_score_basic():
    assert mean_score([0.4, 0.6, 0.8]) == pytest.approx(0.6)


def test_summarize_scores_basic():
    summary = summarize_scores([0.4, 0.6, 0.8])
    assert summary == {"count": 3, "mean": 0.6, "min": 0.4, "max": 0.8}


def test_evaluate_splits_basic():
    splits = [([0, 1], [2]), ([1, 2], [3])]

    def score_fn(train_idx: list[int], test_idx: list[int]) -> float:
        return float(len(train_idx) + len(test_idx))

    scores = evaluate_splits(splits, score_fn)
    assert scores == [3.0, 3.0]
