from __future__ import annotations

import pytest

from wfvkit.evaluate import evaluate_splits, summarize_scores


def test_evaluate_splits_empty_returns_empty_list():
    assert evaluate_splits([], lambda tr, te: 1.0) == []


def test_summarize_scores_rejects_empty_input():
    with pytest.raises(ValueError):
        summarize_scores([])


def test_summarize_scores_values_are_correct():
    summary = summarize_scores([1.0, 2.0, 3.0])
    assert summary["count"] == 3
    assert summary["mean"] == pytest.approx(2.0)
    assert summary["min"] == 1.0
    assert summary["max"] == 3.0
