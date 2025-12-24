# wfv-toolkit (wfvkit)

A tiny Python toolkit for **walk‑forward validation** of time‑ordered data with **purge + embargo** utilities to reduce label leakage (useful for trading/finance ML and any temporal prediction setup).

## What you get

- **Naive time split** (baseline): `naive_time_split`
- **Walk‑forward splits** (rolling windows): `walk_forward_splits`
- **Leakage guards**
  - `purge_overlap(train_idx, test_idx)` — removes train indices that overlap test
  - `embargo_after(test_idx, embargo)` — blocks samples immediately after the test window
- A runnable example: `examples/demo_naive_vs_purged.py`
- Tests: `pytest`

> The core idea is common in financial ML: if labels use a forward horizon, nearby samples can “bleed” information between train/test. Purge and embargo help.

---

## Install

### Option A: editable install (recommended for development)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

### Option B: install from GitHub (once you start tagging releases)

```powershell
pip install "git+https://github.com/Mohsentinal/wfv-toolkit.git@v0.1.0"
```

---

## Quickstart

### 1) Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

### 2) Run the demo

```powershell
.\.venv\Scripts\python.exe examples\demo_naive_vs_purged.py
```

---

## Usage

### Import the public API

```python
from wfvkit import (
    naive_time_split,
    walk_forward_splits,
    purge_overlap,
    embargo_after,
)
```

### Naive split (baseline)

```python
import datetime as dt

times = [dt.datetime(2025, 1, 1) + dt.timedelta(minutes=i) for i in range(10)]
train_end = times[6]

train_idx, test_idx = naive_time_split(times, train_end=train_end)
# train_idx -> [0,1,2,3,4,5]
# test_idx  -> [6,7,8,9]
```

### Walk‑forward splits + purge + embargo

```python
import datetime as dt

times = [dt.datetime(2025, 1, 1) + dt.timedelta(minutes=i) for i in range(50)]

for train_idx, test_idx in walk_forward_splits(
    times,
    train_size=20,
    test_size=5,
    step=5,
    embargo=2,
):
    train_purged = purge_overlap(train_idx, test_idx)
    embargo_idx = embargo_after(test_idx, embargo=2)

    # Fit on `train_purged`, evaluate on `test_idx`,
    # and avoid using indices in `embargo_idx` for training.
```

---

## Concepts (plain English)

### Purge

If a sample in **train** overlaps the **test** interval (or shares a window that touches the test range), it can leak information. Purging removes those training indices.

### Embargo

Even after the test window ends, samples **immediately after** can still be “contaminated” if labels depend on future returns/horizons. Embargo blocks a small number of samples after test.

---

## Project layout

```
wfv-toolkit/
  src/wfvkit/
    __init__.py
    splits.py
    leakage.py
    metrics.py
    evaluate.py
  tests/
  examples/
```

---

## Roadmap (next nice upgrades)

- Add **purged k‑fold** / **combinatorial purged CV**
- Add utilities for **event‑based labels** (start/end times per sample)
- Add richer evaluation helpers (rolling metrics and robustness checks)
- Provide a small CLI (optional)

---

## License

MIT (see `LICENSE`).