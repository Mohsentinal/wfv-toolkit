from importlib.metadata import version as _version

from .evaluate import evaluate_splits, summarize_scores
from .leakage import drop_indices, embargo_after, purge_by_horizon, purge_overlap
from .metrics import accuracy_score, mean_score
from .splits import naive_time_split, walk_forward_splits

__all__ = [
    "naive_time_split",
    "walk_forward_splits",
    "embargo_after",
    "purge_overlap",
    "purge_by_horizon",
    "drop_indices",
    "accuracy_score",
    "mean_score",
    "evaluate_splits",
    "summarize_scores",
]

__version__ = _version("wfvkit")
