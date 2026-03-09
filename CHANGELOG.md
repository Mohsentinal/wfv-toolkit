# Changelog

## v0.1.8 - 2026-03-08

### Added
- Added `purge_by_horizon(...)` to the public package API for forward-horizon label leakage control.
- Added `drop_indices(...)` helper for applying embargo or custom blocked sets back onto training indices.
- Added tiny evaluation helpers: `accuracy_score`, `mean_score`, `evaluate_splits`, and `summarize_scores`.
- Added tests for leakage guards and evaluation helpers.

### Changed
- Updated `examples/leakage_demo.py` to use the real package API instead of carrying the most important leakage logic only inside the example.
- Updated README quickstart and install instructions.
- Bumped package version from `0.1.7` to `0.1.8`.
- Added `numpy` to development dependencies and an `examples` extra so the leakage demo works in a standard dev/example setup.

### Why this matters
- The repo's strongest idea — horizon-aware leakage control — is now part of the actual toolkit, not hidden only in an example script.
