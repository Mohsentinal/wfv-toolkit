# wfv-toolkit (wfvkit)

A tiny Python toolkit for **walk-forward validation** of time-ordered data, with **purge**, **embargo**, and **forward-horizon leakage guards** for finance/trading ML and any temporal prediction setup.

---

## What you get

* **Naive time split** (baseline): `naive_time_split`
* **Walk-forward splits** (rolling windows): `walk_forward_splits`
* **Leakage guards**
  * `purge_overlap(train_idx, test_idx)` — removes exact train/test index overlap
  * `embargo_after(test_idx, embargo)` — blocks samples immediately after the test window
  * `purge_by_horizon(train_idx, test_idx, horizon)` — removes training samples whose **forward-looking labels** would reach into the test window
  * `drop_indices(train_idx, blocked_idx)` — removes arbitrary blocked indices while keeping order
* **Tiny evaluation helpers**
  * `accuracy_score`, `mean_score`
  * `evaluate_splits`, `summarize_scores`
* Runnable examples:
  * `examples/demo_naive_vs_purged.py`
  * `examples/leakage_demo.py`
* Tests: `pytest`

> The subtle but important point: generic purge + embargo are useful, but if labels use a forward horizon, the strongest guard is often **horizon-aware purging**.

---

## Install

### Option A: from PyPI (recommended)

```bash
pip install wfvkit
```

### Option B: editable install (development)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

### Option C: editable install with example dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[examples]"
```

### Option D: install from GitHub tag

```bash
pip install "git+https://github.com/Mohsentinal/wfv-toolkit.git@v0.1.8"
```

---

## Quickstart

### Minimal example

```python
import datetime as dt

from wfvkit import (
    embargo_after,
    naive_time_split,
    purge_by_horizon,
    purge_overlap,
    walk_forward_splits,
)

# 10 timestamps (toy example)
times = [dt.datetime(2025, 1, 1, 0, 0) + dt.timedelta(minutes=i) for i in range(10)]

# 1) naive split: pass an index cutoff OR a datetime cutoff
train_idx, test_idx = naive_time_split(times, train_end=6)
train_idx2, test_idx2 = naive_time_split(times, train_end=times[6])

print("naive_idx:", train_idx, test_idx)
print("naive_dt :", train_idx2, test_idx2)

# 2) walk-forward splits (rolling windows)
splits = list(walk_forward_splits(times, train_size=5, test_size=2, step=2, embargo=1))
print("splits:", splits)

# 3) exact-overlap purge + embargo helpers
tr, te = splits[0]
print("purged overlap:", purge_overlap(tr, te))
print("embargo:", sorted(embargo_after(te, embargo=1)))

# 4) horizon-aware purge for forward-looking labels
print("purged by horizon:", purge_by_horizon(tr, te, horizon=1))
```

### Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

### Run the simple demo

```powershell
.\.venv\Scripts\python.exe examples\demo_naive_vs_purged.py
```

### Run the leakage demo

```powershell
.\.venv\Scripts\python.exe examples\leakage_demo.py
```

Success looks like:
- the simple demo prints naive split indices, walk-forward splits, purge output, and embargo output
- the leakage demo prints **single-split** and **walk-forward summary** blocks comparing naive vs horizon-aware leakage control

---

## Usage

### Import the public API

```python
from wfvkit import (
    accuracy_score,
    drop_indices,
    embargo_after,
    evaluate_splits,
    mean_score,
    naive_time_split,
    purge_by_horizon,
    purge_overlap,
    summarize_scores,
    walk_forward_splits,
)
```

### Naive split (baseline)

```python
import datetime as dt

from wfvkit import naive_time_split

times = [dt.datetime(2025, 1, 1) + dt.timedelta(minutes=i) for i in range(10)]

# Cut by index
train_idx, test_idx = naive_time_split(times, 6)

# Or cut by datetime
train_idx2, test_idx2 = naive_time_split(times, times[6])
```

### Walk-forward splits + leakage guards

```python
import datetime as dt

from wfvkit import embargo_after, purge_by_horizon, walk_forward_splits

times = [dt.datetime(2025, 1, 1) + dt.timedelta(minutes=i) for i in range(50)]

for train_idx, test_idx in walk_forward_splits(
    times,
    train_size=20,
    test_size=5,
    step=5,
    embargo=2,
):
    train_purged = purge_by_horizon(train_idx, test_idx, horizon=3)
    embargo_idx = embargo_after(test_idx, embargo=2)

    # Fit on `train_purged`, evaluate on `test_idx`,
    # and avoid using indices in `embargo_idx` for training.
```

---

## Concepts (plain English)

### Purge

If a sample in **train** overlaps the **test** interval, it can leak information. Purging removes those overlapping training indices.

### Embargo

Even after the test window ends, samples **immediately after** can still be contaminated if labels depend on future horizons. Embargo blocks a small number of samples after the test window.

### Horizon-aware purge

If labels look forward by `horizon` steps, then the last few training labels can still “peek” into the test period even when there is no exact train/test overlap. `purge_by_horizon(...)` removes those boundary samples.

---

## Project layout

```text
wfv-toolkit/
  src/wfvkit/
    __init__.py
    splits.py
    leakage.py
    metrics.py
    evaluate.py
  tests/
  examples/
  CHANGELOG.md
```

---

## Roadmap

* Add purged k-fold / combinatorial purged CV
* Add utilities for event-based labels (start/end times per sample)
* Add richer evaluation helpers (rolling metrics and robustness checks)
* Provide a small CLI (optional)

---

## License

MIT (see `LICENSE`).
